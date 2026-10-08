# Reference results and checking a rerun

Use when deciding what results to ship with the repo, how to state the tolerance, how many runs back a number, and how an evaluator checks a rerun.

## What the sources fix

- Reviewers need "the maximum allowable variation of empirical results (particularly important for performance numbers and speed-ups)" [asplos27-appendix]. cTuning asks for "expected results including maximum allowable variation" [ctuning-checklist].
- ACM requires agreement "within a tolerance" that does not change the main claims [acm-badging].
- The astra reviewers reproduced with "overall trends hold" while exact numbers differed [astra-review].
- vLLM numbers are reproducible only on the same hardware and version [vllm-repro]; PyTorch makes no cross-release guarantee [torch-random].
- The SIGPLAN empirical-evaluation checklist is the community reference for scoping and supporting such claims [sigplan-eval].

## Design for a systems repo

1. **Ship raw per-run values**, not only a mean: `results/reference/<id>.json` with `runs: [...]`, units, workload, engine and versions, and an `env` block (GPU, driver, CUDA, CPU, OS, git commit, lockfile hash).
2. **Three runs, report the median** (house rule). Keep all three values so a reader sees the spread. With three runs an interval is weak, so also keep a per-metric tolerance chosen from the observed run-to-run spread plus a margin.
3. **Tolerance by metric type**: tight (percent-level or exact) for deterministic quantities such as token counts, cache hit rates computed from a trace, accuracy under fixed seeds; wider for latency and throughput. Compare orderings and ratios too: the paper's claims are usually "A beats B by about X", and a faster or slower machine moves both.
4. **Checker**: `scripts/check_results.py` reads `results/runs/` and `results/reference/`, prints reference median, rerun median, relative difference, tolerance and verdict per metric, and exits non-zero on a miss. When the hardware differs from the reference, it switches to ordering and ratio checks only and says so.
5. **Expected output in the docs**: the table the checker prints, and what a pass looks like on the reference hardware and on one cheaper alternative.
6. **Quick mode**: a shrunk workload with its own reference values (astra shrinks the trace from 1 hour to 10 minutes) so evaluators finish in the "kick the tires" window [astra-repo][sysartifacts-evaluator].
7. **Prove the checker**: it passes on the reference machine and fails on a deliberately broken run before release.

## Templates (design; not run)

```json
{"id": "t2/ours/ttft_p50_ms", "unit": "ms", "better": "lower", "rel_tol": 0.10,
 "runs": [0.0, 0.0, 0.0], "env": {"gpu": "<model> x <n>", "driver": "<ver>", "cuda": "<ver>",
 "engine": "<name x.y.z>", "commit": "<sha>", "lock_sha256": "<hex>"}}
```

```python
import json, statistics, sys
from pathlib import Path

def med(p):  # one result file -> median of runs
    return statistics.median(json.loads(Path(p).read_text())["runs"])

ref_dir, run_dir = Path(sys.argv[2]), Path(sys.argv[1])
failed = False
for ref_path in sorted(ref_dir.glob("*.json")):
    ref = json.loads(ref_path.read_text())
    run_path = run_dir / ref_path.name
    if not run_path.exists():
        print(f"MISSING {ref['id']}"); failed = True; continue
    r, n = med(ref_path), med(run_path)
    rel = abs(n - r) / abs(r) if r else abs(n)
    ok = rel <= ref["rel_tol"]
    print(f"{'PASS' if ok else 'FAIL'} {ref['id']}: ref {r:g} rerun {n:g} diff {rel:.1%} tol {ref['rel_tol']:.0%}")
    failed |= not ok
sys.exit(1 if failed else 0)
```

## Benchmark hygiene that the reference run must follow

- Steady state: `num-prompts >= 5 * max-concurrency`; `--disable-ignore-eos` with real prompts; record TTFT, TPOT and ITL definitions [sglang-bench-docs].
- Pin the engine version in the result file; the version decides the numbers [sglang-blog-v02][vllm-repro].
- Ship the harness configs (one per engine and model size, dated like rounds) so the rerun uses the same load [lmbenchmark].

## House rules (design)

- Benchmarks and scientific write-ups report the median of three runs. For long runs, one run plus a validation run; if they disagree, run three; if still unstable, five; if five do not settle within the noise margin, find out why before reporting.
- Marketing headlines are separate: a site headline may use the best measured result as "up to" (the maximum, rounded down) or "from" (the minimum). Medians stay in the receipts.
- Do not benchmark on a production serving box.
- Claims about GPU execution, numerics, model or serving behavior need evidence from that hardware. CPU checks do not establish them.
