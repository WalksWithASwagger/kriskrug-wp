from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEME = ROOT / "theme/kk-aurora"


def test_project_footer_lists_the_sky_smoked_back_once():
    footer = (THEME / "parts/footer.html").read_text(encoding="utf-8")

    assert footer.count('href="https://lightningstrike.org/"') == 1
    assert '>The Sky Smoked Back</a>' in footer


def test_aurora_release_version_is_consistent():
    style = (THEME / "style.css").read_text(encoding="utf-8")
    functions = (THEME / "functions.php").read_text(encoding="utf-8")

    assert "Version: 1.6.12" in style
    assert "define('KK_AURORA_VERSION', '1.6.12');" in functions
