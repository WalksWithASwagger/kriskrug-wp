"""Regression lock: WP payloads must not reintroduce pre-Aurora neon islands.

Issue #585. Publications already forbids these markers in
``test_publications_editorial_payload.py``. This module watches every
source-pack HTML payload so a later agent cannot republish cyan ``#00e5ff``
or hot ``#ff6a6a`` page skins.
"""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAYLOAD_ROOTS = (
    ROOT / "content" / "source-packs" / "keynotes-2026" / "wp-payloads",
    ROOT / "content" / "source-packs" / "content-architecture-2026" / "wp-payloads",
)
REMINT_TARGETS = (
    ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "wp-payloads"
    / "about.html",
    ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "wp-payloads"
    / "work.html",
    ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "wp-payloads"
    / "services.html",
    ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "wp-payloads"
    / "podcast-guesting-page-epk.html",
    ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "wp-payloads"
    / "responsible-ai-professional.html",
)

FORBIDDEN_SKIN_MARKERS = (
    "#00e5ff",
    "#ff6a6a",
    "rgba(0,229,255",
    "rgba(255,106,106",
    "--press-night",
)


def payload_html_files() -> list[Path]:
    files: list[Path] = []
    for root in PAYLOAD_ROOTS:
        files.extend(sorted(path for path in root.rglob("*.html") if path.is_file()))
    return files


class PayloadNeonIslandTests(unittest.TestCase):
    def test_payload_roots_exist(self):
        for root in PAYLOAD_ROOTS:
            self.assertTrue(root.is_dir(), f"missing payload root {root}")
        self.assertGreaterEqual(len(payload_html_files()), 15)

    def test_source_pack_payloads_forbid_dark_neon_markers(self):
        hits: list[str] = []
        for path in payload_html_files():
            lowered = path.read_text(encoding="utf-8").lower()
            found = [marker for marker in FORBIDDEN_SKIN_MARKERS if marker in lowered]
            if found:
                rel = path.relative_to(ROOT)
                hits.append(f"{rel}: {', '.join(found)}")
        self.assertEqual([], hits)

    def test_reminted_keynotes_payloads_inherit_aurora_paper(self):
        for path in REMINT_TARGETS:
            html = path.read_text(encoding="utf-8")
            lowered = html.lower()
            self.assertTrue(path.is_file(), path.name)
            self.assertIn("--aurora-ink", lowered)
            self.assertIn("--aurora-signal", lowered)
            self.assertIn("--aurora-paper", lowered)
            self.assertNotIn("#00e5ff", lowered)
            self.assertNotIn("#ff6a6a", lowered)


if __name__ == "__main__":
    unittest.main()
