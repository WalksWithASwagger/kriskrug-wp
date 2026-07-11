from __future__ import annotations

import dataclasses
import os
import sys
from pathlib import Path

from dotenv import dotenv_values


REPO_ROOT = Path(__file__).resolve().parents[2]
DRAFTS_DIR = REPO_ROOT / "content" / "drafts"
NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
WP_BASE_URL_DEFAULT = "https://kriskrug.co"
WP_DEFAULT_AUTHOR_ID = 1
SCRIPT_DIR = Path(__file__).resolve().parent
LOCAL_ENV_PATH = SCRIPT_DIR / ".env"


def _kkai_env_path() -> Path:
    """Optional sibling-repo .env. Override with KKAI_ENV_PATH / NOTION_ENV_PATH."""
    for key in ("KKAI_ENV_PATH", "NOTION_ENV_PATH"):
        raw = os.environ.get(key)
        if raw:
            return Path(raw).expanduser()
    return Path.home() / "Code" / "notion-local" / "kk-ai-ecosystem" / ".env"


KKAI_ENV_PATH = _kkai_env_path()


@dataclasses.dataclass
class Config:
    notion_token: str
    wp_base_url: str
    wp_user: str | None
    wp_app_password: str | None
    wp_author_id: int

    @property
    def has_wp_credentials(self) -> bool:
        return bool(self.wp_user and self.wp_app_password)


def load_config() -> Config:
    local = dotenv_values(LOCAL_ENV_PATH) if LOCAL_ENV_PATH.exists() else {}
    fallback = dotenv_values(KKAI_ENV_PATH) if KKAI_ENV_PATH.exists() else {}

    def get(key: str, default: str | None = None) -> str | None:
        return local.get(key) or fallback.get(key) or os.environ.get(key) or default

    notion_token = get("NOTION_TOKEN")
    if not notion_token:
        sys.exit(f"NOTION_TOKEN not found. Add to {LOCAL_ENV_PATH} or {KKAI_ENV_PATH}.")
    return Config(
        notion_token=notion_token,
        wp_base_url=get("WP_BASE_URL", WP_BASE_URL_DEFAULT) or WP_BASE_URL_DEFAULT,
        wp_user=get("WP_USER"),
        wp_app_password=(get("WP_APP_PASSWORD") or "").replace(" ", "") or None,
        wp_author_id=int(get("WP_DEFAULT_AUTHOR_ID", str(WP_DEFAULT_AUTHOR_ID)) or WP_DEFAULT_AUTHOR_ID),
    )
