# ofw-mcp-server — Specification

Version 0.0.1 (scaffold). This document is the source of truth for what the
server does, how it accesses OurFamilyWizard (OFW), and the guardrails that keep
a legal co-parenting record accurate.

## 1. Problem & goals

A pro se parent's co-parenting record lives in OFW, a walled-garden web app with:

- **No public/outbound API, no live iCal feed, no webhooks.** OFW's only export
  is an **on-demand static** PDF (messages/reports) or `.ics` snapshot that does
  **not** update and cannot export the parenting schedule.
- **A single-page app (SPA) that is hostile to automation** — programmatic clicks
  on its login/app fields can kill the renderer. Reads via direct URL navigation
  plus page-text extraction are stable; automated *clicks* on OFW elements are not.

Goals of this server:

1. Give an AI agent a small, safe, well-documented tool surface over the user's
   **own** OFW data.
2. Keep OFW mirrored to the parent's Google Calendar and a Google Sheet notes
   tracker — **both directions**, deduped, never destructive.
3. Surface new messages as digests and draft (never send) replies.
4. Analyze the user's own exported message history.
5. Make it easy for **any** parent to run against their own account and keys.

## 2. Non-goals & hard rules

- **Never handle another party's credentials.** Only the user's own account.
- **Never type or store the user's OFW password.** Auth is via a browser session
  the user establishes themselves (see §4).
- **Never fabricate** a message, event, expense, amount, or date. Every value is
  traceable to a real read or a real export file. Absence is reported as absence.
- **Draft-only** for outbound email/replies. No auto-send of anything.
- **No auto-delete.** Sync removals are *flagged*, never silently deleted, because
  the record is legal evidence.

## 3. Architecture

```
                +-------------------- ofw-mcp-server (MCP) --------------------+
   MCP client   |  tools:                                                     |
  (agent/IDE) <-> ofw_session_status  ofw_ingest_export  ofw_analyze_messages |
                |  calendar_sync_status calendar_pull calendar_push           |
                |  sheet_sync_notes  messages_digest  draft_reply_email        |
                |  autodetect_scan   backfill_notes                            |
                +----+-------------------+------------------+-----------------+
                     |                   |                  |
             OFW browser session   Google APIs        Optional sources
             (user-established;    (Calendar,         (social auto-detect,
              read via URL+text;    Sheets, Gmail      email auto-detect)
              static PDF/ICS)       drafts)
```

- **Transport:** stdio MCP server (Python, FastMCP). Config from environment.
- **OFW adapter** (`ofw/`): read-only. Two ingestion modes:
  1. *Session read* — the user is logged into OFW in their browser; the adapter
     reads specific OFW URLs and extracts page text (no clicks on OFW elements).
  2. *Export ingest* — the user runs OFW's native Export; the adapter parses the
     resulting PDF/`.ics` file (wrapping the pohagan72 PDF approach).
- **Google adapter** (`google/`): Calendar + Sheets + Gmail (drafts only), OAuth
  user credentials.
- **Sync engine** (`sync/`): idempotent, deduped via a persisted `state.json`
  (event map, last-message signature, notes row map). Two-phase: `dry_run`
  (default) reports a diff for approval; `live` applies it.

## 4. OFW authentication model

The server **does not log in for you** and never sees your password.

1. User signs into OFW in their own browser (session cookie persists).
2. `ofw_session_status` reports authenticated / not (by reading an app URL and
   detecting redirect to `/app/login`).
3. If not authenticated, tools return a `needs_login` result with the single
   manual step — they do **not** attempt to type credentials.

This mirrors the reality that OFW's SPA resists automated login and that saved
password-manager autofill is the only safe fill path (browser-native, the value
never touches the agent).

## 5. Tool surface

| Tool | Input (summary) | Output | Notes |
|---|---|---|---|
| `ofw_session_status` | — | `{authenticated, url, checkedAt}` | Never types creds |
| `ofw_ingest_export` | `path` to PDF/.ics | parsed records | Static export ingest |
| `ofw_analyze_messages` | `path` or ingested set, `question?` | analysis + citations | Wraps pohagan72 PDF parse; LLM optional |
| `calendar_sync_status` | — | `{mode, direction, lastRunAt, counts}` | Reads `state.json` |
| `calendar_pull` | `mode=dry_run\|live` | event diff / applied | OFW → Google, deduped, no delete |
| `calendar_push` | `mode` | applied | Google → OFW (via user-added subscription) |
| `sheet_sync_notes` | `mode`, `direction` | row diff / applied | OFW ⇄ Google Sheet, tab-categorized |
| `messages_digest` | `since?` | digest of new messages | Read-only |
| `draft_reply_email` | `messageId`, `body` | Gmail **draft** id | Never sends |
| `autodetect_scan` | `sources[]`, `window` | detected items | Email + GCal + social |
| `backfill_notes` | `confirm=true` | rows written | Retroactive: all existing OFW notes → Sheet |

Every tool returns a `source` field (URL / file / API) so the agent can cite it.
Scaffolded tools return `{status:"not_implemented", capability:"..."}`.

## 6. Google Sheet notes template (tab-categorized)

Ships in [`templates/ofw_notes_template.csv`](./templates/ofw_notes_template.csv)
(one file per tab, or a workbook). Tabs mirror OFW's native sections so a row maps
1:1 to an OFW item:

- **Messages** — date, from, to, subject, thread_id, body_excerpt, ofw_url, first_viewed
- **Calendar** — start, end, title, ofw_key, google_event_id, synced_at, notes
- **Expenses** — date, description, amount, category, status, ofw_url, reconciled
- **ActionItems** — created, title, owner, due, status, ofw_url
- **InfoBank** — category, key, value, updated, ofw_url
- **SyncLog** — ts, tool, direction, mode, added, updated, flagged, source

> The exact tab/column names must be reconciled against the user's actual sheet
> on first run (`sheet_sync_notes --align`). Jesse's reference tracker is the
> "Stay // Official Legal Issue and Evidence Tracker" workbook; column alignment
> is a first-run step, not an assumption baked into code.

## 7. Auto-detection

`autodetect_scan` watches configured sources for OFW-relevant activity:
- **Gmail** — OFW notification emails, and (optional) the user's own sent mail.
- **Google Calendar** — the case calendar plus any calendars the user names.
- **Personal social** — optional, opt-in per channel; used only to correlate the
  user's *own* posts/timeline, never to surveil the other party.

Detected items become digest entries and/or proposed note rows (dry-run first).

## 8. Security & configuration

- All secrets via env / `.env` (gitignored). `.env.example` documents every key.
- Google auth via OAuth user credentials (`credentials.json` + token cache).
- `state.json` and any exported PDFs stay local; nothing is committed.
- Designed so **others can configure their own** keys without code changes.

## 9. Roadmap

v0.1 calendar dual-sync port · v0.2 sheet notes dual-sync + backfill ·
v0.3 message digest + draft replies · v0.4 export ingest + analysis ·
v0.5 auto-detection · v1.0 packaged + documented for public use.
