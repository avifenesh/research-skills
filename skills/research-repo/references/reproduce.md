# REPRODUCE.md and the artifact appendix

Use when writing the reproduction guide, the artifact appendix for a venue, or the claims map that ties each paper result to a command, hardware, run time and expected output.

## What the appendix templates ask for

- cTuning unified appendix (template V20240722): Abstract; Artifact check-list (algorithm, program, compilation, binary, model, data set, run-time environment, hardware, metrics, disk space, preparation time, execution time, public availability, licenses, archival status); Description (how to access, hardware and software dependencies, data sets, models); Installation (mandatory); Experiment workflow; Evaluation and expected results (mandatory); Experiment customization; Notes; Methodology [ctuning-appendix].
- ASPLOS 2027: five obligatory sections: Checklist; How to access; Dependencies; Installation and testing, with one command that proves setup; Evaluation, which must state "the maximum allowable variation of empirical results". Practical advice: list several possible devices when you need GPUs or FPGAs, keep VM images to a few GB, avoid AWS-only setups because reviewers cannot pay, show expected results beside actual outputs [asplos27-appendix].
- USENIX Security '26: the appendix is "a roadmap for evaluators": hardware, software and configuration requirements, the paper's major claims and how to reproduce each, and how to compare your output with the paper. At most 3 pages [sec26-ae].
- cTuning checklist ordering: abstract with minimal requirements first, then dependencies, access and installation, workflow, then expected results with tolerance. Disk space, preparation time and execution time help reviewers plan [ctuning-checklist].
- SOSP '23 "Reproduced" checklist: exact environment, precise commands per claim, resource needs per claim, reproducibility scripts, dependencies from established sources with modifications clearly separated [sosp23-badges].
- Packaging guide: automate workflows to avoid human error, test on a clean environment by following your own documentation, log successes and failures without noise, measure CPU, IO, memory and network needs, ship the Dockerfile with the container [sysartifacts-packaging].

## What evaluators do

- A "kick the tires" phase first, then reading the code to confirm it does what the paper says: "Merely running the code is not enough". Badges can be denied when reproduction needs "unreasonable effort" that automation could have removed [sysartifacts-evaluator].
- Hardware: speak to the chairs early; offer remote access to your machines, a simulation mode, or a public testbed such as CloudLab [sigops-sosp23].
- Screencasts replace a live run only for proprietary dependencies, compute above 24 hours, or hardware the evaluators cannot reach [sysartifacts-packaging].
- The astra reviewers ran on a GCP instance with one A100-40G, Debian 12, CUDA 11.3, gcc 10.2; "tiny misconfigurations" were fixed during evaluation; they granted Available, Functional and Reproduced with the note that exact numbers differ run to run while trends hold [astra-review].

## The claims map (design)

Every headline claim gets one row:

| Claim | Paper location | Experiment id | Command | Hardware | Wall time | Expected (median of 3) | Tolerance |
|---|---|---|---|---|---|---|---|

The row is the contract between the paper and the repo. An empty cell is a finding. The same table, shortened, is the "Reproduce" section of the README [sec26-ae][sosp23-badges][asplos27-appendix].

## Run time, hardware and expected output

- State wall time and GPU hours per experiment. The astra repo lists "6+ hours" and "18+ hours" per figure and shrinks the trace from 1 hour to 10 minutes for a quick run [astra-repo]. Long runs with no short path cause timeouts [sysartifacts-evaluator].
- State hardware per claim, not once for the repo: GPU model, count, memory, interconnect, driver, CUDA, CPU and RAM [sosp23-badges][astra-review].
- Show the expected output next to the command: the table the checker prints and what a pass looks like on the reference hardware and on one cheaper alternative (design; `reference-results.md`).
- Say what differs: proprietary inputs and their proxies, re-implemented baselines, untested hardware, known nondeterminism [acm-badging][astra-repo][vllm-repro].

## Skeleton (design; unrun template)

```markdown
# Reproducing "<Paper title>"

Paper version -> tag -> archive: arXiv v1 -> v1.0.0 -> Zenodo DOI 10.5281/zenodo.<id> (HF revision <40-char sha>)

## 0. Claims map
| Claim | Paper location | Experiment id | Command | Hardware | Wall time | Expected (median of 3) | Tolerance |

## 1. Getting started (about 30 minutes)
Hardware needed, install, one command that proves setup, the exact output to expect.

## 2. Full reproduction
One section per experiment id: what it measures, command, output path, run time, GPU hours.
Quick mode: `--quick` shrinks the trace; reference values in results/reference/quick/.

## 3. Check your results
    uv run python scripts/check_results.py results/runs results/reference
The printed table, and what a pass looks like on <reference hardware> and on <cheaper hardware>.

## 4. What differs or cannot be shipped
Proprietary inputs and the proxy data; re-implemented baselines; untested hardware; known nondeterminism.
```

## Mapping to a venue appendix (design)

| Appendix section | Source in the repo |
|---|---|
| Abstract, minimal requirements | README paragraph and Install |
| Check-list (hardware, metrics, disk, time) | REPRODUCE.md section 1 and the claims map |
| How to access | Archive DOI, tag, HF revision |
| Installation and testing | Install plus the quickstart command |
| Evaluation and expected results, maximum variation | Claims map plus `results/reference/` and the checker's tolerance |
| Customization | Configs directory and the adapter interface |

## House rules (design)

- For long runs: one run plus a validation run; if they disagree, three; if still unstable, five; if five do not settle within the noise margin, find out why before shipping a reference value.
- Claims about GPU execution, numerics or serving behavior need evidence from that hardware. A CPU smoke run proves the install, not the number.
