"""Tests for skills/research-repo/scripts/repo_audit.py and the skill's reference files.

Run from the repo root:
    python3 -m unittest discover -s tests -v
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "research-repo")
SCRIPT = os.path.join(SKILL, "scripts", "repo_audit.py")
FIX = os.path.join(ROOT, "tests", "fixtures", "repos")
REFS = os.path.join(SKILL, "references")

sys.path.insert(0, os.path.join(SKILL, "scripts"))
import repo_audit  # noqa: E402

FINDING_RE = re.compile(r"^(.+?)(?::(\d+))?: ([a-z-]+): (.*)$")

# fixture -> {rule: [(path, line or None), ...]}. Exact, so a fixture that stops
# firing, fires on the wrong line, or fires on an extra file fails.
EXPECTED = {
    "license-missing": {"license": [("LICENSE", None)]},
    "license-unknown": {"license": [("LICENSE", None)]},
    "readme-missing": {"readme": [("README.md", None)]},
    "readme-sections": {"readme-sections": [("README.md", None)] * 5 + [("README.md", 3)] * 2},
    "reproduce": {"reproduce": [("REPRODUCE.md", None)]},
    "citation-cff-missing": {"citation-cff": [("CITATION.cff", None)]},
    "citation-cff-keys": {"citation-cff": [(".zenodo.json", None), ("CITATION.cff", None), ("CITATION.cff", 1),
                                           ("CITATION.cff", 3), ("CITATION.cff", 4)]},
    "citation-cff-tabs": {"citation-cff": [("CITATION.cff", None)]},
    "deps-pinned": {"deps-pinned": [("pyproject.toml", 4), ("pyproject.toml", 5), ("pyproject.toml", 6),
                                    ("pyproject.toml", 10), ("requirements.txt", 1)]},
    "deps-pinned-none": {"deps-pinned": [("pyproject.toml", None)]},
    "deps-locked": {"deps-pinned": []},
    "home-path": {"home-path": [("run.sh", 2), ("run.sh", 3), ("run.sh", 4), ("run.sh", 5)]},
    "private-path": {"private-path": [("conf.txt", 1), ("conf.txt", 2), ("conf.txt", 3), ("conf.txt", 4)]},
    "large-file": {"large-file": [("weights.bin", None)]},
    "data-license": {"data-license": [("./", None), ("data/", None)]},
    "tests-missing": {"tests": [("tests/", None)]},
    "tests-undocumented": {"tests": [("README.md", None)]},
    "secret": {"secret": [("config.py", 1), ("config.py", 2), ("config.py", 3), ("config.py", 4)]},
    "todo": {"todo": [("docs/NOTES.md", 2), ("docs/NOTES.md", 3), ("docs/NOTES.md", 4), ("docs/NOTES.md", 5)]},
    "gitignore": {"gitignore": [(".gitignore", None)]},
    "model-card": {"model-card": [("MODEL_CARD.md", None)] + [("model/README.md", None)] * 4 + [("other/README.md", None)]},
}
RUNTIME_RULES = {"git-tag"}  # exercised in a temporary git repository


def audit(name, **kw):
    _, findings, _ = repo_audit.audit(os.path.join(FIX, name), **kw)
    return findings


def locs(findings, rule):
    return sorted(((f.path, f.line) for f in findings if f.rule == rule), key=lambda t: (t[0], t[1] or 0))


def run_cli(*args):
    proc = subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True, text=True)
    findings = []
    for line in proc.stdout.splitlines():
        m = FINDING_RE.match(line)
        if m and m.group(3) in repo_audit.RULES and "more finding" not in m.group(4):
            findings.append((m.group(1), int(m.group(2)) if m.group(2) else None, m.group(3), m.group(4)))
    return proc, findings


class RuleFixtures(unittest.TestCase):
    def test_every_rule_has_a_fixture(self):
        covered = set()
        for want in EXPECTED.values():
            covered.update(r for r, l in want.items() if l)
        self.assertEqual(covered | RUNTIME_RULES, set(repo_audit.RULES))

    def test_each_fixture_flags_its_rule(self):
        for name, want in EXPECTED.items():
            kw = {"max_bytes": 1024} if name == "large-file" else {}
            with self.subTest(fixture=name):
                findings = audit(name, **kw)
                for rule, expected in want.items():
                    self.assertEqual(locs(findings, rule), sorted(expected, key=lambda t: (t[0], t[1] or 0)),
                                     "\n".join(str(f) for f in findings))

    def test_clean_fixture_has_no_findings(self):
        repo, findings, skipped = repo_audit.audit(os.path.join(FIX, "clean"))
        self.assertEqual([str(f) for f in findings], [])
        self.assertEqual(repo.license_id, "MIT")
        self.assertEqual(repo.mode, "walk")
        self.assertIn("git-tag", skipped)


class Negatives(unittest.TestCase):
    """Lines that look like findings but must not be flagged."""

    def test_root_in_dockerfile_is_a_container_path(self):
        self.assertEqual([f.path for f in audit("home-path") if f.rule == "home-path"], ["run.sh"] * 4)

    def test_loopback_and_version_are_not_private_paths(self):
        msgs = [f.message for f in audit("private-path") if f.rule == "private-path"]
        self.assertFalse(any("127.0.0.1" in m or "1.2.3.4" in m or "a@b.org" in m for m in msgs), msgs)

    def test_todo_in_code_is_not_a_doc_marker(self):
        self.assertEqual([f.path for f in audit("todo") if f.rule == "todo"], ["docs/NOTES.md"] * 4)

    def test_short_hf_prefix_is_not_a_secret(self):
        self.assertNotIn(5, [f.line for f in audit("secret") if f.rule == "secret"])

    def test_lockfile_satisfies_pinning(self):
        self.assertEqual(locs(audit("deps-locked"), "deps-pinned"), [])

    def test_exact_engine_pin_passes(self):
        msgs = [f.message for f in audit("deps-pinned") if f.rule == "deps-pinned"]
        self.assertFalse(any("flash-attn" in m or "pytest" in m for m in msgs), msgs)

    def test_covered_data_dir_passes(self):
        self.assertNotIn("covered/", [f.path for f in audit("data-license")])

    def test_messages_never_print_the_secret(self):
        for f in audit("secret"):
            if f.rule == "secret":
                self.assertNotIn("Example", f.message)


class Messages(unittest.TestCase):
    def test_results_section_needs_hardware_and_version(self):
        msgs = [f.message for f in audit("readme-sections") if f.line == 3]
        self.assertEqual(len(msgs), 2)
        self.assertTrue(any("hardware" in m for m in msgs) and any("version" in m for m in msgs), msgs)

    def test_license_type_is_detected(self):
        repo, _, _ = repo_audit.audit(os.path.join(FIX, "license-unknown"))
        self.assertIsNone(repo.license_id)
        self.assertEqual(repo.license_path, "LICENSE")

    def test_warning_level_is_marked(self):
        line = [str(f) for f in audit("gitignore") if f.rule == "gitignore"][0]
        self.assertTrue(line.startswith(".gitignore: gitignore: warning: "))

    def test_model_card_license_is_error_others_warning(self):
        levels = {f.message.split("'")[1]: f.level for f in audit("model-card") if f.path == "model/README.md"}
        self.assertEqual(levels["license"], "error")
        self.assertEqual(levels["base_model"], "warning")


class GitMode(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="repo-audit-")
        self.repo = os.path.join(self.tmp, "repo")
        shutil.copytree(os.path.join(FIX, "clean"), self.repo)
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("-c", "user.name=t", "-c", "user.email=t@example.org", "commit", "-q", "-m", "init")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def git(self, *args):
        return subprocess.run(["git", "-C", self.repo] + list(args), capture_output=True, text=True, check=True)

    def test_untagged_repo_is_flagged_then_passes_after_tag(self):
        repo, findings, skipped = repo_audit.audit(self.repo)
        self.assertEqual(repo.mode, "git")
        self.assertEqual([f.rule for f in findings], ["git-tag"])
        self.git("tag", "-a", "v1.0.0", "-m", "paper v1")
        _, findings, _ = repo_audit.audit(self.repo)
        self.assertEqual(findings, [])

    def test_untracked_files_are_not_scanned(self):
        with open(os.path.join(self.repo, "scratch.sh"), "w") as fh:
            fh.write("DATA=/home/alice/data\n")
        _, findings, _ = repo_audit.audit(self.repo)
        self.assertEqual([f.rule for f in findings], ["git-tag"])
        self.git("add", "scratch.sh")
        _, findings, _ = repo_audit.audit(self.repo)
        self.assertIn("home-path", [f.rule for f in findings])

    def test_subdirectory_of_a_git_repo_is_walked(self):
        repo, _, skipped = repo_audit.audit(os.path.join(self.repo, "model"))
        self.assertEqual(repo.mode, "walk")
        self.assertIn("git-tag", skipped)


class Cli(unittest.TestCase):
    def test_exit_zero_with_findings_and_summary_lists_every_rule(self):
        proc, findings = run_cli(os.path.join(FIX, "secret"))
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(findings)
        for rule in repo_audit.RULES:
            self.assertRegex(proc.stdout, r"(?m)^  %s\s+(\d+|- )" % re.escape(rule))
        self.assertIn("license: none", proc.stdout)

    def test_per_file_cap_prints_a_count(self):
        proc, _ = run_cli(os.path.join(FIX, "readme-sections"))
        self.assertIn("README.md: readme-sections: 2 more findings in this file not shown", proc.stdout)

    def test_disable(self):
        _, findings = run_cli(os.path.join(FIX, "secret"), "--disable", "secret,gitignore")
        self.assertEqual([f for f in findings if f[2] in ("secret", "gitignore")], [])

    def test_unknown_rule_and_missing_dir_are_errors(self):
        proc, _ = run_cli(os.path.join(FIX, "secret"), "--disable", "nope")
        self.assertEqual(proc.returncode, 2)
        proc, _ = run_cli(os.path.join(FIX, "does-not-exist"))
        self.assertEqual(proc.returncode, 2)

    def test_max_bytes(self):
        _, findings = run_cli(os.path.join(FIX, "large-file"), "--max-bytes", "1024")
        self.assertEqual([f[0] for f in findings if f[2] == "large-file"], ["weights.bin"])
        _, findings = run_cli(os.path.join(FIX, "large-file"))
        self.assertEqual([f for f in findings if f[2] == "large-file"], [])

    def test_list_rules(self):
        proc = subprocess.run([sys.executable, SCRIPT, "--list-rules"], capture_output=True, text=True)
        self.assertEqual(len(proc.stdout.strip().splitlines()), len(repo_audit.RULES))

    def test_root_symlink_runs(self):
        proc = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "repo_audit.py"), "--list-rules"],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)


def ref_text(name):
    with open(os.path.join(REFS, name), encoding="utf-8") as fh:
        return fh.read()


class ReferencesInSync(unittest.TestCase):
    def test_every_cited_key_is_in_sources(self):
        keys = set(re.findall(r"(?m)^\| `([a-z0-9.-]+)` \|", ref_text("sources.md")))
        self.assertEqual(len(keys), 89)
        files = [os.path.join(REFS, f) for f in os.listdir(REFS) if f.endswith(".md")] + [os.path.join(SKILL, "SKILL.md")]
        for path in files:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            text = re.sub(r"(?s)```.*?```", "", text)
            text = re.sub(r"`[^`\n]*`", "", text)
            cited = set(re.findall(r"\[([a-z][a-z0-9.-]+)\](?!\()", text))
            with self.subTest(file=os.path.basename(path)):
                self.assertEqual(cited - keys, set())

    def test_skill_routes_to_existing_files(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read()
        routed = set(re.findall(r"`references/([a-z-]+\.md)`", text))
        present = {f for f in os.listdir(REFS) if f.endswith(".md")}
        self.assertEqual(routed, present)

    def test_skill_frontmatter(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read()
        m = re.match(r"---\nname: (.+)\ndescription: \"(.+)\"\nlicense: .+\n---\n", text)
        self.assertTrue(m)
        self.assertEqual(m.group(1), "research-repo")
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_checklist_ids_unique_and_audit_marks_name_real_rules(self):
        text = ref_text("checklist.md")
        ids = re.findall(r"(?m)^- ([A-Z]{2}\d+):", text)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreater(len(ids), 60)
        for mark in re.findall(r"\(audit: ([^)]+)\)", text):
            for rule in re.split(r",\s*", mark):
                rule = rule.split(",")[0].strip()
                if rule in ("partial", "presence only"):
                    continue
                self.assertIn(rule, repo_audit.RULES, mark)

    def test_rules_point_at_existing_reference_files(self):
        present = {f for f in os.listdir(REFS) if f.endswith(".md")}
        for rid, (level, desc, ref) in repo_audit.RULES.items():
            self.assertIn(ref, present, rid)
            self.assertIn(level, ("error", "warning"))


if __name__ == "__main__":
    unittest.main()
