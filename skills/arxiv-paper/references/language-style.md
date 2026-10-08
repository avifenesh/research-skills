# Language and style

Use when editing prose: plain words, sentence and paragraph shape, voice, hedging and hype, numbers and units, tense, acronyms, terminology, and LLM-assisted drafting. The word lists at the end are what `paper_lint.py` checks.

## Rules

| Topic | Rule | Source |
|---|---|---|
| Plain words | Never use a long word where a short one will do. Cut every word you can. Prefer everyday English to jargon. Strip every sentence to its cleanest components | [orwell] rules ii, iii, v; [zinsser]; [strunk] "omit needless words" |
| Everyday speech | "show" not "demonstrate", "let" not "permit", "buy" not "purchase" | [economist] |
| Sentences | Simple sentences help; length alone is not the test. A sentence is too long when it has more candidates for emphasis than it has stress positions | [economist]; [gopen-swan] |
| Word order | Old, linking information at the start of the sentence (topic position); the new point at the end (stress position). Keep subject and verb close | [gopen-swan]; [strunk] "keep related words together", "place the emphatic words at the end" |
| Active voice | Never use the passive where you can use the active. The passive is right when the paragraph's story is about the thing acted on | [orwell] iv; [strunk]; [ernst]; [levin-redell]; [gopen-swan] |
| Paragraphs | One topic per paragraph, topic sentence first | [strunk] 8, 9; [economist] |
| Filler | Avoid "clearly", "obviously", "trivially"; avoid "for various reasons" and "etc." unless the rest is obvious; no bare "this", "that" or "it" without a noun | [ernst]; [widom] |
| Hype | Neutral professional tone; do not boast; no loaded terms or repurposed technical terms. arXiv moderators can decline work for tone | [arxiv-moderation]; [economist]; [lipton-steinhardt] |
| Terminology | One term per concept, no "elegant variation". Define variables once, before use. Name your approach descriptively, not "our method" or "Approach 1" | [ernst]; [widom]; [levin-redell] |
| Acronyms | Define at first use in the abstract and again in the body. Keep the list short | (design), consistent with "define terms before use" [levin-redell] |
| Numbers and units | A space between number and unit symbol (25 kg). Do not pluralize symbols. No ppm-style shorthand. Do not mix symbols and names. Make a range's unit clear | [nist-si] |
| Binary and decimal | MiB, GiB are powers of 2; MB, GB are powers of 10. Say which. flop (count) differs from flop/s (rate); B (byte) differs from b (bit) | [nist-binary]; [hoefler-belli] |
| Percentages | "percent" and "percentage points" are different; give the denominator | [heiser] |
| Tense | Past tense for what you did in the experiments; present for the paper and for general facts | [ernst] (extracted, check the page) |
| Serial comma, singular they | Ernst's choices. Pick a style and keep it | [ernst] |
| Clear thinking | "Clear thinking becomes clear writing." Ask: what am I trying to say, what words express it, could I say it shorter | [zinsser]; [economist] |
| Revision | Cut sections for relevance, paragraphs for one point, sentences for clarity, words for need | [ernst] |
| LLM drafting | Report significant AI use per subject norms. You are responsible for every sentence and every reference. AI cannot be an author. Wholly or largely generated text is prohibited at MLSys and OSDI | [arxiv-moderation]; [mlsys27-cfp]; [osdi27-cfp] |

## House style of this skill (design)

- No em dashes. An em dash usually joins two sentences: split them, or use a colon or a comma.
- Short sentences, the fact first, no hedging. A claim either holds under a stated condition or it is not a claim.
- Sentences over 35 words get split. The limit is a default (`--max-words`), not a sourced number.
- No contractions in the paper.
- "We believe" either gets evidence or goes. "Novel" is for reviewers to say; say what is new and against which prior work. "Significant" needs a named test and its p-value, or the number instead.

## Numbers and units in LaTeX (design, after [nist-si])

