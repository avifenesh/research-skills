# Claims and evidence

Use when planning or checking the evaluation: claim-evidence mapping, what counts as a result, baselines, ablations, repeats and intervals, means and overheads, negative results, LLM serving metric definitions, the setup paragraph, limitations and threats to validity.

## 1. Tie every claim to evidence (design, after [peyton-jones][neurips-checklist])

Keep this table in your notes. Check it before every submission.

| Claim (as worded in the intro) | Evidence (figure, table, proof) | Setup (hardware, workload, versions) | Baselines | Runs and variation | Where it might not hold |
|---|---|---|---|---|---|

An empty cell means the claim is not supported yet, or the sentence must shrink. NeurIPS checklist item 1 asks exactly this: do the abstract and intro claims match the results [neurips-checklist].

## 2. What counts as a result

- Interpretable: enough information to understand the experiment, draw your own conclusions, assess certainty and possibly generalize. A review of 120 papers from three top HPC conferences found the state of practice lacking [hoefler-belli].
- Platform and software specified: hardware model, memory, network, compiler and library versions, measurement setup. "Missing platform specification" is a benchmarking crime [heiser][hoefler-belli].
- Absolute numbers next to relative ones. Hoefler rule 1: for a parallel speedup, say whether the base case is one parallel process or the best serial run, and give the base case's absolute performance. Never report ratios without absolute values [hoefler-belli]. "Relative numbers only" is a crime [heiser].
- Negative and mixed results that bear on a claim belong in the paper. "A seemingly good idea that didn't pan out is at least as interesting as one that did" [levin-redell]. Disclose whether the project used more compute than the reported experiments, including preliminary and failed runs [neurips-checklist].

## 3. Baselines

- Compare to the state of the art, not only to your previous version. Give competitors a fair setup. Include the proper baseline, usually the unmodified system [heiser].
- Do not report only the cases where you win. Use the whole benchmark, report all results, justify any subset (Hoefler rule 2) [hoefler-belli]. "Selective benchmarking" is Heiser's first crime [heiser].
- Tune baselines as hard as your own method and say how. Report expected validation performance as a function of the hyperparameter-search budget: test scores alone mislead, and different budgets pick different winners [dodge]. Report the hyperparameter range, the selection method and all values used [pineau-checklist].
- Invest in strong baselines, red-team your own evidence, and separate pre-specified from post-hoc analyses [nanda].
- Same harness and same node for every system (design).

## 4. Ablations and attribution

- Provide a design breakdown that isolates each design decision and each alternative: "essential but frequently omitted" [zhang].
- Do not credit an architectural change for a gain that came from tuning or other factors. Separate explanation from speculation. Avoid mathiness and loaded terms [lipton-steinhardt].
- One ablation per claimed mechanism, on the same workload and baseline as the headline result (design).

## 5. Repeats, variation and confidence intervals

- NeurIPS item 7: error bars, confidence intervals or significance tests at least for the experiments behind the main claims. State the factors of variability they capture (split, initialization, random draws, whole-run conditions). Say how they were computed (closed form, library call, bootstrap). State assumptions such as normality. Say whether the bar is SD or SEM; 1-sigma is fine if stated. No symmetric bars that reach impossible values such as negative error rates [neurips-checklist].
- Pineau checklist v2.0: the exact number of training and evaluation runs, a clear definition of the measure, central tendency and variation, average runtime or energy per result, the computing infrastructure [pineau-checklist].
- Hoefler rule 5: say whether measurements are deterministic; for nondeterministic data report confidence intervals. In their survey only 15 of 95 applicable papers gave any measure of variance, and only two gave confidence intervals around the mean [hoefler-belli].
- There is no universal repeat count. Model the variance at each level (build, execution, iteration) and put repetitions where the uncertainty is [kalibera-jones]. Data sampling, initialization and hyperparameter choice all add variance; randomizing more sources in a cheaper estimator approaches the ideal estimator at 51 times lower compute cost [bouthillier]. With 3 to 10 runs per task, report interval estimates (stratified bootstrap), score distributions and the interquartile mean rather than point estimates [agarwal].
- Measurement bias is real: innocuous setup changes such as environment size or link order can flip systems conclusions [mytkowicz] (snippet only).

### Practical rule (design)

- 3 runs: show the three values, or min and max. A bootstrap interval from 3 values is not informative.
- 10 or more runs: report the median and a bootstrap interval, and say which.
- Repeat at the level where variance lives (fresh process, fresh build, different node), not only inside one process.

### Bootstrap interval over independent runs (design; run with numpy 2.3.5 on 2026-10-08)

