# Licensing

Use when choosing or checking the license of the code, the data and the weights, writing NOTICE, crediting copied code, or handling a repo that mixes licenses.

## Choices

| Choice | What the sources say | Use for |
|---|---|---|
| Apache-2.0 | Permissive; preserve copyright and license notices, document changes; "express grant of patent rights"; permits commercial and patent use; limits trademark use; no warranty [cal-apache] | Systems code companies will adopt. Mooncake, SGLang and LMCache state Apache-2.0 in their READMEs [mooncake-readme][sglang-readme][lmcache-readme] |
| MIT | Short and simple; preserve copyright and license notice; the page extract does not mention patents [cal-mit] | Small tools and templates (the Papers with Code templates repo is MIT) [pwc-code] |
| BSD, GPL family, AGPL, MPL, OpenRAIL, CC family, ODC, CDLA | Identifiers and names in the Hub license list; each has different conditions [hf-licenses] | Read the license; choose from the list so Hub filters work |
| No license | "exclusive copyright by default": nobody may legally copy, modify or distribute, even on public GitHub [cal-none] | Never ship research code this way |
| `other` | Custom license name, link and a LICENSE file in the repo [hf-model-cards] | Community licenses (Llama and Gemma have their own Hub identifiers; read their terms) [hf-licenses] |

## Mechanics

- NOTICE: LICENSE and NOTICE "must exactly represent the contents of the distribution". Put in NOTICE only what is legally required. Leave BSD and MIT notices in place and point to them from LICENSE. If a bundled Apache dependency has a NOTICE, bubble the relevant parts up. Do not list non-bundled dependencies [asf-howto].
- Third-party code you copy: keep its header and license, say which files, and credit design debts in the README the way SGLang does [sglang-readme][asf-howto].
- Mixed repos (code, data, model): REUSE gives per-file `SPDX-License-Identifier` and copyright headers, a `LICENSES/<SPDX-ID>.txt` directory, `.license` companions or `REUSE.toml` for binary and data files, with aggregate or override precedence [reuse]. Azure's dataset repo carries two licenses (CC-BY-4.0, MIT) in one repo [azure-traces].
- Weights: the license of the base model governs derivatives. State it in `license` and `base_model` and read the base license for naming or attribution duties (not verified here for Llama or Gemma) [hf-model-cards][hf-licenses].
- Data: carry upstream licenses forward and give the derived data its own license compatible with them. CC BY-SA 4.0 adaptations may be relicensed to GPLv3 (one way only); BY-NC-SA has no non-CC compatible license [cc-compat][data-provenance]. Details in `data-release.md`.
- NeurIPS item 12 expects license name, version and URL for every asset used [neurips-checklist].

## What the audit checks

`repo_audit.py` reports whether a `LICENSE` (or `LICENSE.md`, `LICENSE.txt`, `COPYING`) exists at the root and which SPDX identifier its text matches (Apache-2.0, MIT, BSD-2-Clause, BSD-3-Clause, GPL-2.0, GPL-3.0, LGPL, AGPL-3.0, MPL-2.0, CC-BY-4.0, CC-BY-SA-4.0, CC0-1.0, Unlicense). It also flags directories of data files with no LICENSE, README, card or manifest beside them. It cannot judge compatibility; `checklist.md` items LC1 to LC6 cover that.
