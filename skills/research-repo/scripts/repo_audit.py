#!/usr/bin/env python3
"""repo_audit: mechanical checks for the repository behind an ML systems paper.

Usage:
    python3 repo_audit.py REPO_DIR [--max-bytes N] [--disable rule,rule] [--list-rules]

Reports findings as path: rule: message (path:line: rule: message where a
line applies), then a count per rule. Uses `git ls-files` when REPO_DIR is
the top of a git repository, else walks the tree. Always exits 0 unless the
command line is wrong. Dependency-free, Python 3.8 or newer.

It checks what a script can check reliably: files present, headings, keys,
version pins, paths, secrets, sizes. It cannot judge whether the claims map
is complete or the tolerance is honest; references/checklist.md covers that.
"""

import argparse
import os
import re
import subprocess
import sys
from collections import Counter, OrderedDict

# --------------------------------------------------------------------------
# Rules: id -> (level, what it checks, reference file)
# --------------------------------------------------------------------------

RULES = OrderedDict([
    ("license", ("error", "no LICENSE at the root, or its text matches no common SPDX license", "licensing.md")),
    ("readme", ("error", "no README at the root", "readme.md")),
    ("readme-sections", ("error", "README misses the opening paragraph or a section: results with setup, install, quickstart, limits, citation, license", "readme.md")),
    ("reproduce", ("error", "no REPRODUCE.md and no reproduce section in the README", "reproduce.md")),
    ("citation-cff", ("error", "CITATION.cff missing, unparseable, or without cff-version, message, title, authors", "citation.md")),
    ("deps-pinned", ("error", "dependency without a version bound and no lockfile; engine packages need an exact pin", "environment.md")),
    ("home-path", ("error", "hard-coded home path (/home/<user>/, /root/, /Users/<name>/, C:\\Users\\)", "environment.md")),
    ("private-path", ("warning", "IP address, internal hostname, user@host or mount path", "environment.md")),
    ("large-file", ("warning", "tracked file above the size threshold", "layout.md")),
    ("data-license", ("warning", "data files with no LICENSE, README, card or manifest beside them", "data-release.md")),
    ("tests", ("error", "no tests directory, or no documented way to run the tests", "tests-ci.md")),
    ("git-tag", ("warning", "git repository with no tag", "releases.md")),
    ("secret", ("error", "token or private key pattern in a tracked file", "tests-ci.md")),
    ("todo", ("warning", "TODO, FIXME, TBD, XXX or OWNER marker in docs", "readme.md")),
    ("gitignore", ("warning", "no .gitignore at the root", "layout.md")),
    ("model-card", ("error", "model card front matter without license, base_model, tags or library_name", "model-release.md")),
])

DEFAULT_MAX_BYTES = 10 * 1024 * 1024
SCAN_LIMIT = 5 * 1024 * 1024  # text files above this are not scanned line by line

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".mypy_cache", ".pytest_cache",
             ".ruff_cache", ".tox", ".nox", ".eggs", "build", "dist", ".idea", ".vscode"}

DOC_EXT = (".md", ".rst", ".txt", ".cff", ".adoc")
DATA_EXT = (".csv", ".tsv", ".jsonl", ".parquet", ".arrow", ".npy", ".npz", ".h5", ".hdf5", ".feather",
            ".pkl", ".pickle", ".pt", ".pth", ".ckpt", ".safetensors", ".gguf")
LOCKFILES = ("uv.lock", "poetry.lock", "pdm.lock", "Pipfile.lock", "conda-lock.yml", "conda-lock.yaml",
             "requirements.lock", "pixi.lock", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
             "Cargo.lock", "go.sum")
ENGINE_PACKAGES = {"torch", "vllm", "sglang", "transformers", "flash-attn", "flashinfer", "flashinfer-python",
                   "triton", "xformers", "lmcache", "tensorrt-llm", "sgl-kernel", "torchao", "deepspeed",
                   "megatron-core"}
RUN_TESTS_RE = re.compile(r"(pytest|unittest|make test|\btox\b|\bnox\b|cargo test|go test|npm test|yarn test"
                          r"|\bctest\b|bazel test|hatch test)", re.I)

