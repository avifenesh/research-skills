# Reproducibility statements and artifacts

Use when writing the reproducibility statement, filling a venue checklist, preparing artifact evaluation, or releasing code, data, models or a benchmark with the paper.

## What a release must let someone do

Re-run the main table: dependencies, training and evaluation code, exact commands, model weights or an access path, and an archived copy with a DOI. Artifact evaluation is optional and happens after acceptance at MLSys and OSDI [mlsys26-ae][osdi26-ae][pwc-code].

## NeurIPS checklist items that matter for systems [neurips-checklist]

| Item | Asks for |
|---|---|
| 4 | A reasonable avenue for reproducibility: code, detailed instructions, hosted-model access or a checkpoint |
| 5 | Code, data, exact commands and environment for the main results, including baselines; anonymized at submission |
| 6 | The details needed to appreciate the results (data splits, hyperparameters, how they were chosen) in the main paper |
| 7 | Error bars (see `claims-evidence.md`) |
| 8 | Compute: type of workers, memory, time per run and in total, and whether the project used more compute than reported |
| 12 | Cite every asset used: creators, version, URL, license name |
| 13 | Document new assets with structured templates |
| 16 | LLM usage when it is part of the method |

The NeurIPS 2026 checklist is mandatory in the PDF; no checklist means desk reject. "No" or "n/a" with a justification is not grounds for rejection. "No because proprietary" is acceptable for code [neurips-checklist][neurips26-handbook].

## Pineau ML Reproducibility Checklist v2.0 [pineau-checklist]

- Models and algorithms: description, assumptions, complexity analysis.
- Theoretical claims.
- Datasets: statistics, splits, exclusions and pre-processing, a download link, the collection process for new data.
- Shared code: dependencies, training code, evaluation code, pretrained models, a README with a results table and the precise command per result.
- Experimental results: hyperparameter range and selection, exact number of runs, measure definition, central tendency and variation, runtime or energy, infrastructure.

The 2019 NeurIPS program that used it combined a code-submission policy, a reproducibility challenge and the checklist [pineau-2019].

ICLR encourages a paragraph-long Reproducibility Statement before the references that points to the relevant sections rather than repeating them [iclr26-guide].

## Artifact evaluation and badges

ACM badges v1.1 [eurosys25-ae][sigir-badges]:

| Badge | Meaning |
|---|---|
| Artifacts Evaluated: Functional | "Documented, consistent, complete, exercisable, and include appropriate evidence of verification and validation" |
| Artifacts Evaluated: Reusable | Listed in v1.1; the definition text was not read, check the ACM page |
| Artifacts Available | Permanently available for retrieval |
| Results Reproduced | A different person or team obtained the main results using, in part, the author's artifacts |
| Results Replicated | Obtained independently, without the author's artifacts (not implemented in the SIGIR copy) |

Venue rules (as of 2026-10-08):

- MLSys 2026: voluntary for accepted papers, does not affect acceptance. Ran 2026-03-08 to 2026-04-08, results 2026-04-16. Needs an artifact abstract, the paper PDF with an Artifact Appendix, a public repository link, and hardware and software requirements. Single-blind [mlsys26-ae]. MLSys 2027 artifact dates were not published when fetched.
- OSDI '26: only "Artifacts Available" was evaluated, after acceptance. A README with Getting Started instructions (about 30 minutes) and Detailed instructions; an optional two-page Artifact Appendix; archives such as Zenodo, GitHub or FigShare rather than personal websites. Single-blind [osdi26-ae].
- EuroSys 2025 criteria worth copying: a full README (environment, dependencies, build, configuration, usage), every component named as in the paper, no hard-coded machine-specific values, resource requirements per claim, external dependencies from official channels [eurosys25-ae].

## Code, model and benchmark release

- Dependency file, training code with hyperparameters, evaluation code, pretrained models, and a README results table with the precise command (NeurIPS 2020 recommendations) [pwc-code].
- Archive with a DOI; a personal website or a moving GitHub branch is not an archive [osdi26-ae][eurosys25-ae]. An archive DOI is what an "Available" badge needs (design).
- Model weights: release them or give an access path, with the license, the exact base model and version, and the data they were trained on, documented with a structured template [neurips-checklist] (design for the field list).
- Put a `CITATION.cff` at the repository root; see `citations-bib.md` [github-cff].
- Links in the paper to code or data must resolve to a public repository [arxiv-format].
- arXiv ancillary files (`anc/`) can hold extra data and code, but the paper cannot depend on them: they are not indexed and links may break. Never ship TeX as ancillary files [arxiv-anc].

### README results table

```markdown
| Paper result | Command | Time | Hardware |
|---|---|---|---|
| Table 2, row "Ours" | `bash scripts/run_table2.sh --system ours` | 40 min | 8x <GPU model> |
```

One row per reproduced result, each with its precise command [pwc-code][osdi26-ae].

## The statement (design)

One paragraph near the end of the paper. It says:

- what is released (code, configs, raw logs, weights, benchmark) and where (archive DOI);
- which hardware and software versions produced which table;
- how many runs back each number;
- how to re-run (the command);
- what is not released and why (license, privacy, size);
- which results the artifact does not reproduce.

```text
Reproducibility. Code, configurations and raw per-run logs are archived at <DOI> (commit <hash>).
Tables 2 and 3 were produced on <hardware, driver, library versions>; each number is the median of <R> runs,
and per-run values are in results/*.csv. `make table2` reproduces Table 2 in about <t> on the same hardware.
<Weights or benchmark> are released under <license> at <DOI>. We do not release <item> because <reason>;
Figure <n> therefore cannot be reproduced from the artifact.
```

## Compute disclosure

Type of workers, memory, time per run and in total, and whether the project used more compute than the reported experiments, including preliminary or failed runs [neurips-checklist]. Average runtime or energy per result and the infrastructure [pineau-checklist].

## Pitfalls

| Pitfall | Why it happens | Fix |
|---|---|---|
| Artifact only on a personal website or a moving branch | Convenience | Archive with a DOI (Zenodo, Figshare) [osdi26-ae][eurosys25-ae] |
| README without the command per table | Written last, in a hurry | Results table with commands [pwc-code] |
| Hard-coded paths and hostnames | Scripts grew on one machine | Configurable paths; resource needs per claim [eurosys25-ae] |
