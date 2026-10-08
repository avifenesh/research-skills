# arXiv submission

Use when posting to arXiv: endorsement, rate limits, what moderators accept, categories, metadata and the comments field, license, the LaTeX build and tarball, announcement timing, replacements and withdrawal. Facts are as of 2026-10-08; arXiv changed several rules in 2025 and 2026, so re-check the cited page before you rely on a date or limit.

## Dated rules (as of 2026-10-08)

| Rule | Fact | Source |
|---|---|---|
| Endorsement | Since 2026-01-21 an institutional email alone no longer endorses a new submitter. Path 1 needs an institutional email and a previously accepted arXiv paper you have claimed in the target endorsement domain. Path 2 is personal endorsement by an established author in that domain. Staff cannot endorse or waive it | [arxiv-endorse][arxiv-endorse-2026] |
| Rate limit | Since 2026-10-01: at most 2 new submissions per calendar month and 3 active at a time, across all categories. Rejected submissions count; a submission deleted before announcement does not. Submitting for co-authors uses only your quota | [arxiv-rate-2026][arxiv-moderation] |
| Replacements | At most once per week. Versions after v5 are not in the daily mailings. Only journal ref, DOI and report number change without a new version | [arxiv-replace] |
| CS review and position papers | Since 2025-10-31 they must already be accepted at a journal or conference with documented peer review; workshop review is not enough. Research papers are unaffected | [arxiv-cs-review-2025] |
| Language | Since 2026-02-11 every new submission needs a full English version | [arxiv-english-2026] |
| TeX | TeX Live 2025 (state 2025-08-03) is the default; TeX Live 2023 is selectable. XeLaTeX since November 2025. `.bbl` format 3.3 only for TL2025; 3.2 and 3.3 for TL2023 | [arxiv-tex][arxiv-texlive] |
| Announcements | Cutoff 14:00 ET, announced 20:00 ET, Sunday to Thursday evenings. Thursday 14:00 to Friday 14:00 submissions announce Sunday 20:00. QA holds take 1 to 4 days or more | [arxiv-schedule] |
| Abstract | At most 1920 characters. Omit the word "Abstract" | [arxiv-metadata] |
| Images | Warning for images over 34 megapixels since February 2026 | [arxiv-sizes] |
| Organisation | Independent nonprofit since 2026-07-01 | [arxiv-blog] |

## Who can submit

- First-time submitters, and anyone new to a category, need endorsement.
- Path 1 (automatic): an institutional email that meets arXiv's criteria plus a paper you claimed in the same endorsement domain [arxiv-endorse][arxiv-endorse-2026].
- Path 2 (personal): start a submission and take the endorsement-request email. Find endorsers with "Which authors of this paper are endorsers?" on abstract pages. Send them the link, optionally with your ORCID or draft. One positive endorsement per category is enough. Do not mass-email [arxiv-endorse][arxiv-endorse-2026].
- Endorsers must have enough papers in the domain from between three months and five years ago. Endorsement is not peer review and can be revoked [arxiv-endorse].
- Without an institutional email (independent researcher, small company), start Path 2 well before any deadline. Staff cannot endorse you [arxiv-endorse-2026].

## What arXiv accepts

- Research articles with original, substantive results. Not accepted: abstract-only work, course projects, proposals, news, slides and posters, very short work [arxiv-content].
- Moderation is not peer review and gives no feedback. It checks a professional, sufficiently neutral tone and carefully prepared sections, figures, tables and references; scholarly interest (originality, novelty, significance); and declines falsified or plagiarized content and serious misrepresentation. Moderators may reclassify and add or remove cross-lists. Authors with earlier delayed or declined work get closer scrutiny. Appeals are final [arxiv-moderation].
- Format policy: title and authorship (no anonymous submissions), complete references, links to code or data that resolve to a public repository, machine-readable text, single spacing, 10 to 14 pt type, margins of at least 1 inch. No line numbers, obstructing watermarks, highlighted text, margin notes or referee remarks [arxiv-format].
- Generative AI: report significant use consistent with your field's methods; authors are responsible; AI is not an author [arxiv-moderation].
- A paper under double-blind review may be posted at MLSys and NeurIPS; at OSDI, with a different anonymized name for the submitted system [mlsys27-cfp][neurips26-handbook][osdi27-cfp].

