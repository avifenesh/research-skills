# Reviewer objections and how to pre-empt them

Use when reviewing a draft from the reviewer's side, writing a rebuttal plan, or deciding what to add before submission.

## How systems reviewers read

- Levin and Redell's SOSP committee asks about: original ideas; reality (is it built, how was it used); lessons; choices (which alternatives were considered); context (assumptions and the sensitivity to them); focus; presentation and style [levin-redell].
- Roscoe's review order: summarize the paper, state its contributions, then check novelty against related work, the writing, technical flaws, gaps, and venue fit [roscoe].
- OSDI: an excellent paper motivates a significant problem, proposes an interesting solution, shows practicality and benefits, draws appropriate conclusions, and states its contributions and advance over prior work [osdi27-cfp].

## Pre-emption table

| Objection a reviewer writes | Pre-emption | Source |
|---|---|---|
| "Nothing new; this is system Z with a new name" | Say which of X, Y or Z is new; a table of prior systems and the needs they miss; read what you cite | [zhang][levin-redell] |
| "The contribution is not clear" | Refutable contribution bullets on the first page, each with a section pointer | [peyton-jones][roscoe] |
| "The claims are not supported" | Claim-evidence table; scope the words to the evidence | [neurips-checklist][peyton-jones] |
| "Weak or unfair baselines" | State-of-the-art baselines, same tuning budget, same harness, configs in the appendix or artifact | [heiser][dodge][nanda] |
| "No ablation; what gives the gain?" | One ablation per mechanism, on the headline workload | [zhang][lipton-steinhardt] |
| "No variance; one run" | Number of runs, intervals or per-run values, definition of the bar | [neurips-checklist][hoefler-belli][pineau-checklist] |
| "Cherry-picked benchmarks or settings" | Report all, justify subsets, include the worst case and a regime where you lose | [hoefler-belli][heiser] |
| "Only relative numbers" | Add absolute values, baseline throughput and hardware | [hoefler-belli][heiser] |
| "Overhead claimed wrongly" | Cost per unit of work with CPU or GPU load, not the throughput change | [heiser] |
| "Hardware and software not specified" | Setup paragraph and table with versions and commit hashes | [heiser][neurips-checklist] |
| "Metric definitions unclear" | Define TTFT, ITL, goodput and the window; name the tool | [nvidia-llm-metrics] |
| "Does not generalize" | State the assumptions and the sensitivity to them; add a second setting or narrow the claim | [levin-redell][neurips-checklist] |
| "Is it real?" | Say at the start what is implemented and used; describe the usage | [levin-redell] |
| "Design choices are unmotivated" | Alternatives considered and why they lost, including the ones that failed | [levin-redell][zhang] |
| "Limitations hidden" | A limitations section; reviewers are told not to penalize honesty | [neurips-checklist] |
| "Padded or unfinished" | Right length (OSDI: 6 pages or less is risky, padding is down-ranked); no "to be added" sections | [osdi26-cfp][levin-redell] |
| "Hard to read" | Define terms, fewer forward references, one point per paragraph, one figure that carries the idea | [levin-redell][gopen-swan][nanda] |
| "Reproducibility" | Statement, artifact, commands, hardware, runs, DOI | [neurips-checklist][pineau-checklist][osdi26-ae] |
| "Looks LLM-written" | Own every sentence; concrete numbers and named systems; no filler | [mlsys27-cfp][osdi27-cfp][arxiv-moderation] |
| "Wrong venue" | Match the call: OSDI wants insights for a substantial part of attendees; the MLSys industrial track wants lessons from scale | [roscoe][osdi27-cfp][mlsys27-cfp] |

## Review procedure from this table (design)

For each row, find the sentence, figure or section that pre-empts the objection. Report the row as a finding when none exists: quote the claim it hits, give `file:line`, and name the fix from the second column.
