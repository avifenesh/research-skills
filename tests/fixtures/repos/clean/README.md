# Example: a KV cache placement rule

Official code for "Example paper title" (Example venue 2026, arXiv:0000.00000v1). This repository
contains the rule, the vLLM adapter, the benchmark harness and the scripts that produce Table 2.
It does not contain the raw production traces. The paper version maps to tag v1.0.0.

## Results

| Claim | Model | Hardware | Engine (version) | Runs | Median (range) |
|---|---|---|---|---|---|
| C1 | Qwen3-8B | 1 x A100 80 GB GPU | vLLM 0.30.0 | 3 | 0.69 (0.60 to 0.78) |

## Install

    uv sync --locked

Tested on Ubuntu 24.04, driver 570, CUDA 12.8.

## Quickstart (about 30 minutes)

    example smoke

## Reproduce the paper

See [REPRODUCE.md](REPRODUCE.md).

## Limits

The Orca baseline is re-implemented and may differ from the original.

## Tests

    python -m pytest tests

## Citation

See CITATION.cff.

## License

MIT. See LICENSE.
