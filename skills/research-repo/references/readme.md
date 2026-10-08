# README

Use when writing or reviewing the README of a paper repository: what goes on the page, in which order, and the skeleton to start from.

## What the evidence asks for

- The Papers with Code template: title as the "official implementation of" the paper with its arXiv link; Requirements; Training with the exact commands and hyperparameters; Evaluation; Pre-trained Models with download links and training configuration; Results as a table; Contributing and license [pwc-readme].
- The checklist behind it analysed 200+ repos. NeurIPS 2019 repos with all five items had a median of 196 GitHub stars and a mean of 2,664 [pwc-code].
- Pineau's code checklist and Papers with Code both ask for "a table of results accompanied by precise command" [pineau-checklist][pwc-code].
- OSDI '26 wants a README with Getting Started (about 30 minutes, "Hello world"-sized) and Detailed instructions [osdi26-ae]. ASPLOS asks for "a single command that end-users can run to make sure the artifact is set up properly" [asplos27-appendix].
- The astra README opens with a scope note, states hardware (1xA100-40GB; 8xA100-80GB) and total cost (200+ A100 GPU-hours), and says setup takes up to an hour because of CUDA compilation [astra-repo].
- FlashAttention gives each paper version (FA1, FA2, FA3 beta, FA4) its own README section with its own benchmarks and citation, which keeps one repo honest about several papers. It also warns that compiling without ninja can take 2 hours and documents `MAX_JOBS` for low-RAM machines [flash-attn-readme].
- vLLM's install page is the model for stating requirements: Linux, Python 3.11 to 3.14, compute capability 7.5 or higher, default CUDA 12.9 wheels, `cu128` and `cu130` variants, a "fresh new environment" (as of 2026-10-08) [vllm-install].
- vLLM's reproducibility page says numbers are reproducible only on the same hardware and the same vLLM version [vllm-repro].
- SGLang closes its README with the projects it "learned the design and reused code from" [sglang-readme].

## Section order (design, evidence in brackets)

1. **One paragraph.** What it is, which paper (title, venue, arXiv version), what is in the repo, what is not. If the repo is a frozen snapshot, say so and link the living project [astra-repo].
2. **Headline results with exact setup.** One row per headline claim: model, hardware (GPU model and count), engine and version, workload or trace, metric definition, number of runs, median and range. A results table without hardware and versions is a finding [pwc-code][pineau-checklist][vllm-repro].
3. **Install.** The pinned path first (lockfile or container), then from source. State OS, Python, CUDA, driver and compute-capability range. State build time when it is long [vllm-install][flash-attn-readme][astra-repo].
4. **Quickstart.** About 30 minutes, one command that proves the install, the exact output to expect [osdi26-ae][asplos27-appendix].
5. **Reproduce the paper.** Table of result, command, wall time, hardware, expected output, tolerance; link `REPRODUCE.md` for detail. State the GPU-hour total up front [astra-repo].
6. **Layout.** One line per directory, plus where to add an engine adapter or a workload.
7. **Limits.** What does not reproduce, baselines you re-implemented (astra: its Orca implementation "may not be exactly the same" as the original), hardware you did not test, nondeterminism [astra-repo][vllm-repro].
8. **Citation.** BibTeX for the paper, a pointer to `CITATION.cff` and the archive DOI [vllm-readme][flash-attn-readme][mooncake-readme][lmcache-readme].
9. **License and credits.** The license name and the projects whose code or design you reused [sglang-readme].

Keep the README short enough to scan. Detail goes in `REPRODUCE.md` and `docs/`.

## Skeleton (design; unrun template, placeholders in angle brackets)

```markdown
# <Name>: <one-line claim>

Official code for "<Paper title>" (<Venue year>, [arXiv:<id>v1](https://arxiv.org/abs/<id>v1)).
This repository contains <system or library>, <benchmark harness>, <trace or data pointers> and the
scripts that produce Tables <n> and Figures <m>. It does not contain <proprietary parts, raw logs>.
The paper version maps to tag `v1.0.0` and DOI 10.5281/zenodo.<id>.

## Headline results

| Claim | Model | Hardware | Engine (version) | Workload | Metric | Runs | Median (range) |
|---|---|---|---|---|---|---|---|
| <C1> | <model> | <N x GPU model> | <engine x.y.z> | <trace or config id> | <metric definition> | 3 | <value> (<min> to <max>) |

## Install

    uv sync --locked            # or: docker build -t <name> .

Tested on: <OS>, driver <ver>, CUDA <ver>, GPUs <model>. Build time: <min>.

## Quickstart (about 30 minutes)

    uv run <pkg> smoke          # prints "OK" and the table in docs/expected_smoke.txt

## Reproduce the paper

| Result | Command | Wall time | Hardware | Expected | Tolerance |
|---|---|---|---|---|---|
| Table 2 | `bash scripts/run_table2.sh` | <h> | <hw> | results/reference/t2.json | <x>% |

Details, claims map and expected output: [REPRODUCE.md](REPRODUCE.md).

## Layout

## Limits

## Citation

## License and credits
```

## What the audit script checks

`repo_audit.py` detects these sections by heading keywords: results (with a hardware name and a version in the section), install, quickstart, limits, citation, license, and an opening paragraph before the first `##`. A reproduce section or `REPRODUCE.md` is checked by the `reproduce` rule. The script cannot judge whether the paragraph names the paper or whether the results table is complete; `checklist.md` items RM1 to RM9 cover that.
