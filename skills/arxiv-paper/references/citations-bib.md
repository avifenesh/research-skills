# Citations and bibliography

Use when adding or cleaning references, citing arXiv papers, software or models, writing BibTeX, or making your own release citable.

## Rules

- Cite what you read, and compare precisely: "have you actually read the cited material", with comparisons "clear and explicit". Look at your oldest and newest reference, and at citations that exist only as unpublished work: they show blind spots [levin-redell].
- List all authors. MLSys requires every reference to list all authors [mlsys27-cfp].
- Cite the published version when one exists, and optionally add the arXiv ID (design).
- Cite software and models as assets: creators, version, URL and license name for every asset used [neurips-checklist].

## arXiv identifiers and DOIs

- Form: `arXiv:YYMM.NNNNNvN [category]`. With the version number readers see exactly that version; without it they see the latest [arxiv-refs].
- arXiv encourages arXiv identifiers in reference lists for published and unpublished papers. Keep the identifier as one string, with no braces, tildes or font commands, so it can be harvested [arxiv-tex][arxiv-refs].
- One DOI covers all versions of an arXiv paper: `10.48550/arXiv.<id>`. Replacing does not mint a new DOI [arxiv-doi].

## BibTeX hygiene

- Protect capitals and acronyms with braces so the style does not lowercase them: `{PagedAttention}`, `{GPU}`. Do not double-brace whole titles [wilke-bibtex].
- Separate authors only with `and` [wilke-bibtex].
- Consistent journal and venue names; delete unused fields; systematic keys [wilke-bibtex].
- Google Scholar exports often use "and others", export a published paper as an arXiv preprint, lowercase acronyms, and drop pages and volume. Fix them from the proceedings page or DBLP [bibfixer][mlsys27-cfp].

### arXiv entry (check against the abs page's Export BibTeX)

```bibtex
@misc{kwon2023efficient,
  title         = {Efficient Memory Management for Large Language Model Serving with {PagedAttention}},
  author        = {Woosuk Kwon and Zhuohan Li and Siyuan Zhuang and Ying Sheng and Lianmin Zheng
                   and Cody Hao Yu and Joseph E. Gonzalez and Hao Zhang and Ion Stoica},
  year          = {2023},
  eprint        = {2309.06180},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG}
}
```

Authors and the cs.LG primary come from the arXiv listing [arxiv-vllm]; the field layout is arXiv's export convention. The listing's comments field says SOSP 2023, so prefer the SOSP 2023 entry for the published paper and keep all authors [mlsys27-cfp][bibfixer].

## Software and your own release

- Software Citation Principles: importance, credit and attribution, unique identification, persistence, accessibility, specificity. A software citation carries author, title, version, date and a DOI or URL [software-citation].
- Put `CITATION.cff` at the repository root. Required keys: `cff-version`, `message`, `authors`, `title`, `date-released`. GitHub then shows "Cite this repository" with APA and BibTeX; `preferred-citation` points it at your paper [github-cff].
- Zenodo reads `CITATION.cff` for GitHub releases [zenodo-software] (snippet only).

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
- family-names: "Smith"
  given-names: "Jane"
title: "My Software"
date-released: 2024-01-15
```

Add `preferred-citation` with `type: article` to point to the paper [github-cff].

## In the text (design)

- `text~\cite{key}`: the tilde keeps the citation on the line of the word before it. `paper_lint.py` flags a space or a line break before `\cite` and `\citep` (rule `cite-tilde`). `\citet` and `\textcite` take a normal space.
- `et al.` always has its period; `et~al.~\cite{key}` before a citation (rule `et-al`).
- A citation is not a noun: "[12] shows" reads badly; write "Kwon et~al.~\cite{vllm} show".

## Pitfalls

| Pitfall | Why it happens | Fix |
|---|---|---|
| "et al." in the reference list, or the arXiv version of a published paper | Copied from Google Scholar | Proceedings page or DBLP; all authors [mlsys27-cfp][bibfixer] |
| "gpu" and "pagedattention" in titles | Style lowercases unprotected capitals | Brace them [wilke-bibtex] |
| arXiv ID wrapped in `\texttt{}` or split with `~` | Formatting habit | One plain string [arxiv-refs] |
