import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEME = ROOT / "theme/kk-aurora"


def test_project_footer_lists_the_sky_smoked_back_once():
    footer = (THEME / "parts/footer.html").read_text(encoding="utf-8")

    assert footer.count('href="https://lightningstrike.org/"') == 1
    assert ">The Sky Smoked Back</a>" in footer


def first_match(pattern, path):
    match = re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE)
    assert match, f"{path.relative_to(ROOT)} has no release version"
    return match.group(1)


def test_aurora_release_version_is_consistent():
    version = first_match(r"^Version:\s*(\S+)$", THEME / "style.css")

    assert (
        first_match(
            r"define\('KK_AURORA_VERSION',\s*'([^']+)'\);", THEME / "functions.php"
        )
        == version
    )
    assert first_match(r"^= (\S+) =$", THEME / "readme.txt") == version
    assert first_match(r"^## (\d+\.\d+\.\d+)$", THEME / "CHANGELOG.md") == version
