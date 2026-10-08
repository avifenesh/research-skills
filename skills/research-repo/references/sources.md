# Sources

Use to look up a `[key]` cited in any reference file of this skill, or to judge how a source was read.

Every fact in this skill comes from the learning guide "Research artifact repositories for ML systems papers (MLSys / OSDI style)" (generated 2026-10-08 from 89 sources). The `Guide` column is the guide's own source id. `Read as`: `raw` = page or markdown read directly; `PDF` = PDF pages read as images; `extracted` = fetched page passed through a small-model extraction, with numbers re-checked where they matter; `snippet` = search-result snippet only, the page was not read. Treat `snippet` facts as leads, not rules. No command in the guide was run; templates in this skill say so where they appear.

Text marked (design) is judgement from the guide or this skill, not a sourced rule. Sections titled "House rules (design)" hold the owner's local conventions; they are not from the sources.

| Key | Guide | Title | URL | Read as |
|---|---|---|---|---|
| `acm-badging` | S1 | ACM: Artifact Review and Badging, version 1.1 (2020-08-24) | https://www.acm.org/publications/policies/artifact-review-and-badging-current | raw |
| `mlsys26-ae` | S2 | MLSys 2026: Call for Artifact Evaluations | https://mlsys.org/Conferences/2026/CallForAEs | extracted |
| `osdi26-ae` | S3 | OSDI '26 Call for Artifacts | https://www.usenix.org/conference/osdi26/call-for-artifacts | extracted |
| `sec26-ae` | S4 | USENIX Security 2026: Artifact submission instructions | https://secartifacts.github.io/usenixsec2026/instructions | extracted |
| `sysartifacts` | S5 | Systems Research Artifacts (ATC, CAIS, EuroSys, FAST, OSDI, SC, SOSP) | https://sysartifacts.github.io/ | extracted |
| `sysartifacts-packaging` | S6 | Systems Research Artifacts: packaging guide for authors | https://sysartifacts.github.io/packaging-guide.html | extracted |
| `sysartifacts-evaluator` | S7 | Systems Research Artifacts: evaluator guide | https://sysartifacts.github.io/evaluator-guide.html | extracted |
| `sosp23-badges` | S8 | SOSP 2023 artifact badges (ACM v1.1 definitions with checklists) | https://sysartifacts.github.io/sosp2023/badges | extracted |
| `astra-review` | S9 | Artifact review summary: Efficient Memory Management for LLM Serving with PagedAttention (SOSP 2023) | https://sysartifacts.github.io/sosp2023/summaries/astra | extracted |
| `astra-repo` | S10 | sosp-ae-astra: artifact repo for the vLLM/PagedAttention SOSP 2023 paper | https://github.com/sosp-ae-39/sosp-ae-astra | extracted |
| `sigops-sosp23` | S11 | SIGOPS: Lessons learned from chairing the artifact evaluation at SOSP 2023 | https://www.sigops.org/2024/lessons-learned-from-chairing-the-artifact-evaluation-at-sosp-2023/ | extracted |
| `ctuning-appendix` | S12 | cTuning: Artifact Appendix template ae.tex (V20240722) | https://github.com/ctuning/artifact-evaluation/blob/master/docs/template/ae.tex | extracted |
| `ctuning-checklist` | S13 | cTuning: artifact evaluation checklist | https://github.com/ctuning/artifact-evaluation/blob/master/docs/checklist.md | extracted |
| `asplos27-appendix` | S14 | ASPLOS 2027: Artifact Appendix | https://www.asplos-conference.org/asplos2027/ae-artifact-appendix/ | extracted |
| `neurips-checklist` | S15 | NeurIPS Paper Checklist guidelines | https://neurips.cc/public/guides/PaperChecklist | extracted |
| `neurips-code-policy` | S16 | NeurIPS Code and Data Submission Guidelines | https://neurips.cc/public/guides/CodeSubmissionPolicy | extracted |
| `pineau-checklist` | S17 | Pineau: The Machine Learning Reproducibility Checklist v2.0 (2020-04-07) | https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf | PDF |
| `pineau-2019` | S18 | Pineau et al.: Improving Reproducibility in Machine Learning Research (NeurIPS 2019 program), JMLR 2021 | https://www.jmlr.org/papers/volume22/20-303/20-303.pdf | PDF |
| `pwc-code` | S19 | Papers with Code: releasing-research-code (ML Code Completeness Checklist) | https://github.com/paperswithcode/releasing-research-code | raw |
| `pwc-readme` | S20 | Papers with Code README template for ML research repos | https://github.com/paperswithcode/releasing-research-code/blob/master/templates/README.md | extracted |
| `pwc-shutdown` | S21 | paperswithcode-data issue: site redirects to Hugging Face (shutdown, July 2025) | https://github.com/paperswithcode/paperswithcode-data/issues/116 | snippet |
| `datasheets` | S22 | Gebru et al.: Datasheets for Datasets (CACM 2021 version) | https://arxiv.org/abs/1803.09010 | extracted |
| `model-cards-paper` | S23 | Mitchell et al.: Model Cards for Model Reporting | https://arxiv.org/abs/1810.03993 | extracted |
| `hf-model-cards` | S24 | Hugging Face Hub: Model Cards | https://huggingface.co/docs/hub/model-cards | extracted |
| `hf-card-annotated` | S25 | Hugging Face Hub: Annotated Model Card | https://huggingface.co/docs/hub/model-card-annotated | extracted |
| `hf-release-checklist` | S26 | Hugging Face Hub: Model Release Checklist | https://huggingface.co/docs/hub/model-release-checklist | extracted |
| `safetensors` | S27 | Hugging Face: safetensors documentation | https://huggingface.co/docs/safetensors/index | extracted |
| `hf-pickle` | S28 | Hugging Face Hub: Pickle scanning | https://huggingface.co/docs/hub/security-pickle | extracted |
| `hf-doi` | S29 | Hugging Face Hub: Digital Object Identifier (DOI) | https://huggingface.co/docs/hub/doi | extracted |
| `hf-dataset-cards` | S30 | Hugging Face Hub: Dataset Cards | https://huggingface.co/docs/hub/datasets-cards | extracted |
| `hf-dataset-template` | S31 | huggingface_hub: dataset card template | https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md | extracted |
| `hf-dataset-spec` | S32 | hub-docs: dataset card metadata specification | https://github.com/huggingface/hub-docs/blob/main/datasetcard.md | extracted |
| `hf-gated` | S33 | Hugging Face Hub: Gated datasets | https://huggingface.co/docs/hub/datasets-gated | extracted |
| `hf-licenses` | S34 | Hugging Face Hub: Licenses | https://huggingface.co/docs/hub/repositories-licenses | extracted |
| `hf-limits` | S35 | Hugging Face Hub: Storage limits and repository recommendations | https://huggingface.co/docs/hub/repositories-recommendations | extracted |
| `hf-download` | S36 | huggingface_hub: Download files from the Hub | https://huggingface.co/docs/huggingface_hub/guides/download | extracted |
| `github-cff` | S37 | GitHub Docs: About CITATION files | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files | extracted |
| `github-zenodo` | S38 | GitHub Docs: Referencing and citing content (Zenodo DOI) | https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content | extracted |
| `cff-format` | S39 | Citation File Format | https://citation-file-format.github.io/ | extracted |
| `zenodo-github` | S40 | Zenodo: Enable a GitHub repository | https://help.zenodo.org/docs/github/enable-repository/ | extracted |
| `zenodo-software` | S41 | Zenodo: Describe software (CITATION.cff and .zenodo.json) | https://help.zenodo.org/docs/github/describe-software/ | extracted |
| `zenodo-records` | S42 | Zenodo: About records (versioning) | https://help.zenodo.org/docs/deposit/about-records/ | extracted |
| `zenodo-upload` | S43 | Zenodo: Create a new upload | https://help.zenodo.org/docs/deposit/create-new-upload/ | extracted |
| `software-heritage` | S44 | Software Heritage: How to archive and reference your code (plus 2025-05-07 citation feature) | https://www.softwareheritage.org/how-to-archive-reference-code/ | snippet |
| `cal-apache` | S45 | choosealicense.com: Apache License 2.0 | https://choosealicense.com/licenses/apache-2.0/ | extracted |
| `cal-mit` | S46 | choosealicense.com: MIT License | https://choosealicense.com/licenses/mit/ | extracted |
| `cal-none` | S47 | choosealicense.com: No permission (no license) | https://choosealicense.com/no-permission/ | extracted |
| `asf-howto` | S48 | Apache Software Foundation: Licensing HOWTO (LICENSE and NOTICE) | https://infra.apache.org/licensing-howto.html | extracted |
| `reuse` | S49 | REUSE specification 3.3 | https://reuse.software/spec-3.3/ | extracted |
| `cc-compat` | S50 | Creative Commons: Compatible licenses | https://creativecommons.org/share-your-work/licensing-considerations/compatible-licenses/ | extracted |
| `data-provenance` | S51 | Longpre et al.: The Data Provenance Initiative (audit of dataset licensing and attribution) | https://arxiv.org/abs/2310.16787 | extracted |
| `croissant` | S52 | MLCommons: Croissant format specification | https://docs.mlcommons.org/croissant/docs/croissant-spec.html | extracted |
| `neurips26-ed-hosting` | S53 | NeurIPS 2026 Evaluations & Datasets: hosting guidelines | https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting | extracted |
| `neurips26-ed-call` | S54 | NeurIPS 2026 Call for Evaluations & Datasets | https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets | extracted |
| `lmsys-chat-1m` | S55 | LMSYS-Chat-1M dataset card | https://huggingface.co/datasets/lmsys/lmsys-chat-1m | extracted |
| `mooncake-readme` | S56 | Mooncake (kvcache-ai): repository README | https://github.com/kvcache-ai/Mooncake | extracted |
| `mooncake-fast25` | S57 | Mooncake FAST25-release directory (traces, docs) | https://github.com/kvcache-ai/Mooncake/tree/main/FAST25-release | extracted |
| `azure-traces` | S58 | Azure Public Dataset: LLM inference traces (2023 Splitwise, 2024 DynamoLLM) | https://github.com/Azure/AzurePublicDataset | extracted |
| `vllm-readme` | S59 | vLLM repository README | https://github.com/vllm-project/vllm | extracted |
| `vllm-repro` | S60 | vLLM docs: Reproducibility | https://docs.vllm.ai/en/latest/usage/reproducibility.html | extracted |
| `vllm-install` | S61 | vLLM docs: GPU installation | https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html | extracted |
| `vllm-bench` | S62 | vLLM benchmarks directory | https://github.com/vllm-project/vllm/tree/main/benchmarks | extracted |
| `vllm-collect-env` | S63 | vLLM issue 16598 and PR 7310: collect_env.py in bug reports | https://github.com/vllm-project/vllm/issues/16598 | snippet |
| `flash-attn-readme` | S64 | FlashAttention repository README | https://github.com/Dao-AILab/flash-attention | extracted |
| `sglang-readme` | S65 | SGLang repository README | https://github.com/sgl-project/sglang | extracted |
| `sglang-blog-v02` | S66 | SGLang benchmark/blog_v0_2: how to reproduce the v0.2 benchmark results | https://github.com/sgl-project/sglang/tree/main/benchmark/blog_v0_2 | extracted |
| `sglang-bench-docs` | S67 | SGLang docs: Benchmark and profiling | https://docs.sglang.io/docs/developer_guide/benchmark_and_profiling | extracted |
| `lmcache-readme` | S68 | LMCache repository README | https://github.com/LMCache/LMCache | extracted |
| `lmbenchmark` | S69 | LMCache/LMBenchmark: benchmark suite for LLM serving systems | https://github.com/LMCache/LMBenchmark | extracted |
| `repo-roots` | S70 | Root listings of vLLM, LMCache, SGLang and FlashAttention via the GitHub API, plus raw CITATION.cff checks (404s on 2026-10-08) | https://api.github.com/repos/vllm-project/vllm/contents | raw |
| `lm-eval-harness` | S71 | EleutherAI lm-evaluation-harness | https://github.com/EleutherAI/lm-evaluation-harness | extracted |
| `mlperf-inference` | S72 | MLCommons inference (MLPerf Inference) repository | https://github.com/mlcommons/inference | extracted |
| `uv-lock` | S73 | uv docs: locking and syncing (uv.lock) | https://docs.astral.sh/uv/concepts/projects/sync/ | extracted |
| `pip-hashes` | S74 | pip docs: Secure installs (hash-checking mode) | https://pip.pypa.io/en/stable/topics/secure-installs/ | extracted |
| `docker-practices` | S75 | Docker docs: Building best practices (pinning base images) | https://docs.docker.com/build/building/best-practices/ | extracted |
| `cuda-compat` | S76 | NVIDIA: CUDA Compatibility | https://docs.nvidia.com/deploy/cuda-compatibility/index.html | extracted |
| `nvidia-ctk` | S77 | NVIDIA Container Toolkit overview | https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html | extracted |
| `torch-random` | S78 | PyTorch docs: Reproducibility notes | https://docs.pytorch.org/docs/stable/notes/randomness.html | extracted |
| `src-layout` | S79 | Python Packaging User Guide: src layout vs flat layout | https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/ | extracted |
| `good-enough` | S80 | Wilson et al.: Good Enough Practices in Scientific Computing | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510 | extracted |
| `collberg` | S81 | Collberg, Proebsting, Warren: Repeatability and Benefaction in Computer Systems Research (technical report, 2015) | https://reproducibility.cs.arizona.edu/v2/RepeatabilityTR.pdf | PDF |
| `raff` | S82 | Raff: A Step Toward Quantifying Independently Reproducible Machine Learning Research | https://arxiv.org/abs/1909.06674 | extracted |
| `trisovic` | S83 | Trisovic et al.: A large-scale study on research code quality and execution | https://arxiv.org/abs/2103.12793 | extracted |
| `keep-changelog` | S84 | Keep a Changelog 1.1.0 | https://keepachangelog.com/en/1.1.0/ | extracted |
| `semver` | S85 | Semantic Versioning 2.0.0 | https://semver.org/ | extracted |
| `github-releases` | S86 | GitHub Docs: Managing releases in a repository | https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository | extracted |
| `pytest-approx` | S87 | pytest docs: pytest.approx | https://docs.pytest.org/en/stable/reference/reference.html#pytest-approx | extracted |
| `ml-test-score` | S88 | Breck et al.: The ML Test Score (Google Research) | https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/ | extracted |
| `sigplan-eval` | S89 | SIGPLAN Empirical Evaluation Guidelines | https://www.sigplan.org/Resources/EmpiricalEvaluation/ | extracted |