LICENSE_PATTERNS = [
    ("Apache-2.0", r"Apache License[\s\S]{0,40}Version 2\.0"),
    ("AGPL-3.0", r"GNU AFFERO GENERAL PUBLIC LICENSE"),
    ("LGPL-2.1", r"GNU LESSER GENERAL PUBLIC LICENSE[\s\S]{0,40}Version 2\.1"),
    ("LGPL-3.0", r"GNU LESSER GENERAL PUBLIC LICENSE[\s\S]{0,40}Version 3"),
    ("GPL-3.0", r"GNU GENERAL PUBLIC LICENSE[\s\S]{0,40}Version 3"),
    ("GPL-2.0", r"GNU GENERAL PUBLIC LICENSE[\s\S]{0,40}Version 2"),
    ("MPL-2.0", r"Mozilla Public License[\s\S]{0,20}2\.0"),
    ("CC-BY-SA-4.0", r"Attribution-ShareAlike 4\.0"),
    ("CC-BY-NC-4.0", r"Attribution-NonCommercial 4\.0"),
    ("CC-BY-4.0", r"Attribution 4\.0 International"),
    ("CC0-1.0", r"CC0 1\.0 Universal"),
    ("Unlicense", r"free and unencumbered software released into the public domain"),
    ("BSD-3-Clause", r"Redistribution and use in source and binary forms[\s\S]*Neither the name"),
    ("BSD-2-Clause", r"Redistribution and use in source and binary forms"),
    ("ISC", r"ISC License"),
    ("MIT", r"Permission is hereby granted, free of charge"),
]

HOME_PATH_RE = re.compile(r"(?<![\w/])(/home/[A-Za-z0-9_.-]+/|/root/|/Users/[A-Za-z0-9_.-]+/|[A-Za-z]:\\Users\\)")
IP_RE = re.compile(r"(?<![\w.])((?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?![\w.])")
HOSTNAME_RE = re.compile(r"\b[a-z0-9][a-z0-9-]*\.(local|internal|lan|corp|intranet)\b", re.I)
USER_HOST_RE = re.compile(r"(?<![\w.@-])[a-z_][a-z0-9_-]{0,31}@[a-z0-9][a-z0-9.-]*:(?!//)", re.I)
MOUNT_RE = re.compile(r"(?<![\w/])/(mnt|data|scratch|workspace|nfs|lustre|datasets|shared|srv|media)/[A-Za-z0-9_.-]+")
SECRET_PATTERNS = [
    ("Hugging Face token", re.compile(r"\bhf_[A-Za-z0-9]{20,}\b")),
    ("sk- API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\b(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("GitLab token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b")),
]
TODO_RE = re.compile(r"\b(TODO|FIXME|XXX|TBD|OWNER)\b")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
HARDWARE_RE = re.compile(r"\b(GPUs?|CPUs?|TPUs?|hardware|machine|node|A100|H100|H200|B200|B300|GB200|L40S?|L4|T4|V100|RTX|"
                         r"MI300X?|MI250|MI325X?|Gaudi|Xeon|EPYC|Graviton|DGX|Spark)\b", re.I)
VERSION_RE = re.compile(r"\b(version|commit|release|tag)\b|\bv\d+\.\d+|==\s*\d|"
                        r"\b(vllm|sglang|torch|pytorch|transformers|cuda|triton|tensorrt|lmcache|flashinfer|driver|python)\W{0,3}v?\d+\.\d+", re.I)
SECTION_KEYS = OrderedDict([
    ("results", (r"result|benchmark|performance|headline|evaluation|numbers", "results")),
    ("install", (r"install|setup|set up|requirements|getting started|dependencies|build", "install")),
    ("quickstart", (r"quick\s*start|usage|getting started|hello|smoke|try it|run it|example", "quickstart")),
    ("limits", (r"limit|caveat|known issues|scope|non-goals|not reproduc|what does not|threats|assumptions", "limits")),
    ("citation", (r"cit(e|ation|ing)|bibtex|reference", "citation")),
    ("license", (r"licen[sc]e|legal", "license")),
])
REQ_NAME_RE = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")
REQ_SPEC_RE = re.compile(r"(===|==|~=|!=|>=|<=|>|<|@)")


class Finding(object):
    def __init__(self, path, rule, message, line=None, level=None):
        self.path = path
        self.rule = rule
        self.message = message
        self.line = line
        self.level = level or RULES[rule][0]

    def __str__(self):
        loc = self.path if self.line is None else "%s:%d" % (self.path, self.line)
        prefix = "warning: " if self.level == "warning" else ""
        return "%s: %s: %s%s" % (loc, self.rule, prefix, self.message)


# --------------------------------------------------------------------------
# File access
# --------------------------------------------------------------------------

def git_toplevel(repo):
    try:
        out = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return os.path.realpath(out.stdout.strip())


def list_files(repo):
    """Return (relative paths, mode). mode is 'git' or 'walk'."""
    top = git_toplevel(repo)
    if top is not None and top == os.path.realpath(repo):
        out = subprocess.run(["git", "-C", repo, "ls-files", "-z"], capture_output=True, text=True, timeout=120)
        files = [f for f in out.stdout.split("\0") if f]
        files = [f for f in files if os.path.isfile(os.path.join(repo, f))]
        return sorted(files), "git"
    files = []
    for base, dirs, names in os.walk(repo):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.endswith(".egg-info"))
        for n in names:
            p = os.path.join(base, n)
            if os.path.isfile(p) and not os.path.islink(p):
                files.append(os.path.relpath(p, repo).replace(os.sep, "/"))
    return sorted(files), "walk"


