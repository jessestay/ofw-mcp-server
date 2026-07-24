"""Guardrail tests — the legal-record safety contract.

A co-parenting record is evidence. These tests assert the server NEVER
fabricates and NEVER performs destructive/send actions from a scaffold. As each
capability is implemented, its real behavior must keep these guarantees
(dry-run default, draft-only email, no auto-delete, cited sources).
"""
import importlib
import pytest

server = importlib.import_module("ofw_mcp.server")

# (tool_callable, kwargs) for every scaffolded tool
SCAFFOLD_CALLS = [
    (server.ofw_ingest_export, {"path": "sample.pdf"}),
    (server.ofw_analyze_messages, {}),
    (server.calendar_pull, {"mode": "dry_run"}),
    (server.calendar_push, {"mode": "dry_run"}),
    (server.sheet_sync_notes, {"mode": "dry_run"}),
    (server.messages_digest, {}),
    (server.draft_reply_email, {"message_id": "1", "body": "x"}),
    (server.autodetect_scan, {}),
    (server.backfill_notes, {"confirm": False}),
]


@pytest.mark.parametrize("fn,kwargs", SCAFFOLD_CALLS)
def test_scaffold_never_fabricates(fn, kwargs):
    """A not-yet-implemented tool returns an honest status, never fake data."""
    out = fn(**kwargs)
    assert isinstance(out, dict)
    assert out.get("status") == "not_implemented"
    # must not smuggle any invented records back
    for leak in ("events", "messages", "rows", "expenses"):
        assert leak not in out


def test_session_status_never_reports_authenticated_without_a_read():
    out = server.ofw_session_status()
    # scaffold cannot claim an authenticated session it did not verify
    assert out.get("authenticated") in (None, False)


def test_draft_reply_is_draft_only_by_contract():
    """Draft tool must never expose a 'send' path."""
    out = server.draft_reply_email(message_id="1", body="hello")
    assert "sent" not in out
    assert out.get("status") == "not_implemented"
