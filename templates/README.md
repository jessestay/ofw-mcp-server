# Notes template

`ofw_notes_template.csv` is a **schema map** (Tab, Column, Description, Example)
for the tab-categorized Google Sheet the server syncs with.

## Import as a Google Sheet
1. Create a new Google Sheet (this becomes your `GSHEET_NOTES_ID`).
2. Create one tab per **Tab** value: `Messages`, `Calendar`, `Expenses`,
   `ActionItems`, `InfoBank`, `SyncLog`.
3. In each tab, put the **Column** values (for that tab) as the header row.
4. Run `sheet_sync_notes --align` on first use to reconcile the exact tab and
   column names against your existing tracker (e.g. an "Official Legal Issue and
   Evidence Tracker") before any data flows.

## Why a schema map instead of a filled sheet
This is a **legal record**. The template ships structure only — no invented
messages, amounts, or dates. Example values are illustrative and clearly marked;
real values come only from a real OFW read or export.
