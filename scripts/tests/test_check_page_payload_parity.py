"""Offline tests for scripts/check_page_payload_parity.py (#1222).

WPClient is replaced by an in-memory fake that fails the test on anything but
a GET. No network, no credentials, no .env files are read.
"""

import ast
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import common  # noqa: E402
import check_page_payload_parity as parity  # noqa: E402
import content_architecture_deploy as cad  # noqa: E402

PAYLOAD = "<!-- wp:html -->\n<section>marker-about</section>\n<!-- /wp:html -->\n"
COMMIT_DATE = "2026-11-11T09:00:00-08:00"


def live_page(raw, **over):
    page = {
        "id": 100,
        "slug": "about",
        "status": "publish",
        "modified": "2026-11-11T09:25:47",
        "content": {"raw": raw, "rendered": "<p>rendered</p>"},
    }
    page.update(over)
    return page


class GetOnlyWP:
    """Serves pages by ID; any non-GET call fails the test."""

    def __init__(self, pages=None, errors=None):
        self.pages = pages or {}
        self.errors = errors or {}
        self.gets = []

    def get(self, path, *, params=None):
        self.gets.append((path, params))
        page_id = int(path.rsplit("/", 1)[1])
        if page_id in self.errors:
            raise self.errors[page_id]
        return json.loads(json.dumps(self.pages[page_id]))

    def _write(self, *args, **kwargs):
        raise AssertionError(f"parity check attempted a non-GET call: {args!r}")

    post = put = patch = delete = _write

    def request(self, method, *args, **kwargs):
        if method.upper() != "GET":
            raise AssertionError(f"parity check attempted {method}")
        return self.get(*args, **kwargs)


class ParityTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write_map(self, pages, name="page-map.json", directory=None):
        directory = directory or self.root
        directory.mkdir(parents=True, exist_ok=True)
        page_map = {}
        for key, (page_id, slug, body) in pages.items():
            (directory / f"{key}.html").write_text(body, encoding="utf-8")
            page_map[key] = {
                "id": page_id,
                "slug": slug,
                "url": f"https://kriskrug.co/{slug}/",
                "payload": f"{key}.html",
                "markers": [f"marker-{key}"],
            }
        path = directory / name
        path.write_text(json.dumps(page_map), encoding="utf-8")
        return path

    def http_error(self, code, reason):
        err = HTTPError("https://example.test", code, reason, None, None)
        self.addCleanup(err.close)
        return err

    def run_main(self, argv, wp):
        out, err = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(parity.WPClient, "from_env", return_value=wp),
            mock.patch.object(parity, "payload_commit_date", return_value=COMMIT_DATE),
            redirect_stdout(out),
            redirect_stderr(err),
        ):
            code = parity.main(argv)
        return code, out.getvalue(), err.getvalue()


class CheckPageTests(ParityTestBase):
    def check(self, wp, page_id=100, slug="about"):
        map_path = self.write_map({"about": (page_id, slug, PAYLOAD)})
        page = json.loads(map_path.read_text())["about"]
        return parity.check_page(wp, map_path, "about", page, lambda _p: COMMIT_DATE)

    def test_match_reports_hash_and_dates(self):
        wp = GetOnlyWP({100: live_page(PAYLOAD.strip())})
        row = self.check(wp)
        self.assertEqual("match", row["verdict"])
        self.assertEqual(row["live_sha256"], row["payload_sha256"])
        self.assertEqual("2026-11-11T09:25:47", row["live_modified"])
        self.assertEqual(COMMIT_DATE, row["payload_last_commit"])
        self.assertEqual(
            [
                (
                    "pages/100",
                    {"context": "edit", "_fields": "id,slug,status,modified,content"},
                )
            ],
            wp.gets,
        )

    def test_drift_reports_byte_and_line_delta_and_first_line(self):
        live = (
            PAYLOAD.replace("marker-about", "marker-about newer live copy")
            + "<p>x</p>\n"
        )
        row = self.check(GetOnlyWP({100: live_page(live)}))
        self.assertEqual("DRIFT", row["verdict"])
        self.assertNotEqual(row["live_sha256"], row["payload_sha256"])
        self.assertEqual(2, row["first_diff_line"])
        self.assertEqual(-1, row["line_delta"])
        self.assertEqual(
            len(PAYLOAD.encode()) - len(cad.normalize_body(live).encode()),
            row["byte_delta"],
        )

    def test_wrong_slug_aborts_before_comparing(self):
        row = self.check(GetOnlyWP({100: live_page(PAYLOAD, slug="projects")}))
        self.assertEqual("ERROR", row["verdict"])
        self.assertIn("target check failed: slug", row["error"])
        self.assertNotIn("live_sha256", row)

    def test_non_publish_status_aborts_before_comparing(self):
        row = self.check(GetOnlyWP({100: live_page(PAYLOAD, status="draft")}))
        self.assertEqual("ERROR", row["verdict"])
        self.assertIn("status: expected 'publish'", row["error"])
        self.assertNotIn("live_sha256", row)

    def test_missing_raw_is_an_error_not_a_drift(self):
        page = live_page(PAYLOAD)
        page["content"] = {"rendered": "<p>public view</p>"}
        row = self.check(GetOnlyWP({100: page}))
        self.assertEqual("ERROR", row["verdict"])
        self.assertIn("content.raw", row["error"])


