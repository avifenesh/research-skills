---
name: research-repo
description: "Use when building, releasing, auditing or preparing for artifact evaluation the code, benchmark and model repository behind an ML systems paper (serving, training, kernels, schedulers, traces, benchmarks): layout, README and REPRODUCE.md, ACM badges and MLSys, OSDI, USENIX and NeurIPS artifact rules, environment pinning, dataset and model cards, content-free traces, licenses, CITATION.cff and Zenodo DOIs, tests and CI, tags tied to paper versions, reference results and tolerances. Ships repo_audit.py, a repository checker. Not for writing the paper itself (use arxiv-paper), production deployment, packaging a library for PyPI, Jupyter notebooks, DVC or experiment trackers, model signing or SBOMs, or privacy law."
license: Apache-2.0
---

Reference files live under `references/`. Open the smallest file that matches the task; open a second one only when the task crosses a boundary.

Dated facts are as of 2026-10-08. Venue and hub rules change every cycle: re-read the cited page before acting on a date, a limit or a badge rule. `[key]` is a source in `references/sources.md`. (design) marks judgement, not a sourced rule. "House rules (design)" sections hold the owner's local conventions.

## Rules for every task

1. Release what lets a stranger regenerate the main table: dependency spec, training and evaluation code, the exact command per result, the data or a content-free substitute, weights or an access path, and expected outputs with a stated tolerance [pwc-code][acm-badging].
2. Every headline claim has a row in a claims map: paper location, experiment id, command, hardware, wall time, expected value, tolerance. An empty cell is a finding [sec26-ae][sosp23-badges][asplos27-appendix].
3. Pin every layer: lockfile, container digest, CUDA and driver written down, engine versions exact. `latest` and `pip install vllm` are unpinned [uv-lock][docker-practices][sglang-blog-v02].
4. Ship raw per-run values and a checker, not a lone mean. Three runs, median reported, all values kept (house rule) [asplos27-appendix][acm-badging].
5. Archive a tagged release with a DOI. A personal page or a moving branch is not an archive; GitHub alone is not enough for most badges [acm-badging][osdi26-ae][sec26-ae].
6. No license means nobody may use the code. Add the license on day one and carry data and weight licenses forward from their sources [cal-none][data-provenance].
7. No absolute paths, no PII, no secrets in tracked files or history [trisovic][hf-limits].

## Build routing

| User task | Open |
|-----------|------|
| Start the repo, frozen artifact vs living project vs harness repo, directory tree, where data and results live | `references/layout.md` |
| Write or fix the README: section order, headline table with setup, install, quickstart, limits, the skeleton | `references/readme.md` |
| REPRODUCE.md, the claims map, artifact appendix for a venue, run times, hardware per claim, quick mode, what evaluators do | `references/reproduce.md` |
| Lockfiles, hashes, Docker digests, CUDA and driver, engine pins, determinism flags, env capture, hard-coded paths | `references/environment.md` |
| What to test, smoke test with a fake adapter, expected-output tests, what CI runs, clean-machine test | `references/tests-ci.md` |
| Shipping results with the repo, tolerances, median of runs, the checker, quick-mode references, benchmark hygiene | `references/reference-results.md` |

## Release routing

| User task | Open |
|-----------|------|
| Dataset or trace release: datasheet, dataset card fields, Croissant, content-free traces, PII and gating, source licenses, manifest and checksums, hub revisions and DOIs | `references/data-release.md` |
| Model release: model card fields, `license`, `base_model`, `library_name`, safetensors, checksums, HF DOI, release checklist | `references/model-release.md` |
| Choosing or checking a license, NOTICE, copied code, mixed-license repos, weight and data licenses | `references/licensing.md` |
| `CITATION.cff`, BibTeX in the README, Zenodo and `.zenodo.json`, Software Heritage, where the DOI goes | `references/citation.md` |
| Tags tied to paper versions, SemVer, changelog, GitHub release flow, fixing a released version | `references/releases.md` |

## Audit routing

| User task | Open |
|-----------|------|
| Which badge to aim for, ACM definitions, MLSys, OSDI, USENIX Security, SOSP, ASPLOS and NeurIPS rules, Pineau and Papers with Code checklists | `references/badges-venues.md` |
| What evaluators and users complain about, with the measured evidence and the fix | `references/complaints.md` |
| Repos to copy for a frozen artifact, a harness, a trace release, a multi-paper repo | `references/examples.md` |
| Final pass before the release, item list for an audit | `references/checklist.md` |
| Source keys, how each source was read, known gaps | `references/sources.md` |

## Audit script

```bash
python3 scripts/repo_audit.py REPO_DIR            # from this skill directory
python3 scripts/repo_audit.py --list-rules
```

Reports `path: rule: finding` (with `path:line:` where a line applies) and a count per rule; always exits 0. Uses `git ls-files` when `REPO_DIR` is the top of a git repo, else walks the tree. Options: `--max-bytes N` for the large-file threshold (default 10 MiB), `--disable rule,rule`. It checks what a script can check: files present, headings, keys, pins, paths, secrets, sizes. It cannot judge whether the claims map is complete or the tolerance is honest.

## Audit a repo

1. Run `repo_audit.py` on the repo root. Keep its findings as they are; they are already `path: rule: finding`.
2. Read the README first paragraph, the headline table and the reproduce table. Walk `checklist.md` items LY1 to LY8 and RM1 to RM11. Skip the items marked `audit:`; step 1 has them.
3. Build the claims map from the paper's headline claims and the repo's commands (`reproduce.md`). Every empty cell is a finding against RP1.
4. Walk the rest of `checklist.md` in order: RP, BV, EN, DA, MO, LC, CT, TS, RL, RR. Open the data and model directories and the dependency files; do not trust the README's description of them.
5. Walk `complaints.md`. A row with nothing in the repo that pre-empts it is a finding.
6. Report one finding per line: `path: ID: the rule broken; the fix`. Order: blocks the release or the badge (no license, unpinned engine, secret or PII, no archive, no claims map), then reproduction risk (hard-coded paths, no hardware statement, no tolerance, no quick mode), then hygiene (changelog, tags, docs). Separate what the owner must decide (license choice, what data to release, which badge) from what can be fixed directly. Do not change the repo unless asked.
