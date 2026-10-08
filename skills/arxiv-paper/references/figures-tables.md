# Figures and tables

Use when making or checking a figure, a caption, a table, colors, number precision, or the LaTeX label and reference mechanics. arXiv file formats and image size limits are in `arxiv-submission.md`.

## Captions

- Captions are not optional. They explain how to read the figure and give numeric precision the picture cannot [rougier].
- Figures are self-contained. The caption says why the figure matters, not only what it shows [ernst]. Captions on graphs state what to read from them [zhang].
- Start the caption with a title that makes an assertion. Figure captions go below the figure [wilke-captions]; table captions go above the table [wilke-captions][booktabs].
- Every axis and every legend has a title. Numeric variables carry units: "body mass (grams)" [wilke-captions].
- Name the bar: SD, SEM or CI, how computed, over how many runs [neurips-checklist]. See `claims-evidence.md`.

## Plots

- Decide each figure's message before plotting (Rougier rule 2). Put the strongest results in the figures readers look at first [rougier][nanda].
- Do not trust plotting defaults. Use full axis ranges and honest plot types. Remove chartjunk. Message over beauty [rougier].
- Show the distribution when you have one. Hoefler's Figure 1 plots 50 runs of one benchmark with min, median, mean, 95% quantile, max and the 99% CI of the median; the slowest run was 20% off the best [hoefler-belli].
- The same box or arrow style only for the same concept [ernst].

## Color

- Qualitative scales work best with 3 to 5 categories and should not exceed about 8 [wilke-color].
- No rainbow scale [wilke-color].
- About 8% of males and 0.5% of females have color-vision deficiency. Avoid red-green-only distinctions, use the Okabe-Ito palette, and label series directly when there are many [wilke-color].

## Precision

- Report only the digits you can justify. Same decimals within a column. Keep relative and absolute values apart [ernst][wilke-captions].
- Do not print fractions of a percent on a measurement with 5% run-to-run noise (design).

## Tables

- No vertical rules. No horizontal rules between data rows. Left-align text columns, right-align number columns with consistent decimals. Header alignment matches the data. Caption above the table [wilke-captions].
- booktabs gives three rule weights (`\toprule`, `\midrule`, `\bottomrule`) and advises against vertical rules and grids [booktabs].

### Template (compiled with pdflatex, TeX Live 2025, 2026-10-08)

```latex
\begin{table}[t]
  \caption{Time to first token (ms, median of $R$ runs; range in parentheses) on <hardware>, <workload>.}
  \label{tab:ttft}
  \centering
  \begin{tabular}{lrr}
    \toprule
    System & p50 (ms) & p99 (ms) \\
    \midrule
    Baseline A & 112 (108--119) & 840 (790--905) \\
    Ours       &  61 (59--64)   & 310 (295--338) \\
    \bottomrule
  \end{tabular}
\end{table}
```

Caption above, numbers right-aligned with the same decimals, units in the header, no vertical rules [wilke-captions][booktabs]. The numbers are layout placeholders, not results.

## LaTeX mechanics (design)

- `\label` goes after `\caption` (or inside it). Before the caption, `\ref` prints the section number instead of the figure number.
- Every figure and table is referenced in the text. A float nobody points to is either unneeded or unexplained.
- `Figure~\ref{fig:x}`, `Table~\ref{tab:x}`, `Section~\ref{sec:x}`: the `~` keeps the number on the same line as its noun. `\cref` and `\autoref` insert the noun themselves.
- Vector formats for plots (PDF); PNG or JPEG for raster [arxiv-tex]. Check fonts are embedded and text is readable at print size.

## What paper_lint.py checks here

`float-label` (no `\label`, or `\label` before `\caption`), `float-unref` (label never referenced), `float-caption` (no caption, table caption below the tabular, figure caption above the graphic), `table-rules` (`|` in the column spec, more than three `\hline` in one tabular), `ref-tilde` (space or line break before `\ref`). It does not see inside images, so axis titles, units, colors and precision stay a manual check.
