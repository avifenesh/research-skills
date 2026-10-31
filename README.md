# research-skills

Two AI agent skills for ML systems research: serving, training, compilers, kernels, schedulers and benchmarks.

- `arxiv-paper`: writing, checking and submitting the paper to arXiv or to MLSys, OSDI, SOSP, NeurIPS or ICLR. Ships `paper_lint.py`, a LaTeX style checker.
- `research-repo`: building, releasing and auditing the code, benchmark and model repository behind the paper, and preparing it for artifact evaluation. Ships `repo_audit.py`, a repository checker.

The file format is the [AgentSkills](https://agentskills.io) open standard. A skill works in Claude Code, Codex, Cursor and the other agents that read it. Install one or both.

## arxiv-paper: what it gives the agent

`skills/arxiv-paper/SKILL.md` is a router: a few rules for every task, then tables that map a task to one reference file. The agent reads the file that matches the task and leaves the rest out of context.

| File | Contents |
|------|----------|
| `structure.md` | Word budget, what each section must do, length, writing order |
| `abstract-intro.md` | Page one, abstract, title, introduction, refutable contributions, a contributions template |
| `claims-evidence.md` | Claim-evidence table, baselines, ablations, repeats and intervals, means and overheads, TTFT and ITL definitions, setup paragraph, threats to validity |
| `figures-tables.md` | Captions, axes, color, precision, booktabs, label and ref mechanics |
| `reproducibility-artifacts.md` | NeurIPS and Pineau checklists, ACM badges, MLSys and OSDI artifact evaluation, release, statement template |
| `citations-bib.md` | arXiv IDs and DOIs, BibTeX hygiene, all authors, software citation, `CITATION.cff` |
| `language-style.md` | Plain English rules, hedges, hype, units, tense, acronyms, terminology, the lint word lists |
| `reviewer-objections.md` | Twenty common objections and how to pre-empt each |
| `venues.md` | MLSys 2027, OSDI '27, NeurIPS 2026, ICLR 2026: dates, limits, criteria, anonymity, LLM policy |
| `arxiv-submission.md` | Endorsement and rate limits as of 2026, moderation, categories, metadata, license, TeX Live, tarball, versions |
| `checklist.md` | 77 one-line pre-submission items with IDs, used by the review procedure |
| `sources.md` | The 80 sources with short keys, how each was read, and known gaps |

Every rule cites a source key. Facts that change (deadlines, arXiv policy) carry their "as of" date. Judgement is tagged (design) so it is not mistaken for a sourced rule.

## research-repo: what it gives the agent

`skills/research-repo/SKILL.md` routes the same way and adds an "audit a repo" procedure: run the checker, then walk the checklist in order and report `path: ID: rule broken; fix`.

| File | Contents |
|------|----------|
| `layout.md` | Frozen artifact repo vs paper directory vs harness repo, the recommended tree, what each root file is for |
| `readme.md` | Section order, the headline table with setup, the README skeleton |
| `reproduce.md` | REPRODUCE.md, the claims map, venue appendix skeletons (cTuning, ASPLOS, USENIX Security), run time and hardware per claim, quick mode |
| `badges-venues.md` | ACM badges v1.1, MLSys, OSDI, USENIX Security, SOSP, ASPLOS and NeurIPS rules, Pineau and Papers with Code checklists |
| `environment.md` | Lockfiles and hashes, Docker digests, CUDA and driver, exact engine pins, determinism flags, env capture, hard-coded paths |
| `data-release.md` | Dataset cards and datasheets, Croissant, content-free traces, PII and gating, source licenses, manifest with checksums, hub revisions, DOIs |
| `model-release.md` | Model card fields (`license`, `base_model`, `library_name`), safetensors, checksums, HF DOI, the release checklist |
| `licensing.md` | Apache-2.0, MIT and the rest, NOTICE, copied code, REUSE for mixed repos, weight and data licenses |
| `citation.md` | `CITATION.cff`, BibTeX in the README, Zenodo and `.zenodo.json`, Software Heritage |
| `tests-ci.md` | What to test in research code, the smoke test, thin CI, the clean-machine test |
| `releases.md` | Tags tied to paper versions, SemVer, Keep a Changelog, the release flow |
| `reference-results.md` | Shipping raw per-run values, tolerances by metric type, median of three, the checker |
| `complaints.md` | What evaluators and users complain about, with the measured evidence and the fix |
| `examples.md` | vLLM's SOSP artifact, FlashAttention, SGLang, Mooncake, LMCache, Azure traces, lm-evaluation-harness, MLPerf |
| `checklist.md` | 81 one-line pre-release items with IDs, used by the audit procedure |
| `sources.md` | The 89 sources with short keys, how each was read, and known gaps |

The same conventions hold: source keys, "as of" dates, (design) tags. The owner's local conventions sit under labeled "House rules (design)" sections.

## Install

### Claude Code

Copy or symlink a skill directory into your skills folder:

```bash
git clone https://github.com/avifenesh/research-skills ~/src/research-skills
ln -s ~/src/research-skills/skills/arxiv-paper ~/.claude/skills/arxiv-paper       # all projects
ln -s ~/src/research-skills/skills/research-repo ~/.claude/skills/research-repo
# or, for one project:
mkdir -p .claude/skills && cp -r ~/src/research-skills/skills/arxiv-paper ~/src/research-skills/skills/research-repo .claude/skills/
```

### Other AgentSkills agents

Copy `skills/arxiv-paper/` or `skills/research-repo/` into the agent's skills directory (for example `.codex/skills/`, `.cursor/skills/`), or use the `skills` CLI: `npx skills add avifenesh/research-skills`.

## paper_lint.py

```bash
python3 scripts/paper_lint.py paper/main.tex                # from the repo root
python3 skills/arxiv-paper/scripts/paper_lint.py main.tex   # the copy that ships with the skill
python3 scripts/paper_lint.py --list-rules
```

Python 3.8 or newer, no dependencies. Prints `path:line: rule: message` and a count per rule. Follows `\input` and `\include`. Always exits 0, so it never blocks a build. Options: `--max-words N` (default 35), `--allow GLM,MLA` for names that need no definition, `--disable rule,rule`. A comment in the source works too: `% paper-lint: allow GLM MLA`.

It skips comments, `verbatim`, `lstlisting`, `minted` and similar environments, `\iffalse` blocks, math, and the preamble except `\title`.

### What it checks

| Rule | Flags |
|------|-------|
| `em-dash` | Unicode em dash or `---` |
| `en-dash` | Spaced `--`, `-` or en dash used as a prose dash; ranges like `1--4` pass |
| `hedge`, `filler`, `hype`, `plain-words` | Words from the lists in `language-style.md` |
| `unsupported` | "we believe", "novel", "significant(ly)" with no named test in the sentence |
| `contraction` | don't, it's, we're and the like, outside quotes |
| `acronym` | An all-caps token used before its `(ACRONYM)` definition; the abstract and body are separate scopes |
| `unit-space` | `16GiB` or `16 GiB`; write `16\,GiB` or `16~GiB` |
| `unit-consistency` | GB and GiB mixed, `sec` next to `s`, and nonstandard symbols (`sec`, `msec`, `hrs`) |
| `todo` | `\todo`, TODO, FIXME, TBD, XXX |
| `sentence-length` | Sentences over the word limit |
| `et-al` | `et al` without a period, `et. al.` |
| `cite-tilde`, `ref-tilde` | A space or line break before `\cite` or `\ref` |
| `float-label`, `float-unref`, `float-caption` | Missing `\label`, label before caption, label never referenced, missing caption, table caption below or figure caption above |
| `table-rules` | `\|` in a column spec, more than three `\hline` in a tabular |
| `abstract-length` | Abstract over arXiv's 1920-character limit |
| `arxiv-source` | `\today`, line numbers, double spacing, review or anonymous class options |

### What it does not check

Whether claims match evidence, baselines are fair, variance is reported, captions say what to read, or a sentence is clear. Passive voice, terminology drift and tense need a reader. The skill's review procedure in `SKILL.md` covers those with the checklist. The acronym rule is a heuristic: tokens with digits (A100, FP8) and unit symbols are skipped, and product names may need `--allow`.

## repo_audit.py

```bash
python3 scripts/repo_audit.py path/to/repo                       # from the repo root
python3 skills/research-repo/scripts/repo_audit.py path/to/repo  # the copy that ships with the skill
python3 scripts/repo_audit.py --list-rules
```

Python 3.8 or newer, no dependencies. Prints `path: rule: message` (`path:line:` where a line applies), then a count per rule and the detected license. Uses `git ls-files` when the directory is the top of a git repository, else walks the tree. Always exits 0. Options: `--max-bytes N` (large-file threshold, default 10 MiB), `--disable rule,rule`. Warnings carry a `warning:` prefix. More than five findings of one rule in one file are counted and summarized, not printed.

### What it checks

| Rule | Flags |
|------|-------|
| `license` | No LICENSE at the root (error); license text that matches no common SPDX license (warning). The summary names the detected type |
| `readme` | No README at the root |
| `readme-sections` | No opening paragraph; no results, install, quickstart, limits, citation or license section by heading; a results section that names no hardware or no software version |
| `reproduce` | No `REPRODUCE.md` and no reproduce section in the README |
| `citation-cff` | `CITATION.cff` missing, with tabs, or without `cff-version`, `message`, `title`, a list under `authors`; malformed `cff-version` or `date-released`; `.zenodo.json` next to it (warning) |
| `deps-pinned` | No dependency file and no lockfile; without a lockfile, torch, vllm, sglang, transformers and other engine packages with no version (error) or a range (warning), other packages with no bound (warning). Reads `requirements*.txt`, `pyproject.toml`, `environment.yml`, `setup.py`, `setup.cfg` |
| `home-path` | `/home/<user>/`, `/root/`, `/Users/<name>/`, `C:\Users\` in tracked text files; `/root/` is allowed in Dockerfiles |
| `private-path` | IP addresses (loopback and `0.0.0.0` excepted), `.local`, `.internal`, `.lan`, `.corp` hostnames, `user@host:` targets, `/mnt/`, `/data/`, `/scratch/` style mount paths (warnings) |
| `large-file` | A tracked file above the threshold (warning) |
| `data-license` | A directory of data files (`.csv`, `.jsonl`, `.parquet`, `.npy`, `.pt`, `.safetensors`, and so on) with no LICENSE, README, card, datasheet or manifest in it or a parent (warning) |
| `tests` | No tests directory or test files; tests with no README, CONTRIBUTING or docs command to run them |
| `git-tag` | A git repository with no tag (warning); skipped outside git |
| `secret` | Hugging Face, `sk-`, AWS, GitHub, Slack, Google and GitLab token shapes, private key headers. The token is not printed |
| `todo` | TODO, FIXME, XXX, TBD or OWNER in `.md`, `.rst`, `.txt`, `.cff`, `.adoc` files (warning) |
| `gitignore` | No `.gitignore` (warning) |
| `model-card` | A Markdown file with `base_model`, `pipeline_tag`, `library_name` or `model-index` in its front matter, or named like `MODEL_CARD.md`: missing `license` (error), `base_model`, `tags` or `library_name` (warnings), `license: other` without `license_name` |

### What it does not check

Whether the claims map is complete, the tolerance is honest, the hardware statement matches the paper, the data is content-free, or the archive DOI exists. `checklist.md` in the skill covers those with IDs, and the audit procedure in `SKILL.md` walks them.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Both scripts are covered. For the lint: one fixture per rule with the exact lines it must flag, a clean fixture that must produce no findings, CLI checks, and checks that the lint word lists match `language-style.md`. For the audit: one fixture repo per rule under `tests/fixtures/repos/` with the exact paths and lines it must flag, a clean repo that must produce no findings, negative cases (loopback addresses, `/root/` in a Dockerfile, TODO in code, a lockfile), a temporary git repository for the tag rule and the `git ls-files` scope, and CLI checks. Both skills: every cited key exists in `sources.md`, the router names every reference file, checklist IDs are unique, and no file contains an em dash.

## Credits

The content is distilled from two cited learning guides (2026-10-08): one on arXiv paper writing for ML systems research, one on research artifact repositories for ML systems papers. The sources behind each are listed with links in `skills/arxiv-paper/references/sources.md` and `skills/research-repo/references/sources.md`: Peyton Jones, Widom, Ernst, Levin and Redell, Zhang, Roscoe, Heiser, Hoefler and Belli, Gopen and Swan, Orwell, Strunk, Zinsser, Rougier et al., Wilke, the NeurIPS paper checklist, Pineau's reproducibility checklist, NIST, the arXiv help pages, the ACM badging policy, the sysartifacts guides, the cTuning and ASPLOS appendix templates, Papers with Code, Datasheets for Datasets, Model Cards, the Hugging Face Hub docs, Zenodo, GitHub, REUSE, Collberg et al., Trisovic et al., Raff, and the public repositories of vLLM, SGLang, FlashAttention, Mooncake and LMCache. The skills quote short passages and paraphrase the rest; the original works belong to their authors.

## License

Apache-2.0. See [LICENSE](LICENSE). To cite this repo, see [CITATION.cff](CITATION.cff).