## Which source for what

| Source | Best for |
|---|---|
| `[acm-badging]` | Badge definitions and the tolerance language |
| `[sysartifacts-packaging]`, `[sysartifacts-evaluator]`, `[sigops-sosp23]` | What systems evaluators check and trip on |
| `[ctuning-appendix]`, `[asplos27-appendix]`, `[sec26-ae]` | Appendix skeletons and the "maximum allowable variation" rule |
| `[pwc-code]`, `[pineau-checklist]`, `[neurips-checklist]` | The code checklist, the README results table, the paper-side items |
| `[astra-repo]`, `[astra-review]` | A frozen artifact repo that passed Available, Functional and Reproduced |
| `[mooncake-fast25]`, `[azure-traces]`, `[lmsys-chat-1m]` | Content-free traces and the gated route |
| `[hf-model-cards]`, `[hf-card-annotated]`, `[hf-release-checklist]` | Model card fields and release steps |
| `[uv-lock]`, `[pip-hashes]`, `[docker-practices]`, `[torch-random]`, `[vllm-repro]` | Pinning and what determinism an engine can promise |
| `[collberg]`, `[trisovic]`, `[raff]` | Evidence on why repos fail to build or run |

## Unverified and gaps (as of 2026-10-08)

- 80 of 89 pages were read through a small-model extraction. Raw reads: the ACM badging page, the Papers with Code README and the CITATION.cff 404 checks. PDFs read as images: Pineau v2.0, Pineau et al. (pages 8 to 12), Collberg et al. (pages 1 and 2).
- The MLSys 2026 call for artifacts lives at `/Conferences/2026/CallForAEs`. MLSys 2027 artifact dates were not published when fetched.
- Archive rules disagree: OSDI '26 lists GitHub and GitLab among accepted archives; USENIX Security '26 prohibits them for the final archive; cTuning says GitHub does not qualify. The OSDI '26 page returned an empty body to the raw fetcher; its facts come from the extraction and a matching earlier guide.
- The CACM version of Collberg and Proebsting was not read (403); numbers are from the 2015 technical report abstract.
- The Nature page for Trisovic et al. required a login; figures are from the arXiv abstract and the PMC copy. It studies R code, not ML code.
- Zenodo's all-versions ("concept") DOI was not described in the fetched pages. Zenodo's pages differ on whether published files can change (records page: no; upload page: a 45-day window).
- FlashAttention and vLLM license types were not read. FlashAttention's lack of CITATION.cff comes from a listing summary; vLLM, SGLang, LMCache and Mooncake were confirmed by raw 404s. SGLang's README citation block was not seen.
- The Llama and Gemma license terms (naming and attribution duties for derivatives) were not read.
- Software Heritage, vLLM `collect-env` and the Papers with Code shutdown are snippet-level. The ML Test Score summary came from the landing page only. The NVIDIA Container Toolkit overview did not cover driver placement.
- No primary source exists for the "tag v1 = arXiv v1" convention; it is design. The directory tree, checker, tolerance policy, manifest and CI scope are design.
- Not covered: Jupyter notebooks, Nix, Apptainer or Singularity, DVC and experiment trackers, model signing and SBOMs, privacy law beyond platform features, ReScience, journal artifact tracks, OpenRAIL terms in detail, HF Spaces demos, Kaggle and OpenML hosting steps.
- No snippet in the guide or in this skill was run or type-checked unless the file says so.
