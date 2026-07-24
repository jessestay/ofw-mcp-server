# Upstream evaluation tracker

We build on / evaluate existing open-source work rather than reinventing it.
Nothing here is treated as a dependency until its capabilities are verified.

## pohagan72 OurFamilyWizard Message Analyzer — VERIFIED (search-level)
- Repo: https://github.com/pohagan72/pohagan72-OurFamilyWizard-Message-Analyzer
- License: MIT.
- What it does: parses OFW message-log **PDF exports**, extracts messages
  organized by date, and analyzes content with an LLM (Google Gemini or Azure
  OpenAI).
- How we use it: model `ofw_analyze_messages` on its PDF-parse + analyze flow.
  TODO: read the repo in depth, confirm parser structure, decide vendor-in vs
  depend-on, verify license compatibility (MIT ✓).

## `kherryofw-client` (Python OFW wrapper) — UNVERIFIED
- Referenced for evaluation. A GitHub user `kherry` exists, but a specific
  OurFamilyWizard client library under that name was **not confirmed** via
  search as of this writing.
- Action: locate the exact repo/package, confirm it exists and what it does,
  before claiming or depending on any capability. Do **not** describe its
  features until verified. If it cannot be confirmed, drop the reference.

## OFW native export — VERIFIED via OFW support docs
- Static PDF/`.ics` on demand; no live feed; cannot export parenting schedule.
- Used for point-in-time ingest only. See OFW_NOTES.md.
