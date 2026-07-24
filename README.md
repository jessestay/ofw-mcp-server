# ofw-mcp-server

An open-source **Model Context Protocol (MCP) server** that gives an AI agent
safe, structured access to a co-parent's **own** OurFamilyWizard® (OFW) records —
so a self-represented (pro se) parent can keep their co-parenting communications,
calendar, and expense records mirrored, searchable, and analyzable without living
inside the OFW web app.

> **Status: early scaffold / specification (v0.0.1).**
> This repository currently contains the architecture spec, the MCP tool
> surface, configuration scaffolding, and a downloadable notes template.
> Tools are declared with honest capability states — a tool marked
> `scaffold` is *not yet implemented* and returns a clear "not implemented"
> error rather than fabricating data. See [`SPEC.md`](./SPEC.md) and the
> **Capability status** table below.

> ⚠️ **This handles a legal co-parenting record.** OFW messages and calendar
> entries are used as evidence in family-law matters. Accuracy is non-negotiable:
> this server never invents, paraphrases-as-fact, or "fills in" a message, event,
> expense, or date. If a value cannot be read from a real source, the tool says so.

## Who this is for

Parents who have their **own** OFW account and want to use an AI assistant to:

- Mirror their OFW parenting calendar into Google Calendar (both directions).
- Keep tab-categorized notes in a Google Sheet that stays in sync with OFW.
- Get digests of new OFW messages without logging in constantly.
- Draft (never auto-send) replies for the parent to review.
- Analyze their own exported message history for patterns and dates.

It is **not** a scraper-for-hire and stores **no other party's** credentials.
You configure it against your own account and your own API keys.

## Capability status (honest)

| Capability | Tool(s) | Status | Backed by |
|---|---|---|---|
| OFW auth / session | `ofw_session_status` | scaffold | Browser session (user logs in); **no password handling** |
| OFW native PDF/ICS export ingest | `ofw_ingest_export` | scaffold | OFW's own Export (static PDF/.ics) |
| Message-history analysis | `ofw_analyze_messages` | scaffold | Wraps/inspired by pohagan72 Message Analyzer |
| Python OFW client (evaluate) | — | to evaluate | `kherryofw-client` (existence/scope **unverified**) |
| Calendar dual-sync | `calendar_sync_status`, `calendar_pull`, `calendar_push` | design (a working browser-automation version exists outside this repo) | Google Calendar API |
| Google Sheet notes dual-sync | `sheet_sync_notes` | scaffold | Google Sheets API + template |
| New-message digest | `messages_digest` | scaffold | Session read |
| Draft-only email replies | `draft_reply_email` | scaffold | Gmail API (drafts only) |
| Auto-detection (email/calendar/social) | `autodetect_scan` | scaffold | Gmail + GCal + social sources |
| Retroactive notes backfill | `backfill_notes` | scaffold | Existing OFW notes → Sheet |

"design" = a proven implementation exists in the maintainer's private automation
and is being ported here. "scaffold" = interface defined, logic not yet written.
"to evaluate" = an upstream we intend to assess before depending on it.

## Upstream projects we build on / evaluate

- **pohagan72 OurFamilyWizard Message Analyzer** —
  <https://github.com/pohagan72/pohagan72-OurFamilyWizard-Message-Analyzer>
  (MIT). Parses OFW message-log **PDF exports**, extracts messages organized by
  date, and analyzes content with an LLM (Google Gemini or Azure OpenAI). We wrap
  its PDF-parsing approach for `ofw_analyze_messages`.
- **`kherryofw-client`** — a Python OFW wrapper referenced for evaluation. Its
  existence and exact capabilities are **not yet verified**; `docs/UPSTREAM.md`
  tracks the evaluation. We will not depend on it or claim its features until
  confirmed.
- **OFW native export** — OFW provides an on-demand static PDF/`.ics` export
  (it does **not** offer an outbound API or live iCal feed). See `docs/OFW_NOTES.md`.

## Quick start

See [`docs/SETUP.md`](./docs/SETUP.md). In short: copy `.env.example` to `.env`,
fill in your own Google / Gmail / (optional) social keys, `pip install -e .`,
then register the server with your MCP client.

## License

MIT — see [`LICENSE`](./LICENSE). Not affiliated with or endorsed by
OurFamilyWizard®. "OurFamilyWizard" is a trademark of its owner; used here only
to describe interoperability with a user's own account.
