"""Tests for skills/arxiv-paper/scripts/paper_lint.py and the skill's reference files.

Run from the repo root:
    python3 -m unittest discover -s tests -v
"""

import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "arxiv-paper")
SCRIPT = os.path.join(SKILL, "scripts", "paper_lint.py")
FIX = os.path.join(ROOT, "tests", "fixtures")
REFS = os.path.join(SKILL, "references")

sys.path.insert(0, os.path.join(SKILL, "scripts"))
import paper_lint  # noqa: E402

FINDING_RE = re.compile(r"^(.+?):(\d+): ([a-z-]+): (.*)$")

# fixture -> {rule: [lines it must flag]}. Lines are exact, so a fixture that
# stops firing, or fires on the wrong line, fails.
EXPECTED = {
    "em-dash": {"em-dash": [3, 4]},
    "en-dash": {"en-dash": [3, 4]},
    "hedge": {"hedge": [3, 4]},
    "filler": {"filler": [3, 4]},
    "hype": {"hype": [3, 4]},
    "plain-words": {"plain-words": [3, 3, 4]},
    "unsupported": {"unsupported": [3, 4, 5]},
    "contraction": {"contraction": [3, 4]},
    "acronym": {"acronym": [8, 12]},
    "unit-space": {"unit-space": [3, 4]},
    "unit-consistency": {"unit-consistency": [4, 5]},
    "todo": {"todo": [3, 4, 5]},
    "sentence-length": {"sentence-length": [3]},
    "et-al": {"et-al": [3, 4]},
    "cite-tilde": {"cite-tilde": [3, 5]},
    "ref-tilde": {"ref-tilde": [3, 5]},
    "float-label": {"float-label": [4, 10]},
    "float-unref": {"float-unref": [8]},
    "float-caption": {"float-caption": [4, 18, 22]},
    "table-rules": {"table-rules": [8, 16]},
    "abstract-length": {"abstract-length": [3]},
    "arxiv-source": {"arxiv-source": [1, 2, 3]},
}


def run(*args):
    proc = subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True, text=True)
    findings = []
    for line in proc.stdout.splitlines():
        m = FINDING_RE.match(line)
        if m:
            findings.append((m.group(1), int(m.group(2)), m.group(3), m.group(4)))
    return proc, findings


def lines_for(findings, rule):
    return sorted(ln for _, ln, r, _ in findings if r == rule)


class RuleFixtures(unittest.TestCase):
    def test_every_rule_has_a_fixture(self):
        self.assertEqual(sorted(EXPECTED), sorted(paper_lint.RULES))

    def test_each_fixture_flags_its_rule(self):
        for name, want in EXPECTED.items():
            path = os.path.join(FIX, name + ".tex")
            with self.subTest(fixture=name):
                proc, findings = run(path)
                self.assertEqual(proc.returncode, 0)
                for rule, lines in want.items():
                    self.assertEqual(lines_for(findings, rule), sorted(lines), proc.stdout)

    def test_clean_fixture_has_no_findings(self):
        proc, findings = run(os.path.join(FIX, "clean", "main.tex"))
        self.assertEqual(findings, [], proc.stdout)
        self.assertIn("summary: 0 findings in 2 files", proc.stdout)  # \input{part} was followed

    def test_input_is_followed(self):
        # The part file references fig:trace; without following \input the count of files is 1.
        proc, _ = run(os.path.join(FIX, "clean", "main.tex"))
        self.assertIn("2 files", proc.stdout)


class Messages(unittest.TestCase):
    def test_abstract_definition_does_not_carry_over(self):
        _, findings = run(os.path.join(FIX, "acronym.tex"))
        msgs = [m for _, ln, r, m in findings if r == "acronym" and ln == 12]
        self.assertTrue(msgs and "abstract definition does not carry over" in msgs[0])

    def test_significance_with_named_test_passes(self):
        _, findings = run(os.path.join(FIX, "unsupported.tex"))
        self.assertNotIn(6, lines_for(findings, "unsupported"))

    def test_units_report_both_forms(self):
        _, findings = run(os.path.join(FIX, "unit-space.tex"))
        msgs = " ".join(m for _, _, r, m in findings if r == "unit-space")
        self.assertIn("80\\,GB", msgs)
        self.assertIn("plain space", msgs)


