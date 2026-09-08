import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SNIPPET = ROOT / "fixes/issue-1002-xmlrpc-constrain.php"
CHECK = ROOT / "scripts/check_xmlrpc_reachability.sh"
PACKET = ROOT / "docs/current-state/XML-RPC-CONSTRAIN-DECISION-2026-09-08.md"
FIXES_README = ROOT / "fixes/README.md"
CURRENT_STATE_README = ROOT / "docs/current-state/README.md"


class Issue1002XmlrpcConstrainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snippet = SNIPPET.read_text(encoding="utf-8")
        cls.check = CHECK.read_text(encoding="utf-8")
        cls.packet = PACKET.read_text(encoding="utf-8")
        cls.fixes_readme = FIXES_README.read_text(encoding="utf-8")
        cls.behavior = cls._run_php_harness()

    @staticmethod
    def _run_php_harness():
        snippet_path = json.dumps(str(SNIPPET))
        harness = f"""<?php
function add_filter() {{
    return true;
}}

require {snippet_path};

echo json_encode(
    array(
        'true_becomes_false'  => false === kk_1002_disable_xmlrpc(true),
        'false_stays_false'   => false === kk_1002_disable_xmlrpc(false),
    ),
    JSON_THROW_ON_ERROR
);
"""
        result = subprocess.run(
            ["php"],
            input=harness,
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_php_syntax_and_filter_always_returns_false(self):
        result = subprocess.run(
            ["php", "-l", str(SNIPPET)],
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn("No syntax errors detected", result.stdout)
        self.assertTrue(self.behavior["true_becomes_false"])
        self.assertTrue(self.behavior["false_stays_false"])
        self.assertEqual(1, self.snippet.count("add_filter("))
        self.assertIn("add_filter( 'xmlrpc_enabled', 'kk_1002_disable_xmlrpc' );", self.snippet)

    def test_snippet_is_prep_only_and_prefers_host_deny(self):
        for expected in (
            "PREP ONLY",
            "Not deployed",
            "Pagely / WAF deny",
            "check_xmlrpc_reachability.sh",
            "Jetpack core is not a required XML-RPC client",
            "is_user_logged_in()",
            "Rollback",
        ):
            self.assertIn(expected, self.snippet)

        self.assertNotIn("is_user_logged_in();", self.snippet)
        self.assertNotRegex(self.snippet, r"(?i)system\.multicall")
        self.assertNotRegex(self.snippet, r"(?i)\bPOST\b")

    def test_check_script_is_get_head_only(self):
        self.assertTrue(CHECK.is_file())
        self.assertIn("GET and HEAD only", self.check)
        self.assertIn("-I", self.check)
        self.assertIn("-o /dev/null", self.check)
        self.assertIn("%{http_code}", self.check)
        self.assertNotRegex(self.check, r"(?i)system\.multicall")
        self.assertNotRegex(self.check, r"(?i)--data")
        self.assertNotRegex(self.check, r"(?i)-X\s+POST")
        self.assertNotRegex(self.check, r"(?i)curl[^\n]*\s-d\s")
        self.assertNotIn("listMethods", self.check)
        self.assertIn("No POST", self.check)

    def test_packet_cross_links_and_no_live_apply(self):
        for expected in (
            "issue #1002",
            "#767",
            "#709",
            "live disable not authorized",
            "scripts/check_xmlrpc_reachability.sh",
            "fixes/issue-1002-xmlrpc-constrain.php",
            "Pagely / WAF deny",
        ):
            self.assertIn(expected, self.packet)

        self.assertNotRegex(self.packet, r"(?i)system\.multicall")
        self.assertIn("issue-1002-xmlrpc-constrain.php", self.fixes_readme)
        self.assertIn("Not live; prep only", self.fixes_readme)
        self.assertIn("XML-RPC-CONSTRAIN-DECISION-2026-09-08.md", CURRENT_STATE_README.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
