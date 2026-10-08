#!/usr/bin/env python3
"""paper_lint: mechanical style checks for LaTeX papers.

Usage:
    python3 paper_lint.py main.tex [more.tex ...] [--max-words N]
                          [--allow ACR,ACR] [--disable rule,rule] [--list-rules]

Reports findings as path:line: rule: message, then a count per rule.
Follows \\input and \\include. Skips comments, verbatim-like environments,
\\iffalse blocks and math. Exits 0 unless the command line is wrong.

The word lists below mirror references/language-style.md. The test suite
checks that they stay in sync. Dependency-free, Python 3.8 or newer.

In-file directive (a LaTeX comment):
    % paper-lint: allow GLM FP8      acronyms that need no definition here
"""

import argparse
import os
import re
import sys
from collections import Counter, OrderedDict

# --------------------------------------------------------------------------
# Rules: id -> (what it checks, reference file)
# --------------------------------------------------------------------------

RULES = OrderedDict([
    ("em-dash", ("em dash (unicode or ---); rewrite as two sentences, a colon or a comma", "language-style.md")),
    ("en-dash", ("spaced dash in prose (' -- ', ' - ', ' \u2013 '); -- is only for ranges like 1--4", "language-style.md")),
    ("hedge", ("hedge word; state the claim and its condition", "language-style.md")),
    ("filler", ("filler word or phrase; cut it", "language-style.md")),
    ("hype", ("hype word; give the number instead", "language-style.md")),
    ("plain-words", ("long or stock word where a short one works", "language-style.md")),
    ("unsupported", ("'we believe', 'novel', or 'significant(ly)' without a named test", "language-style.md")),
    ("contraction", ("contraction in formal prose", "language-style.md")),
    ("acronym", ("all-caps acronym used before its '(ACRONYM)' definition", "language-style.md")),
    ("unit-space", ("number and unit not joined by \\, or ~ (16GiB, 16 GiB)", "language-style.md")),
    ("unit-consistency", ("mixed unit spellings in one paper (GB and GiB, s and sec) or a nonstandard symbol", "language-style.md")),
    ("todo", ("\\todo, TODO, FIXME, TBD or XXX left in the text", "checklist.md")),
    ("sentence-length", ("sentence longer than the word limit", "language-style.md")),
    ("et-al", ("'et al' without a period, or 'et. al.'", "citations-bib.md")),
    ("cite-tilde", ("space before \\cite; write text~\\cite{key}", "citations-bib.md")),
    ("ref-tilde", ("space before \\ref; write Figure~\\ref{key}", "figures-tables.md")),
    ("float-label", ("figure or table without \\label, or \\label before \\caption", "figures-tables.md")),
    ("float-unref", ("figure or table whose label is never referenced", "figures-tables.md")),
    ("float-caption", ("float without \\caption, table caption below the table, or figure caption above the graphic", "figures-tables.md")),
    ("table-rules", ("vertical rules in a tabular spec, or \\hline between data rows", "figures-tables.md")),
    ("abstract-length", ("abstract longer than arXiv's 1920-character metadata limit", "arxiv-submission.md")),
    ("arxiv-source", ("source arXiv rejects or rebuilds badly: \\today, line numbers, double spacing, review or anonymous mode", "arxiv-submission.md")),
])

# --------------------------------------------------------------------------
# Word lists (mirror references/language-style.md, section "Word lists")
# --------------------------------------------------------------------------

HEDGES = [
    "arguably", "perhaps", "possibly", "presumably", "conceivably", "seemingly",
    "somewhat", "fairly", "quite", "rather", "to some extent", "to a certain extent",
    "in some sense", "more or less", "it seems", "seems to", "appears to",
    "could potentially", "may potentially", "might potentially", "it is possible that",
    "we hope",
]

FILLER = [
    "clearly", "obviously", "trivially", "it is easy to see", "it is clear that",
    "for various reasons", "etc.", "very", "really", "basically", "actually",
    "it should be noted that", "it is worth noting that", "it is important to note that",
]

HYPE = [
    "groundbreaking", "revolutionary", "unprecedented", "game-changing", "game changer",
    "paradigm shift", "breakthrough", "cutting-edge", "best-in-class", "world-class",
    "first-ever", "unparalleled", "unmatched", "remarkable", "remarkably", "dramatic",
    "dramatically", "drastically", "tremendous", "tremendously", "massive", "massively",
    "incredible", "incredibly", "amazing", "astonishing", "stunning", "superb",
    "outstanding", "impressive", "impressively", "blazing", "lightning-fast",
    "seamless", "seamlessly", "effortless", "effortlessly", "magic", "magical",
    "powerful", "holistic",
]

UNSUPPORTED = ["we believe", "we think", "we feel", "novel", "significant", "significantly"]

# word -> replacement. Single words also match -s, -d/-ed and -ing forms.
PLAIN_WORDS = OrderedDict([
    ("utilize", "use"), ("utilise", "use"), ("leverage", "use"), ("demonstrate", "show"),
    ("facilitate", "help"), ("commence", "start"), ("endeavor", "try"),
    ("methodology", "method"), ("purchase", "buy"), ("delve", "look"),
    ("showcase", "show"), ("in order to", "to"), ("a number of", "some, or the number"),
    ("due to the fact that", "because"), ("in spite of the fact that", "although"),
    ("at this point in time", "now"), ("prior to", "before"), ("subsequent to", "after"),
    ("a wide range of", "many, or the range"), ("a plethora of", "many"),
    ("plays a crucial role", "matters, and say how"), ("pivotal", "key, or say why"),
    ("in the realm of", "in"),
])

# Acronyms that need no definition in an ML systems paper (design).
ACRONYM_ALLOW = [
    "GPU", "CPU", "RAM", "DRAM", "SRAM", "SSD", "HDD", "USB", "API", "URL", "HTTP", "HTTPS",
    "JSON", "YAML", "CSV", "PDF", "HTML", "XML", "SQL", "TCP", "UDP", "IP", "DNS", "OS",
    "ID", "UTC", "ET", "PDT", "PST", "EST", "US", "USA", "UK", "EU", "AI", "ML",
    "CUDA", "NVIDIA", "RTX", "AMD", "AWS", "GCP", "IBM", "ACM", "IEEE", "USENIX", "OSDI", "SOSP",
    "NSDI", "ASPLOS", "ISCA", "MICRO", "ICML", "ICLR", "CVPR", "ACL", "EMNLP", "NAACL",
    "KDD", "VLDB", "SIGMOD", "SIGCOMM", "ATC", "FP32", "FP16", "FP8", "FP4", "BF16",
    "TF32", "INT8", "INT4", "GPT", "BERT", "MIT", "BSD", "GPL", "CC", "BY", "SA", "NC",
    "ND", "DOI", "ORCID", "ISBN", "TODO", "FIXME", "TBD", "XXX",
]

