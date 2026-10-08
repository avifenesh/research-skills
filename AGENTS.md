# AGENTS.md

Rules for agents working in this repo.

## What this repo is

One AgentSkills skill in `skills/arxiv-paper/`. `skills/arxiv-paper/SKILL.md` is the router, `skills/arxiv-paper/references/` holds one topic per file, and `skills/arxiv-paper/scripts/paper_lint.py` is the LaTeX checker. `scripts/paper_lint.py` at the repo root is a symlink to it. `tests/` covers the lint and the reference files.

## Writing rules

1. No em dashes anywhere. No emojis.
2. Short sentences, the fact first, no hedging, no generic assistant phrasing.
3. Every rule cites a source key that exists in `skills/arxiv-paper/references/sources.md`. A new source gets a row there with title, URL and how it was read.
4. A fact that can change (a deadline, a limit, an arXiv policy) carries its "as of" date.
5. Judgement is tagged (design). Do not present it as a sourced rule.
6. A template or command in a reference file says whether it was compiled or run, and when.
7. Split reference files by user task. Do not fragment a topic to meet a line count.

## Lint rules

- The lint has no dependencies and exits 0 on findings.
- Its word lists mirror the "Word lists" section of `skills/arxiv-paper/references/language-style.md`. Change both; the tests check it.
- A new rule gets an entry in `RULES`, a fixture named after the rule in `tests/fixtures/`, exact expected lines in `EXPECTED` in `tests/test_paper_lint.py`, and a row in the README table. `tests/fixtures/clean/main.tex` must stay at zero findings.
- A rule ships only if a script can check it reliably. Judgement checks go in `skills/arxiv-paper/references/checklist.md`.

## Before committing

```bash
python3 -m unittest discover -s tests
agnix . --strict
```

## Scratch

Lint reports and other local output go in `work/` (git-ignored). Nothing else transient goes in the repo.