## Categories

arXiv's one-line definitions [arxiv-taxonomy], with a judgement column (design):

| Category | arXiv description (shortened) | Use for ML systems when |
|---|---|---|
| cs.LG | Machine learning research, all aspects | The claim is about training, models or algorithms, or ML people are the readers |
| cs.DC | Fault tolerance, distributed algorithms, parallel computation, cluster computing | The claim is about serving, scheduling, parallelism or communication |
| cs.PF | Performance measurement and evaluation, queueing, simulation | The contribution is measurement methodology or performance modelling |
| cs.AR | Systems organization and hardware architecture | Accelerator or hardware design |
| cs.OS, cs.DB, cs.NI, cs.SE | Operating systems; databases and data processing; networking; software engineering | The system sits in that field |
| cs.AI | AI except vision, robotics, ML, multiagent, language | Rarely the right primary for systems work |
| stat.ML | ML papers (supervised, unsupervised, reinforcement learning, bandits) | Rarely needed |

Seen on listings: vLLM/PagedAttention is cs.LG with a cs.DC cross-list [arxiv-vllm], DistServe is cs.DC [arxiv-distserve], FlashAttention is cs.LG [arxiv-flashattention]. Choose the primary by where the claim lives. Add at most one or two cross-lists: "rarely appropriate to add more than one or two" [arxiv-crosslist]. Expect moderators to move a wrong choice [arxiv-moderation]. There is no official arXiv rule for cs.LG versus cs.DC in ML systems.

## Metadata [arxiv-metadata]

- Title: no ALL CAPS, no Unicode, some MathJax, macros expanded.
- Authors: "Firstname Lastname", all authors, no honorifics or degrees; affiliation city and country only.
- Abstract: at most 1920 characters, no word "Abstract", no formatting commands.
- Comments: page and figure counts, venue ("to appear in ..."), URLs followed by a space before any period.
- Report-no: only institution-assigned numbers.
- Journal-ref: only once published; the full reference, no URLs.
- DOI: the publisher DOI, never the arXiv-assigned one.
- ACM-class: optional, in "F.2.2; I.2.7" form.

Comments examples:

```text
14 pages, 9 figures, 4 tables. Code at https://doi.org/10.5281/zenodo.NNNNNNN . To appear in OSDI 2027
14 pages, 9 figures; v2: added H100 results and ablation, claims unchanged
```

The second is for a replacement: say why, and merge the old comments [arxiv-replace].

## License [arxiv-license]

Six choices: CC BY 4.0, CC BY-SA 4.0, CC BY-NC-SA 4.0, CC BY-NC-ND 4.0, CC0, or the arXiv perpetual non-exclusive license 1.0. The choice is irrevocable per version; later versions may carry another license. arXiv encourages a liberal license. Check any venue copyright or license form against your choice before submitting (design).

## LaTeX build

- Processor: pdflatex (the default if unsure), latex (DVI, EPS only), xelatex (since November 2025). TeX Live 2025 default, 2023 selectable. Compilation runs from the submission root, even when the main file is in a subdirectory [arxiv-tex][arxiv-texlive].
- Bibliography: upload the `.bbl` named like the main `.tex`, or the `.bib` files; a present `.bbl` wins. For biblatex the `.bbl` must come from the same backend (Biber or BibTeX) and format (3.3 for TL2025). Do not submit `.aux`, `.log`, `.toc`, `.dvi`, or the `.pdf` of the main file [arxiv-tex].
- Figures: PDF, PNG, JPEG for pdflatex; EPS or PS for latex. No on-the-fly conversion: convert yourself and check the result. No JavaScript in PDFs; animations go in ancillary files. Photos as JPEG, diagrams as PDF or PNG; a warning appears above 34 megapixels [arxiv-tex][arxiv-sizes].
- File names: `a-z A-Z 0-9 _ + - . , =` only; case-sensitive [arxiv-submit]. Relative paths only. Hidden files and directories (for example `.cache/`) are deleted on announcement and break packages that rely on them [arxiv-tex][arxiv-mistakes].
- Packages: arXiv has only what TeX Live has; ship custom `.sty` and `.cls` files. Known TL2025 issues: `cleveref` names, `array` with `revtex`, loading packages inside groups, `hyperref` before `hyperxmp`, minted v3 [arxiv-texlive]. `psfig` is gone. Do not use `\pdfoutput` to switch output; use `ifpdf` [arxiv-tex].
- Shell escape: for minted, run LaTeX once with `-shell-escape`, upload the `_minted` directory, and check with `-no-shell-escape` [arxiv-texlive]. Assume shell escape is off [arxiv-mistakes].
- `hyperref`: arXiv loads it with its own options. Set options with `\hypersetup`, or put `nohypertex` in a `00README` file if your class loads it [overleaf-arxiv]. `\input` is safer than `\include` for files in subdirectories, because only the top directory is writable [arxiv-mistakes].
- No double-spaced "referee" mode. No `\today` in `\date`: PDFs are rebuilt [arxiv-tex].
- You must view the PDF arXiv builds before you can finish. arXiv also converts to HTML with LaTeXML: supported packages, few custom macros and alt text help [arxiv-html].
- arXiv serves the source to anyone who asks. Strip comments and drafts you do not want public (design).