# --------------------------------------------------------------------------
# Environments and patterns
# --------------------------------------------------------------------------

VERBATIM_ENVS = {
    "verbatim", "verbatim*", "Verbatim", "Verbatim*", "BVerbatim", "LVerbatim",
    "lstlisting", "minted", "comment", "alltt", "spverbatim", "filecontents",
    "filecontents*", "pycode", "pyverbatim",
}
MATH_ENVS = {
    "equation", "equation*", "align", "align*", "alignat", "alignat*", "gather",
    "gather*", "multline", "multline*", "flalign", "flalign*", "eqnarray",
    "eqnarray*", "displaymath", "math", "dmath", "dmath*",
}
TABULAR_ENVS = {"tabular", "tabular*", "tabularx", "tabulary", "longtable", "longtable*", "supertabular", "tblr"}
FIGURE_ENVS = {"figure", "figure*", "wrapfigure", "sidewaysfigure", "SCfigure"}
TABLE_ENVS = {"table", "table*", "wraptable", "sidewaystable", "SCtable"}
FLOAT_ENVS = FIGURE_ENVS | TABLE_ENVS

ABBREVIATIONS = {
    "e.g.", "i.e.", "al.", "fig.", "figs.", "sec.", "secs.", "eq.", "eqs.", "vs.", "cf.",
    "approx.", "resp.", "tab.", "no.", "ref.", "refs.", "dr.", "mr.", "ms.", "prof.",
    "inc.", "ltd.", "jr.", "st.", "alg.", "app.", "ch.", "vol.", "pp.", "ca.", "viz.",
}

SECTION_RE = re.compile(r"\\(part|chapter|section|subsection|subsubsection|paragraph|subparagraph)\*?\s*[\[{]")
INPUT_RE = re.compile(r"\\(input|include|subfile)\s*\{([^}]+)\}")
REF_COLLECT_RE = re.compile(
    r"\\(ref|eqref|pageref|autoref|cref|Cref|vref|Vref|nameref|subref|labelcref|cpageref|Cpageref|crefrange|Crefrange|autopageref)\*?\{([^}]*)\}")
EVENT_RE = re.compile(
    r"\\(begin|end)\s*\{([^}]+)\}|\\(caption)\b|\\label\s*\{([^}]*)\}|\\(includegraphics|includesvg|includepdf|input|import)\b|\\(hline)\b")

# Units for unit-space (longest first so GiB/s wins over GiB).
UNITS = [
    "GiB/s", "MiB/s", "TiB/s", "GB/s", "MB/s", "TB/s", "Gb/s", "Mb/s", "TFLOP/s",
    "PFLOP/s", "GFLOP/s", "tok/s", "tokens/s", "TFLOPS", "GFLOPS", "PFLOPS", "Gbps",
    "Mbps", "KiB", "MiB", "GiB", "TiB", "PiB", "KB", "kB", "MB", "GB", "TB", "PB",
    "Kb", "Mb", "Gb", "Tb", "kHz", "MHz", "GHz", "Hz", "kW", "MW", "W", "msec", "msecs",
    "ms", "\u00b5s", "\u03bcs", "us", "ns", "secs", "sec", "mins", "min", "hrs", "hr", "s",
]
UNIT_SET = set(UNITS)
UNIT_ALT = "|".join(re.escape(u) for u in UNITS)
# group(1) number, group(2) separator (empty or whitespace), group(3) unit
UNIT_RE = re.compile(r"(?<![\w.,\\/-])(\d[\d,]*(?:\.\d+)?)([ \t]*)(" + UNIT_ALT + r")(?![A-Za-z0-9/])")

# Families for unit-consistency: name -> list of spellings, standard first.
UNIT_FAMILIES = OrderedDict([
    ("byte prefixes (decimal GB vs binary GiB)", [("decimal", ["KB", "kB", "MB", "GB", "TB", "PB"]),
                                                   ("binary", ["KiB", "MiB", "GiB", "TiB", "PiB"])]),
    ("seconds", [("s", ["s"]), ("sec", ["sec", "secs"])]),
    ("milliseconds", [("ms", ["ms"]), ("msec", ["msec", "msecs"])]),
    ("microseconds", [("\u00b5s", ["\u00b5s", "\u03bcs"]), ("us", ["us"])]),
    ("minutes", [("min", ["min"]), ("mins", ["mins"])]),
    ("hours", [("h", ["h"]), ("hr", ["hr", "hrs"])]),
    ("bit rates", [("Gb/s", ["Gb/s", "Mb/s"]), ("Gbps", ["Gbps", "Mbps"])]),
    ("token rates", [("tok/s", ["tok/s"]), ("tokens/s", ["tokens/s"])]),
])
NONSTANDARD_UNITS = {"sec": "s", "secs": "s", "msec": "ms", "msecs": "ms", "mins": "min", "hr": "h", "hrs": "h"}
SEP = r"(?:[ \t]|~|\\,|\\;|\\:|\\ |\\thinspace\s*|\\nobreakspace\s*)*"
FAMILY_TOKEN_RE = re.compile(r"(?<![A-Za-z])(KiB|MiB|GiB|TiB|PiB|KB|kB|MB|GB|TB|PB|Gb/s|Mb/s|Gbps|Mbps|tok/s|tokens/s)(?![A-Za-z])")
FAMILY_TIME_RE = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?" + SEP + r"(secs|sec|msecs|msec|ms|\u00b5s|\u03bcs|us|mins|min|hrs|hr|h|s)(?![A-Za-z0-9])")

