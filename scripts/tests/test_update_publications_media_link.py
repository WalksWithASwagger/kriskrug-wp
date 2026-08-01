from pathlib import Path
import importlib.util


SCRIPT = Path(__file__).parents[1] / "update_publications_media_link.py"
SPEC = importlib.util.spec_from_file_location("update_publications_media_link", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_build_updated_adds_one_reciprocal_link():
    before = f"<p>{MODULE.ANCHOR}</p>"

    after, already_applied = MODULE.build_updated(before)

    assert not already_applied
    assert after.count(MODULE.MEDIA_PATH) == 1
    assert after.count("Media Appearances") == 1


def test_build_updated_is_idempotent():
    before = f"<p>{MODULE.INSERTION}</p>"

    after, already_applied = MODULE.build_updated(before)

    assert already_applied
    assert after == before