class MainTests(ParityTestBase):
    def two_page_map(self, about_live, work_live):
        map_path = self.write_map(
            {
                "about": (100, "about", PAYLOAD),
                "work": (200, "work", PAYLOAD.replace("about", "work")),
            }
        )
        wp = GetOnlyWP(
            {
                100: live_page(about_live),
                200: live_page(work_live, id=200, slug="work"),
            }
        )
        return map_path, wp

    def test_all_match_exits_zero_and_prints_no_content(self):
        map_path, wp = self.two_page_map(PAYLOAD, PAYLOAD.replace("about", "work"))
        code, out, err = self.run_main(["--map", str(map_path)], wp)
        self.assertEqual(0, code, err)
        self.assertIn("summary: expected=2 checked=2 match=2 drift=0 error=0", out)
        self.assertIn(
            "excluded: content/source-packs/content-architecture-2026/issue-480-retire-inline-css/",
            out,
        )
        self.assertNotIn("<section>", out)
        self.assertNotIn("rendered", out)

    def test_drift_exits_zero_without_flag_and_one_with_it(self):
        map_path, wp = self.two_page_map(PAYLOAD, "<p>edited live</p>")
        code, out, _ = self.run_main(["--map", str(map_path)], wp)
        self.assertEqual(0, code)
        self.assertIn("DRIFT bytes=", out)
        code, _, _ = self.run_main(["--map", str(map_path), "--fail-on-drift"], wp)
        self.assertEqual(1, code)

    def test_target_failure_exits_two(self):
        map_path = self.write_map({"about": (100, "about", PAYLOAD)})
        wp = GetOnlyWP({100: live_page(PAYLOAD, slug="other")})
        code, out, _ = self.run_main(["--map", str(map_path), "--fail-on-drift"], wp)
        self.assertEqual(2, code)
        self.assertIn("ERROR target check failed", out)

    def test_rejected_credentials_stop_after_first_page(self):
        map_path, wp = self.two_page_map(PAYLOAD, PAYLOAD)
        wp.errors[100] = self.http_error(401, "Unauthorized")
        code, out, _ = self.run_main(["--map", str(map_path)], wp)
        self.assertEqual(2, code)
        self.assertEqual(1, len(wp.gets))
        self.assertIn("ERROR HTTP 401 Unauthorized", out)
        self.assertIn("stopped after an authentication failure", out)

    def test_server_error_is_recorded_and_other_pages_still_checked(self):
        map_path, wp = self.two_page_map(PAYLOAD, PAYLOAD.replace("about", "work"))
        wp.errors[100] = self.http_error(503, "Unavailable")
        code, out, _ = self.run_main(["--map", str(map_path)], wp)
        self.assertEqual(2, code)
        self.assertEqual(2, len(wp.gets))
        self.assertIn("match=1 drift=0 error=1", out)

    def test_bare_json_prints_machine_output_only(self):
        map_path, wp = self.two_page_map(PAYLOAD, "<p>edited live</p>")
        code, out, _ = self.run_main(["--map", str(map_path), "--json"], wp)
        self.assertEqual(0, code)
        report = json.loads(out)
        self.assertEqual(
            ["match", "DRIFT"], [row["verdict"] for row in report["pages"]]
        )
        self.assertEqual(1, report["summary"]["drift"])
        self.assertIn("issue-480-retire-inline-css", report["excluded"][0])
        for row in report["pages"]:
            self.assertFalse({"content", "raw", "rendered"} & set(row))

    def test_json_path_writes_only_that_file(self):
        map_path, wp = self.two_page_map(PAYLOAD, PAYLOAD.replace("about", "work"))
        json_path = self.root / "out" / "parity.json"
        json_path.parent.mkdir()
        before = sorted(p.name for p in self.root.rglob("*"))
        code, out, _ = self.run_main(
            ["--map", str(map_path), "--json", str(json_path)], wp
        )
        self.assertEqual(0, code)
        self.assertIn("summary:", out)
        self.assertEqual(2, json.loads(json_path.read_text())["summary"]["match"])
        after = sorted(p.name for p in self.root.rglob("*"))
        self.assertEqual(sorted([*before, "parity.json"]), after)

    def test_missing_credentials_exit_two_with_one_line(self):
        env = {
            key: ""
            for key in (
                "WP_USER",
                "WP_APP_PASSWORD",
                "WP_API_USERNAME",
                "WP_API_PASSWORD",
            )
        }
        out, err = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(common, "DEFAULT_ENV_PATHS", ()),
            mock.patch.dict(os.environ, env),
            redirect_stdout(out),
            redirect_stderr(err),
        ):
            code = parity.main([])
        self.assertEqual(2, code)
        self.assertEqual("", out.getvalue())
        lines = err.getvalue().strip().splitlines()
        self.assertEqual(1, len(lines))
        self.assertIn("credentials", lines[0])
        self.assertIn("make varlock-run CMD='make payload-parity'", lines[0])
        self.assertNotIn("Traceback", err.getvalue())