## Tarball checklist (commands run on 2026-10-08 in a test tree)

```bash
# 1. clean build in an empty copy, shell escape off, same TeX Live as the arXiv choice
pdflatex -no-shell-escape main && bibtex main && pdflatex -no-shell-escape main && pdflatex -no-shell-escape main

# 2. things arXiv deletes or rejects
find . -name '.*' -not -name '.' -not -path './.git*'                     # hidden files and dirs
find . -type f \( -iname '*.eps' -o -iname '*.svg' -o -iname '*.gif' \)   # not usable with pdflatex
find . -type f | grep -v -E '^[./a-zA-Z0-9_+,=-]+$'                       # characters outside the allowed set

# 3. bbl name must match the main tex name
test -f main.bbl && echo ok

# 4. pack without build products (keep main.bbl)
tar czf ../arxiv.tar.gz --exclude='*.aux' --exclude='*.log' --exclude='*.out' --exclude='*.blg' \
    --exclude='main.pdf' --exclude='.git' .
```

Rules behind each line: aux, log and pdf excluded and the bbl name [arxiv-tex]; allowed characters [arxiv-submit]; hidden files and no figure conversion [arxiv-mistakes]. After upload, read the PDF arXiv builds. `paper_lint.py` rule `arxiv-source` flags `\today`, line numbers, double spacing and review or anonymous class options; `abstract-length` flags an abstract over 1920 characters.

## Timing, versions and withdrawal

- Edits before 14:00 ET on the same day create no version and do not delay the announcement. Edits after 14:00 ET but before announcement create no version but irrevocably delay it [arxiv-replace].
- A replacement always creates a new version; say why in Comments and merge the old comments. Earlier versions stay public. Journal-ref, DOI and report-no can be added without a new version [arxiv-replace].
- Withdrawal does not remove the paper: it makes a new version marked withdrawn, with a public reason. Do not withdraw to update; replace [arxiv-withdraw].
- Identifiers cannot be reserved or backdated [arxiv-schedule]. QA holds of days are normal: submit well before any date you need.
- Batch fixes into one replacement; the limit is once per week [arxiv-replace].
- Plan the quota around deadlines: 2 per month, 3 active [arxiv-rate-2026].

## Pitfalls

| Pitfall | Why it happens | Fix |
|---|---|---|
| arXiv build fails | `.bbl` mismatch, EPS figures, hidden files, TL2025 package changes | Build with the same TeX Live; read arXiv's log [arxiv-tex][arxiv-texlive][arxiv-mistakes] |
| Wrong category | Chosen by habit | Primary by claim, at most 1 or 2 cross-lists [arxiv-crosslist] |
| Quota spent before a deadline | Side papers posted first | 2 per month, 3 active; plan [arxiv-rate-2026] |
| Hold or decline for tone | Marketing language | Neutral facts [arxiv-moderation] |
| Survey or position paper declined | Assumed arXiv takes it | Publish at a peer-reviewed venue first; add journal ref and DOI [arxiv-cs-review-2025] |
| Paper under review promoted loudly | Excitement | NeurIPS warns this can break double blind [neurips26-handbook] |
| No endorsement at the deadline | Path 2 started late | Ask an endorser well before the deadline [arxiv-endorse-2026] |
