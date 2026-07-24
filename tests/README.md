# Tests & debugging harness

Owned by the MACF **Testing** and **Debugging** agents (same standard as the
n8n work). The server is **not considered deployed** until this suite is green
and `scripts/debug_harness.py` reports clean.

## Run

```bash
pip install -e ".[dev]"
pytest -q
python scripts/debug_harness.py
```

## What's here (baseline scaffold)

- `test_server_contract.py` — every tool in SPEC.md §5 exists and is callable;
  config loads with safe defaults; state read is crash-safe.
- `test_guardrails.py` — the legal-record safety contract: scaffolds return
  `not_implemented` (never fabricate), no fabricated records leak, session status
  never claims unverified auth, email is draft-only.
- `scripts/debug_harness.py` — runnable health report; non-zero exit on any
  violated guarantee.

## What the agents add next (per capability, as implemented)

- **auth/export**: session-detection unit tests; PDF/.ics export parser tests
  against sample exports (fixtures, no real PII committed).
- **calendar dual-sync**: dedupe, no-auto-delete, dry-run→live diff correctness.
- **sheet dual-sync**: tab/column alignment, idempotent row mapping, backfill.
- **digest / draft replies**: draft-only guarantee, correct threading.
- **auto-detection**: source filtering, own-activity-only scope.

Every behavioral test must preserve the guardrails in `test_guardrails.py`.
