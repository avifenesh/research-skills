# Paper structure, section by section

Use when outlining a paper, deciding section order, or checking that each section does its job. The first page and contributions have their own file (`abstract-intro.md`); the evaluation's evidence rules are in `claims-evidence.md`.

## Before you write

- The system or method is built, measured and can be run again. A paper is not where you find out whether the idea works. "Has it actually been implemented" is a first reviewer question [levin-redell].
- The target venue's call for papers is open next to the draft. Page limits, anonymity and artifact rules differ by venue and by year [mlsys27-cfp][osdi27-cfp][neurips-checklist]. See `venues.md`.
- Every number in the paper can be regenerated from raw logs by a script. Automate all data processing [ernst].

## Spend words where readers are

Peyton Jones' conference-paper budget [peyton-jones]:

| Part | Length | Readers |
|---|---|---|
| Title | | 1000 |
| Abstract | 4 sentences | 100 |
| Introduction | 1 page | 100 |
| The problem | 1 page | 10 |
| The idea | 2 pages | 10 |
| The details | 5 pages | 3 |
| Related work | 1 to 2 pages | 10 |
| Conclusions | 0.5 page | |

Invest most in title, abstract and figures because they reach the most readers [mensh-kording]. Nanda advises comparable time on abstract, introduction, figures and body [nanda].

## Section table

| Section | What it must do | Concrete rules |
|---|---|---|
| Title | One central contribution, memorable | Rule 1 of [mensh-kording]. arXiv metadata: no ALL CAPS, no Unicode, expand macros [arxiv-metadata] |
| Abstract | Stand alone: problem, why it matters, what the solution achieves, what follows | Four sentences [peyton-jones]. Write it early so it focuses the paper; avoid passive; include assumptions and results [levin-redell]. No jargon that exists only in the body [zhang]. Context, content, conclusion [mensh-kording]. arXiv field limit 1920 characters [arxiv-metadata] |
| Introduction | Problem, then contributions, in about a page | "Describe the problem, state contributions, and that is all" [peyton-jones]. Answer: what is the problem, why is it interesting, why is it hard, why is it unsolved, what are the key parts of the approach; end with a bulleted list of contributions [widom]. State a thesis "X is better for application Y in environment Z", say which of X, Y or Z is new, and extract broader lessons [zhang] |
| Background and motivation | Define Y and Z so the design is understandable; no excess baggage | Restate context in the design section with a figure of where X fits [zhang]. Include just enough prior material, minimize forward references, define terms before use [levin-redell] |
| Design | The idea, the alternatives, the limits | A table of new APIs and a table of new terms; justify trade-offs against alternatives; state what X does not handle [zhang]. Say which alternatives were considered and why they lost [levin-redell]. Examples before generalities [peyton-jones] |
| Implementation | Prove it is real and say what is prototype | Say at the outset that the system is built; say whether the prototype matches the design and which parts were built to test the hypothesis [levin-redell][zhang] |
| Evaluation | Support each claim with a fair setup | Every experiment serves a stated hypothesis; state the conclusion at the start of the section and summarize at the end; captions say what to read from each graph; include a breakdown that isolates each design decision [zhang]. Measure running time, parameter sensitivity and scalability against naive and previous approaches [widom]. Full rules: `claims-evidence.md` |
| Related work | Compare, do not list | Place it late [peyton-jones][ernst]; early only if brief or defensive, late if it needs technical context [widom]. A table of previous systems against the needs of Y in Z [zhang]. Be specific ("uses magnetic media rather than paper tape") and read what you cite [levin-redell] |
| Limitations | Scope of the claims, assumptions, failure cases | NeurIPS checklist item 2: strong assumptions, robustness to their violation, scope (few datasets or runs), factors that influence performance; reviewers are told not to penalize honesty [neurips-checklist]. Scope limitations explicitly [zhang] |
| Conclusion | Short; not the abstract again | Three sentences: hypothesis, solution, results [zhang]. Do not repeat the abstract [widom]. Restate the assumptions with the conclusions [levin-redell] |

## Length

- OSDI '26: papers of 6 pages or less are unlikely to get full consideration, and padding is down-ranked [osdi26-cfp].
- No "to be added" sections, no placeholders [levin-redell]. `paper_lint.py` flags `\todo`, TODO, FIXME, TBD and XXX.
- Effort is not novelty: two years of work is not a contribution, and a small innovation is a short paper [levin-redell]. Experience and lessons papers have their own tracks (OSDI Operational Systems, MLSys industrial track) [osdi27-cfp][mlsys27-cfp].

## Writing order (design)

1. Contributions list, each bullet refutable, each with a section pointer [peyton-jones].
2. Abstract [levin-redell][zhang].
3. Claim-evidence table (`claims-evidence.md`). Run the missing experiments now, or shrink the claim.
4. Figures and their captions, strongest results first [rougier][nanda].
5. Evaluation, then design, then introduction, then the rest.
6. Test the outline on a colleague before the full draft [mensh-kording][peyton-jones]. Ask for sequential reviews, not parallel ones [ernst].
