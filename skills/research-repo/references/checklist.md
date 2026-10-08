# Pre-release checklist

Use as the final pass before tagging the release that goes with a paper, and as the item list for auditing a repo. Each item is one checkable line with an ID; report a failure as `path: ID: the rule broken; the fix`. Items marked `audit:` are covered by `repo_audit.py`; run it first and keep its output. Details live in the file named in each section heading.

## Layout (`layout.md`)

- LY1: The README's first paragraph says whether the repo is a frozen artifact, a paper directory in a living project, or a separate harness, and links the other side.
- LY2: Reusable logic is an installable package; paper orchestration is configs and thin scripts.
- LY3: Every table and figure in the paper maps to one experiment id that names its config, result file and script.
- LY4: Engines under test are adapters behind one interface, not branches in the harness.
- LY5: Data is referenced by a manifest with URL and sha256, not committed (audit: large-file).
- LY6: No absolute or machine-specific path in tracked files (audit: home-path, private-path).
- LY7: `results/runs/` or its equivalent is git-ignored; a `.gitignore` exists (audit: gitignore).
- LY8: Figure and table scripts read result files; no paper number is typed by hand.

## README (`readme.md`)

- RM1: An opening paragraph names the paper (title, venue, arXiv version), what is in the repo and what is not (audit: readme-sections).
- RM2: A headline results table has one row per claim with model, hardware, engine and version, workload, metric definition, run count, median and range (audit: readme-sections, partial).
- RM3: Install names the pinned path first and states OS, Python, CUDA, driver and compute-capability range (audit: readme-sections, partial).
- RM4: Build time is stated when it exceeds a few minutes.
- RM5: A quickstart of about 30 minutes gives one command that proves the install and shows its expected output (audit: readme-sections, partial).
- RM6: A reproduce table or a link to `REPRODUCE.md` gives command, wall time, hardware, expected output and tolerance per result (audit: reproduce).
- RM7: A limits section names what does not reproduce, re-implemented baselines, untested hardware and nondeterminism (audit: readme-sections, partial).
- RM8: Citation gives BibTeX for the paper and points to `CITATION.cff` and the archive DOI (audit: readme-sections, partial).
- RM9: License and credits name the license and the projects whose code or design was reused (audit: readme-sections, partial).
- RM10: The README is tested on a clean machine by someone who did not write it.
- RM11: No TODO, FIXME, TBD, XXX or OWNER placeholder is left in the docs (audit: todo).

## REPRODUCE.md and appendix (`reproduce.md`)

- RP1: A claims map lists every headline claim with paper location, experiment id, command, hardware, wall time, expected value and tolerance, no empty cell.
- RP2: Getting started finishes in about 30 minutes on the stated hardware and ends with a stated output.
- RP3: Each experiment states wall time and GPU hours.
- RP4: A quick mode exists for every experiment over an hour, with its own reference values.
- RP5: What differs or cannot be shipped is listed: proprietary inputs and their proxies, re-implemented baselines, untested hardware, nondeterminism.
- RP6: The venue appendix sections (checklist, access, dependencies, installation and test command, evaluation with maximum variation) are filled from the repo and match it.
- RP7: Hardware the evaluators cannot reach has a plan: remote access, simulation mode or a public testbed.

## Badges and venue (`badges-venues.md`)

- BV1: The target badges are chosen and the current call for artifacts has been read, with its date noted.
- BV2: The archive meets the venue's rule (Zenodo or equivalent; no personal page; GitHub only where the venue allows it).
- BV3: Proprietary components are documented with how to obtain them, and a proxy is included.
- BV4: The NeurIPS checklist items 4, 5, 8, 12 and 13 match what the repo ships.
- BV5: Compute is disclosed: worker type, memory, time per run and total, including failed runs.

## Environment (`environment.md`)

- EN1: A lockfile is committed or every dependency has a version bound (audit: deps-pinned).
- EN2: torch, vllm, sglang, transformers and the other engine packages are pinned exactly or locked (audit: deps-pinned).
- EN3: Container base images are pinned by digest; apt packages have versions.
- EN4: OS, driver, CUDA, GPU model and count, CPU and RAM are stated for the reference runs.
- EN5: Every result file carries an env block: GPU, driver, CUDA, CPU, OS, commit, lockfile hash.
- EN6: Seeds and determinism flags are set and their limits are stated.

