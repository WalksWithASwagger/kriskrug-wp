from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


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
