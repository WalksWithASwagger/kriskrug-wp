from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).parents[1] / "changelog_from_prs.py"
SPEC = importlib.util.spec_from_file_location("changelog_from_prs", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


DASH = "\N{EM DASH}"


def pr(number, title, merged, *paths):
    return {
        "number": number,
        "title": title,
        "mergedAt": merged,
        "files": [{"path": p} for p in paths],
    }


FIXTURE = [
    pr(1, "content: add a post", "2026-10-01T10:00:00Z", "content/drafts/a.md"),
    pr(
        2, "theme: tune the header", "2026-10-02T10:00:00Z", "theme/kk-aurora/style.css"
    ),
    pr(
        3,
        "fix: guard the slug lookup",
        "2026-10-03T10:00:00Z",
        "scripts/notion-to-wp/a.py",
    ),
    pr(
        4,
        "fix: update qs override",
        "2026-10-04T10:00:00Z",
        "package.json",
        "package-lock.json",
    ),
    pr(5, "docs: record the plan", "2026-10-05T10:00:00Z", "docs/current-state/a.md"),
    pr(
        6,
        "Redesign Writing",
        "2026-10-06T10:00:00Z",
        "theme/kk-aurora/a.php",
        "theme/kk-aurora/b.css",
        "scripts/tests/t.py",
    ),
    pr(
        7,
        "chore(deps-dev): bump foo from 1 to 2",
        "2026-10-07T10:00:00Z",
        "docs/x.md",
        "package.json",
    ),
    pr(
        8,
        "Events catalog: Meetup 33",
        "2026-10-08T10:00:00Z",
        "scripts/events_page/a.py",
    ),
    pr(9, "Keep it " + DASH + " and tidy", "2026-10-09T10:00:00Z"),
    pr(10, "Old one", "2026-09-01T10:00:00Z", "docs/a.md"),
]


def test_prefix_and_path_classification():
    areas = {p["number"]: MODULE.classify(p) for p in FIXTURE}
    assert areas[1] == "Content"
    assert areas[2] == "Theme"
    assert areas[3] == "Publisher and tooling"
    assert areas[4] == "CI and tests"
    assert areas[5] == "Docs and ops"
    assert areas[6] == "Theme"
    assert areas[7] == "CI and tests"
    assert areas[8] == "Content"
    assert areas[9] == "Docs and ops"


def test_clean_title_strips_prefix_and_dashes():
    assert MODULE.clean_title("fix: guard the lookup") == "Guard the lookup"
    assert MODULE.clean_title("Keep it " + DASH + " and tidy") == "Keep it - and tidy"
    assert MODULE.clean_title("Unknown: stays") == "Unknown: stays"


def test_render_orders_areas_and_newest_first():
    out = MODULE.render([p for p in FIXTURE if p["number"] in (1, 2, 3, 6)])
    assert (
        out.index("### Content")
        < out.index("### Theme")
        < out.index("### Publisher and tooling")
    )
    assert out.index("(#6)") < out.index("(#2)")
    assert "### Docs and ops" not in out


def test_main_filters_dates_from_stdin(capsys):
    with mock.patch.object(sys, "stdin", io.StringIO(json.dumps(FIXTURE))):
        MODULE.main(["--stdin", "--since", "2026-10-01", "--until", "2026-10-03"])
    out = capsys.readouterr().out
    assert "(#1)" in out and "(#3)" in out
    assert "(#10)" not in out and "(#4)" not in out
