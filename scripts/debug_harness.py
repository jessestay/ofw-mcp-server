#!/usr/bin/env python
"""OFW MCP debugging harness.

Exercises every tool and prints a health report — the same standard as the n8n
debug harness. The MACF Debugging agent runs this on a schedule; a red result
should be filed to the CTO as a concrete debug task.

Usage:  python scripts/debug_harness.py
Exit code 0 = healthy contract; non-zero = a guarantee was violated.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))


def main() -> int:
    try:
        from ofw_mcp import server as s
    except SystemExit as e:
        print(f"[FAIL] server import: {e} (is 'mcp' installed? pip install -e .)")
        return 2

    checks: list[tuple[str, bool, str]] = []

    # 1. session status must not claim auth it didn't verify
    ss = s.ofw_session_status()
    checks.append(("session_status honest", ss.get("authenticated") in (None, False), str(ss.get("authenticated"))))

    # 2. every scaffold tool returns not_implemented, no fabricated records
    scaffold_calls = {
        "ofw_ingest_export": lambda: s.ofw_ingest_export("x.pdf"),
        "ofw_analyze_messages": lambda: s.ofw_analyze_messages(),
        "calendar_pull": lambda: s.calendar_pull("dry_run"),
        "calendar_push": lambda: s.calendar_push("dry_run"),
        "sheet_sync_notes": lambda: s.sheet_sync_notes("dry_run"),
        "messages_digest": lambda: s.messages_digest(),
        "draft_reply_email": lambda: s.draft_reply_email("1", "x"),
        "autodetect_scan": lambda: s.autodetect_scan(),
        "backfill_notes": lambda: s.backfill_notes(False),
    }
    for name, call in scaffold_calls.items():
        out = call()
        ok = out.get("status") == "not_implemented" and not any(
            k in out for k in ("events", "messages", "rows", "expenses")
        )
        checks.append((f"{name} no-fabricate", ok, out.get("status", "?")))

    # 3. calendar_sync_status reads state safely
    cs = s.calendar_sync_status()
    checks.append(("calendar_sync_status reads", cs.get("status") in ("ok", "no_state", "error"), cs.get("status")))

    failed = [c for c in checks if not c[1]]
    print("OFW MCP debug harness")
    for name, ok, detail in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} ({detail})")
    print(f"summary: {len(checks) - len(failed)}/{len(checks)} passed")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
