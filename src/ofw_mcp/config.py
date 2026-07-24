"""Environment-based configuration. Users set their OWN values in .env."""
from __future__ import annotations
import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:  # dotenv optional at runtime
    pass


def _split(v: str | None) -> list[str]:
    return [x.strip() for x in (v or "").split(",") if x.strip()]


@dataclass(frozen=True)
class Config:
    ofw_base_url: str = os.getenv("OFW_BASE_URL", "https://ofw.ourfamilywizard.com")
    ofw_app_home_path: str = os.getenv("OFW_APP_HOME_PATH", "/app/home")
    ofw_login_path: str = os.getenv("OFW_LOGIN_PATH", "/app/login")

    google_credentials_file: str = os.getenv("GOOGLE_CREDENTIALS_FILE", "./credentials.json")
    google_token_file: str = os.getenv("GOOGLE_TOKEN_FILE", "./token.json")
    gcal_target_calendar_id: str = os.getenv("GCAL_TARGET_CALENDAR_ID", "")

    gsheet_notes_id: str = os.getenv("GSHEET_NOTES_ID", "")
    gmail_address: str = os.getenv("GMAIL_ADDRESS", "")

    social_enabled: bool = os.getenv("SOCIAL_ENABLED", "false").lower() == "true"
    sync_mode: str = os.getenv("SYNC_MODE", "dry_run")
    sync_state_file: str = os.getenv("SYNC_STATE_FILE", "./state.json")

    @property
    def gcal_watch_calendar_ids(self) -> list[str]:
        return _split(os.getenv("GCAL_WATCH_CALENDAR_IDS"))


CONFIG = Config()