- `16\,GiB` or `16~GiB`: a thin or non-breaking space. `16GiB` has no space; `16 GiB` can break across lines.
- Pick decimal or binary prefixes for each quantity and keep them. If memory is in GiB and disk in GB, say so once.
- `s`, `ms`, `min`, `h`: not `sec`, `msec`, `mins`, `hrs`.
- `siunitx` (`\qty{16}{\gibi\byte}`) enforces both rules if the venue style allows it.

## Word lists

`paper_lint.py` keeps the same lists; `tests/test_paper_lint.py` fails if they drift. Lists are comma-separated; plain words are semicolon-separated `word -> replacement` pairs. Matching is case-insensitive and whole-word. Plain-word entries that are single words also match their -s, -d or -ed and -ing forms. "rather" does not match "rather than". Quoted text is not checked, so quoted paper titles do not trigger.

- Hedges: arguably, perhaps, possibly, presumably, conceivably, seemingly, somewhat, fairly, quite, rather, to some extent, to a certain extent, in some sense, more or less, it seems, seems to, appears to, could potentially, may potentially, might potentially, it is possible that, we hope
- Filler: clearly, obviously, trivially, it is easy to see, it is clear that, for various reasons, etc., very, really, basically, actually, it should be noted that, it is worth noting that, it is important to note that
- Hype: groundbreaking, revolutionary, unprecedented, game-changing, game changer, paradigm shift, breakthrough, cutting-edge, best-in-class, world-class, first-ever, unparalleled, unmatched, remarkable, remarkably, dramatic, dramatically, drastically, tremendous, tremendously, massive, massively, incredible, incredibly, amazing, astonishing, stunning, superb, outstanding, impressive, impressively, blazing, lightning-fast, seamless, seamlessly, effortless, effortlessly, magic, magical, powerful, holistic
- Unsupported: we believe, we think, we feel, novel, significant, significantly
- Plain words: utilize -> use; utilise -> use; leverage -> use; demonstrate -> show; facilitate -> help; commence -> start; endeavor -> try; methodology -> method; purchase -> buy; delve -> look; showcase -> show; in order to -> to; a number of -> some, or the number; due to the fact that -> because; in spite of the fact that -> although; at this point in time -> now; prior to -> before; subsequent to -> after; a wide range of -> many, or the range; a plethora of -> many; plays a crucial role -> matters, and say how; pivotal -> key, or say why; in the realm of -> in
- Acronyms that need no definition: GPU, CPU, RAM, DRAM, SRAM, SSD, HDD, USB, API, URL, HTTP, HTTPS, JSON, YAML, CSV, PDF, HTML, XML, SQL, TCP, UDP, IP, DNS, OS, ID, UTC, ET, PDT, PST, EST, US, USA, UK, EU, AI, ML, CUDA, NVIDIA, RTX, AMD, AWS, GCP, IBM, ACM, IEEE, USENIX, OSDI, SOSP, NSDI, ASPLOS, ISCA, MICRO, ICML, ICLR, CVPR, ACL, EMNLP, NAACL, KDD, VLDB, SIGMOD, SIGCOMM, ATC, FP32, FP16, FP8, FP4, BF16, TF32, INT8, INT4, GPT, BERT, MIT, BSD, GPL, CC, BY, SA, NC, ND, DOI, ORCID, ISBN, TODO, FIXME, TBD, XXX

LLM, KV, TTFT, ITL, SLO, LRU and the like are not on the list: define them. Tokens with a digit (A100, H100, FP8) and unit symbols (GB, GiB) are never treated as acronyms. Add paper-specific names with `--allow GLM,MLA` or a comment in the source: `% paper-lint: allow GLM MLA`.

## What paper_lint.py checks here, and what it does not

Checks: `em-dash`, `en-dash`, `hedge`, `filler`, `hype`, `plain-words`, `unsupported`, `contraction`, `acronym`, `unit-space`, `unit-consistency`, `sentence-length`. Run `python3 scripts/paper_lint.py --list-rules`.

Does not check: passive voice, topic and stress position, one point per paragraph, terminology drift (two names for one concept), vague "this", tense, or whether a number has its baseline. Those need a reader.
