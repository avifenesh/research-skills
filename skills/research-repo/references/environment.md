# Environment pinning

Use when writing the install path, the Dockerfile, the lockfile, the hardware statement, or when a reviewer cannot rebuild the environment.

Pin each layer on its own. A lockfile does not pin the CUDA driver, the container, or the engine you benchmark against.

## Layers

| Layer | What to do | Source |
|---|---|---|
| Python dependencies | Commit `uv.lock` (exact versions with hashes); install with `uv sync --locked`; `uv lock --check` verifies the lock matches `pyproject.toml`; the lock is not upgraded because newer versions exist | [uv-lock] |
| Hash-checked pip | `pip install --require-hashes -r requirements.txt` needs every requirement pinned with `==` and a hash; sha256 recommended. pip 26.2 added `--no-require-hashes` (as of 2026-10-08) | [pip-hashes] |
| Container base | Tags are mutable; pin the base image by digest (`image:tag@sha256:...`) and let Dependabot (`package-ecosystem: docker`) raise update PRs; combine `apt-get update` and `install` in one `RUN` and pin versions (`pkg=1.3.*`) | [docker-practices] |
| Systems-artifact advice | "Use a tag when using another image (and not the `latest` one)"; `apt-get update` returns different versions over time; archive the image on Zenodo as insurance | [sysartifacts-packaging] |
| CUDA and driver | Document platform, driver, GPU and CUDA toolkit together. CUDA 11+ minor-version compatibility lets apps built for one major release run on newer drivers with some feature limits; the `cuda-compat` package lets newer toolkits run on older base drivers within platform and GPU limits | [cuda-compat] |
| GPU in containers | NVIDIA Container Toolkit provides the runtime and CLI; the overview page does not say where the driver lives, read the install guide | [nvidia-ctk] |
| Engines under test | SGLang's v0.2 reproduction pins `git checkout v0.2.7` and `pip install vllm==0.5.2`, and notes that vLLM 0.5.3 "often crashes under high loads"; FlashInfer comes from a CUDA- and torch-specific wheel index | [sglang-blog-v02] |
| Engine install ranges | vLLM: Linux, Python 3.11 to 3.14, compute capability 7.5+, default CUDA 12.9 wheels, `cu128` and `cu130` variants, nightly wheels, a "fresh new environment" because kernels are compiled per version (as of 2026-10-08) | [vllm-install] |
| Build from source | FlashAttention: PyTorch 2.2+, CUDA 12.0+ (ROCm 6.0+), `ninja`, `MAX_JOBS`; 2 hours without ninja | [flash-attn-readme] |

Exact engine versions, not ranges: the version decides the numbers [sglang-blog-v02][vllm-repro]. `repo_audit.py` flags torch, vllm, sglang, transformers and the other engine packages when they have no `==` pin and no lockfile.

## Determinism and what an engine promises

- PyTorch gives no reproducibility guarantee across releases, commits or platforms. Use seeds, `torch.use_deterministic_algorithms(True)`, `CUBLAS_WORKSPACE_CONFIG`, `cudnn.benchmark = False`, controlled DataLoader workers [torch-random].
- vLLM: the seed defaults to 0 in V1; set `VLLM_ENABLE_V1_MULTIPROCESSING=0` for deterministic scheduling offline, or enable batch invariance; results are reproducible "only on the same hardware and the same vLLM version" [vllm-repro].
- Write what the engine cannot promise into the README's Limits section and into the tolerance of the reference results (`reference-results.md`).

## Environment capture

- vLLM ships `collect_env.py` (`vllm collect-env`) and asks for its output in bug reports (snippet-level) [vllm-collect-env].
- Write an `env.json` into every result file: GPU model and count, driver, CUDA, CPU, OS, git commit, lockfile hash (design).
- The hardware statement belongs in the README and in the result files, not only in the paper. The astra reviewers' machine: a GCP instance with one A100-40G, Debian 12, CUDA 11.3, gcc 10.2 [astra-review].

## Templates (design; from the cited docs, not run)

```bash
uv lock                     # resolve; commit uv.lock
uv sync --locked            # install exactly what the lock says; fails if the lock is stale
uv lock --check             # CI: lock matches pyproject.toml
```

```dockerfile
# Tag for humans, digest for the machine (Docker docs).
FROM <registry>/<cuda-base>:<tag>@sha256:<digest>
RUN apt-get update && apt-get install -y --no-install-recommends \
      <pkg>=<version> && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock ./
RUN uv sync --locked
```

```bash
# Capture the environment next to every result
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv
python -c "import torch; print(torch.__version__, torch.version.cuda)"
git rev-parse HEAD; sha256sum uv.lock
```

```python
# Determinism preamble (PyTorch notes; add engine flags)
import os, torch
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"   # the notes list :16:8 or :4096:8
torch.manual_seed(0); torch.cuda.manual_seed_all(0)
torch.use_deterministic_algorithms(True)
torch.backends.cudnn.benchmark = False
```

## Hard-coded paths and machine state

- A 9,000-file rerun study found 74% of scripts crashed on first execution; leading causes were hard-coded working directories and absolute paths, library problems and missing files. Its fixes: capture library versions, relative paths, a workflow manager, the runtime in Docker, a clean-environment test, open-source tools [trisovic].
- `repo_audit.py` flags `/home/<user>/`, `/root/`, `/Users/<name>/` and `C:\Users\` in tracked text files, and warns on IP addresses, internal hostnames and mount paths.
