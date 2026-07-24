# Setup

## 1. Install

```bash
git clone https://github.com/jessestay/ofw-mcp-server
cd ofw-mcp-server
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

## 2. Configure your own keys

```bash
cp .env.example .env
```

Fill in `.env` with **your** values:

- **Google Calendar / Sheets / Gmail** — create an OAuth *Desktop app* client in
  the Google Cloud Console, enable the Calendar, Sheets, and Gmail APIs, download
  `credentials.json` into the repo root. First run opens a browser to authorize;
  a `token.json` is cached locally (gitignored).
- **`GCAL_TARGET_CALENDAR_ID`** — the id of your OFW-mirror parenting calendar.
- **`GSHEET_NOTES_ID`** — the id of your notes workbook (import the template in
  `templates/`).
- **Social** — optional; leave `SOCIAL_ENABLED=false` to skip.

Nothing in `.env` is committed. Every user runs against their own account.

## 3. OFW login

The server never logs in for you and never handles your password. Sign into OFW
in your own browser; the session persists. `ofw_session_status` reports whether
you're authenticated.

## 4. Register with your MCP client

Point your MCP client at the `ofw-mcp-server` command (stdio). Example config:

```json
{
  "mcpServers": {
    "ofw": { "command": "ofw-mcp-server" }
  }
}
```

## 5. Safety defaults

`SYNC_MODE=dry_run` by default: sync tools report a proposed diff for your
approval and write nothing until you set `live`. No tool ever deletes records or
sends email; email replies are created as **drafts** only.