```python
import numpy as np

def median_ci(per_run_values, n_boot=10_000, alpha=0.05, seed=0):
    """per_run_values: one number per independent run, e.g. each run's p99 latency."""
    x = np.asarray(per_run_values, dtype=float)
    if len(x) < 10:
        raise ValueError("fewer than 10 runs: report the individual values instead")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(n_boot, len(x)))
    boots = np.median(x[idx], axis=1)
    lo, hi = np.quantile(boots, [alpha / 2, 1 - alpha / 2])
    return float(np.median(x)), float(lo), float(hi)
```

Caption: "median over R runs, bars are 95% percentile-bootstrap intervals of the median". NeurIPS wants the method named [neurips-checklist]. The 10-run floor is a design choice, not a sourced threshold.

## 6. Summaries and overhead arithmetic

- Arithmetic mean only for costs (time, energy, money). Harmonic mean for rates. Never average ratios; if only ratios exist, use the geometric mean and say so (Hoefler rules 3 and 4) [hoefler-belli].
- A throughput drop of x% is not an overhead of x%. Compare processing cost per unit of work and include total CPU load [heiser].
- Report an overhead in percent, not percentage points [heiser].
- Do not offload work to an uncounted "free" core [heiser].

## 7. ML serving and training metrics (design on top of [nvidia-llm-metrics][mlperf-inference])

Define every latency metric in the paper. NVIDIA's benchmarking documentation [nvidia-llm-metrics]:

| Metric | Definition |
|---|---|
| TTFT (time to first token) | Includes queueing, prefill and network latency |
| ITL (inter-token latency) | (end-to-end latency minus TTFT) divided by (output tokens minus 1) |
| End-to-end latency | TTFT plus generation time |
| System tokens/s | Total output tokens over the measurement window |
| Per-user tokens/s | The rate one user sees; a different number from system tokens/s, so name which one you report |

Definitions vary between tools: some exclude the first or last token or count streaming chunks [nvidia-llm-metrics]. Use one harness for every system.

Name in the paper (design): the tool and its version, the request arrival process, the prompt and output length distributions, the concurrency, the warm-up, the measurement window. Report latency percentiles with the load at which they were taken, not only mean throughput.

MLPerf Inference shows the comparability approach: prescribed rules and best practices so systems with different architectures can be compared [mlperf-inference].

## 8. Evaluation setup paragraph (checklist)

Hardware (model, count, memory, interconnect); driver and library versions; commit hashes; model and dataset names with versions and licenses; workload definition (arrival process, prompt and output lengths, concurrency); warm-up; measurement window; number of runs and what varies between them; metric definitions and the tool; baseline versions and their tuning.

Sources: run counts, duration, sizes, parameters [zhang]; runs, measure definition, infrastructure [pineau-checklist]; compute, NeurIPS item 8 [neurips-checklist]; platform [heiser].

## 9. Limitations and threats to validity

NeurIPS item 2 is the template: assumptions, how robust the results are if they fail, scope (few datasets, few runs), factors that influence performance. Limits a reviewer finds are worse than limits you state [neurips-checklist]. Software-engineering research sorts threats into conclusion, internal, construct and external validity [feldt-magazinius] (snippet only).

Systems version (design):

| Threat | Typical ML systems instance | Mitigation |
|---|---|---|
| Conclusion | Too few runs, no variance, tuned on the test workload | Report run counts and intervals; separate tuning and evaluation workloads |
| Internal | Warm-up, thermal or clock state, noisy neighbours, different library versions between baselines | Same node, same build, interleaved runs, recorded versions |
| Construct | Metric definitions differ across tools (TTFT), goodput versus throughput, synthetic prompts | Define metrics, one harness for all systems |
| External | One GPU generation, one model family, one workload shape | Say so; add a second setting or narrow the claim |

## Pitfalls

| Pitfall | Why it happens | Fix |
|---|---|---|
| Overhead stated as throughput loss | Throughput hides CPU load and latency | Cost per unit of work, with load [heiser] |
| Mean of speedups across benchmarks | The arithmetic mean feels natural | Harmonic for rates, arithmetic for costs, geometric only for ratios, or give absolute values [hoefler-belli] |
| Baseline tuned less than the new method | Effort goes to the new system | Same budget and harness; report the budget [dodge][heiser] |
| Error bars with no definition | Plotting default | Name SD, SEM or CI, the method, and what varies [neurips-checklist] |
| 3 runs shown as a confidence interval | Wish for a tight bar | Show the 3 values or min and max (design) |
| TTFT defined differently from the baseline's tool | Tool defaults differ | One harness; state the definition [nvidia-llm-metrics] |
