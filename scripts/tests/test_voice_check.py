"""Unit tests for the #747 voice gate.

Fixtures live in ``fixtures/voice_check/`` rather than inline strings so that the
em-dash cases are real files on disk, the same shape the gate sees in CI. They
sit outside ``content/drafts/`` and outside the theme, so they are deliberately
out of the gate's own scan scope and cannot trip it.
"""

import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import voice_check  # noqa: E402

FIXTURES = Path("scripts/tests/fixtures/voice_check")
EM_DASH = "\u2014"


def run(paths, waivers=None, stdin=None):
    """Run main() with an optional temporary waiver set; return (code, stdout)."""
    buf = io.StringIO()
    waiver_path = voice_check.WAIVER_PATH
    if waivers is not None:
        waiver_path = Path(__file__).parent / "_tmp_voice_waivers.json"
        waiver_path.write_text(json.dumps({"waivers": waivers}), encoding="utf-8")
    try:
        with mock.patch.object(voice_check, "WAIVER_PATH", waiver_path):
            if stdin is not None:
                with mock.patch.object(sys, "stdin", io.StringIO(stdin)):
                    with redirect_stdout(buf):
                        code = voice_check.main(paths)
            else:
                with redirect_stdout(buf):
                    code = voice_check.main(paths)
    finally:
        if waivers is not None:
            waiver_path.unlink(missing_ok=True)
    return code, buf.getvalue()


class ExitCodeTests(unittest.TestCase):
    def test_clean_fixture_exits_zero(self):
        code, out = run([str(FIXTURES / "clean-post.md")], waivers=[])
        self.assertEqual(code, 0, out)
        self.assertIn("0 violation(s)", out)

    def test_dashed_fixture_exits_nonzero(self):
        code, out = run([str(FIXTURES / "dashed-post.md")], waivers=[])
        self.assertEqual(code, 1)
        self.assertIn("2 violation(s)", out)
        self.assertEqual(out.count("[em-dash]"), 2)

    def test_slop_fixture_flags_every_lexicon_term(self):
        code, out = run([str(FIXTURES / "slop-post.md")], waivers=[])
        self.assertEqual(code, 1)
        for rule in (
            "slop:in-a-world",
            "slop:delve",
            "slop:tapestry",
            "slop:testament",
            "slop:nestled",
        ):
            self.assertIn(rule, out)
        self.assertIn("5 violation(s)", out)

    def test_stdin_mode_gates_chrome_copy(self):
        """#756: the sitewide <title> is a Jetpack setting, so it arrives piped."""
        title = f"<title>AI Lands Inside Every Profession {EM_DASH} Kris Krug</title>"
        code, out = run(["-"], waivers=[], stdin=title)
        self.assertEqual(code, 1)
        self.assertIn("<stdin>:1:", out)
        code, _ = run(
            ["-"], waivers=[], stdin="<title>Kris Krug: AI Keynote Speaker</title>"
        )
        self.assertEqual(code, 0)


class CommentExclusionTests(unittest.TestCase):
    """The distinction that matters: a dash in a comment never reaches a reader."""

    def test_html_and_css_comments_are_not_flagged(self):
        code, out = run([str(FIXTURES / "commented-template.html")], waivers=[])
        self.assertEqual(code, 0, out)

    def test_php_docblock_and_line_comments_are_not_flagged(self):
        code, out = run([str(FIXTURES / "commented-pattern.php")], waivers=[])
        self.assertEqual(code, 1)
        self.assertIn("1 violation(s)", out)
        self.assertIn("aurora-photo-lede", out)

    def test_url_scheme_is_not_mistaken_for_a_php_line_comment(self):
        text = f"<p>See https://kriskrug.co/about/ for more {EM_DASH} it is worth it.</p>\n"
        self.assertEqual(len(voice_check.scan_text(text, ".php")), 1)

    def test_line_numbers_survive_multi_line_comment_blanking(self):
        text = f"<!--\n\n\n-->\n<p>a {EM_DASH} b</p>\n"
        hits = voice_check.scan_text(text, ".html")
        self.assertEqual([hit[1] for hit in hits], [5])

    def test_emdash_token_convention_is_not_a_violation(self):
        text = "| Original (dash = `{EMDASH}`) | Here is the story `{EMDASH}` the rest. |\n"
        self.assertEqual(voice_check.scan_text(text, ".md"), [])


class WaiverTests(unittest.TestCase):
    def test_waiver_suppresses_its_own_rule_only(self):
        waivers = [{"path": str(FIXTURES / "slop-post.md"), "rules": ["slop:delve"]}]
        code, out = run([str(FIXTURES / "slop-post.md")], waivers=waivers)
        self.assertEqual(code, 1)
        self.assertNotIn("slop:delve", out)
        self.assertIn("slop:tapestry", out)
        self.assertIn("1 waived", out)

    def test_wildcard_waiver_clears_the_file(self):
        waivers = [{"path": str(FIXTURES / "dashed-post.md"), "rules": ["*"]}]
        code, out = run([str(FIXTURES / "dashed-post.md")], waivers=waivers)
        self.assertEqual(code, 0, out)
        self.assertIn("2 waived", out)

    def test_stale_waiver_fails_so_the_baseline_ratchets_down(self):
        waivers = [
            {
                "path": str(FIXTURES / "clean-post.md"),
                "rules": ["em-dash"],
                "issue": "#751",
            }
        ]
        code, out = run([str(FIXTURES / "clean-post.md")], waivers=waivers)
        self.assertEqual(code, 1)
        self.assertIn("[stale-waiver]", out)
        self.assertIn("#751", out)

    def test_unscanned_waiver_is_not_reported_stale(self):
        """CI may scan a subset; a waiver for an untouched file must stay quiet."""
        waivers = [{"path": str(FIXTURES / "dashed-post.md"), "rules": ["*"]}]
        code, out = run([str(FIXTURES / "clean-post.md")], waivers=waivers)
        self.assertEqual(code, 0, out)
        self.assertNotIn("[stale-waiver]", out)


class RepoBaselineTests(unittest.TestCase):
    def test_committed_waiver_file_parses_and_documents_every_entry(self):
        data = json.loads(voice_check.WAIVER_PATH.read_text(encoding="utf-8"))
        self.assertTrue(data["waivers"])
        for entry in data["waivers"]:
            self.assertTrue(entry.get("issue"), entry)
            self.assertTrue(entry.get("reason"), entry)
            self.assertTrue(entry.get("rules"), entry)

    def test_repo_is_green_under_the_gate(self):
        """#747 acceptance: `make voice-check` passes on main with the baseline."""
        code, out = run([])
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
