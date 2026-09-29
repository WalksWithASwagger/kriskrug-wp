"""Names-only checks that notion-to-wp is wired through Varlock."""

from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECT_IMPORT = (
    "# @import(~/.agents/env/values/.env.kriskrug-wp.local, allowMissing=true)"
)
PROJECT_PICK_IMPORT = "# @import(~/.agents/env/values/.env.kriskrug-wp.local, pick=["
SHARED_PICK_IMPORT = (
    "# @import(~/.agents/env/values/.env.shared.local, pick=["
)
CONNECTOR_KEYS = (
    "WP_USER",
    "WP_APP_PASSWORD",
    "WP_API_USERNAME",
    "WP_API_PASSWORD",
    "WP_BASE_URL",
    "WP_DEFAULT_AUTHOR_ID",
    "WP_AUTH_MODE",
    "NOTION_TOKEN",
)


def _read(relative: str) -> str:
    return (REPO_ROOT / relative).read_text(encoding="utf-8")


class VarlockContractTests(unittest.TestCase):
    def test_root_schema_imports_project_values_without_pick_list(self):
        schema = _read(".env.schema")
        self.assertIn(PROJECT_IMPORT, schema)
        self.assertNotIn(PROJECT_PICK_IMPORT, schema)
        self.assertIn(SHARED_PICK_IMPORT, schema)
        for name in CONNECTOR_KEYS:
            self.assertIn(f"{name}=", schema)

    def test_nested_schema_imports_the_same_project_values_file(self):
        schema = _read("scripts/notion-to-wp/.env.schema")
        self.assertIn(PROJECT_IMPORT, schema)
        self.assertNotIn(PROJECT_PICK_IMPORT, schema)
        self.assertIn(SHARED_PICK_IMPORT, schema)
        for name in CONNECTOR_KEYS:
            self.assertIn(f"{name}=", schema)

    def test_draft_queue_audit_target_injects_through_varlock(self):
        makefile = _read("Makefile")
        self.assertIn(
            "$(VARLOCK) run --inject vars -- "
            "scripts/notion-to-wp/.venv/bin/python "
            "scripts/notion-to-wp/draft_queue_audit.py",
            makefile,
        )
        self.assertIn(
            "python3 scripts/notion-to-wp/draft_queue_audit.py --local-only",
            makefile,
        )

    def test_readme_secret_commands_go_through_varlock(self):
        readme = _read("scripts/notion-to-wp/README.md")
        self.assertIn("varlock run --inject vars -- python scripts/notion-to-wp/kk_notion_to_wp.py", readme)
        self.assertIn(
            "varlock run --inject vars -- scripts/notion-to-wp/.venv/bin/python "
            "scripts/notion-to-wp/create_local_wp_draft.py",
            readme,
        )
        self.assertIn(
            "varlock run --inject vars -- scripts/notion-to-wp/.venv/bin/python "
            "scripts/notion-to-wp/draft_queue_audit.py",
            readme,
        )
        self.assertNotIn("cp scripts/notion-to-wp/.env.example scripts/notion-to-wp/.env", readme)
        self.assertIn("unittest discover scripts/notion-to-wp/tests", readme)
        self.assertNotIn("varlock run --inject vars -- python -m unittest", readme)


if __name__ == "__main__":
    unittest.main()