class Repo(object):
    def __init__(self, root, max_bytes):
        self.root = root
        self.max_bytes = max_bytes
        self.files, self.mode = list_files(root)
        self._text = {}
        self.license_id = None
        self.license_path = None

    def abspath(self, rel):
        return os.path.join(self.root, rel)

    def size(self, rel):
        try:
            return os.path.getsize(self.abspath(rel))
        except OSError:
            return 0

    def text(self, rel):
        """File contents as text, or None when binary or too large."""
        if rel in self._text:
            return self._text[rel]
        result = None
        try:
            if self.size(rel) <= SCAN_LIMIT:
                with open(self.abspath(rel), "rb") as fh:
                    data = fh.read()
                if b"\0" not in data[:8192]:
                    result = data.decode("utf-8", "replace")
        except OSError:
            result = None
        self._text[rel] = result
        return result

    def lines(self, rel):
        t = self.text(rel)
        return t.splitlines() if t is not None else []

    def root_file(self, *names):
        """First root-level file whose basename matches one of the names (case-insensitive)."""
        wanted = [n.lower() for n in names]
        for f in self.files:
            if "/" in f:
                continue
            base = f.lower()
            stem = base.split(".")[0]
            if base in wanted or stem in wanted:
                return f
        return None

    def has_lockfile(self):
        return any(os.path.basename(f) in LOCKFILES for f in self.files) or any(
            os.path.basename(f).startswith("requirements") and "--hash=" in (self.text(f) or "") for f in self.files)


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check_license(repo, out):
    path = repo.root_file("LICENSE", "LICENCE", "COPYING", "UNLICENSE", "LICENSE.md", "LICENSE.txt", "LICENSE.rst")
    if path is None:
        out.append(Finding("LICENSE", "license", "no LICENSE file at the repository root; without one nobody may copy, modify or distribute the code (add Apache-2.0 or MIT)"))
        return
    repo.license_path = path
    text = repo.text(path) or ""
    m = re.search(r"SPDX-License-Identifier:\s*([A-Za-z0-9.+-]+)", text)
    if m:
        repo.license_id = m.group(1)
        return
    for spdx, pat in LICENSE_PATTERNS:
        if re.search(pat, text):
            repo.license_id = spdx
            return
    out.append(Finding(path, "license", "license text matches no common SPDX license; name the license in the README and the model or data cards", level="warning"))


def readme_path(repo):
    return repo.root_file("README", "README.md", "README.rst", "README.txt")


