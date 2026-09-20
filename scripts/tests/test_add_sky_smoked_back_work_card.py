from __future__ import annotations

import argparse
import importlib.util
import json
import stat
import sys
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "add_sky_smoked_back_work_card.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("add_sky_smoked_back_work_card", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def current_work_body() -> str:
    return f"""
<article class="aurora-media-card">
  <a href="https://darkcrystal.app/" aria-label="Explore Dark Crystal">Dark Crystal</a>
</article>
{MODULE.PHOTOGRAPHY_CARD_ANCHOR}
"""


def fake_page(raw: str) -> dict:
    return {
        "id": MODULE.PAGE_ID,
        "slug": MODULE.PAGE_SLUG,
        "status": "publish",
        "title": {"raw": MODULE.PAGE_TITLE},
        "content": {"raw": raw},
        "modified": "2026-09-20T10:00:00",
        "modified_gmt": "2026-09-20T18:00:00",
        "link": "https://kriskrug.co/work/",
    }


class FakeWP:
    def __init__(self, raw: str, *, changed_fresh_raw: str | None = None, snapshot_dir=None):
        self.raw = raw
        self.changed_fresh_raw = changed_fresh_raw
        self.snapshot_dir = snapshot_dir
        self.get_calls = 0
        self.posts = []

    def get(self, _path, *, params=None):
        self.get_calls += 1
        if self.get_calls == 2 and self.changed_fresh_raw is not None:
            return fake_page(self.changed_fresh_raw)
        return fake_page(self.raw)

    def post(self, _path, payload):
        if self.snapshot_dir is not None:
            assert list(self.snapshot_dir.glob("page-2672-before-project-card-*.json"))
        self.posts.append(payload)
        self.raw = payload["content"]
        return fake_page(self.raw)


def test_build_updated_inserts_one_card_before_photography():
    before = current_work_body()

    after, already_applied = MODULE.build_updated(before)

    assert not already_applied
    assert after.count(MODULE.PROJECT_HREF) == 1
    assert after.count("The Sky Smoked Back") == 3
    assert after.index(MODULE.PROJECT_HREF) < after.index(MODULE.PHOTOGRAPHY_CARD_ANCHOR)
    assert "https://darkcrystal.app/" in after
    assert MODULE.remove_project_card(after) == before


def test_build_updated_is_idempotent():
    once, _ = MODULE.build_updated(current_work_body())

    twice, already_applied = MODULE.build_updated(once)

    assert already_applied
    assert twice == once


def test_build_updated_rejects_missing_or_ambiguous_anchor():
    for raw in ("<p>missing</p>", current_work_body() * 2):
        try:
            MODULE.build_updated(raw)
        except SystemExit as exc:
            assert "expected one Photography card anchor" in str(exc)
        else:
            raise AssertionError("unsafe body should abort")


def test_apply_snapshots_before_write_and_preserves_unrelated_content(tmp_path):
    before = current_work_body()
    fake = FakeWP(before, snapshot_dir=tmp_path)
    args = argparse.Namespace(apply=True, restore=None, snapshot_dir=tmp_path)

    with (
        mock.patch.object(MODULE, "parse_args", return_value=args),
        mock.patch.object(MODULE.WPClient, "from_env", return_value=fake),
        mock.patch.object(MODULE, "verify_public", return_value="https://kriskrug.co/work/?cb=test"),
    ):
        assert MODULE.main() == 0

    assert len(fake.posts) == 1
    assert MODULE.remove_project_card(fake.raw) == before
    snapshot = next(tmp_path.glob("page-2672-before-project-card-*.json"))
    assert json.loads(snapshot.read_text(encoding="utf-8"))["content"]["raw"] == before
    assert stat.S_IMODE(snapshot.stat().st_mode) == 0o600
    assert stat.S_IMODE((tmp_path / "rollback-manifest.json").stat().st_mode) == 0o600


def test_apply_aborts_if_the_page_changes_after_preflight(tmp_path):
    before = current_work_body()
    fake = FakeWP(before, changed_fresh_raw=before + "<!-- concurrent edit -->")
    args = argparse.Namespace(apply=True, restore=None, snapshot_dir=tmp_path)

    with (
        mock.patch.object(MODULE, "parse_args", return_value=args),
        mock.patch.object(MODULE.WPClient, "from_env", return_value=fake),
    ):
        try:
            MODULE.main()
        except SystemExit as exc:
            assert "changed after preflight" in str(exc)
        else:
            raise AssertionError("concurrent content change should abort")

    assert fake.posts == []
    assert not tmp_path.exists() or not any(tmp_path.iterdir())