class SupersededPackTests(ParityTestBase):
    def test_default_maps_are_the_canonical_pair_and_exclude_issue_480(self):
        self.assertEqual(
            {
                cad.PAYLOAD_DIR / "page-map.json",
                cad.PAYLOAD_DIR / "topic-hubs" / "page-map.json",
            },
            set(parity.DEFAULT_MAPS),
        )
        for path in parity.DEFAULT_MAPS:
            self.assertTrue(path.is_file(), path)
            self.assertFalse(parity.is_superseded(path), path)
            self.assertNotIn("issue-480-retire-inline-css", str(path))

    def test_issue_480_map_is_refused_under_either_name(self):
        for name in ("page-map.json", "page-map.superseded.json"):
            with self.subTest(name=name):
                path = parity.SUPERSEDED_PACK / name
                self.assertTrue(parity.is_superseded(path))
                with mock.patch.object(parity.WPClient, "from_env") as from_env:
                    err = io.StringIO()
                    with redirect_stdout(io.StringIO()), redirect_stderr(err):
                        code = parity.main(["--map", str(path)])
                self.assertEqual(2, code)
                from_env.assert_not_called()
                self.assertIn("excluded --map", err.getvalue())
                self.assertIn("no active page map", err.getvalue())

    def test_issue_480_map_is_skipped_next_to_an_active_map(self):
        map_path = self.write_map({"about": (100, "about", PAYLOAD)})
        wp = GetOnlyWP({100: live_page(PAYLOAD)})
        code, out, err = self.run_main(
            [
                "--map",
                str(parity.SUPERSEDED_PACK / "page-map.superseded.json"),
                "--map",
                str(map_path),
            ],
            wp,
        )
        self.assertEqual(0, code, err)
        self.assertIn("excluded --map", err)
        self.assertEqual(["pages/100"], [path for path, _ in wp.gets])


class ReadOnlySourceTests(unittest.TestCase):
    def test_script_source_has_no_write_call(self):
        source = (SCRIPTS / "check_page_payload_parity.py").read_text(encoding="utf-8")
        forbidden = {
            "post",
            "put",
            "patch",
            "delete",
            "request",
            "_exchange",
            "urlopen",
            "Request",
        }
        calls = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Call):
                func = node.func
                name = (
                    func.attr
                    if isinstance(func, ast.Attribute)
                    else getattr(func, "id", "")
                )
                calls.add(name)
        self.assertFalse(calls & forbidden, calls & forbidden)
        self.assertIn("get", calls)


class DeployDryRunParityTests(ParityTestBase):
    def run_deploy_dry_run(self, live_raw):
        payload = PAYLOAD.replace("<section>", '<section class="aurora-hero-2026">')
        map_path = self.write_map({"about": (100, "about", payload)})
        wp = GetOnlyWP({100: live_page(live_raw)})
        out = io.StringIO()
        argv = ["content_architecture_deploy.py", "--map", str(map_path)]
        with (
            mock.patch.object(cad.WPClient, "from_env", return_value=wp),
            mock.patch.object(sys, "argv", argv),
            redirect_stdout(out),
        ):
            cad.main()
        return payload, out.getvalue()

    def test_dry_run_prints_match_before_the_dry_run_line(self):
        payload, out = self.run_deploy_dry_run(
            PAYLOAD.replace("<section>", '<section class="aurora-hero-2026">')
        )
        self.assertIn("parity: about id=100 match sha256=", out)
        self.assertLess(
            out.index("parity: about"), out.index("[dry-run] planned pages=1")
        )
        self.assertNotIn(payload.strip(), out)

    def test_dry_run_prints_drift(self):
        _, out = self.run_deploy_dry_run("<p>newer live body</p>")
        self.assertIn("parity: about id=100 DRIFT bytes=", out)
        self.assertLess(
            out.index("parity: about"), out.index("[dry-run] planned pages=1")
        )

    def test_deploy_refuses_issue_480_map_under_either_name(self):
        for name in ("page-map.json", "page-map.superseded.json"):
            for extra in ([], ["--execute"], ["--restore", "--snapshot-dir", "x"]):
                with self.subTest(name=name, extra=extra):
                    argv = [
                        "content_architecture_deploy.py",
                        "--map",
                        str(cad.SUPERSEDED_PACK / name),
                        *extra,
                    ]
                    with (
                        mock.patch.object(cad.WPClient, "from_env") as from_env,
                        mock.patch.object(sys, "argv", argv),
                        self.assertRaisesRegex(SystemExit, "superseded"),
                    ):
                        cad.main()
                    from_env.assert_not_called()

    def test_deploy_and_parity_share_one_superseded_rule(self):
        self.assertIs(parity.is_superseded, cad.is_superseded)
        self.assertTrue(
            cad.is_superseded(cad.SUPERSEDED_PACK / "page-map.superseded.json")
        )
        self.assertFalse(cad.is_superseded(cad.PAGE_MAP_PATH))


if __name__ == "__main__":
    unittest.main()
