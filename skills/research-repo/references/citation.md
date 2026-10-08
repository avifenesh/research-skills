# Citation and archiving

Use when adding `CITATION.cff`, the BibTeX block in the README, a Zenodo or Software Heritage archive, or a DOI for the code, the data or the model.

## CITATION.cff

- A plain-text file with human- and machine-readable citation data for software and datasets (CFF 1.2.0). GitHub reads it from the repository root on the default branch, shows "Cite this repository", and generates APA and BibTeX. `preferred-citation` points users to the paper instead of the software. Zenodo and Zotero also read CFF [github-cff][cff-format].
- Minimal keys in GitHub's example: `cff-version`, `message`, `authors`, `title`, `version`, `doi`, `date-released`, `url` [github-cff].
- The ML-systems repos checked here had none: vLLM, SGLang, LMCache and Mooncake returned 404 for `CITATION.cff` on `main` (2026-10-08); the FlashAttention listing showed none either [repo-roots]. vLLM, FlashAttention, Mooncake and LMCache put BibTeX in the README instead; FlashAttention gives one entry per paper version and LMCache cites its own paper plus CacheGen and CacheBlend [vllm-readme][flash-attn-readme][mooncake-readme][lmcache-readme]. Do both: CFF for machines, BibTeX for people (design).

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite the paper below."
title: "<Software name>"
version: 1.0.0
date-released: 2026-10-08
doi: 10.5281/zenodo.<id>
url: "https://github.com/<org>/<repo>"
authors:
  - family-names: "<Family>"
    given-names: "<Given>"
preferred-citation:
  type: conference-paper
  title: "<Paper title>"
  authors:
    - family-names: "<Family>"
      given-names: "<Given>"
  collection-title: "<Venue>"
  year: 2026
  url: "https://arxiv.org/abs/<id>v1"
```

Keys follow GitHub's example; check `preferred-citation` against the CFF schema guide before relying on it. The template was not validated with `cffconvert`.

`repo_audit.py` checks that `CITATION.cff` exists, parses as simple YAML, and has `cff-version`, `message`, `title` and a non-empty `authors` list.

## Archiving with a DOI

- Zenodo through GitHub releases: enable the repository in Zenodo's GitHub settings; each GitHub release is archived and gets a DOI [github-zenodo][zenodo-github].
- Zenodo metadata comes from `.zenodo.json` or `CITATION.cff`. If both exist, "only the `.zenodo.json` metadata will be used" [zenodo-software]. Keep one, or keep them identical.
- Each Zenodo version is a separate record with its own identifier; files cannot change after publication (the upload page mentions a 45-day window; treat files as immutable). Limit: 100 files and 50 GB per upload (as of 2026-10-08) [zenodo-records][zenodo-upload]. Zenodo's all-versions "concept" DOI was not described in the fetched pages; verify before writing "cite all versions" advice.
- A Zenodo record is what OSDI, USENIX Security and ACM accept as permanent; GitHub alone is not archival for the badge [acm-badging][osdi26-ae][sec26-ae]. lm-evaluation-harness cites a release (v0.4.3) with a Zenodo DOI in its README, the pattern to copy [lm-eval-harness].
- Software Heritage archives public repositories ("Save Code Now") and gives intrinsic SWHIDs; it can generate BibTeX from `codemeta.json` or `citation.cff` (snippet-level) [software-heritage].
- Hugging Face: link the paper on the card and generate a DOI for the exact revision [hf-model-cards][hf-doi]. Details in `model-release.md` and `data-release.md`.

## Where the DOI goes

README first paragraph, `CITATION.cff` (`doi`), `REPRODUCE.md` paper-version table, and the paper's reproducibility statement (design). The DOI arrives after the release; copy it back in a patch release (`releases.md`).

## House rules (design)

- An R2 mirror is fine for users but is not an archival repository; the badge needs Zenodo or an equivalent with a stated permanence plan [acm-badging].
