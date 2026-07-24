"""ofw-mcp-server — MCP tool surface for your OWN OurFamilyWizard records.

Capability states are honest. A tool marked `scaffold` is NOT implemented and
returns {"status": "not_implemented", ...} rather than fabricating data. This is
deliberate: OFW records are legal evidence and must never be invented.
"""
from __future__ import annotations
from typing import Any
from .config import CONFIG

try:
    from mcp.server.fastmcp import FastMCP
except Exception as e:  # pragma: no cover
    raise SystemExit(
        "The 'mcp' package is required. Install with: pip install -e .\n"
        f"Import error: {e}"
    )

mcp = FastMCP("ofw-mcp-server")

# Tools whose logic is not yet written. Keep this list in sync with SPEC.md §5
# and the README capability table. NEVER return fabricated data from these.
_SCAFFOLD = {
    "ofw_ingest_export": "Parse OFW native PDF/.ics export into structured records.",
    "ofw_analyze_messages": "Analyze exported message history (wraps pohagan72 approach).",
    "calendar_pull": "OFW -> Google Calendar, deduped, no auto-delete.",
    "calendar_push": "Google -> OFW via user-added inbound subscription.",
    "sheet_sync_notes": "OFW <-> Google Sheet notes, tab-categorized.",
    "messages_digest": "Digest of new OFW messages since a timestamp.",
    "draft_reply_email": "Create a Gmail DRAFT reply (never sends).",
    "autodetect_scan": "Scan email/calendar/social for OFW-relevant activity.",
    "backfill_notes": "Retroactively sync all existing OFW notes to the Sheet.",
}


def _not_implemented(tool: str) -> dict[str, Any]:
    return {
        "status": "not_implemented",
        "tool": tool,
        "capability": _SCAFFOLD.get(tool, ""),
        "note": "Scaffold. See SPEC.md. This tool never returns fabricated data.",
    }


@mcp.tool()
def ofw_session_status() -> dict[str, Any]:
    """Report whether an authenticated OFW browser session appears to exist.

    Never types or stores a password. This scaffold reports how the check is
    made; the browser-session probe is wired in via the sync engine.
    """
    return {
        "status": "scaffold",
        "method": "Navigate to OFW app URL; if it redirects to the login path, "
                  "the session is not authenticated.",
        "base_url": CONFIG.ofw_base_url,
        "app_home_path": CONFIG.ofw_app_home_path,
        "login_path": CONFIG.ofw_login_path,
        "authenticated": None,
        "note": "No credentials are handled here. If not authenticated, the "
                "user logs in themselves in their browser.",
    }


@mcp.tool()
def calendar_sync_status() -> dict[str, Any]:
    """Return the persisted calendar-sync state (mode, direction, last run)."""
    import json, os
    path = CONFIG.sync_state_file
    if not os.path.exists(path):
        return {"status": "no_state", "state_file": path,
                "sync_mode_default": CONFIG.sync_mode}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return {"status": "ok", "state_file": path, "state": json.load(fh)}
    except Exception as e:
        return {"status": "error", "state_file": path, "error": str(e)}


# --- Scaffolded tools (declared, honest, not yet implemented) ---
@mcp.tool()
def ofw_ingest_export(path: str) -> dict[str, Any]:
    """Ingest an OFW native export (PDF/.ics) from a local file path."""
    return _not_implemented("ofw_ingest_export")


@mcp.tool()
def ofw_analyze_messages(path: str = "", question: str = "") -> dict[str, Any]:
    """Analyze the user's own exported OFW message history."""
    return _not_implemented("ofw_analyze_messages")


@mcp.tool()
def calendar_pull(mode: str = "dry_run") -> dict[str, Any]:
    """Sync OFW events into Google Calendar (dry_run by default)."""
    return _not_implemented("calendar_pull")


@mcp.tool()
def calendar_push(mode: str = "dry_run") -> dict[str, Any]:
    """Reflect Google Calendar changes back to OFW (user subscription)."""
    return _not_implemented("calendar_push")


@mcp.tool()
def sheet_sync_notes(mode: str = "dry_run", direction: str = "both") -> dict[str, Any]:
    """Dual-sync OFW notes with the tab-categorized Google Sheet."""
    return _not_implemented("sheet_sync_notes")


@mcp.tool()
def messages_digest(since: str = "") -> dict[str, Any]:
    """Digest of new OFW messages since an ISO timestamp."""
    return _not_implemented("messages_digest")


@mcp.tool()
def draft_reply_email(message_id: str, body: str) -> dict[str, Any]:
    """Create a Gmail DRAFT reply. Never sends."""
    return _not_implemented("draft_reply_email")


@mcp.tool()
def autodetect_scan(sources: list[str] | None = None, window: str = "7d") -> dict[str, Any]:
    """Scan email/calendar/social for OFW-relevant activity."""
    return _not_implemented("autodetect_scan")


@mcp.tool()
def backfill_notes(confirm: bool = False) -> dict[str, Any]:
    """Retroactively sync all existing OFW notes into the Google Sheet."""
    return _not_implemented("backfill_notes")


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