ABSTRACT_LIMIT = 1920

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def inflections(word):
    """Base form plus -s, -d/-ed and -ing forms for a single word."""
    stem = word[:-1] if word.endswith("e") else word
    return {word, word + "s", word + ("d" if word.endswith("e") else "ed"), stem + "ing"}


def phrase_alt(phrase, inflect=False):
    if inflect and " " not in phrase:
        return "|".join(sorted((re.escape(f) for f in inflections(phrase)), key=len, reverse=True))
    alt = r"\s+".join(re.escape(w) for w in phrase.split())
    if phrase == "rather":
        alt += r"(?!\s+than)"
    return alt


def make_list_re(phrases, inflect=False):
    """Case-insensitive whole-phrase regexes. Entries ending in '.' (like 'etc.') need no trailing boundary."""
    words = [p for p in phrases if not p.endswith(".")]
    dotted = [p for p in phrases if p.endswith(".")]
    regs = []
    if words:
        regs.append(re.compile(r"(?<![\w-])(" + "|".join("(?:%s)" % phrase_alt(p, inflect) for p in words) + r")(?![\w-])", re.I))
    if dotted:
        regs.append(re.compile(r"(?<![\w-])(" + "|".join(re.escape(p) for p in dotted) + r")", re.I))
    return regs


HEDGE_RES = make_list_re(HEDGES)
FILLER_RES = make_list_re(FILLER)
HYPE_RES = make_list_re(HYPE)
PLAIN_RES = [(make_list_re([k], inflect=True)[0], v) for k, v in PLAIN_WORDS.items()]
BELIEVE_RE = re.compile(r"(?<![\w-])(we\s+believe|we\s+think|we\s+feel)(?![\w-])", re.I)
NOVEL_RE = re.compile(r"(?<![\w-])(novel)(?![\w-])", re.I)
SIGNIF_RE = re.compile(r"(?<![\w-])(significant|significantly)(?![\w-])", re.I)
TEST_MARKER_RE = re.compile(
    r"\bp\s*[<=>\u2264]|\bp\\?[-~ ]?values?\b|\bp\s*\\(le|leq|ll)\b|"
    r"(statistical|signed-rank|rank-sum|paired|two-sided|one-sided|welch|student'?s|exact|sign|permutation|\bt)[- ]tests?\b|"
    r"wilcoxon|mann-whitney|bootstrap|confidence interval|\bCI\b|chi-squared|\bchi\^?2|anova|kolmogorov|significance level", re.I)
CONTRACTION_RE = re.compile(
    r"(?<![\w])([A-Za-z]+n['\u2019]t|(?:it|that|there|what|here|let|who|he|she)['\u2019]s|"
    r"(?:we|they|you|i)['\u2019](?:re|ve|ll|d|m)|(?:it|that|there)['\u2019](?:ll|d))(?![\w])", re.I)
ETAL_RE = re.compile(r"\bet\s+al\b(?!\.)|\bet\.\s*al\b\.?")
ACR_TOKEN_RE = re.compile(r"(?<![\w\\])([A-Z][A-Z0-9]+)(s?)(?![\w]|\.[a-z])")
ACR_DEF_PAREN_RE = re.compile(r"\(\s*([A-Z][A-Za-z0-9/-]*[A-Z0-9])s?\s*[),;]")
ACR_DEF_REVERSE_RE = re.compile(r"(?<![\w-])([A-Z][A-Z0-9]+)s?\s*\(\s*[A-Za-z][a-z]")
ACR_NEWACRONYM_RE = re.compile(r"\\(?:newacronym|newabbreviation)\s*(?:\[[^\]]*\])?\s*\{[^}]*\}\s*\{([^}]*)\}|\\acro\s*\{([^}]*)\}")
TODO_RE = re.compile(r"\\(todo|fixme|missingfigure|TODO)\b|(?<![\w\\])(TODO|FIXME|TBD|XXX)(?![\w])")
DEFINE_RE = re.compile(r"\\(newcommand|renewcommand|providecommand|DeclareRobustCommand|def|let)\b")
CITE_SPACE_RE = re.compile(r"([^\s~({\[])([ \t]+)\\(cite|citep|parencite|autocite|citealp|citeyearpar|supercite)\*?(?=[\[{])")
CITE_LINESTART_RE = re.compile(r"^\s*\\(cite|citep|parencite|autocite|citealp|citeyearpar)\*?(?=[\[{])")
REF_SPACE_RE = re.compile(r"([^\s~({\[])([ \t]+)\\(ref|eqref|pageref|subref|vref)\*?\{")
REF_LINESTART_RE = re.compile(r"^\s*\\(ref|eqref|pageref|subref|vref)\*?\{")
EMDASH_RE = re.compile("\u2014|(?<!-)---(?!-)")
ENDASH_RE = re.compile("(?<=\\s)(--|\u2013|-)(?=\\s)")
ROMAN_RE = re.compile(r"^[IVX]+$")
DIRECTIVE_RE = re.compile(r"paper-lint:\s*allow\s+(.+)", re.I)