## Data (`data-release.md`)

- DA1: Every data directory has a card, README, LICENSE or manifest beside it (audit: data-license).
- DA2: The dataset card covers creation, composition, uses, sensitive data, licensing and citation; Croissant is present when the venue requires it.
- DA3: Production traces are content-free: derived fields only, and the card says what the reduction cannot support.
- DA4: No PII in the repo or its history; gating is used where the data needs a license agreement.
- DA5: Every source dataset's license is traced to its origin and recorded with name, version and URL; the derived license is compatible.
- DA6: Every data file has a sha256 in the manifest and a verify script.
- DA7: Data on a hub is pinned by a 40-character revision and has a DOI; Zenodo uploads respect the file and size limits.

## Model (`model-release.md`)

- MO1: The model card front matter has `license`, `base_model` (or says the model is trained from scratch), `library_name`, `pipeline_tag` and `tags` (audit: model-card).
- MO2: The card has intended use, out-of-scope use, limitations and risks, training data and procedure, and evaluation with harness version, engine version and hardware.
- MO3: Weights are safetensors; no pickle checkpoint is shipped.
- MO4: A `SHA256SUMS` or equivalent is published for the weights.
- MO5: One repo per weight variant; quantized variants link the base with `base_model_relation`.
- MO6: Every usage snippet was tested in a clean environment after upload.
- MO7: The base model's license permits the release, and its naming or attribution duties are met.
- MO8: Batching, modalities, KV cache and concurrency are supported before the model is released (house rule).

## Licensing (`licensing.md`)

- LC1: A LICENSE file exists at the root and its SPDX type is recognized (audit: license).
- LC2: NOTICE exists when Apache-2.0 dependencies with a NOTICE are bundled, and lists only what is required.
- LC3: Copied third-party code keeps its header and license, and the README says which files.
- LC4: Mixed-license repos mark per-file licenses (REUSE or an equivalent table).
- LC5: Data and weights have their own license statements, compatible with their sources.
- LC6: Every asset used is cited with creator, version, URL and license name.

## Citation (`citation.md`)

- CT1: `CITATION.cff` exists with `cff-version`, `message`, `title`, `authors`, `version`, `date-released` and, once minted, `doi` (audit: citation-cff).
- CT2: `preferred-citation` points at the paper.
- CT3: The README carries BibTeX for the paper.
- CT4: Only one of `.zenodo.json` and `CITATION.cff` exists, or both are identical.
- CT5: The archive DOI appears in the README, `CITATION.cff` and `REPRODUCE.md`.

## Tests and CI (`tests-ci.md`)

- TS1: A `tests/` directory exists and the README or CONTRIBUTING says how to run it (audit: tests).
- TS2: Pure logic the paper's numbers depend on (metrics, loaders, simulators, parsers) has tests.
- TS3: Result files are validated against a schema.
- TS4: A CPU smoke test runs the whole pipeline on a toy input in minutes.
- TS5: CI runs lint, build, lockfile check, unit and smoke tests on CPU; no GPU benchmark runs in CI.
- TS6: No secret, token or private key is tracked (audit: secret).

## Releases (`releases.md`)

- RL1: An annotated tag exists for the code behind each paper version (audit: git-tag, presence only).
- RL2: `CHANGELOG.md` has an entry per release, newest first, naming the paper version.
- RL3: A GitHub release was created as a draft, assets attached, then published; no released version was edited.
- RL4: Zenodo archived the release and the DOI was copied back into README and `CITATION.cff`.
- RL5: `REPRODUCE.md` has the paper version to tag to DOI to model revision table.

## Reference results (`reference-results.md`)

- RR1: Reference results ship raw per-run values with units, workload, engine version and env block.
- RR2: Every reference value is the median of three runs, or the long-run rule was followed and the values are kept.
- RR3: Each metric has a tolerance chosen from the observed spread, tighter for deterministic quantities.
- RR4: A checker compares a rerun to the reference, prints a table, exits non-zero on a miss, and falls back to ordering and ratio checks when the hardware differs.
- RR5: The checker passed on the reference machine and failed on a deliberately broken run.
- RR6: The expected output of the checker is shown in the docs for the reference hardware and one alternative.
- RR7: Benchmark runs follow steady-state rules (prompts at least 5x concurrency, real-prompt EOS handling) and record the metric definitions.
