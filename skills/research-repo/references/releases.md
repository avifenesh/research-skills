# Releases, tags and the changelog

Use when cutting the release that goes with a paper version, tagging, writing the changelog, or fixing a released version.

## Rules

- A released version does not change: "the contents of that version MUST NOT be modified". Pre-releases use `-alpha.1` style suffixes [semver].
- GitHub releases are made from tags and carry assets. With immutable releases you "cannot add, replace, or delete assets after a release is published": create a draft, attach assets, then publish [github-releases].
- SOSP, USENIX and ACM want a specific version (commit or release) archived; USENIX notes that versioning lets readers reach the paper's version [sosp23-badges][sec26-ae][acm-badging].
- Keep a Changelog: newest first, an `Unreleased` section, categories Added, Changed, Deprecated, Removed, Fixed, Security; ISO 8601 dates; linkable versions [keep-changelog].
- Zenodo mints a new DOI per GitHub release; DOIs come from tags, not branches [zenodo-github][github-zenodo].

## Tags tied to paper versions (design; no primary source for the convention)

| Paper version | Git tag | Archive | Model or data revision |
|---|---|---|---|
| arXiv v1 | `v1.0.0` | Zenodo DOI 10.5281/zenodo.<id> | HF revision <40-char sha> |
| arXiv v2 (a number changed) | `v1.1.0` or `v2.0.0` | New Zenodo version | New HF revision and DOI |

Put this table in `REPRODUCE.md`. When a paper version changes a number, cut a new tag and write the change in CHANGELOG under the paper version. arXiv assigns one DOI for all versions of a paper (see the arxiv-paper skill), so the code DOI is what has to carry the version.

The `git-tag` audit rule flags a git repo with no tag at all.

## Release flow (design; standard git and gh syntax, not checked against the fetched docs)

```bash
git tag -a v1.0.0 -m "Code for arXiv v1"
git push origin v1.0.0
gh release create v1.0.0 --draft --notes-file CHANGELOG.md   # attach assets, then publish
# Zenodo archives the release and mints a DOI; copy the DOI into CITATION.cff and the README in the next patch release
```

## Changelog entry (design)

```markdown
## [1.0.0] - 2026-10-08
Code for arXiv:<id>v1. Zenodo DOI 10.5281/zenodo.<id>.
### Added
- Experiments t2_ours_8b, f5_sweep_qps and their reference results.
```

## What not to do

- Edit a published release because of a "small fix". Cut a patch release [semver][github-releases].
- Mint the DOI from a branch. Tag, release, then archive [zenodo-github].
- Keep `.zenodo.json` and `CITATION.cff` with different content. Zenodo ignores the CFF when `.zenodo.json` exists [zenodo-software].

## House rules (design)

- Ship positive results. Delete the code of negative results unless there is a reason to keep it; note the deletion in the changelog.
- Avoid feature flags in a release. Keep one only for a special case or during a transition, and remove the OFF path unless another model or user needs it.
