# Model release on Hugging Face

Use when publishing weights with the paper: the model card, its YAML fields, `base_model`, license, safetensors, checksums, DOIs and the release checklist.

## The card

A model card is the repo's `README.md`: YAML metadata plus text. Metadata drives filters and widgets: `license`, `base_model`, `datasets`, `language`, `library_name`, `pipeline_tag`, `tags`, `new_version`, evaluation results, CO2 [hf-model-cards]. The text describes the model, intended uses and limits (bias and ethical considerations as in Mitchell et al.), training parameters, training data and evaluation results [hf-model-cards][model-cards-paper].

Field rules (as of 2026-10-08):

| Field | Rule | Source |
|---|---|---|
| `license` | An identifier from the Hub list (`apache-2.0`, `mit`, `cc-by-4.0`, the `openrail` family, `llama3.x`, `gemma`, and so on). Anything else: `license: other` plus `license_name` and `license_link`, with the text in a `LICENSE` file | [hf-model-cards][hf-licenses] |
| `base_model` | A single ID or a list. The Hub infers the relation (adapter, merge, quantized, finetune) or you set `base_model_relation`. Quantized variants go in separate repos linked this way, with the performance difference documented | [hf-model-cards][hf-release-checklist] |
| `library_name` | Set it explicitly; the old inference from `config.json` stopped for repos created after August 2024 | [hf-model-cards] |
| `datasets` | Hub dataset IDs so the model page links its training data | [hf-model-cards] |
| `pipeline_tag`, `tags`, `language` | Needed for search and the widget | [hf-model-cards] |
| Evaluation | The older `model-index` format came from Papers with Code; the newer format uses `.eval_results/*.yaml` files that reference Hub benchmark datasets and tasks | [hf-model-cards][hf-release-checklist] |

Annotated card sections [hf-card-annotated]: Model Details (developed by, funded by, type, language, license, finetuned from); Uses (direct, downstream, out-of-scope); Bias, Risks and Limitations (bias = skew for subpopulations; risk = socially relevant issue; limitation = likely technical failure mode) plus Recommendations; Training Details (data, preprocessing, speeds, sizes, times); Evaluation (testing data, factors, metrics, results, summary; ideally disaggregated); Environmental Impact (hardware, hours, provider, region, carbon); Technical Specifications; Citation; Glossary; Authors; Contact; Getting Started code.

For a systems paper, the Evaluation section also names the harness and its version, the hardware, and the serving engine and version that produced the numbers (design).

## Weights

- Pickle `.bin` files can execute arbitrary code when loaded. The Hub's pickle-import scan "is not 100% foolproof" and a ClamAV scan does not cover pickle exploits [hf-pickle]. Safetensors is safe and zero-copy; a converter exists for old files [safetensors][hf-release-checklist].
- Every LFS file carries a sha256 OID visible in the Hub UI and in pointer files; the download client queries Xet storage by that sha256 [hf-limits][hf-download]. Also publish a `SHA256SUMS` so users can verify out-of-band (design).
- Files under 200 GB (hard limit 500 GB); split larger weights [hf-limits].
- Pin loads to a revision: the full 40-character commit hash, a tag or a PR ref [hf-download].

## Release checklist [hf-release-checklist]

1. One repo per weight variant, grouped in a collection.
2. Weights in safetensors.
3. The metadata block filled.
4. Copy-and-run usage snippets.
5. Limitations stated.
6. Gated access if needed.
7. After upload, test every snippet in a clean environment.

## DOI and permanence

- "Generate DOI" in repo settings mints a DOI for the current revision; new versions get a new DOI and the old one becomes outdated; a repo with a DOI is locked against delete, rename and visibility changes without a support request [hf-doi].
- Link the paper on the card; the Hub extracts the arXiv id into a tag [hf-model-cards].

## Template (fields from the Hub docs; not run)

```yaml
---
license: apache-2.0            # or: other + license_name + license_link, plus a LICENSE file
base_model: <org>/<base-model>
base_model_relation: finetune  # adapter | merge | quantized | finetune
library_name: transformers
pipeline_tag: text-generation
datasets:
  - <org>/<dataset>
language: [en]
tags: [<tag>]
---
# <Model name>
Intended use / Out-of-scope use / Limitations and risks / Training data and procedure /
Evaluation (data, metrics, results, harness version, hardware) / How to load (pinned revision) /
Citation / Contact
```

`repo_audit.py` treats any Markdown file with YAML front matter that carries `base_model`, `pipeline_tag`, `library_name` or `model-index`, or a file named like `MODEL_CARD.md`, as a model card, and flags a missing `license`, `base_model`, `tags` or `library_name`. A model trained from scratch has no `base_model`; say so in the card and accept the warning.

## House rules (design)

- Release a model only when it is fully supported: batching, the modalities it takes (image, video, audio), KV cache, concurrency and the rest of what serving it needs.
- Loading and running a model does not show its family is supported. Check that model's own weights, quantization and outputs before the card claims support.
- The license of the base model governs derivatives. State it in `license` and `base_model`, and read the base license for naming and attribution duties (the Llama and Gemma terms were not read for this skill) [hf-model-cards][hf-licenses].
