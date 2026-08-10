from pathlib import Path
import importlib.util


SCRIPT = Path(__file__).parents[1] / "update_both_hands_power_cord.py"
SPEC = importlib.util.spec_from_file_location("update_both_hands_power_cord", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_build_updated_replaces_only_wrong_cbc_image_block():
    before = f"<p>before</p>\n{MODULE.OLD_IMAGE_BLOCK}\n<p>after</p>"

    after, already_applied = MODULE.build_updated(
        before,
        13000,
        "https://kriskrug.co/wp-content/uploads/2026/08/kris-krug-jason-dsouza-cbc-vancouver-2026-08-03.jpg",
    )

    assert not already_applied
    assert "Stephen Quinn" not in after
    assert '"id":13000' in after
    assert "wp-image-13000" in after
    assert MODULE.MEDIA_ALT in after
    assert after.startswith("<p>before</p>")
    assert after.endswith("<p>after</p>")


def test_build_updated_recognizes_new_state():
    current = MODULE.image_block(
        13000,
        "https://kriskrug.co/wp-content/uploads/2026/08/kris-krug-jason-dsouza-cbc-vancouver-2026-08-03.jpg",
    )

    after, already_applied = MODULE.build_updated(current, 13000, "ignored")

    assert already_applied
    assert after == current
