# Well-regarded repos and what to copy

Use when looking for a model to copy for a frozen artifact, a benchmark harness, a trace release or a multi-paper repo. Facts are as read on 2026-10-08; repos change.

| Repo | What it does well | Gap or caution |
|---|---|---|
| vLLM paper artifact `sosp-ae-39/sosp-ae-astra` [astra-repo][astra-review] | Frozen snapshot with a scope note; stated hardware (1xA100-40GB, 8xA100-80GB, 200+ A100 GPU-hours); `setup.sh` builds four conda environments (astra, orca, prefix-astra, prefix-orca; up to 1 hour of CUDA compilation); one section per figure with run times; shrunk traces; plotting scripts that write PDFs; baseline caveat. Reviewers on a GCP A100-40G granted Available, Functional and Reproduced and noted "tiny misconfigurations" fixed during evaluation | CUDA 11.3-era environment; a snapshot by design |
| vLLM [vllm-readme][vllm-repro][vllm-install][vllm-bench][vllm-collect-env] | README with About, Getting Started, Contributing, Citation, Contact; BibTeX for the SOSP '23 paper; `vllm bench latency/serve/throughput` and `benchmarks/` for serving, throughput and prefix-caching tests; an install page with exact ranges; a reproducibility page that states its limits; `collect-env` | No CITATION.cff or NOTICE at the root; the fetched benchmarks page did not describe result dashboards |
| FlashAttention [flash-attn-readme] | Per-version README sections with their own papers, benchmarks and BibTeX; explicit build requirements and the 2-hour ninja warning; the test command (`pytest -q -s tests/test_flash_attn.py`); an AUTHORS file | License named only as "see LICENSE" in the fetched README (type not checked); no CITATION.cff seen |
| SGLang [sglang-readme][sglang-blog-v02][sglang-bench-docs] | Credits to projects it learned from; `benchmark/` subdirectories per blog result with hardware tiers, pinned versions and offline and online command sets; documented benchmark tools and steady-state rules | Numbers are tied to old versions (v0.2.7), so pins matter |
| Mooncake [mooncake-readme][mooncake-fast25] | Content-free FAST '25 traces with field docs, request counts and token statistics; simulator and calculator tools; BibTeX; Apache-2.0 | The data license was not stated separately in the fetched pages |
| LMCache and LMBenchmark [lmcache-readme][lmbenchmark] | Product repo with CONTRIBUTING, SECURITY and CODE_OF_CONDUCT; a separate benchmark repo with dated config folders per model size and engine, one orchestration script, CSV outputs; cites three papers | Two repos to keep in step |
| Azure public dataset [azure-traces] | A trace release per paper, assets on GitHub Releases, one doc per version, a citation instruction, CC-BY-4.0 | Release assets are on GitHub, not an archival DOI |
| lm-evaluation-harness [lm-eval-harness] | Pluggable backends, YAML tasks, sample logging, an integrity check, a Zenodo DOI for a cited version | A harness, not a paper repo |
| MLPerf Inference [mlperf-inference] | Reference implementations, loadgen, compliance tests, versioned rounds with deadlines and seed commits | Process heavy; copy the idea of versioned rounds |

## What to copy for each job (design)

| Job | Copy from |
|---|---|
| A frozen artifact repo for one paper | astra: scope note, per-figure sections with run times, shrunk traces, baseline caveat |
| A living project that carries several papers | FlashAttention: one README section per paper version with its own benchmarks and BibTeX |
| Reproducing one blog or paper result inside a living repo | SGLang `benchmark/blog_v0_2`: pinned engine versions and command sets per hardware tier |
| A benchmark harness that compares engines | LMBenchmark: one config per engine and size, dated rounds; lm-evaluation-harness: adapters and integrity checks |
| A production trace release | Mooncake and Azure: derived fields only, field docs, request counts, a citation instruction |
| Stating install limits | vLLM install and reproducibility pages |
