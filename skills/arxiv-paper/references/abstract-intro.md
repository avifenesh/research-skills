# Abstract, first page and contributions

Use when writing or checking the title, the abstract, the introduction or the contributions list. Reviewers decide from the abstract and the first page.

## What page one must deliver

After page one a reviewer knows:

1. The problem and who has it.
2. Why existing approaches fail.
3. The one idea.
4. What is new and what is not. The reviewer asks "is the work significantly different from existing related work" [levin-redell].
5. The claims, with headline numbers and the setup behind them.
6. Where the evidence is (section, figure, table pointers).

## Abstract

- Four sentences: the problem, why it is interesting, what the solution achieves, what follows [peyton-jones].
- Write it early; it is your outline and the PC's filter. Avoid passive; include assumptions and results [levin-redell].
- No term that only the body defines [zhang]. Define acronyms in the abstract and again in the body (design).
- Context, content, conclusion [mensh-kording].
- arXiv's abstract field takes at most 1920 characters and must not start with the word "Abstract" [arxiv-metadata]. `paper_lint.py` checks the length.

### Numbers in the abstract (design, from [hoefler-belli][heiser][zhang])

- Next to every headline number: the baseline, the hardware class, the workload and the metric.
- Give the absolute value, or the base of the ratio.
- Use "up to" only with the condition under which the maximum holds.
- Claim no generality the evaluated hardware, models and workloads do not support. NeurIPS item 1: claims match the results "in terms of how much the results can be expected to generalize" [neurips-checklist].

## Title

- One central contribution, memorable [mensh-kording].
- arXiv metadata title: no ALL CAPS, no Unicode, expand macros [arxiv-metadata].
- For OSDI, the submitted system name must differ from any public name (an arXiv version, a repo) [osdi27-cfp].

## Introduction

- Widom's five questions: what is the problem, why is it interesting, why is it hard, why is it unsolved, what are the key components of the approach. End with a bulleted list of contributions [widom].
- Zhang's thesis: "X is better for application Y in environment Z". Say which of X, Y or Z is new. Extract broader lessons [zhang].
- Introduce the problem with a concrete example early: "molehills, not mountains" [peyton-jones].
- One "ping": one clear, sharp idea. You may not know it when you start; you must know it when you finish [peyton-jones]. Build the paper around 1 to 3 specific claims and answer what, why, so what [nanda].
- Say when a goal is aspirational. Aspirational goals are fine as motivation if the paper is clear it does not reach them [neurips-checklist].

## Contributions list

Write it first; it drives the paper. Each contribution is refutable, and each gets a forward pointer to its evidence (analysis, theorem, measurement, case study). Do not leave the reader to guess the contributions [peyton-jones].

| Not refutable | Refutable |
|---|---|
| We describe the WizWoz system. It is really cool. | We give the syntax and semantics of a language that supports concurrent processes (Section 3). Its innovative features are... |
| We study its properties. | We prove that the type system is sound and that type checking is decidable (Section 4). |
| We have used WizWoz in practice. | We have built a GUI toolkit in WizWoz and used it to implement a text editor (Section 5). The result is half the length of the Java version. |

Examples from [peyton-jones].

### Template (design; compiled with pdflatex, TeX Live 2025, 2026-10-08)

```latex
\noindent We make three claims.
\begin{itemize}
  \item \textbf{Design.} We show that <mechanism> removes <named bottleneck> for <workload Y> on <setting Z>
        (Section~\ref{sec:design}).
  \item \textbf{System.} We implement it in <N> lines on top of <framework, version> and release it at <archive DOI>
        (Section~\ref{sec:impl}).
  \item \textbf{Evidence.} On <hardware> with <models>, it improves <metric, defined in Section~X> by <a--b>$\times$
        over <baseline A> and <baseline B> at equal <quality or SLO>, over <R> runs
        (Figures~\ref{fig:main}--\ref{fig:slo}); the ablation in Table~\ref{tab:ablation} attributes <share> to <mechanism>.
\end{itemize}
```

Replace every `<...>` before building; pdflatex prints `<` as an inverted exclamation mark in the default font encoding.

## Pitfalls

| Pitfall | Why it happens | Fix |
|---|---|---|
| Abstract says "2x faster" but the figure shows one workload | The abstract is written from the best case | Claim-evidence table; the condition next to every number [neurips-checklist][peyton-jones] |
| "Nothing new; this is Z with a new name" | Novelty is asserted, not located | Say which of X, Y, Z is new; a table of prior systems [zhang][levin-redell] |
| Effort presented as contribution | Two years of work feels like a result | State the refutable claim; small idea, short paper [levin-redell] |