# Commands whose leading arguments are not prose: name -> number of {} groups to drop.
DROP_ARGS = {
    "cite": 9, "citep": 9, "citet": 9, "citealp": 9, "citealt": 9, "citeauthor": 9, "citeyear": 9,
    "citeyearpar": 9, "parencite": 9, "textcite": 9, "autocite": 9, "footcite": 9, "nocite": 9,
    "supercite": 9, "ref": 9, "eqref": 9, "autoref": 9, "cref": 9, "Cref": 9, "pageref": 9,
    "vref": 9, "Vref": 9, "nameref": 9, "subref": 9, "labelcref": 9, "label": 9, "includegraphics": 9,
    "includesvg": 9, "includepdf": 9, "input": 9, "include": 9, "subfile": 9, "import": 9,
    "bibliography": 9, "bibliographystyle": 9, "usepackage": 9, "RequirePackage": 9,
    "documentclass": 9, "begin": 2, "end": 1, "hypersetup": 9, "vspace": 9, "hspace": 9,
    "setlength": 9, "addtolength": 9, "setcounter": 9, "addtocounter": 9, "newcommand": 9,
    "renewcommand": 9, "providecommand": 9, "DeclareMathOperator": 9, "definecolor": 9,
    "newacronym": 9, "acro": 9, "thispagestyle": 9, "pagestyle": 9, "bibitem": 9, "rule": 9,
    "cline": 9, "cmidrule": 9, "color": 1, "textcolor": 1, "colorbox": 1, "fontsize": 2,
    "linespread": 9, "captionsetup": 9, "graphicspath": 9, "todo": 9, "fixme": 9,
    "missingfigure": 9, "multicolumn": 2, "multirow": 2, "resizebox": 2, "scalebox": 1,
    "raisebox": 1, "makebox": 0, "parbox": 1, "phantom": 9, "hphantom": 9, "vphantom": 9,
    "newlength": 9, "newtheorem": 9, "crefname": 9, "Crefname": 9, "addbibresource": 9,
    "printbibliography": 9, "setlist": 9, "lstset": 9, "url": 9, "nolinkurl": 9, "href": 1,
    "texttt": 9, "path": 9, "verb": 0, "lstinline": 9, "mintinline": 9, "code": 9,
    "ac": 9, "acs": 9, "acl": 9, "acf": 9, "acp": 9, "gls": 9, "glspl": 9, "Gls": 9, "Glspl": 9,
}
CODE_LIKE = {"url", "nolinkurl", "texttt", "path", "lstinline", "mintinline", "code"}
REF_LIKE = {"ref", "eqref", "autoref", "cref", "Cref", "pageref", "vref", "Vref", "nameref", "subref", "labelcref"}


class Finding(object):
    __slots__ = ("path", "line", "rule", "msg")

    def __init__(self, path, line, rule, msg):
        self.path, self.line, self.rule, self.msg = path, line, rule, msg

    def __str__(self):
        return "%s:%d: %s: %s" % (self.path, self.line, self.rule, self.msg)


def strip_comment(line):
    """Return (code, comment_or_None). A % preceded by an even number of backslashes starts a comment."""
    i, n = 0, len(line)
    while i < n:
        c = line[i]
        if c == "\\":
            i += 2
            continue
        if c == "%":
            return line[:i], line[i + 1:]
        i += 1
    return line, None


def read_group(s, i, open_ch="{", close_ch="}"):
    """s[i] == open_ch. Return index after the matching close, or len(s) if unbalanced."""
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    return len(s)


def strip_inline_verb(s):
    s = re.sub(r"\\verb\*?([^A-Za-z\s{])(.*?)\1", " code ", s)
    s = re.sub(r"\\lstinline(?:\[[^\]]*\])?([^A-Za-z\s{\[])(.*?)\1", " code ", s)
    s = re.sub(r"\\mintinline\{[^}]*\}([^A-Za-z\s{])(.*?)\1", " code ", s)
    return s


class MathState(object):
    def __init__(self):
        self.mode = None   # None, '$', '$$', ')', ']', 'env'
        self.env = None


def strip_math(code, st):
    out = []
    i, n = 0, len(code)
    while i < n:
        c = code[i]
        if st.mode is None:
            if code.startswith("\\begin", i):
                m = re.match(r"\\begin\s*\{([^}]*)\}", code[i:])
                if m and m.group(1) in MATH_ENVS:
                    st.mode, st.env = "env", m.group(1)
                    out.append(" math ")
                    i += m.end()
                    continue
            if code.startswith("\\(", i):
                st.mode = ")"
                out.append(" math ")
                i += 2
                continue
            if code.startswith("\\[", i):
                st.mode = "]"
                out.append(" math ")
                i += 2
                continue
            if c == "\\":
                out.append(code[i:i + 2])
                i += 2
                continue
            if code.startswith("$$", i):
                st.mode = "$$"
                out.append(" math ")
                i += 2
                continue
            if c == "$":
                st.mode = "$"
                out.append(" math ")
                i += 1
                continue
            out.append(c)
            i += 1
        else:
            if st.mode == "env":
                m = re.match(r"\\end\s*\{([^}]*)\}", code[i:]) if code.startswith("\\end", i) else None
                if m and m.group(1) == st.env:
                    st.mode, st.env = None, None
                    i += m.end()
                    continue
            elif st.mode in (")", "]") and code.startswith("\\" + st.mode, i):
                st.mode = None
                i += 2
                continue
            elif st.mode == "$$" and code.startswith("$$", i):
                st.mode = None
                i += 2
                continue
            elif st.mode == "$" and c == "$":
                st.mode = None
                i += 1
                continue
            if c == "\\":
                i += 2
                continue
            i += 1
    return "".join(out)


def drop_command_args(s):
    """Remove non-prose command arguments; keep the text of formatting commands."""
    out = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        m = re.match(r"\\([A-Za-z@]+)\*?", s[i:])
        if not m:
            nxt = s[i + 1:i + 2]
            if nxt in ("%", "&", "_", "#", "$", "{", "}"):
                out.append(nxt)
            elif nxt in (",", ";", ":", "!", " ", "\\"):
                out.append(" ")
            # accents and other control symbols vanish
            i += 2
            continue
        name = m.group(1)
        j = i + m.end()
        if name in DROP_ARGS:
            limit = DROP_ARGS[name]
            groups = 0
            while j < n:
                k = j
                while k < n and s[k] in " \t":
                    k += 1
                if k < n and s[k] == "[":
                    j = read_group(s, k, "[", "]")
                    continue
                if k < n and s[k] == "{" and groups < limit:
                    j = read_group(s, k)
                    groups += 1
                    continue
                break
            if name in CODE_LIKE:
                out.append(" code ")
            elif name in REF_LIKE:
                out.append(" 0 ")
            else:
                out.append(" ")
            i = j
            continue
        out.append(" ")
        i = j
    text = "".join(out)
    text = text.replace("~", " ").replace("{", " ").replace("}", " ")
    text = text.replace("``", '"').replace("''", '"')
    return text


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------


class SrcLine(object):
    __slots__ = ("path", "lineno", "raw", "root")

    def __init__(self, path, lineno, raw, root):
        self.path, self.lineno, self.raw, self.root = path, lineno, raw, root


def resolve_input(name, base_dirs):
    name = name.strip()
    cands = [name] if name.endswith(".tex") else [name + ".tex", name]
    for d in base_dirs:
        for c in cands:
            p = os.path.normpath(os.path.join(d, c))
            if os.path.isfile(p):
                return p
    return None


