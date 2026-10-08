# What reviewers and users complain about

Use when auditing a repo before release: each row is a failure that has been measured or named by evaluators, with the fix. A repo with nothing that pre-empts a row is a finding.

| Complaint | Evidence | Fix |
|---|---|---|
| Code is not there, or does not build | Collberg et al. (601 papers from eight ACM conferences and five journals; 402 backed by code): for 32.3% the code could be obtained and built within 30 minutes, for 48.3% it built but may have needed extra effort, for 54.0% either they built it or the authors said it would build with reasonable effort. They propose a "sharing specification" stating what readers may assume [collberg] | Install from a lockfile or container; a clean-machine test; the sharing specification is the README's Limits section |
| Hard-coded paths, missing libraries, missing files | Trisovic et al. re-ran 9,000+ R files from 2,109 Harvard Dataverse datasets: 74% crashed on first execution, 56% after automatic cleaning; leading causes were hard-coded working directories and absolute paths, library problems and missing files. Six fixes: capture library versions, relative paths, a workflow manager, document the runtime in Docker, test in a clean environment, prefer open-source tools (R code, not ML; the failure classes are the same) [trisovic] | `repo_audit.py` rules `home-path` and `private-path`; a manifest for data files |
| Missing or incomplete dependency declarations, undeclared system requirements, weak install instructions, no high-level code docs | The evaluator guide lists all four [sysartifacts-evaluator] | Lockfile, OS and CUDA statement, a repository map in the README |
| Undocumented hardware | Specialized hardware, too little RAM or CPU, shared-hardware scheduling conflicts [sysartifacts-evaluator]; chairs: speak early, offer remote access or simulation [sigops-sosp23] | Hardware per claim in `REPRODUCE.md`; a CPU or simulation mode |
| Long runs and timeouts | The evaluator guide names long runtimes causing timeouts; astra lists 6+ and 18+ hour experiments [sysartifacts-evaluator][astra-repo] | Quick mode with its own reference values |
| Unclear parameters or expected results; scripts that need debugging | Evaluator guide; ASPLOS asks for expected results beside outputs and a maximum variation [sysartifacts-evaluator][asplos27-appendix] | Claims map with expected value and tolerance; the checker |
| Manual setup repeated per data point | Evaluator guide and packaging guide: automate [sysartifacts-evaluator][sysartifacts-packaging] | One script per table or figure |
| Unpinned versions | SGLang's reproduction note that vLLM 0.5.3 crashes under load while 0.5.2 works; Docker advice against mutable tags [sglang-blog-v02][docker-practices][sysartifacts-packaging] | Exact engine pins; digest-pinned images; `deps-pinned` rule |
| No license | Legally unusable by default [cal-none] | Add Apache-2.0 or MIT on day one; `license` rule |
| Baselines not faithful | astra says its Orca baseline is built on the vLLM architecture and "may not be exactly the same" as the original; saying so is the right fix [astra-repo] | Name re-implemented baselines in Limits and in the paper |
| Code alone is not enough | Raff: 255 papers reimplemented without the authors' code; releasing code "is not sufficient for determining reproducibility"; paper quality matters [raff] | The method is described in the paper well enough to re-implement |
| Scope confusion | Frozen artifact repos should say they are a snapshot and where the living project is [astra-repo] | First paragraph of the README |
| Contamination or unsafe content in data | The LMSYS-Chat-1M card warns of both [lmsys-chat-1m] | Say it in the dataset card |
| Paper numbers typed by hand | Figure scripts read nothing; the LaTeX table drifts from the results | Figure and table scripts read `results/*.json`; one command regenerates all [astra-repo] |
| Only a mean is shipped | Looks clean | Raw per-run values, env block and tolerance [asplos27-appendix][acm-badging] |
| Weights as pickle `.bin` | Default of `torch.save` | Safetensors; test loading [safetensors][hf-pickle] |
| Model card without limits or evaluation setup | Treated as an afterthought | Fill the annotated sections; state harness version and hardware [hf-card-annotated][hf-release-checklist] |
| Source-dataset license copied from a hub tag | Tags are often wrong | Trace to the original; record in card and manifest [data-provenance] |
| Raw prompts or user text in a release | Easiest to dump | Derived fields only (lengths, timestamps, remapped hashes) [mooncake-fast25][azure-traces] |
| Both `.zenodo.json` and `CITATION.cff` with different content | Added both for safety | One source of truth; Zenodo ignores the CFF when `.zenodo.json` exists [zenodo-software] |
| DOI minted from a branch | Zenodo needs a release | Tag, release, archive [zenodo-github][github-zenodo] |
| Edited a published release | "Small fix" | Never modify a released version; cut a patch release [semver][github-releases] |
| GPU benchmarks in CI | Wanting a green check | Thin CPU CI; GPU runs are local with attached reference results (design) |
| Fixing a PII leak by deleting a file | Git keeps history | Never commit PII; on the Hub, squash history knowing it is irreversible [hf-limits] |

Code release rates rose from 40% at submission to 74.4% at camera-ready at NeurIPS 2019 [pineau-2019]. The bar has moved from "is there code" to "does it run and match" (design).