def parse_sections(lines):
    """Return (preamble_lines, [(level, title, lineno, body_lines)])."""
    sections = []
    preamble = []
    start = 0
    if lines and lines[0].strip() == "---":  # YAML front matter
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    cur = None
    in_code = False
    for i in range(start, len(lines)):
        line = lines[i]
        if line.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else HEADING_RE.match(line)
        if m:
            cur = (len(m.group(1)), m.group(2), i + 1, [])
            sections.append(cur)
        elif cur is None:
            preamble.append(line)
        else:
            cur[3].append(line)
    return preamble, sections


def prose_words(lines):
    words = 0
    for line in lines:
        s = line.strip()
        if not s or s.startswith(("[![", "<", "!", "|", "```", "    ", "- ", "* ")):
            continue
        words += len(s.split())
    return words


def check_readme(repo, out):
    rp = readme_path(repo)
    if rp is None:
        out.append(Finding("README.md", "readme", "no README at the repository root"))
        return None
    lines = repo.lines(rp)
    preamble, sections = parse_sections(lines)
    # Opening paragraph: prose after the title, before the first level-2+ heading.
    opening = list(preamble)
    for level, title, lineno, body in sections:
        if level == 1:
            opening.extend(body)
        else:
            break
    if prose_words(opening) < 12:
        out.append(Finding(rp, "readme-sections", "no opening paragraph before the first section; say what the repo is, which paper it belongs to, what is in it and what is not"))
    titles = [(title, lineno, body) for level, title, lineno, body in sections if level >= 2]
    for key, (pat, label) in SECTION_KEYS.items():
        hits = [(t, ln, b) for t, ln, b in titles if re.search(pat, t, re.I)]
        if not hits:
            out.append(Finding(rp, "readme-sections", "no %s section (heading matching /%s/)" % (label, pat)))
            continue
        if key == "results":
            body = "\n".join("\n".join(b) for _, _, b in hits)
            if not HARDWARE_RE.search(body):
                out.append(Finding(rp, "readme-sections", "results section names no hardware (GPU model and count); the numbers depend on it", line=hits[0][1]))
            if not VERSION_RE.search(body):
                out.append(Finding(rp, "readme-sections", "results section names no engine or software version; the version decides the numbers", line=hits[0][1]))
    return rp


def check_reproduce(repo, out, rp):
    for f in repo.files:
        base = os.path.basename(f).lower()
        if (base.startswith("reproduc") or base.startswith("artifact")) and base.endswith(DOC_EXT):
            return
    if rp is not None:
        _, sections = parse_sections(repo.lines(rp))
        for level, title, lineno, body in sections:
            if re.search(r"reproduc|replicat|artifact|re-?run|experiments", title, re.I):
                return
    out.append(Finding("REPRODUCE.md", "reproduce", "no REPRODUCE.md and no reproduce section in the README; add the claims map (claim, command, hardware, wall time, expected output, tolerance)"))


def top_level_keys(lines):
    keys = OrderedDict()
    for i, line in enumerate(lines):
        if line.startswith((" ", "\t", "-", "#")) or not line.strip():
            continue
        m = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(.*)$", line)
        if m:
            keys[m.group(1)] = (m.group(2).strip(), i)
    return keys


def check_citation(repo, out):
    path = repo.root_file("CITATION.cff")
    if path is None:
        out.append(Finding("CITATION.cff", "citation-cff", "no CITATION.cff at the repository root; GitHub shows 'Cite this repository' from it and Zenodo reads it"))
        return
    lines = repo.lines(path)
    if not lines or "\t" in (repo.text(path) or ""):
        out.append(Finding(path, "citation-cff", "file is empty or contains tabs; CFF is YAML and YAML forbids tabs"))
        return
    keys = top_level_keys(lines)
    for k in ("cff-version", "message", "title", "authors"):
        if k not in keys:
            out.append(Finding(path, "citation-cff", "missing key '%s'" % k))
    if "cff-version" in keys and not re.match(r"^\d+\.\d+\.\d+$", keys["cff-version"][0].strip('"\'')):
        out.append(Finding(path, "citation-cff", "cff-version is not of the form 1.2.0", line=keys["cff-version"][1] + 1))
    if "authors" in keys:
        val, i = keys["authors"]
        nxt = next((l for l in lines[i + 1:] if l.strip()), "")
        if not (val.startswith("[") or nxt.lstrip().startswith("- ")):
            out.append(Finding(path, "citation-cff", "'authors' is empty or not a list", line=i + 1))
    if "date-released" in keys and not re.match(r"^\d{4}-\d{2}-\d{2}$", keys["date-released"][0].strip('"\'')):
        out.append(Finding(path, "citation-cff", "date-released is not YYYY-MM-DD", line=keys["date-released"][1] + 1))
    if repo.root_file(".zenodo.json"):
        out.append(Finding(".zenodo.json", "citation-cff", ".zenodo.json and CITATION.cff both exist; Zenodo uses only .zenodo.json, keep one or keep them identical", level="warning"))


