# Pre-submission checklist

Use as the final pass before posting to arXiv or submitting to a venue, and as the item list for reviewing a draft. Each item is one checkable line with an ID; report a failure as `file:line: ID: what is wrong`. Items marked `lint` are covered by `paper_lint.py`; run it first and keep its output. Details live in the file named in each section heading.

## First page (`abstract-intro.md`)

- FP1: The abstract states the problem, why it matters, what the solution achieves, and what follows.
- FP2: Every headline number names its baseline, hardware class, workload and metric.
- FP3: Every ratio has its base or an absolute value next to it.
- FP4: Every "up to" carries the condition under which it holds.
- FP5: The abstract uses no term that only the body defines.
- FP6: The abstract is at most 1920 characters for arXiv (lint: abstract-length).
- FP7: Page one says what is new and what is not.
- FP8: The contributions are a bulleted list of 2 to 4 refutable claims, each with a section pointer.
- FP9: The introduction answers what the problem is, why it is interesting, hard and unsolved, and what the approach is.
- FP10: Aspirational goals are marked as not reached.

## Claims (`claims-evidence.md`)

- CL1: Each intro claim has a row in the claim-evidence table with no empty cell.
- CL2: No sentence claims more generality than the hardware, models and workloads evaluated.
- CL3: Explanation and speculation are separated; no gain is credited to a mechanism without an ablation.
- CL4: "Significant" appears only with a named test and p-value (lint: unsupported).

## Evidence (`claims-evidence.md`)

- EV1: Baselines are the state of the art plus the unmodified system, not only your previous version.
- EV2: Baselines got the same tuning budget and harness as your method, and the paper says how they were tuned.
- EV3: The whole benchmark is reported; any subset is justified; at least one regime where you lose is shown.
- EV4: Every result states the number of runs and what varies between runs.
- EV5: Every error bar is named (SD, SEM or CI), with how it was computed.
- EV6: With fewer than 10 runs, per-run values or min and max are shown instead of an interval.
- EV7: No average of ratios; costs use the arithmetic mean, rates the harmonic mean, ratios the geometric mean.
- EV8: Overheads are cost per unit of work with CPU or GPU load, not a throughput drop.
- EV9: Absolute numbers appear next to every relative number.
- EV10: One ablation per claimed mechanism, on the headline workload and baseline.
- EV11: Every latency metric is defined (TTFT, ITL, end-to-end, tokens/s), with the tool and version.
- EV12: The setup paragraph names hardware, versions, commit hashes, models, datasets, workload, warm-up, window and runs.
- EV13: Negative and mixed results that bear on a claim are reported.

## Limits (`claims-evidence.md`)

- LI1: A limitations section states assumptions, robustness to their failure, scope and performance factors.
- LI2: Threats to validity cover conclusion, internal, construct and external validity.
- LI3: The scope of hardware, models and workloads is stated next to the claims it limits.

## Figures and tables (`figures-tables.md`)

- FT1: Every caption starts with an assertion and stands without the body text.
- FT2: Every axis and legend has a title, and numeric axes have units.
- FT3: Precision matches the noise; decimals are consistent within a column.
- FT4: Colors survive color-vision deficiency (no red-green-only distinctions, at most about 8 categories).
- FT5: Tables have no vertical rules and no rules between data rows (lint: table-rules).
- FT6: Table captions sit above the table and figure captions below the figure (lint: float-caption).
- FT7: Every float has a `\label` after its `\caption` and is referenced in the text (lint: float-label, float-unref).
- FT8: References use `Figure~\ref` with a tilde (lint: ref-tilde).

## Reproducibility (`reproducibility-artifacts.md`)

- RE1: A reproducibility statement says what is released, where, which versions produced which table, and how to re-run.
- RE2: Code, configs and raw per-run logs are archived with a DOI, or the plan to do so is stated.
- RE3: The README has one row per paper result with its exact command.
- RE4: Compute is disclosed: worker type, memory, time per run and total, and unreported preliminary or failed runs.
- RE5: What is not released is named, with the reason and the results it affects.
- RE6: Models and datasets released with the paper have a license and a structured description.

## Citations (`citations-bib.md`)

- CT1: Every reference lists all authors (no "and others").
- CT2: Published papers are cited at their venue, not as arXiv preprints.
- CT3: arXiv IDs are plain strings with a version where the version matters.
- CT4: Capitals and acronyms in titles are brace-protected in the `.bib`.
- CT5: Every software, model and dataset used is cited with version, URL and license.
- CT6: `et al.` has its period and citations use `~\cite` (lint: et-al, cite-tilde).

## Language (`language-style.md`)

- LA1: No em dashes and no spaced dashes in prose (lint: em-dash, en-dash).
- LA2: No hedges, filler, hype or stock phrases (lint: hedge, filler, hype, plain-words).
- LA3: No "we believe" and no "novel" (lint: unsupported).
- LA4: No contractions (lint: contraction).
- LA5: Every acronym is defined at first use in the abstract and again in the body (lint: acronym).
- LA6: Numbers and units are joined by `\,` or `~`, and one prefix system is used per quantity (lint: unit-space, unit-consistency).
- LA7: No sentence over the word limit (lint: sentence-length).
- LA8: One term per concept throughout; the system has one name.
- LA9: Active voice unless the paragraph is about the thing acted on.
- LA10: Past tense for experiments, present tense for the paper and general facts.
- LA11: No `\todo`, TODO, FIXME, TBD or XXX left (lint: todo).

## Venue (`venues.md`)

- VE1: Page limit and template match the current call for papers.
- VE2: Anonymization covers authors, affiliations, PDF metadata, self-citations, links, and (OSDI) the system name.
- VE3: The venue's LLM policy is followed and any required disclosure is in the paper.
- VE4: A required checklist (NeurIPS) is in the PDF.
- VE5: The paper fits the venue or track (research, industrial, operational systems).

## arXiv (`arxiv-submission.md`)

- AX1: An endorsement path is ready for every author who submits.
- AX2: The submitter's quota allows it (2 per month, 3 active).
- AX3: The primary category matches where the claim lives, with at most two cross-lists.
- AX4: Metadata: title without caps or Unicode, all authors, abstract at most 1920 characters, no word "Abstract".
- AX5: Comments carry page and figure counts, venue, and URLs followed by a space.
- AX6: The license is chosen on purpose and is compatible with the venue's form.
- AX7: The tarball builds from a clean tree with arXiv's TeX Live, includes `main.bbl`, has no hidden files and no EPS with pdflatex.
- AX8: No `\today`, line numbers, double spacing or review mode (lint: arxiv-source).
- AX9: Comments and drafts you do not want public are stripped from the source.
- AX10: A full English version is included.
- AX11: The PDF arXiv built has been read page by page.
