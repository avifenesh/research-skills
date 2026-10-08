---
name: arxiv-paper
description: "Use when drafting, revising, reviewing or submitting an ML systems paper (serving, training, compilers, kernels, schedulers, benchmarks) to arXiv or to MLSys, OSDI, SOSP, NeurIPS or ICLR: structure, abstract and contributions, claims and evidence, baselines, variance and intervals, LLM serving metrics, figures and tables, reproducibility and artifacts, citations and BibTeX, plain-English style, reviewer objections, arXiv endorsement, rate limits, categories, TeX build and metadata. Ships paper_lint.py, a LaTeX style checker. Not for theory-only or non-CS papers, grant proposals, theses, slides or posters, journal submission, or venue camera-ready templates and copyright forms."
license: Apache-2.0
---

Reference files live under `references/`. Open the smallest file that matches the task; open a second one only when the task crosses a boundary.

Dated facts are as of 2026-10-08. Venue and arXiv rules change every year: re-check the cited page before acting on a date or a limit. `[key]` is a source in `references/sources.md`. (design) marks judgement, not a sourced rule.

## Rules for every task

1. Reviewers decide from the abstract and page one: the problem, the one idea, 2 to 4 refutable claims with pointers to their evidence [peyton-jones][widom].
2. Every claim has a figure, table or proof with the setup, baselines, run count and variation stated. Shrink the claim when the evidence is narrower [neurips-checklist].
3. Report variation, not a lone number. Name the bar and the runs. With 3 runs, show the three values. Never average ratios; never give a ratio without its absolute base [hoefler-belli][heiser].
4. Release what re-runs the main table: code, configs, exact commands, weights or an access path, an archive with a DOI [pwc-code][osdi26-ae].
5. Plain words, short sentences, active voice, one term per concept, units with a space and an unambiguous prefix, no hype [orwell][ernst][nist-si][arxiv-moderation].
6. arXiv in 2026 is strict: endorsement needs prior authorship in the domain or a personal endorser; 2 submissions per month, 3 active; CS surveys and position papers need prior peer review [arxiv-endorse-2026][arxiv-rate-2026][arxiv-cs-review-2025].

## Writing routing

| User task | Open |
|-----------|------|
| Outline, section order, what each section must do, word budget, length, writing order | `references/structure.md` |
| Title, abstract, first page, introduction, contributions list, numbers in the abstract | `references/abstract-intro.md` |
| Baselines, tuning budget, ablations, repeats, error bars, bootstrap intervals, means and overheads, negative results, TTFT and ITL definitions, setup paragraph, limitations, threats to validity | `references/claims-evidence.md` |
| Captions, axes, units on axes, color, precision, booktabs tables, `\label` and `\ref` mechanics | `references/figures-tables.md` |
| Plain English, hedges, hype, filler, contractions, sentence length, acronyms, numbers and units, GB vs GiB, tense, terminology, LLM-assisted drafting | `references/language-style.md` |
| References, BibTeX, arXiv IDs and DOIs, all authors, Google Scholar fixes, software and model citation, `CITATION.cff` | `references/citations-bib.md` |

## Evidence release and review routing

| User task | Open |
|-----------|------|
| Reproducibility statement, NeurIPS and Pineau checklists, artifact evaluation, ACM badges, code, model and benchmark release, compute disclosure | `references/reproducibility-artifacts.md` |
| What reviewers will object to and how to pre-empt it, rebuttal planning | `references/reviewer-objections.md` |
| MLSys, OSDI, NeurIPS, ICLR: deadlines, page limits, review criteria, anonymity, preprint rules, LLM policy | `references/venues.md` |

## Submission routing

| User task | Open |
|-----------|------|
| arXiv endorsement, rate limit, moderation, categories and cross-lists, metadata, comments field, license, TeX Live, `.bbl`, figures, tarball, announcement times, replacing, withdrawing | `references/arxiv-submission.md` |
| Final pass before submitting, item list for a review | `references/checklist.md` |
| Source keys, how each source was read, which classic writing guide to read, known gaps | `references/sources.md` |

## Lint

```bash
python3 scripts/paper_lint.py main.tex [more.tex ...]   # from this skill directory
python3 scripts/paper_lint.py --list-rules
```

Reports `path:line: rule: message` and a count per rule; follows `\input`; always exits 0. Options: `--max-words N` (default 35), `--allow GLM,MLA`, `--disable rule,rule`. In-source: `% paper-lint: allow GLM MLA`. It checks mechanics only; it cannot judge claims, evidence or clarity.

## Review a draft

1. Run the lint on the main file. Keep its findings as they are; they are already `file:line: rule`.
2. Read the abstract and first page only. Walk `checklist.md` items FP1 to FP10.
3. Build the claim-evidence table from the contributions list (`claims-evidence.md` section 1). Every empty cell is a finding against CL1.
4. Walk the rest of `checklist.md` in order: CL, EV, LI, FT, RE, CT, LA, VE, AX. Skip the lint-covered items; step 1 has them.
5. Walk `reviewer-objections.md`. A row with nothing in the draft that pre-empts it is a finding.
6. Report one finding per line: `file:line: ID: the rule broken; the fix`. Quote the sentence when the line alone is not clear. Order: blocks submission (unsupported claim, missing variance, arXiv or venue policy violation), then reviewer risk, then style. Do not rewrite the paper unless asked.
