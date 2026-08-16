"""Unit tests for the #747 voice gate.

Fixtures live in ``fixtures/voice_check/`` rather than inline strings so that the
em-dash cases are real files on disk, the same shape the gate sees in CI. They
sit outside ``content/drafts/`` and outside the theme, so they are deliberately
out of the gate's own scan scope and cannot trip it.
"""

import io
import hashlib
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import voice_check  # noqa: E402

FIXTURES = Path("scripts/tests/fixtures/voice_check")
EM_DASH = "\u2014"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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
        """#756: public readbacks can verify the theme-owned title source."""
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
        path = FIXTURES / "slop-post.md"
        waivers = [
            {
                "path": str(path),
                "sha256": digest(path),
                "rules": ["slop:delve"],
            }
        ]
        code, out = run([str(FIXTURES / "slop-post.md")], waivers=waivers)
        self.assertEqual(code, 1)
        self.assertNotIn("slop:delve", out)
        self.assertIn("slop:tapestry", out)
        self.assertIn("1 baseline-waived", out)

    def test_wildcard_waiver_clears_the_file(self):
        path = FIXTURES / "dashed-post.md"
        waivers = [
            {"path": str(path), "sha256": digest(path), "rules": ["*"]}
        ]
        code, out = run([str(FIXTURES / "dashed-post.md")], waivers=waivers)
        self.assertEqual(code, 0, out)
        self.assertIn("2 baseline-waived", out)

    def test_changed_file_cannot_reuse_an_old_baseline_waiver(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "post.md"
            path.write_text(f"Known baseline {EM_DASH} one hit.\n", encoding="utf-8")
            waivers = [
                {"path": str(path), "sha256": digest(path), "rules": ["em-dash"]}
            ]
            code, out = run([str(path)], waivers=waivers)
            self.assertEqual(code, 0, out)

            path.write_text(
                f"Known baseline {EM_DASH} one hit.\nNew copy {EM_DASH} regression.\n",
                encoding="utf-8",
            )
            code, out = run([str(path)], waivers=waivers)
            self.assertEqual(code, 1)
            self.assertIn("2 violation(s)", out)

    def test_removing_a_waived_violation_does_not_block_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "post.md"
            path.write_text(f"Old copy {EM_DASH} pending cleanup.\n", encoding="utf-8")
            waivers = [
                {"path": str(path), "sha256": digest(path), "rules": ["em-dash"]}
            ]
            path.write_text("Clean replacement copy.\n", encoding="utf-8")

            code, out = run([str(path)], waivers=waivers)

        self.assertEqual(code, 0, out)
        self.assertNotIn("stale-waiver", out)

    def test_unscanned_waiver_is_not_reported_stale(self):
        """CI may scan a subset; a waiver for an untouched file must stay quiet."""
        path = FIXTURES / "dashed-post.md"
        waivers = [
            {"path": str(path), "sha256": digest(path), "rules": ["*"]}
        ]
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
            self.assertEqual(len(entry.get("sha256", "")), 64, entry)

    def test_theme_title_source_is_in_default_scan(self):
        self.assertIn(
            Path("theme/kk-aurora/functions.php"), voice_check.default_targets()
        )

    def test_repo_is_green_under_the_gate(self):
        """#747 acceptance: `make voice-check` passes on main with the baseline."""
        code, out = run([])
        self.assertEqual(code, 0, out)


class WorkflowWiringTests(unittest.TestCase):
    def test_pull_request_workflow_has_changed_file_voice_job(self):
        workflow = (
            voice_check.REPO_ROOT / ".github/workflows/test-pr.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("has_voice", workflow)
        self.assertIn("voice-gate:", workflow)
        self.assertIn("needs.validate.outputs.has_voice == 'true'", workflow)


if __name__ == "__main__":
    unittest.main()