def load(path, root_dir, seen, root, relative):
    out = []
    real = os.path.realpath(path)
    if real in seen:
        return out
    seen.add(real)
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().split("\n")
    except OSError as e:
        sys.stderr.write("paper_lint: cannot read %s: %s\n" % (path, e))
        return out
    shown = os.path.relpath(path) if relative and os.path.isabs(path) else path
    for idx, raw in enumerate(lines, 1):
        out.append(SrcLine(shown, idx, raw.rstrip("\r"), root))
        code, _ = strip_comment(raw)
        for m in INPUT_RE.finditer(code):
            target = resolve_input(m.group(2), [root_dir, os.path.dirname(path)])
            if target:
                out.extend(load(target, root_dir, seen, root, relative))
    return out


# --------------------------------------------------------------------------
# Linting
# --------------------------------------------------------------------------


class FloatRec(object):
    def __init__(self, kind, env, line):
        self.kind, self.env, self.line = kind, env, line
        self.labels = []         # (key, line, order)
        self.captions = []       # (line, order)
        self.graphics = []       # order
        self.tabulars = []       # order


class Linter(object):
    def __init__(self, max_words=35, allow=(), disabled=()):
        self.max_words = max_words
        self.allow = set(ACRONYM_ALLOW) | set(allow)
        self.disabled = set(disabled)
        self.findings = []
        self.refs = set()
        self.global_acr_defs = set()
        self._ord = 0
        self._hlines = 0

    def _next(self):
        self._ord += 1
        return self._ord

    def add(self, rec, rule, msg):
        if rule in self.disabled:
            return
        self.findings.append(Finding(rec.path, rec.lineno, rule, msg))

    # ---- pass 1: collect refs, acronym definitions from glossaries, directives
    def prepass(self, lines):
        verb = None
        for rec in lines:
            raw = rec.raw
            code, comment = strip_comment(strip_inline_verb(raw))
            if comment:
                m = DIRECTIVE_RE.search(comment)
                if m:
                    self.allow |= set(t for t in re.split(r"[\s,]+", m.group(1).strip()) if t)
            if verb:
                if re.search(r"\\end\s*\{" + re.escape(verb) + r"\}", code):
                    verb = None
                continue
            mv = re.search(r"\\begin\s*\{([^}]+)\}", code)
            if mv and mv.group(1) in VERBATIM_ENVS and not re.search(r"\\end\s*\{" + re.escape(mv.group(1)) + r"\}", code):
                code = code[:mv.start()]
                verb = mv.group(1)
            for m in REF_COLLECT_RE.finditer(code):
                for key in m.group(2).split(","):
                    self.refs.add(key.strip())
            for m in ACR_NEWACRONYM_RE.finditer(code):
                self.global_acr_defs.add((m.group(1) or m.group(2) or "").strip())

    # ---- pass 2: per-line scan, building paragraphs
    def run(self, lines):
        self.prepass(lines)
        roots_with_doc = set()
        for rec in lines:
            code, _ = strip_comment(rec.raw)
            if re.search(r"\\begin\s*\{document\}", code):
                roots_with_doc.add(rec.root)

        math = MathState()
        verb = None
        iffalse = 0
        stack = []
        floats = []
        body = {}
        done = set()
        paragraphs = []      # list of dicts: segments [(text, rec)], kind
        cur = {"segs": [], "kind": "prose", "scope": "body"}
        self.abstract_parts = []
        self.unit_tokens = []  # (rec, spelling) for consistency
        prev_tail = {"char": "", "eaten": False}

        def flush():
            if cur["segs"]:
                paragraphs.append(dict(cur))
            cur["segs"] = []

        for rec in lines:
            root = rec.root
            if root not in body:
                body[root] = root not in roots_with_doc
            if root in done:
                continue
            raw = strip_inline_verb(rec.raw)
            code, comment = strip_comment(raw)
            stripped_raw = rec.raw.strip()
            if stripped_raw.startswith("%"):
                continue

            if verb:
                if re.search(r"\\end\s*\{" + re.escape(verb) + r"\}", code):
                    verb = None
                continue
            if iffalse:
                iffalse += len(re.findall(r"\\if[A-Za-z@]*", code)) - len(re.findall(r"\\fi\b", code))
                continue
            if re.match(r"\s*\\iffalse\b", code):
                iffalse = 1 + len(re.findall(r"\\if[A-Za-z@]*", code[code.index("\\iffalse") + 8:])) - len(re.findall(r"\\fi\b", code))
                if iffalse <= 0:
                    iffalse = 0
                continue
            mv = re.search(r"\\begin\s*\{([^}]+)\}", code)
            if mv and mv.group(1) in VERBATIM_ENVS:
                endm = re.search(r"\\end\s*\{" + re.escape(mv.group(1)) + r"\}", code[mv.end():])
                if endm:
                    code = code[:mv.start()] + " " + code[mv.end() + endm.end():]
                else:
                    code = code[:mv.start()]
                    verb = mv.group(1)

            # arxiv-source: checked in preamble and body
            self.check_arxiv_source(rec, code)

            if not body[root]:
                if re.search(r"\\begin\s*\{document\}", code):
                    body[root] = True
                    flush()
                    cur["scope"] = "body"
                    code = code[re.search(r"\\begin\s*\{document\}", code).end():]
                else:
                    m = re.search(r"\\title\s*(\[[^\]]*\])?\s*\{", code)
                    if not m:
                        continue
                    code = code[m.end() - 1:]
                    code = code[1:read_group(code, 0) - 1] if code.startswith("{") else code
                    flush()
                    cur["scope"] = "title"
            if re.search(r"\\end\s*\{document\}", code):
                code = code[:re.search(r"\\end\s*\{document\}", code).start()]
                done.add(root)

            if not code.strip():
                if math.mode in ("$", ")"):
                    math.mode = None
                flush()
                prev_tail = {"char": "", "eaten": False}
                if root in done:
                    break
                continue

            code_nm = strip_math(code, math)
            in_tab_before = any(e in TABULAR_ENVS for e in stack)

            # events: environments, floats, tables
            boundary = False
            for m in EVENT_RE.finditer(code_nm):
                if m.group(1):
                    env = m.group(2).strip()
                    boundary = True
                    if m.group(1) == "begin":
                        stack.append(env)
                        if env in FLOAT_ENVS:
                            floats.append(FloatRec("table" if env in TABLE_ENVS else "figure", env, rec))
                        if env in TABULAR_ENVS:
                            self.check_tabular_spec(rec, code_nm, m.end(), env)
                            self._hlines = 0
                            if floats:
                                floats[-1].tabulars.append(self._next())
                        if env == "tikzpicture" and floats:
                            floats[-1].graphics.append(self._next())
                        if env == "abstract":
                            flush()
                            cur["scope"] = "abstract"
                    else:
                        if env in stack:
                            while stack:
                                top = stack.pop()
                                if top == env:
                                    break
                        if env in TABULAR_ENVS and self._hlines > 3:
                            self.add(rec, "table-rules", "%d \\hline rules in one tabular; use booktabs \\toprule, \\midrule, \\bottomrule and no rules between data rows" % self._hlines)
                            self._hlines = 0
                        if env in FLOAT_ENVS and floats:
                            self.close_float(floats.pop())
                        if env == "abstract":
                            flush()
                            cur["scope"] = "body"
                elif m.group(3):
                    if floats:
                        floats[-1].captions.append((rec, self._next()))
                elif m.group(4) is not None:
                    if floats:
                        floats[-1].labels.append((m.group(4).strip(), rec, self._next()))
                elif m.group(5):
                    if floats and m.group(5) != "import":
                        floats[-1].graphics.append(self._next())
                elif m.group(6):
                    if any(e in TABULAR_ENVS for e in stack):
                        self._hlines = self._hlines + 1

            in_tab = in_tab_before or any(e in TABULAR_ENVS for e in stack)

            # code-level rules
            self.check_code_rules(rec, code, code_nm, in_tab, prev_tail)
            prev_tail = {"char": code_nm.rstrip()[-1:], "eaten": comment is not None}

            # prose
            prose = drop_command_args(code_nm)
            if cur["scope"] == "abstract" and "abstract" in stack:
                self.abstract_parts.append((rec, code_nm))
            is_section = bool(SECTION_RE.search(code_nm))
            starts_item = bool(re.match(r"\s*\\(item|caption|bibitem)\b", code_nm))
            if is_section or starts_item or boundary or in_tab:
                flush()
            cur["kind"] = "table" if in_tab else "prose"
            if prose.strip():
                cur["segs"].append((prose, rec))
            if is_section or in_tab:
                flush()
            if root in done:
                flush()
        flush()
        for f in floats:
            self.close_float(f)

        self.check_paragraphs(paragraphs)
        self.check_abstract_length()
        self.check_unit_consistency()
        return self.findings

    # ---- code-level checks
    def check_arxiv_source(self, rec, code):
        if re.search(r"\\today\b", code):
            self.add(rec, "arxiv-source", "\\today changes when arXiv rebuilds the PDF; write the date or leave \\date{} empty")
        if re.search(r"\\usepackage\s*(\[[^\]]*\])?\s*\{[^}]*\blineno\b", code) or re.search(r"\\linenumbers\b", code):
            self.add(rec, "arxiv-source", "line numbers are not allowed on arXiv (format policy)")
        if re.search(r"\\doublespacing\b|\\usepackage\s*\[[^\]]*doublespacing[^\]]*\]\s*\{setspace\}|\\linespread\s*\{\s*(1\.[6-9]|2)", code):
            self.add(rec, "arxiv-source", "double spacing; arXiv wants single-spaced text")
        m = re.search(r"\\(documentclass|usepackage)\s*\[([^\]]*)\]", code)
        if m and re.search(r"(?<![\w-])(review|referee|anonymous|anonymized)(?![\w-])", m.group(2)):
            self.add(rec, "arxiv-source", "review or anonymous mode option '%s'; arXiv needs named authors and no referee formatting" % m.group(2).strip())

    def check_tabular_spec(self, rec, code, pos, env):
        s = code[pos:]
        i = 0
        skip = 1 if env in ("tabular*", "tabularx", "tabulary") else 0
        groups = []
        while i < len(s) and len(groups) < skip + 1:
            while i < len(s) and s[i] in " \t":
                i += 1
            if i < len(s) and s[i] == "[":
                i = read_group(s, i, "[", "]")
                continue
            if i < len(s) and s[i] == "{":
                j = read_group(s, i)
                groups.append(s[i + 1:j - 1])
                i = j
                continue
            break
        if len(groups) == skip + 1:
            spec = groups[-1]
            spec_clean = re.sub(r"[@!>< ]?\{[^{}]*\}", "", spec)
            if "|" in spec_clean:
                self.add(rec, "table-rules", "vertical rules in column spec {%s}; drop them (booktabs)" % spec)

    def check_code_rules(self, rec, code, code_nm, in_tab, prev_tail):
        # em dash: on code without math
        for m in EMDASH_RE.finditer(code_nm):
            self.add(rec, "em-dash", "em dash '%s'" % m.group(0))
        if not in_tab:
            for m in ENDASH_RE.finditer(code_nm):
                self.add(rec, "en-dash", "spaced dash '%s' in prose; use -- only inside ranges (1--4) and rewrite the sentence" % m.group(1))
        # todo
        if not DEFINE_RE.search(code_nm):
            for m in TODO_RE.finditer(code_nm):
                self.add(rec, "todo", "'%s' left in the text" % m.group(0))
        # units: drop non-prose command arguments first so labels and keys do not match
        unit_code = self._unit_code(code_nm)
        for m in UNIT_RE.finditer(unit_code):
            num, sep, unit = m.group(1), m.group(2), m.group(3)
            if unit == "s" and re.match(r"^\d{3}0$", num):
                continue  # 1990s, 2020s
            if sep == "":
                self.add(rec, "unit-space", "'%s%s': write %s\\,%s (or %s~%s)" % (num, unit, num, unit, num, unit))
            elif not in_tab:
                self.add(rec, "unit-space", "'%s %s': plain space can break the line; write %s\\,%s or %s~%s" % (num, unit, num, unit, num, unit))
        for m in FAMILY_TOKEN_RE.finditer(unit_code):
            self.unit_tokens.append((rec, m.group(1)))
        for m in FAMILY_TIME_RE.finditer(unit_code):
            if m.group(1) == "s" and re.match(r"\d{3}0\D*s$", m.group(0)):
                continue
            self.unit_tokens.append((rec, m.group(1)))
        # cite and ref spacing
        for m in CITE_SPACE_RE.finditer(code_nm):
            self.add(rec, "cite-tilde", "space before \\%s; write ~\\%s" % (m.group(3), m.group(3)))
        for m in REF_SPACE_RE.finditer(code_nm):
            self.add(rec, "ref-tilde", "space before \\%s; write ~\\%s (Figure~\\ref{...})" % (m.group(3), m.group(3)))
        ch = prev_tail.get("char", "")
        if ch and not prev_tail.get("eaten") and (ch.isalnum() or ch in ",;:"):
            if CITE_LINESTART_RE.match(code_nm):
                self.add(rec, "cite-tilde", "line break before \\cite; end the previous line with ~ or %")
            if REF_LINESTART_RE.match(code_nm):
                self.add(rec, "ref-tilde", "line break before \\ref; end the previous line with ~ or %")

    def _unit_code(self, code_nm):
        out = []
        i, n = 0, len(code_nm)
        while i < n:
            m = re.match(r"\\([A-Za-z@]+)\*?", code_nm[i:]) if code_nm[i] == "\\" else None
            if m and m.group(1) in DROP_ARGS and m.group(1) not in ("begin", "end", "multicolumn", "multirow",
                                                                     "textcolor", "color", "resizebox", "raisebox",
                                                                     "scalebox", "parbox", "href", "fontsize"):
                j = i + m.end()
                while j < n:
                    k = j
                    while k < n and code_nm[k] in " \t":
                        k += 1
                    if k < n and code_nm[k] in "[{":
                        j = read_group(code_nm, k, code_nm[k], "]" if code_nm[k] == "[" else "}")
                        continue
                    break
                out.append(" ")
                i = j
                continue
            if m:
                out.append(code_nm[i:i + m.end()])
                i += m.end()
                continue
            out.append(code_nm[i])
            i += 1
        return "".join(out)

    def close_float(self, f):
        rec = f.line
        if not f.captions:
            self.add(rec, "float-caption", "%s has no \\caption" % f.env)
        if not f.labels:
            self.add(rec, "float-label", "%s has no \\label, so the text cannot reference it" % f.env)
        else:
            first_cap = min(o for _, o in f.captions) if f.captions else None
            for key, lrec, order in f.labels:
                if first_cap is None or order < first_cap:
                    self.add(lrec, "float-label", "\\label{%s} before \\caption; \\ref will print the section number" % key)
            if not any(key in self.refs for key, _, _ in f.labels):
                key, lrec, _ = f.labels[-1]
                self.add(lrec, "float-unref", "\\label{%s} is never referenced; cite every figure and table in the text" % key)
        if f.captions:
            first_cap_rec, first_cap = min(f.captions, key=lambda t: t[1])
            if f.kind == "table" and f.tabulars and first_cap > min(f.tabulars):
                self.add(first_cap_rec, "float-caption", "table caption below the table; put it above")
            if f.kind == "figure" and f.graphics and first_cap < min(f.graphics):
                self.add(first_cap_rec, "float-caption", "figure caption above the graphic; put it below")

    # ---- paragraph-level checks
    def check_paragraphs(self, paragraphs):
        defined = {"title": set(), "abstract": set(), "body": set()}
        reported = set()
        for para in paragraphs:
            text, offsets = self._join(para["segs"])
            if not text.strip():
                continue
            scope = para.get("scope", "body")

            def rec_at(pos):
                r = offsets[0][1]
                for start, rr in offsets:
                    if start <= pos:
                        r = rr
                    else:
                        break
                return r

            # Quoted text (titles, examples) is masked for the word-list rules.
            wtext = re.sub(r'"[^"]*"', lambda q: " " * len(q.group(0)), text)
            for regs, rule, fmt in ((HEDGE_RES, "hedge", "hedge '%s': state the claim and the condition under which it holds"),
                                    (FILLER_RES, "filler", "filler '%s': cut it"),
                                    (HYPE_RES, "hype", "hype '%s': replace with the measured number")):
                for rg in regs:
                    for m in rg.finditer(wtext):
                        self.add(rec_at(m.start()), rule, fmt % m.group(1).lower())
            for rg, repl in PLAIN_RES:
                for m in rg.finditer(wtext):
                    self.add(rec_at(m.start()), "plain-words", "'%s': write '%s'" % (m.group(1).lower(), repl))
            for m in BELIEVE_RE.finditer(wtext):
                self.add(rec_at(m.start()), "unsupported", "'%s': give the evidence or cut the sentence" % re.sub(r"\s+", " ", m.group(1).lower()))
            for m in NOVEL_RE.finditer(wtext):
                self.add(rec_at(m.start()), "unsupported", "'novel': say what is new and against which prior work; reviewers judge novelty")
            for m in CONTRACTION_RE.finditer(wtext):
                self.add(rec_at(m.start()), "contraction", "contraction '%s'" % m.group(1))
            for m in ETAL_RE.finditer(wtext):
                self.add(rec_at(m.start()), "et-al", "'%s': write 'et al.' (et~al.\\ before a citation)" % m.group(0))

            # acronyms
            defs_here = []
            for m in ACR_DEF_PAREN_RE.finditer(text):
                defs_here.append((m.start(1), m.group(1)))
            for m in ACR_DEF_REVERSE_RE.finditer(text):
                defs_here.append((m.start(1), m.group(1)))
            def_pos = {p: a for p, a in defs_here}
            for m in ACR_TOKEN_RE.finditer(text):
                tok = m.group(1)
                if sum(1 for ch in tok if ch.isupper()) < 2 or ROMAN_RE.match(tok):
                    continue
                if scope == "title" or any(ch.isdigit() for ch in tok) or tok in UNIT_SET:
                    continue  # titles, model or format names with digits (A100, FP8), unit symbols
                if tok in self.allow or tok in self.global_acr_defs:
                    continue
                if m.start(1) in def_pos:
                    defined[scope].add(def_pos[m.start(1)])
                    continue
                if tok in defined[scope]:
                    continue
                key = (scope, tok)
                if key in reported:
                    continue
                reported.add(key)
                extra = ""
                if scope == "body" and tok in defined["abstract"]:
                    extra = "; the abstract definition does not carry over, define it again at first use in the body"
                self.add(rec_at(m.start()), "acronym", "'%s' used before a '(%s)' definition%s" % (tok, tok, extra))
            for p, a in defs_here:
                defined[scope].add(a)

            if para["kind"] == "table":
                continue
            # sentences
            for start, end in self._sentences(text):
                sent = text[start:end]
                words = re.findall(r"[A-Za-z0-9]+(?:['\u2019./-][A-Za-z0-9]+)*", sent)
                if len(words) > self.max_words:
                    self.add(rec_at(start), "sentence-length", "sentence of %d words (limit %d): split it" % (len(words), self.max_words))
                for m in SIGNIF_RE.finditer(sent):
                    r0, r1 = rec_at(start), rec_at(end - 1)
                    raw_span = self._raw_span(para["segs"], r0, r1)
                    if not TEST_MARKER_RE.search(sent) and not TEST_MARKER_RE.search(raw_span):
                        self.add(rec_at(start + m.start()), "unsupported", "'%s' without a named statistical test in the sentence; give the test and p, or the number" % m.group(1).lower())

    @staticmethod
    def _raw_span(segs, r0, r1):
        out, on = [], False
        for _, rec in segs:
            if rec is r0:
                on = True
            if on:
                out.append(strip_comment(rec.raw)[0])
            if rec is r1:
                break
        return " ".join(out)

    @staticmethod
    def _join(segs):
        parts, offsets, pos = [], [], 0
        for text, rec in segs:
            offsets.append((pos, rec))
            parts.append(text)
            pos += len(text) + 1
        return " ".join(parts), offsets

    @staticmethod
    def _sentences(text):
        spans = []
        start = 0
        for m in re.finditer(r"[.!?]+(?=[\"')\]]*(\s|$))", text):
            end = m.end()
            tokens = text[start:end].split()
            last = tokens[-1] if tokens else ""
            if last.lower().lstrip("(\"'[") in ABBREVIATIONS:
                continue
            if re.match(r"^\(?[A-Z]\.$", last):
                continue  # an initial, as in "J. Smith"
            spans.append((start, end))
            start = end
        if text[start:].strip():
            spans.append((start, len(text)))
        return spans

    def check_abstract_length(self):
        if not self.abstract_parts:
            return
        text = " ".join(c for _, c in self.abstract_parts)
        text = re.sub(r"\\(begin|end)\s*\{abstract\}", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > ABSTRACT_LIMIT:
            self.add(self.abstract_parts[0][0], "abstract-length",
                     "abstract is about %d characters; arXiv's abstract field takes at most %d" % (len(text), ABSTRACT_LIMIT))

    def check_unit_consistency(self):
        for rec, tok in self.unit_tokens:
            if tok in NONSTANDARD_UNITS:
                self.add(rec, "unit-consistency", "nonstandard unit symbol '%s'; write '%s'" % (tok, NONSTANDARD_UNITS[tok]))
        for fam, groups in UNIT_FAMILIES.items():
            counts = OrderedDict()
            first = {}
            for gname, spellings in groups:
                counts[gname] = 0
            for rec, tok in self.unit_tokens:
                for gname, spellings in groups:
                    if tok in spellings:
                        counts[gname] += 1
                        first.setdefault(gname, rec)
            used = [g for g, c in counts.items() if c]
            if len(used) < 2:
                continue
            # majority wins; a tie keeps the first (standard) group
            major = max(used, key=lambda g: (counts[g], -[x[0] for x in groups].index(g)))
            done = set()
            for rec, tok in self.unit_tokens:
                if (rec.path, rec.lineno, tok) in done:
                    continue
                done.add((rec.path, rec.lineno, tok))
                for gname, spellings in groups:
                    if tok in spellings and gname != major and tok not in NONSTANDARD_UNITS:
                        self.add(rec, "unit-consistency",
                                 "%s: '%s' mixed with %s (%d uses, first at line %d); use one, or say which quantity uses which" %
                                 (fam, tok, major, counts[major], first[major].lineno))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mechanical style checks for LaTeX papers. Always exits 0.")
    ap.add_argument("files", nargs="*", help="main.tex and any extra .tex files (\\input files are followed)")
    ap.add_argument("--max-words", type=int, default=35, help="sentence word limit (default 35)")
    ap.add_argument("--allow", default="", help="comma-separated acronyms that need no definition")
    ap.add_argument("--disable", default="", help="comma-separated rule ids to skip")
    ap.add_argument("--list-rules", action="store_true", help="print the rules and exit")
    args = ap.parse_args(argv)

    if args.list_rules:
        for rid, (desc, ref) in RULES.items():
            print("%-17s %s [references/%s]" % (rid, desc, ref))
        return 0
    if not args.files:
        ap.print_usage()
        return 2
    disabled = [r.strip() for r in args.disable.split(",") if r.strip()]
    for r in disabled:
        if r not in RULES:
            sys.stderr.write("paper_lint: unknown rule '%s' (see --list-rules)\n" % r)
            return 2

    seen = set()
    lines = []
    for f in args.files:
        root_dir = os.path.dirname(os.path.abspath(f))
        lines.extend(load(f, root_dir, seen, f, not os.path.isabs(f)))
    linter = Linter(max_words=args.max_words,
                    allow=[a.strip() for a in args.allow.split(",") if a.strip()],
                    disabled=disabled)
    findings = linter.run(lines)
    order = {}
    for i, rec in enumerate(lines):
        order.setdefault((rec.path, rec.lineno), i)
    findings.sort(key=lambda f: (order.get((f.path, f.line), 0), list(RULES).index(f.rule)))
    for f in findings:
        print(f)
    counts = Counter(f.rule for f in findings)
    files = len({rec.path for rec in lines})
    print("")
    print("summary: %d findings in %d file%s" % (len(findings), files, "" if files == 1 else "s"))
    for rid in RULES:
        mark = " (disabled)" if rid in disabled else ""
        print("  %-17s %4d%s" % (rid, counts.get(rid, 0), mark))
    return 0


if __name__ == "__main__":
    sys.exit(main())
