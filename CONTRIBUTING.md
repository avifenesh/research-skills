# Contributing

Issues and pull requests are welcome.

## Content fixes

- A wrong or stale fact (a venue date, an arXiv rule, a page limit): open an issue or PR with the source URL and the date you read it. Update the "as of" date with the fact.
- A new rule: cite a source and add it to `skills/arxiv-paper/references/sources.md` with its title, URL and how you read it (page, PDF, snippet). Judgement without a source is welcome too; tag it (design).
- Keep the house style: no em dashes, short sentences, the fact first.

## Lint changes

- A false positive: add the sentence to `tests/fixtures/clean/main.tex`, then fix the rule until the clean fixture has zero findings again.
- A missed case: add it to the rule's fixture with its expected line in `tests/test_paper_lint.py`, then fix the rule.
- Run `python3 -m unittest discover -s tests` before you push.

## Sign-off

Sign your commits (`git commit -s`) to certify the [Developer Certificate of Origin](https://developercertificate.org/). Contributions are under the Apache-2.0 license of this repo.