def parse_requirement(spec):
    """Return (name, has_bound, exact) or None for lines that are not requirements."""
    s = spec.split("#", 1)[0].strip().strip(",")
    if not s or s.startswith(("-", "git+", "http://", "https://", "file:", "./", "/")):
        return None
    s = s.split(";", 1)[0].strip()
    m = REQ_NAME_RE.match(s)
    if not m:
        return None
    name = m.group(1).lower().replace("_", "-")
    rest = s[m.end():]
    rest = re.sub(r"^\s*\[[^\]]*\]", "", rest)  # extras
    bound = bool(REQ_SPEC_RE.search(rest))
    exact = bool(re.search(r"(===|==|@)", rest))
    return name, bound, exact


def pyproject_requirements(lines):
    """Yield (requirement string, lineno) from dependency arrays in pyproject.toml."""
    in_block = False
    section = ""
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("["):
            section = s
            in_block = False
            continue
        if not in_block:
            if re.match(r"^(dependencies|[A-Za-z0-9_.\"-]+)\s*=\s*\[", s) and (
                    section.startswith("[project") or "dependency-groups" in section or "poetry" in section):
                if s.startswith("dependencies") or "optional-dependencies" in section or "dependency-groups" in section:
                    in_block = True
                    tail = s.split("[", 1)[1]
                    for q in re.findall(r"\"([^\"]+)\"|'([^']+)'", tail):
                        yield (q[0] or q[1]), i + 1
                    if "]" in tail:
                        in_block = False
            continue
        for q in re.findall(r"\"([^\"]+)\"|'([^']+)'", s):
            yield (q[0] or q[1]), i + 1
        if "]" in s:
            in_block = False


def check_deps(repo, out):
    dep_files = []
    for f in repo.files:
        base = os.path.basename(f)
        if any(part in ("tests", "test", "fixtures", "docs", "examples") for part in f.split("/")[:-1]):
            continue
        if base.startswith("requirements") and base.endswith(".txt"):
            dep_files.append(("req", f))
        elif base == "pyproject.toml":
            dep_files.append(("pyproject", f))
        elif base in ("environment.yml", "environment.yaml"):
            dep_files.append(("conda", f))
        elif base in ("setup.py", "setup.cfg"):
            dep_files.append(("setup", f))
    locked = repo.has_lockfile()
    if not dep_files and not locked:
        out.append(Finding("pyproject.toml", "deps-pinned", "no dependency specification (pyproject.toml, requirements.txt, environment.yml) and no lockfile"))
        return
    if locked:
        return
    for kind, f in dep_files:
        lines = repo.lines(f)
        reqs = []
        if kind == "req":
            reqs = [(l, i + 1) for i, l in enumerate(lines)]
        elif kind == "pyproject":
            reqs = list(pyproject_requirements(lines))
        elif kind == "conda":
            in_deps = False
            for i, l in enumerate(lines):
                if re.match(r"^dependencies\s*:", l):
                    in_deps = True
                    continue
                if in_deps and re.match(r"^\S", l):
                    in_deps = False
                if in_deps:
                    m = re.match(r"^\s*-\s*([^#\n]+)", l)
                    if m and not m.group(1).strip().startswith(("pip", "python")):
                        reqs.append((m.group(1).replace("=", "==", 1) if re.match(r"^[^=<>!~]+=[^=]", m.group(1)) else m.group(1), i + 1))
        else:
            for i, l in enumerate(lines):
                for q in re.findall(r"\"([^\"]+)\"|'([^']+)'", l):
                    reqs.append(((q[0] or q[1]), i + 1))
        for spec, lineno in reqs:
            parsed = parse_requirement(spec)
            if parsed is None:
                continue
            name, bound, exact = parsed
            if kind == "setup" and not re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]*(\[.*\])?\s*([=<>!~@].*)?$", spec.strip()):
                continue
            if name in ENGINE_PACKAGES:
                if not bound:
                    out.append(Finding(f, "deps-pinned", "'%s' has no version and there is no lockfile; the engine version decides the numbers, pin it with == or commit a lockfile" % name, line=lineno))
                elif not exact:
                    out.append(Finding(f, "deps-pinned", "'%s' has a range, not an exact pin, and there is no lockfile; the engine version decides the numbers" % name, line=lineno, level="warning"))
            elif not bound:
                out.append(Finding(f, "deps-pinned", "'%s' has no version bound and there is no lockfile" % name, line=lineno, level="warning"))


