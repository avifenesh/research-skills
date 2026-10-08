# arxiv-paper-skill

An AI agent skill for writing, checking and submitting ML systems papers: serving, training, compilers, kernels, schedulers and benchmarks, posted to arXiv or sent to MLSys, OSDI, SOSP, NeurIPS or ICLR. It ships a LaTeX style checker, `paper_lint.py`.

The file format is the [AgentSkills](https://agentskills.io) open standard. One skill works in Claude Code, Codex, Cursor and the other agents that read it.

## What it gives the agent

`skills/arxiv-paper/SKILL.md` is a router: a few rules for every task, then tables that map a task to one reference file. The agent reads the file that matches the task and leaves the rest out of context.

| File | Contents |
|------|----------|
| `structure.md` | Word budget, what each section must do, length, writing order |
| `abstract-intro.md` | Page one, abstract, title, introduction, refutable contributions, a contributions template |
| `claims-evidence.md` | Claim-evidence table, baselines, ablations, repeats and intervals, means and overheads, TTFT and ITL definitions, setup paragraph, threats to validity |
| `figures-tables.md` | Captions, axes, color, precision, booktabs, label and ref mechanics |
| `reproducibility-artifacts.md` | NeurIPS and Pineau checklists, ACM badges, MLSys and OSDI artifact evaluation, release, statement template |
| `citations-bib.md` | arXiv IDs and DOIs, BibTeX hygiene, all authors, software citation, `CITATION.cff` |
| `language-style.md` | Plain English rules, hedges, hype, units, tense, acronyms, terminology, the lint word lists |
| `reviewer-objections.md` | Twenty common objections and how to pre-empt each |
| `venues.md` | MLSys 2027, OSDI '27, NeurIPS 2026, ICLR 2026: dates, limits, criteria, anonymity, LLM policy |
| `arxiv-submission.md` | Endorsement and rate limits as of 2026, moderation, categories, metadata, license, TeX Live, tarball, versions |
| `checklist.md` | 77 one-line pre-submission items with IDs, used by the review procedure |
| `sources.md` | The 80 sources with short keys, how each was read, and known gaps |

Every rule cites a source key. Facts that change (deadlines, arXiv policy) carry their "as of" date. Judgement is tagged (design) so it is not mistaken for a sourced rule.

## Install

### Claude Code

Copy or symlink the skill directory into your skills folder:

```bash
git clone <this repo> ~/src/arxiv-paper-skill
ln -s ~/src/arxiv-paper-skill/skills/arxiv-paper ~/.claude/skills/arxiv-paper     # all projects
# or, for one project:
mkdir -p .claude/skills && cp -r ~/src/arxiv-paper-skill/skills/arxiv-paper .claude/skills/
```

### Other AgentSkills agents

Copy `skills/arxiv-paper/` into the agent's skills directory (for example `.codex/skills/`, `.cursor/skills/`), or use the `skills` CLI: `npx skills add <owner>/arxiv-paper-skill`.

## paper_lint.py

```bash
python3 scripts/paper_lint.py paper/main.tex                # from the repo root
python3 skills/arxiv-paper/scripts/paper_lint.py main.tex   # the copy that ships with the skill
python3 scripts/paper_lint.py --list-rules
```

Python 3.8 or newer, no dependencies. Prints `path:line: rule: message` and a count per rule. Follows `\input` and `\include`. Always exits 0, so it never blocks a build. Options: `--max-words N` (default 35), `--allow GLM,MLA` for names that need no definition, `--disable rule,rule`. A comment in the source works too: `% paper-lint: allow GLM MLA`.

It skips comments, `verbatim`, `lstlisting`, `minted` and similar environments, `\iffalse` blocks, math, and the preamble except `\title`.

### What it checks

| Rule | Flags |
|------|-------|
| `em-dash` | Unicode em dash or `---` |
| `en-dash` | Spaced `--`, `-` or en dash used as a prose dash; ranges like `1--4` pass |
| `hedge`, `filler`, `hype`, `plain-words` | Words from the lists in `language-style.md` |
| `unsupported` | "we believe", "novel", "significant(ly)" with no named test in the sentence |
| `contraction` | don't, it's, we're and the like, outside quotes |
| `acronym` | An all-caps token used before its `(ACRONYM)` definition; the abstract and body are separate scopes |
| `unit-space` | `16GiB` or `16 GiB`; write `16\,GiB` or `16~GiB` |
| `unit-consistency` | GB and GiB mixed, `sec` next to `s`, and nonstandard symbols (`sec`, `msec`, `hrs`) |
| `todo` | `\todo`, TODO, FIXME, TBD, XXX |
| `sentence-length` | Sentences over the word limit |
| `et-al` | `et al` without a period, `et. al.` |
| `cite-tilde`, `ref-tilde` | A space or line break before `\cite` or `\ref` |
| `float-label`, `float-unref`, `float-caption` | Missing `\label`, label before caption, label never referenced, missing caption, table caption below or figure caption above |
| `table-rules` | `\|` in a column spec, more than three `\hline` in a tabular |
| `abstract-length` | Abstract over arXiv's 1920-character limit |
| `arxiv-source` | `\today`, line numbers, double spacing, review or anonymous class options |

### What it does not check

Whether claims match evidence, baselines are fair, variance is reported, captions say what to read, or a sentence is clear. Passive voice, terminology drift and tense need a reader. The skill's review procedure in `SKILL.md` covers those with the checklist. The acronym rule is a heuristic: tokens with digits (A100, FP8) and unit symbols are skipped, and product names may need `--allow`.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

One fixture per rule with the exact lines it must flag, a clean fixture that must produce no findings, CLI checks, and checks that the lint word lists match `language-style.md`, that every cited key exists in `sources.md`, and that no file contains an em dash.

## Credits

The content is distilled from a cited learning guide on arXiv paper writing for ML systems research (2026-10-08). The classic guides behind it are listed with links in `skills/arxiv-paper/references/sources.md`: Peyton Jones, Widom, Ernst, Levin and Redell, Zhang, Roscoe, Heiser, Hoefler and Belli, Gopen and Swan, Orwell, Strunk, Zinsser, Rougier et al., Wilke, the NeurIPS paper checklist, Pineau's reproducibility checklist, NIST, and the arXiv help pages. The skill quotes short passages and paraphrases the rest; the original works belong to their authors.

## License

Apache-2.0. See [LICENSE](LICENSE). To cite the skill, see [CITATION.cff](CITATION.cff).