class Cli(unittest.TestCase):
    def test_summary_lists_every_rule(self):
        proc, _ = run(os.path.join(FIX, "hype.tex"))
        for rule in paper_lint.RULES:
            self.assertRegex(proc.stdout, r"(?m)^  %s\s+\d+" % re.escape(rule))

    def test_exit_zero_with_findings(self):
        proc, findings = run(os.path.join(FIX, "hype.tex"))
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(findings)

    def test_disable(self):
        _, findings = run(os.path.join(FIX, "hype.tex"), "--disable", "hype")
        self.assertEqual(lines_for(findings, "hype"), [])

    def test_unknown_rule_is_an_error(self):
        proc, _ = run(os.path.join(FIX, "hype.tex"), "--disable", "nope")
        self.assertEqual(proc.returncode, 2)

    def test_allow(self):
        _, findings = run(os.path.join(FIX, "acronym.tex"), "--allow", "TTFT,KV")
        self.assertEqual(lines_for(findings, "acronym"), [])

    def test_max_words(self):
        _, findings = run(os.path.join(FIX, "sentence-length.tex"), "--max-words", "60")
        self.assertEqual(lines_for(findings, "sentence-length"), [])

    def test_list_rules(self):
        proc = subprocess.run([sys.executable, SCRIPT, "--list-rules"], capture_output=True, text=True)
        self.assertEqual(len(proc.stdout.strip().splitlines()), len(paper_lint.RULES))


def ref_text(name):
    with open(os.path.join(REFS, name), encoding="utf-8") as fh:
        return fh.read()


def list_line(text, label):
    m = re.search(r"(?m)^- %s: (.*)$" % re.escape(label), text)
    assert m, label
    return m.group(1)


class ReferencesInSync(unittest.TestCase):
    def test_word_lists_match_language_style(self):
        text = ref_text("language-style.md")
        for label, values in (("Hedges", paper_lint.HEDGES), ("Filler", paper_lint.FILLER),
                              ("Hype", paper_lint.HYPE), ("Unsupported", paper_lint.UNSUPPORTED),
                              ("Acronyms that need no definition", paper_lint.ACRONYM_ALLOW)):
            with self.subTest(list=label):
                self.assertEqual(list_line(text, label).split(", "), list(values))
        pairs = [p.split(" -> ", 1) for p in list_line(text, "Plain words").split("; ")]
        self.assertEqual([(k, v) for k, v in pairs], list(paper_lint.PLAIN_WORDS.items()))

    def test_every_cited_key_is_in_sources(self):
        keys = set(re.findall(r"(?m)^\| `([a-z0-9.-]+)` \|", ref_text("sources.md")))
        self.assertEqual(len(keys), 80)
        files = [os.path.join(REFS, f) for f in os.listdir(REFS) if f.endswith(".md")] + [os.path.join(SKILL, "SKILL.md")]
        for path in files:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            text = re.sub(r"(?s)```.*?```", "", text)  # code blocks
            text = re.sub(r"`[^`\n]*`", "", text)        # inline code
            cited = set(re.findall(r"\[([a-z][a-z0-9.-]+)\](?!\()", text))
            with self.subTest(file=os.path.basename(path)):
                self.assertEqual(cited - keys, set())

    def test_skill_routes_to_existing_files(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read()
        routed = set(re.findall(r"`references/([a-z-]+\.md)`", text))
        present = {f for f in os.listdir(REFS) if f.endswith(".md")}
        self.assertEqual(routed, present)

    def test_skill_frontmatter(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read()
        m = re.match(r"---\nname: (.+)\ndescription: \"(.+)\"\nlicense: .+\n---\n", text)
        self.assertTrue(m)
        self.assertEqual(m.group(1), "arxiv-paper")
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_checklist_ids_unique(self):
        ids = re.findall(r"(?m)^- ([A-Z]{2}\d+):", ref_text("checklist.md"))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreater(len(ids), 50)


class NoEmDashes(unittest.TestCase):
    def test_repo_text_has_no_em_dash(self):
        bad = []
        for base, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", "work", "fixtures", "__pycache__")]
            for f in files:
                if not f.endswith((".md", ".py", ".txt", ".cff", ".tex")):
                    continue
                path = os.path.join(base, f)
                with open(path, encoding="utf-8") as fh:
                    for i, line in enumerate(fh, 1):
                        if "\u2014" in line:
                            bad.append("%s:%d" % (os.path.relpath(path, ROOT), i))
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