def is_container_file(rel):
    base = os.path.basename(rel).lower()
    return base.startswith("dockerfile") or base.endswith(".dockerfile") or base.startswith(("docker-compose", "compose.y"))


def check_text_rules(repo, out, disabled):
    for f in repo.files:
        lines = repo.lines(f)
        if not lines:
            continue
        container = is_container_file(f)
        is_doc = f.lower().endswith(DOC_EXT)
        for i, line in enumerate(lines, 1):
            if "home-path" not in disabled:
                for m in HOME_PATH_RE.finditer(line):
                    if container and m.group(1) == "/root/":
                        continue
                    out.append(Finding(f, "home-path", "hard-coded path '%s'; use a path relative to the repo root or a variable" % m.group(1).rstrip("/\\"), line=i))
                    break
            if "private-path" not in disabled:
                msg = None
                m = IP_RE.search(line)
                if m:
                    ip = m.group(0)
                    before = line[:m.start()][-2:]
                    if not (ip.startswith(("127.", "0.0.0.0", "255.255.255.255")) or before.endswith(("v", "=", "-"))):
                        msg = "IP address %s" % ip
                if msg is None and HOSTNAME_RE.search(line):
                    msg = "internal hostname '%s'" % HOSTNAME_RE.search(line).group(0)
                if msg is None and USER_HOST_RE.search(line):
                    msg = "user@host target '%s'" % USER_HOST_RE.search(line).group(0).rstrip(":")
                if msg is None and not container and MOUNT_RE.search(line):
                    msg = "machine-specific path '%s'" % MOUNT_RE.search(line).group(0)
                if msg:
                    out.append(Finding(f, "private-path", msg + "; a stranger's machine does not have it", line=i))
            if "secret" not in disabled:
                for kind, pat in SECRET_PATTERNS:
                    if pat.search(line):
                        out.append(Finding(f, "secret", "possible %s; rotate it and purge it from history (git keeps every commit)" % kind, line=i))
                        break
            if "todo" not in disabled and is_doc:
                m = TODO_RE.search(line)
                if m:
                    out.append(Finding(f, "todo", "%s marker left in the docs" % m.group(1), line=i))


