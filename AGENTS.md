# AGENTS.md

Rules for agents working in this repo.

## What this repo is

Two AgentSkills skills, one directory each under `skills/`:

- `skills/arxiv-paper/`: the paper. `skills/arxiv-paper/SKILL.md` is the router, `skills/arxiv-paper/references/` holds one topic per file, `skills/arxiv-paper/scripts/paper_lint.py` is the LaTeX checker.
- `skills/research-repo/`: the repository behind the paper. `skills/research-repo/SKILL.md` is the router with an audit procedure, `skills/research-repo/references/` holds one topic per file, `skills/research-repo/scripts/repo_audit.py` is the repository checker.

`scripts/paper_lint.py` and `scripts/repo_audit.py` at the repo root are symlinks to the copies inside the skills. `tests/` covers both scripts and both sets of reference files; the LaTeX files directly under `tests/fixtures/` are lint fixtures and `tests/fixtures/repos/` holds the audit fixture repos.

## Writing rules

1. No em dashes anywhere. No emojis.
2. Short sentences, the fact first, no hedging, no generic assistant phrasing.
3. Every rule cites a source key that exists in the skill's own sources file (`skills/arxiv-paper/references/sources.md` or `skills/research-repo/references/sources.md`). A new source gets a row there with title, URL and how it was read. The two skills have separate key sets.
4. A fact that can change (a deadline, a limit, an arXiv policy) carries its "as of" date.
5. Judgement is tagged (design). Do not present it as a sourced rule.
6. A template or command in a reference file says whether it was compiled or run, and when.
7. Split reference files by user task. Do not fragment a topic to meet a line count.
8. The owner's local conventions go under a section titled "House rules (design)", separate from the sourced rules.

## Lint rules

- The lint has no dependencies and exits 0 on findings.
- Its word lists mirror the "Word lists" section of `skills/arxiv-paper/references/language-style.md`. Change both; the tests check it.
- A new rule gets an entry in `RULES`, a fixture named after the rule in `tests/fixtures/`, exact expected lines in `EXPECTED` in `tests/test_paper_lint.py`, and a row in the README table. `tests/fixtures/clean/main.tex` stays at zero findings.
- A rule ships only if a script can check it reliably. Judgement checks go in `skills/arxiv-paper/references/checklist.md`.

## Audit rules

- `skills/research-repo/scripts/repo_audit.py` has no dependencies and exits 0 on findings. It uses `git ls-files` only when the audited directory is the top of a git repository, else it walks the tree.
- Each rule has a level, `error` or `warning`; a finding may override the level (model-card does). Warnings print with a `warning:` prefix.
- A new rule gets an entry in `RULES`, a fixture repo named after it in `tests/fixtures/repos/`, exact expected `(path, line)` pairs in `EXPECTED` in `tests/test_repo_audit.py`, a row in the README table, and an `(audit: rule)` mark on the checklist item it covers. `tests/fixtures/repos/clean/` stays at zero findings.
- A rule ships only if a script can check it reliably. Judgement checks go in `skills/research-repo/references/checklist.md`.
- A secret finding prints the token kind and the line number only; the matched text stays out of the output.

## Before committing

```bash
python3 -m unittest discover -s tests
agnix . --strict
```

## Scratch

Lint and audit reports and other local output go in `work/` (git-ignored). Nothing else transient goes in the repo.
