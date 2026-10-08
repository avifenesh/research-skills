# Tests and CI

Use when deciding what to test in a research repo, what CI should run, and what stays off CI.

## What to test (design, supported by [ml-test-score][osdi26-ae][asplos27-appendix])

| Test | Covers | Why |
|---|---|---|
| Pure logic | Metric functions, trace loaders, scheduling or cache simulators, parsers of engine logs | Cheap, fail loudly, and the paper's numbers depend on them |
| Schema | Every result JSON validates against the result schema: fields, units, run count, env block | A result without its environment cannot be checked later |
| Smoke | The whole pipeline on a toy input with a fake adapter on CPU, finishing in minutes | This is the "single command that proves setup" [asplos27-appendix] and the OSDI Getting Started run [osdi26-ae] |
| Expected output | A small input whose output is committed; compare with `pytest.approx` (default relative tolerance 1e-6, absolute 1e-12; `rel=` and `abs=` override) for deterministic code | Catches silent changes in the logic [pytest-approx] |
| Reference-results check | Hardware-dependent numbers go through the checker with a stated tolerance, not through `approx` | See `reference-results.md` |

The ML Test Score rubric (28 tests and monitoring checks in four groups: features and data, model development, ML infrastructure, monitoring) is a source of test ideas, written for production systems [ml-test-score].

Not in CI: GPU benchmarks. Run them locally or on a dedicated box before the release and attach the run as reference results (design).

```python
# Smoke test with a fake adapter (design; not run)
import pytest
from mypkg.harness import run_experiment
from mypkg.adapters.fake import FakeAdapter

def test_smoke_pipeline(tmp_path):
    out = run_experiment("configs/smoke.yaml", adapter=FakeAdapter(seed=0), out_dir=tmp_path)
    assert out["runs"] and out["env"]["commit"]
    assert out["metrics"]["output_tokens"] == pytest.approx(128, rel=0)
```

## Document how to run the tests

FlashAttention names the command (`pytest -q -s tests/test_flash_attn.py`) in its README [flash-attn-readme]. `repo_audit.py` flags a repo with no `tests/` or `test/` directory, and a repo whose README, CONTRIBUTING or REPRODUCE never mentions `pytest`, `unittest`, `make test`, `tox`, `nox`, `cargo test`, `go test`, `npm test` or `ctest`.

## CI (design)

Lint, build, install from the lockfile (`uv lock --check`, `uv sync --locked`), unit and smoke tests on CPU, a link check of the README. The `src/` layout makes CI test the installed package, not the checkout [src-layout][uv-lock].

## Clean-machine test

Test your own instructions on a clean machine by following the documentation, and have someone who did not write them do it once before release [sysartifacts-packaging][trisovic]. The astra reviewers fixed "tiny misconfigurations" during evaluation; a clean-machine run before submission finds them first [astra-review].

## House rules (design)

- CI stays thin: lint, build and merge validation. Run your own tests locally or on the dev server before pushing. External contributors' PRs, a daily full run and every release get the full suite.
- Private repos use the self-hosted runner server, never GitHub-hosted runners.
- In large active projects write tests only when needed: an integration test per piece of functionality, an e2e test per full feature, a unit test only for pure logic nothing else reaches. When the same error repeats in CI or review, add a lint rule for it.
- A test proves something only if it failed before the change and passes after it.
