# Repository layout

Use when starting the repo for a paper, deciding whether the artifact lives inside the project or beside it, or reorganizing a repo before release.

## Three patterns that work

| Pattern | Example | What it gives | Cost |
|---|---|---|---|
| Frozen artifact repo, separate from the living project | `sosp-ae-39/sosp-ae-astra` for the vLLM/PagedAttention SOSP '23 paper. Its README says it is "merely for reproducing the experiments" and points to the vLLM repo for current performance [astra-repo] | The exact code the paper ran, baselines included, one script per figure; never breaks because the project moved on | Goes stale on purpose; the first lines must say so |
| Paper directory inside the living repo | Mooncake `FAST25-release/` holds the traces, the paper PDF and docs [mooncake-fast25]; SGLang `benchmark/blog_v0_2/` holds hardware, version pins and commands for one release's numbers [sglang-blog-v02] | One place for users; versioned with the code | Needs tags, or the directory stops matching the code it was written for |
| Separate benchmark or harness repo | `LMCache/LMBenchmark`: `run_benchmarks.sh`, scenarios (ShareGPT replay, short in and out, long in and short out), `configs/April2025/<size>/<engine>.yaml`, CSV outputs named by QPS, TTFT and ITL processing scripts [lmbenchmark] | Competing engines measured by one harness; configs dated like rounds | Two repos to version together |

Pick one and say which in the README's first paragraph. A frozen repo that looks like the living project is a known complaint [astra-repo] (see `complaints.md`).

## Evidence on structure

- Good Enough Practices: one directory per project; `doc/`, `data/` for raw data and metadata, `results/` for generated files, `src/` for source, `bin/` for compiled programs; name files by function; keep a CHANGELOG; add README, LICENSE and CITATION [good-enough].
- The `src/` layout stops tests from importing the in-development copy by accident. The cost is an editable install before tests run [src-layout].
- Roots of well-regarded repos: vLLM keeps `benchmarks/`, `tests/`, `docs/`, `examples/`, `docker/`, `.github/`, LICENSE and SECURITY; LMCache adds CONTRIBUTING, CODE_OF_CONDUCT, MAINTAINERS; SGLang has `benchmark/`, `test/`, `docs/`, `docker/`; FlashAttention has `benchmarks/`, `tests/`, `training/`, `hopper/`, `AUTHORS`, `usage.md` [repo-roots].
- Engine adapters: lm-evaluation-harness separates evaluation logic from inference through pluggable backends (`hf`, `vllm`, API), YAML task configs, `--log_samples` for post-hoc analysis and `--check_integrity` for task data [lm-eval-harness]. MLPerf Inference ships a reference implementation per task, a `loadgen`, compliance tests and versioned rounds with seed commits [mlperf-inference]. LMBenchmark keeps one config per engine and model size [lmbenchmark].
- Harness layers in SGLang's docs: `bench_serving` for online metrics (TTFT, TPOT, ITL), `bench_one_batch_server`, `bench_offline_throughput`, `bench_one_batch` for kernels only. Use `num-prompts >= 5 * max-concurrency` to measure steady state, and `--disable-ignore-eos` with real prompts [sglang-bench-docs].
- Figure pipeline: the astra repo maps experiments to paper figures, notes run time per figure ("6+ hours", "18+ hours"), shrinks traces from 1 hour to 10 minutes for quick runs, and has plotting scripts that write PDFs [astra-repo].

## Recommended tree (design)

```
<repo>/
  README.md  REPRODUCE.md  LICENSE  NOTICE  CITATION.cff  CHANGELOG.md
  pyproject.toml  uv.lock  Dockerfile
  src/<pkg>/                 # installable library: algorithm, metrics, trace IO, result schema
    adapters/                # one module per engine (vllm.py, sglang.py), same interface
    harness/                 # load generator, runner, env capture, result writer
  configs/                   # one YAML per experiment id (t2_ours_8b, f5_sweep_qps)
  data/MANIFEST.json         # URL, sha256, size, license, source; the data itself lives on Zenodo or HF
  results/reference/         # shipped: per-run values plus env.json, one file per experiment id
  results/runs/              # git-ignored; reruns land here
  scripts/                   # thin wrappers: run_table2.sh, run_all.sh, make_figures.sh, check_results.sh
  paper/figures/             # figure code reads results/*.json only; no number typed by hand
  tests/                     # smoke, schema and expected-output tests
  docs/
```

Rules behind the tree:

1. Reusable logic in the package; paper-specific orchestration in configs and thin scripts.
2. Every table and figure maps to one experiment id, and the id names the config, the result file and the script.
3. The engine under test is an adapter, not an `if` in the harness.
4. Data is referenced by manifest and checksum, not committed (see `data-release.md`).
5. `results/runs/` is git-ignored; `results/reference/` is committed (see `reference-results.md`).
6. No absolute path anywhere. Paths come from a repo-root variable or the CLI. Hard-coded paths were the top failure class in a 9,000-file rerun study [trisovic].

## Files at the root and what each is for

| File | Purpose | Reference |
|---|---|---|
| `README.md` | What, results with setup, install, quickstart, reproduce, limits, citation, license | `readme.md` |
| `REPRODUCE.md` | Claims map, commands, hardware, wall time, expected output, tolerance | `reproduce.md` |
| `LICENSE`, `NOTICE` | The code license; required third-party notices | `licensing.md` |
| `CITATION.cff` | Machine-readable citation; `preferred-citation` points at the paper | `citation.md` |
| `CHANGELOG.md` | Newest first, one entry per release, paper version named | `releases.md` |
| `pyproject.toml`, `uv.lock`, `Dockerfile` | Pinned environment at every layer | `environment.md` |
| `data/MANIFEST.json` | Name, URL, size, sha256, license, source for every data file | `data-release.md` |
| `.gitignore` | `results/runs/`, caches, local env files | `tests-ci.md` |