def check_large_files(repo, out):
    for f in repo.files:
        size = repo.size(f)
        if size > repo.max_bytes:
            human = "%.1f MiB" % (size / 1048576.0) if size >= 1048576 else "%d KiB" % (size // 1024)
            out.append(Finding(f, "large-file", "%s tracked; put data on Zenodo or Hugging Face and reference it in a manifest with sha256 (git keeps every version)" % human))


def check_data_license(repo, out):
    covered_names = re.compile(r"^(readme|license|licence|copying|manifest|datasheet|croissant|dataset_infos|licenses)|card", re.I)
    by_dir = {}
    for f in repo.files:
        parts = f.split("/")
        if any(p.lower() in ("tests", "test", "fixtures", "__pycache__") for p in parts[:-1]):
            continue
        if f.lower().endswith(DATA_EXT):
            by_dir.setdefault("/".join(parts[:-1]), []).append(parts[-1])
    dirs_with_cover = set()
    for f in repo.files:
        d, base = os.path.split(f)
        if covered_names.search(base):
            dirs_with_cover.add(d)
    for d in sorted(by_dir):
        probe = d
        ok = False
        while True:
            if probe in dirs_with_cover and (probe != "" or d == ""):
                ok = True
                break
            if probe == "":
                break
            probe = "/".join(probe.split("/")[:-1])
        if d == "" and ok:
            # Root data files: the root README is the code's; require a manifest, card or datasheet.
            ok = any("/" not in f and re.match(r"^(manifest|datasheet|croissant|dataset_infos|licenses)|card", os.path.basename(f), re.I) for f in repo.files)
        if not ok:
            names = by_dir[d]
            shown = ", ".join(names[:3]) + (" and %d more" % (len(names) - 3) if len(names) > 3 else "")
            out.append(Finding((d or ".") + "/", "data-license", "data files (%s) with no LICENSE, README, card, datasheet or manifest in this directory or a parent; state the license, the source and the fields" % shown))


def check_tests(repo, out, rp):
    has_tests = False
    for f in repo.files:
        parts = f.split("/")
        base = parts[-1]
        if any(p in ("tests", "test") for p in parts[:-1]) or re.match(r"^(test_.*\.py|.*_test\.(py|go|rs)|.*\.test\.[jt]sx?|tests\.rs)$", base):
            has_tests = True
            break
    if not has_tests:
        out.append(Finding("tests/", "tests", "no tests directory or test files; add a CPU smoke test and tests for the logic the numbers depend on"))
        return
    docs = [f for f in repo.files if ("/" not in f and f.lower().endswith(DOC_EXT)) or f.lower().startswith("docs/") and f.lower().endswith(DOC_EXT)]
    docs += [f for f in repo.files if os.path.basename(f).lower() in ("makefile", "justfile", "tox.ini", "noxfile.py")]
    for f in docs:
        t = repo.text(f) or ""
        if RUN_TESTS_RE.search(t) or (os.path.basename(f).lower() in ("makefile", "justfile") and re.search(r"(?m)^test\b", t)):
            return
    out.append(Finding(rp or "README.md", "tests", "tests exist but no README, CONTRIBUTING or docs file says how to run them; add the command"))


def check_git_tag(repo, out):
    if repo.mode != "git":
        return "skipped: not a git repository"
    proc = subprocess.run(["git", "-C", repo.root, "tag", "--list"], capture_output=True, text=True, timeout=30)
    if not proc.stdout.strip():
        out.append(Finding(".", "git-tag", "no git tag; tag the code behind each paper version (v1.0.0 for arXiv v1) and archive the tag"))
    return None


def check_gitignore(repo, out):
    if repo.root_file(".gitignore") is None:
        out.append(Finding(".gitignore", "gitignore", "no .gitignore; results of reruns, caches and local env files will be committed by accident"))


def front_matter(lines):
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return None


def check_model_cards(repo, out):
    for f in repo.files:
        if not f.lower().endswith(".md"):
            continue
        base = os.path.basename(f).lower()
        fm = front_matter(repo.lines(f))
        keys = top_level_keys(fm) if fm else OrderedDict()
        named = re.search(r"model[-_]?card", base) is not None
        if not named and not any(k in keys for k in ("base_model", "pipeline_tag", "library_name", "model-index")):
            continue
        if fm is None:
            out.append(Finding(f, "model-card", "model card without YAML front matter; the Hub reads license, base_model, library_name, pipeline_tag and tags from it"))
            continue
        if "license" not in keys:
            out.append(Finding(f, "model-card", "front matter has no 'license'; use a Hub identifier, or 'other' with license_name and license_link"))
        elif keys["license"][0].strip("\"'") == "other" and "license_name" not in keys:
            out.append(Finding(f, "model-card", "license is 'other' without license_name and license_link"))
        if "base_model" not in keys:
            out.append(Finding(f, "model-card", "front matter has no 'base_model'; add it, or say in the card that the model is trained from scratch", level="warning"))
        if "tags" not in keys:
            out.append(Finding(f, "model-card", "front matter has no 'tags'", level="warning"))
        if "library_name" not in keys:
            out.append(Finding(f, "model-card", "front matter has no 'library_name'; the Hub no longer infers it for repos created after August 2024", level="warning"))


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def audit(root, max_bytes=DEFAULT_MAX_BYTES, disabled=()):
    repo = Repo(root, max_bytes)
    out = []
    skipped = {}
    rp = None
    if "license" not in disabled:
        check_license(repo, out)
    if "readme" not in disabled or "readme-sections" not in disabled:
        rp = check_readme(repo, out)
    else:
        rp = readme_path(repo)
    if "reproduce" not in disabled:
        check_reproduce(repo, out, rp)
    if "citation-cff" not in disabled:
        check_citation(repo, out)
    if "deps-pinned" not in disabled:
        check_deps(repo, out)
    check_text_rules(repo, out, disabled)
    if "large-file" not in disabled:
        check_large_files(repo, out)
    if "data-license" not in disabled:
        check_data_license(repo, out)
    if "tests" not in disabled:
        check_tests(repo, out, rp)
    if "git-tag" not in disabled:
        note = check_git_tag(repo, out)
        if note:
            skipped["git-tag"] = note
    if "gitignore" not in disabled:
        check_gitignore(repo, out)
    if "model-card" not in disabled:
        check_model_cards(repo, out)
    out = [f for f in out if f.rule not in disabled]
    return repo, out, skipped


PER_FILE_CAP = 5


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mechanical checks for a paper's code, benchmark and model repository. Always exits 0.")
    ap.add_argument("repo", nargs="?", help="repository root")
    ap.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="large-file threshold in bytes (default 10 MiB)")
    ap.add_argument("--disable", default="", help="comma-separated rule ids to skip")
    ap.add_argument("--list-rules", action="store_true", help="print the rules and exit")
    args = ap.parse_args(argv)

    if args.list_rules:
        for rid, (level, desc, ref) in RULES.items():
            print("%-16s %-8s %s [references/%s]" % (rid, level, desc, ref))
        return 0
    if not args.repo:
        ap.print_usage()
        return 2
    if not os.path.isdir(args.repo):
        sys.stderr.write("repo_audit: not a directory: %s\n" % args.repo)
        return 2
    disabled = [r.strip() for r in args.disable.split(",") if r.strip()]
    for r in disabled:
        if r not in RULES:
            sys.stderr.write("repo_audit: unknown rule '%s' (see --list-rules)\n" % r)
            return 2

    root = os.path.abspath(args.repo)
    repo, findings, skipped = audit(root, args.max_bytes, disabled)
    order = list(RULES)
    findings.sort(key=lambda f: (order.index(f.rule), f.path, f.line or 0))
    print("repo: %s (%d files, %s)" % (root, len(repo.files), "git ls-files" if repo.mode == "git" else "walk"))
    shown = Counter()
    hidden = Counter()
    prev = None
    for f in findings + [None]:
        key = (f.path, f.rule) if f is not None else None
        if prev is not None and key != prev and hidden[prev]:
            n = hidden[prev]
            print("%s: %s: %d more finding%s in this file not shown" % (prev[0], prev[1], n, "" if n == 1 else "s"))
        if f is None:
            break
        if shown[key] < PER_FILE_CAP:
            shown[key] += 1
            print(f)
        else:
            hidden[key] += 1
        prev = key
    counts = Counter(f.rule for f in findings)
    errors = sum(1 for f in findings if f.level == "error")
    warnings = len(findings) - errors
    print("")
    print("summary: %d findings (%d errors, %d warnings) in %d files" % (len(findings), errors, warnings, len(repo.files)))
    for rid in RULES:
        if rid in disabled:
            print("  %-16s    - disabled" % rid)
        elif rid in skipped:
            print("  %-16s    - %s" % (rid, skipped[rid]))
        else:
            print("  %-16s %4d" % (rid, counts.get(rid, 0)))
    if repo.license_path:
        print("license: %s (%s)" % (repo.license_id or "unrecognized", repo.license_path))
    else:
        print("license: none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
