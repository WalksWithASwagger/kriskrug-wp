import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import connector_config  # noqa: E402
import create_local_wp_draft  # noqa: E402


class VarlockPrecedenceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        root = Path(self.tempdir.name)
        self.local_env = root / ".env"
        self.fallback_env = root / "fallback.env"
        self.local_env.write_text(
            "NOTION_TOKEN=file-notion\n"
            "WP_USER=file-user\n"
            "WP_APP_PASSWORD=file-password\n"
            "WP_DEFAULT_AUTHOR_ID=1\n",
            encoding="utf-8",
        )
        self.fallback_env.write_text("WP_BASE_URL=https://fallback.example\n", encoding="utf-8")

    def test_connector_config_prefers_injected_process_values(self):
        injected = {
            "NOTION_TOKEN": "injected-notion",
            "WP_USER": "injected-user",
            "WP_APP_PASSWORD": "injected-password",
            "WP_DEFAULT_AUTHOR_ID": "18",
        }
        with mock.patch.object(connector_config, "LOCAL_ENV_PATH", self.local_env), \
                mock.patch.object(connector_config, "KKAI_ENV_PATH", self.fallback_env), \
                mock.patch.dict(os.environ, injected, clear=True):
            config = connector_config.load_config()

        self.assertEqual(config.notion_token, "injected-notion")
        self.assertEqual(config.wp_user, "injected-user")
        self.assertEqual(config.wp_app_password, "injected-password")
        self.assertEqual(config.wp_author_id, 18)

    def test_local_draft_config_prefers_injected_process_values(self):
        injected = {
            "WP_USER": "injected-user",
            "WP_APP_PASSWORD": "injected-password",
            "WP_DEFAULT_AUTHOR_ID": "18",
        }
        with mock.patch.object(create_local_wp_draft, "LOCAL_ENV_PATH", self.local_env), \
                mock.patch.object(create_local_wp_draft, "KKAI_ENV_PATH", self.fallback_env), \
                mock.patch.dict(os.environ, injected, clear=True):
            config = create_local_wp_draft.load_wp_config()

        self.assertEqual(config.user, "injected-user")
        self.assertEqual(config.app_password, "injected-password")
        self.assertEqual(config.author_id, 18)


if __name__ == "__main__":
    unittest.main()
