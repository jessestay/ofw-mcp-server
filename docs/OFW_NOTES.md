# OFW access — what is and isn't possible (field notes)

These constraints drive the architecture. They are based on OFW's own support
docs and hands-on testing.

## No API / no live feed
- OFW has **no public/outbound API**, no webhooks, and no live iCal feed of your
  own data.
- OFW's **Export** produces a **static** snapshot (PDF for messages/reports, or
  an `.ics`) that does **not** update, and it **cannot** export the parenting
  schedule. So it is not a usable live feed — only a point-in-time ingest.
- OFW **Calendar Subscriptions** are **inbound only**: OFW can subscribe to an
  external calendar's iCal URL, but does not expose an outbound feed. This is the
  mechanism used for the reverse (Google → OFW) leg.

## The SPA resists automation
- Programmatic clicks on OFW's login/app fields can kill the page renderer
  (observed `RESULT_CODE_KILLED`). **Reading** via direct URL navigation + page
  text extraction is stable; automated **clicks** on OFW elements are not.
- Therefore the OFW adapter is **read-only via URLs**, and login is done by the
  user in their browser (password-manager autofill is the only safe fill path,
  and the value never reaches the agent).

## Consequences for this server
- Calendar/message reads: navigate to specific OFW URLs, extract text, parse.
- Never click OFW page elements from automation.
- Never store or type the OFW password.
- Prefer the user's native browser session; fall back to static export ingest.
