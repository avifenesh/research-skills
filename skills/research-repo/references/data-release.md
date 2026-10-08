# Data and benchmark release

Use when releasing a dataset, a trace or a benchmark with the paper: the card, the datasheet, content-free derived data, PII, source licenses, checksums, hosting and DOIs.

## Documentation

- Datasheets for Datasets: document motivation, composition, collection process, preprocessing, cleaning and labeling, uses, distribution and maintenance [datasheets].
- Hugging Face dataset cards implement this as a `README.md` with YAML (`license`, `license_name`, `license_link`, `source_datasets`, `size_categories`, `task_categories`, `pretty_name`, `configs`, `dataset_info`, `extra_gated_*`) and sections Dataset Creation, Considerations for Using the Data, Personal and Sensitive Information, Licensing and Citation [hf-dataset-cards][hf-dataset-spec].
- The template's sensitive-data section asks whether the data may be personal, sensitive or private, naming categories such as addresses, uniquely identifiable names, health or financial data [hf-dataset-template].
- Croissant is a schema.org-based format with four layers: dataset metadata, resources (`FileObject`, `FileSet`), `RecordSet` structure, ML semantics. `FileObject` carries a sha256; licenses are SPDX identifiers; datasets use semantic versioning [croissant]. NeurIPS 2026 E&D requires Croissant with Responsible AI fields; Hugging Face, Kaggle and Dataverse generate the core part, self-hosted data needs a hand-built file [neurips26-ed-hosting][neurips26-ed-call].
- NeurIPS asks for a persistent identifier (DOI); the preferred hosts provide one; new datasets must stay available long-term [neurips-code-policy][neurips26-ed-hosting].

## Content-free and derived data

What systems papers release from production traffic:

- Mooncake FAST '25 traces: JSONL with `timestamp` (relative ms), `input_length`, `output_length`, `hash_ids` (remapped prefix block hashes, 512 tokens per block; equal ids across requests mean a shareable KV prefix). No raw text or tokens. Three files: conversation (12,031 requests), tool and agent (23,608), synthetic (3,993, built from public datasets with Poisson arrivals); the first two come from one hour of production traffic. Companion tools: a KV cache size calculator and a hit-rate simulator [mooncake-fast25][mooncake-readme].
- Azure LLM inference traces: a 2023 single-day sample (Splitwise, ISCA 2024) and a 2024 week-long sample (DynamoLLM, HPCA 2025); token counts only; files as GitHub Release assets; one markdown page per dataset version; CC-BY-4.0 (the repo header also lists MIT); citation of the matching paper required [azure-traces].
- Rule (design): release the fields the claim depends on (arrival times, lengths, prefix-sharing structure), drop everything that identifies a user or reproduces content, and say in the card which analyses the reduced data cannot support.

A content-free trace line (Mooncake field names; values are placeholders):

```json
{"timestamp": 0, "input_length": 0, "output_length": 0, "hash_ids": [0, 1, 2]}
```

## Privacy and sensitive data

- LMSYS-Chat-1M is the gated route: access needs a license agreement; names are redacted ("NAME_1") with a `redacted` field; moderation outputs ship with each message; the card warns about unsafe content and lack of decontamination [lmsys-chat-1m].
- Hub gating supports `extra_gated_prompt`, `extra_gated_fields`, manual or automatic approval and an EU-restriction flag. The gate is not anonymization; authors can revoke access [hf-gated].
- Never put PII in the repo history. Removing it later does not remove old commits (design). On the Hub, `super_squash_history` is destructive and "cannot be undone" [hf-limits].

## Source-dataset licenses

- Do not copy a license from a hub tag. The Data Provenance Initiative audited 1,800+ text datasets and found license omission above 70% and error rates above 50% on widely used hosting platforms [data-provenance].
- Trace each source to its original license, record it in the card (`source_datasets`, `license`) and the manifest, and check compatibility: CC BY-SA 4.0 adaptations may be relicensed to GPLv3 (one way only); BY-NC-SA has no non-CC compatible license; ShareAlike or NonCommercial inputs constrain the derived release [cc-compat][hf-licenses].
- NeurIPS item 12 expects license name, version and URL for every asset, and attention to terms of service for scraped data [neurips-checklist].

## Integrity, versioning and hosting

- Ship `data/MANIFEST.json` (name, URL, size, sha256, license, source, version) and a verify script (design). Croissant stores the same checksum field [croissant].
- Pin Hub downloads by the full 40-character commit hash (`revision=`), not a branch; tags and PR refs also work; the CLI accepts `hf://datasets/<id>@<revision>/<path>` [hf-download].
- Hub DOIs: "Generate DOI" in repo settings mints a DOI for the current revision; a new DOI can be generated for new versions and the old one becomes outdated; repos with a DOI are locked against delete, rename and visibility changes without a support request; DataCite receives the author names [hf-doi].
- Zenodo: each version is a separate record with its own metadata, files and identifier; metadata can be edited after publication, files and the identifier cannot (the upload page separately mentions a 45-day window; treat published files as immutable and cut a new version). Limit per upload: 100 files and 50 GB (as of 2026-10-08) [zenodo-records][zenodo-upload].
- Storage shape on the Hub: prefer Parquet or WebDataset; avoid custom loading scripts ("datasets that require custom code to use often end up with limited reuse"); stay under 100k files per repo, 10k entries per folder, 200 GB per file (hard limit 500 GB) [hf-limits].

## Templates (design; not run)

```json
{"name": "<trace-name>", "version": "1.0.0", "license": "CC-BY-4.0",
 "source": "<upstream URL and its license>", "files": [
  {"path": "traces/conversation.jsonl", "url": "https://zenodo.org/records/<id>/files/...",
   "bytes": 0, "sha256": "<64 hex>"}]}
```

```python
import hashlib, json, sys
from pathlib import Path

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

manifest = json.loads(Path(sys.argv[1]).read_text())
root = Path(sys.argv[2])
bad = [e["path"] for e in manifest["files"] if sha256(root / e["path"]) != e["sha256"]]
sys.exit(f"checksum mismatch: {bad}" if bad else 0)
```

```yaml
---
pretty_name: <Name>
license: cc-by-4.0
source_datasets: [<upstream/dataset>]
size_categories: [10K<n<100K]
task_categories: [<task>]
configs:
  - config_name: default
    data_files: [{split: train, path: data/train-*.parquet}]
# for sensitive data:
# extra_gated_prompt: "<terms>"
# extra_gated_fields: {Affiliation: text, I agree to the terms: checkbox}
---
```

## House rules (design)

- Public-data-only release when the paper's credibility depends on it: content-free or derived benchmark data, a frozen tag per paper version, and a checker that runs on public inputs only.
- Off-box storage defaults to Cloudflare R2. An R2 mirror is for users; it is not an archival repository. Pair it with a Zenodo or Hugging Face DOI for the badge.
