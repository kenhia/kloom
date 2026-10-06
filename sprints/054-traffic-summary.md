# 054 — Traffic summary for admins

## Goal

korg proposal 3571, covering korg 3570. Ken wants a traffic summary in the
style of GitHub's contribution graph, for admins only. It has a row per
subject and a square per frame, lit by how many readers opened it. It also
starts a visit counter now, so the data builds up while about eight readers
are getting started. kloom had no site admin before this sprint, so the
sprint adds the first one.

## Decisions

- **Premises held** (checked at start). `seen` (sprint 043's migration)
  holds one row per reader, subject and frame, backfilled. `ask_access` is
  the pattern for a flag kept in `reader.db`. deploying.md still said
  "There is no admin on the site". kloom is not in the cross-project plan
  index, and no grow branch was pending.
- **Ken's decisions (2026-10-05, on 3571 and 3570).**
  - Brightness counts distinct readers in five steps: 0, 1, 2, 3, 4+.
  - Admin only, and only `ken` for now.
  - The visit counter goes in now.
  - A visit is 5 s on a frame.
  - The `place` write stays at 800 ms. What's new's "opened" moves to the
    5 s visit.
- **One migration, the ninth**, holds both `frame_visit (reader, subject,
frame, day, n)` and `admin (reader, enabled)`. `day` is the UTC date of
  the visit's own timestamp. Both tables shipped together, so one entry
  keeps the schema history readable.
- **Admins live in their own module** (`src/lib/server/admins.ts`), as
  ask's allow-list lives in `ask-ledger.ts`. They are keyed by login, not
  username, so the same table works for the public site (`ken@kloom…`) and
  for kai (`ken@github`). It imports only `node:` modules, so `admin.mjs`
  loads it with plain Node.
- **The personal edition: the same page, behind the same check** (the
  choice 3570 left open). The alternative was to leave the page out of
  the full edition behind `$edition`. That would add a marker and a code
  path to save a page Ken may want on kai anyway. On kai the grid shows his
  reading alone once he makes `ken@github` an admin. This is recorded in
  deploying.md §The admin CLI.
- **The visit opens the frame; the place no longer does.** The store's
  `visit()` (the place) still starts a subject and counts as activity.
  `frameVisit()` adds to the visit count, writes `seen`, and starts the
  subject if nothing had. A reader who goes Home within the five seconds
  has not visited.
- **`traffic()` returns readers and visits together**, through one query
  over `seen` and `frame_visit`. The grid uses readers. Visits are there for
  the later toggle 3570 asked to leave room for.
- **Readers come from `seen`, as 3570 specified.** That table includes
  "Mark all as seen", so a reader who marked a subject seen counts toward
  every frame they marked. This is accepted: it was the specified source,
  and visits will be the stricter measure when the toggle comes.
- **Export leaves visits out.** They are telemetry, not something the
  reader made, so the export format stays at version 4.
- **The entry point is a link, not an icon.** _Traffic_ sits with the
  start screen's Welcome and User's Guide links, and it is drawn only when
  the page load says `admin: true`. An icon in the corner would have
  needed a new glyph for a link one person uses.
- **Keyboard: a roving tabindex per row.** About 780 squares as separate
  tab stops would make the page unusable from the keyboard. Each row is one
  stop. ←/→, Home and End move along the row, and ↑/↓ move between rows.
  The focused or hovered square is described in a sticky readout, which
  also covers touch, since hover never fires there.

## What shipped

- `src/lib/server/sqlite-reader-store.ts`: migration 9; `frameVisit`,
  `traffic`; `visit` no longer writes `seen`; `deleteReader` removes
  visits and reports `visits`.
- `engine/reader-data.ts`: the interface's `frameVisit` and `traffic`,
  `FrameTraffic`, `DeletedCounts.visits`, and the `PLACE_MS` (800) and
  `VISIT_MS` (5000) constants.
- `src/lib/server/admins.ts` and `admins()` / `useAdmins()` in
  `reader-store.ts`.
- `admin.mjs admin enable|disable|list`. `delete` also takes the admin
  flag. `just site-admin` runs it on the public site.
- `POST /api/reader/visit`.
- `engine/traffic.ts`: `levelOf`, `trafficRow` over `contentsOf`.
- `/admin/traffic`: the load (a 404 for anyone but an admin) and the page.
  `Plain` gains `wide`.
- The subject page: a 5 s visit timer beside the 800 ms place timer,
  cleared on a move or on Home. The load reports `admin`, and the start
  screen shows _Traffic_ to an admin.
- `just traffic-check` (`create-tools/traffic-check/traffic_check.mjs`).
- Docs:
  - design.md: §Reader data (the ninth migration, `POST visit`, a place no
    longer opening the frame), §What's new (the 5 s open), and a new
    §Traffic.
  - deploying.md: §The admin CLI (admins, both editions, `site-admin`; the
    "no admin on the site" line replaced, and `reader-ask` added to the
    command list, where it was missing).

## Verification

- Store tests:
  - the upsert across a UTC midnight;
  - a place not opening a frame, and a visit opening it;
  - distinct readers and visits per frame, including frames seen without a
    visit;
  - deletion removing a reader's visits;
  - visits left out of the export;
  - the migration from a schema-8 file, with history counted.
- Seven older migration tests now also drop the new tables, as sprint 046
  did for its own.
- `engine/traffic.test.ts`: levels 0/1/2/3/4+, every frame once, the main
  spine in order, and each trail's squares right after its anchor.
- Route tests: an admin gets the rows, with levels matching readers seeded
  at 1, 2, 3 and 5. A non-admin, no reader at all, and a disabled admin all
  get 404. `POST visit` refuses with no reader (401), an unknown frame
  (400) and an unknown subject (404). What's new: a place alone leaves a
  frame new, and a visit clears it.
- `admin.test.ts`: `admin enable` refuses an unknown username and accepts
  a username or a login. Then `list`, `disable` twice (the second fails),
  and `delete` taking the flag.
- `just traffic-check`, 32 checks against its own dev server over a seeded
  `.scratch` data directory:
  - no visit or open after 1.5 s, and one after 6 s;
  - a frame left after 1 s is not counted;
  - levels for readers seeded at 1/2/3/5, and every other square at 0;
  - every trail's squares together and right after its anchor;
  - ArrowRight moving within a row, with the readout naming the square;
  - no sideways scroll at 390px in dark and in light, each on its own
    background (screenshots checked by eye);
  - the start screen's link for an admin;
  - once the admin row is gone, no link and a 404.
- **Negative tests**, each planted, seen to fail, then reverted:
  - `VISIT_MS = 1000`: traffic-check fails 4 of 32 (the 1.5 s and the
    flick checks).
  - Uncapped levels: the unit test and the route's level test fail.
  - The admin check removed from the load: the 404 test fails.
- `just check` green.

## Repaired in passing

- deploying.md's admin CLI command list was missing `reader-ask` (sprint
  046 documented it only in §Ask). It is listed now, beside `admin`.

## Follow-ups

- Run `just site-admin enable ken` once this is deployed to the public
  site. The migration creates the table empty, so nobody is an admin until
  then. On kai: `just admin --data ~/.local/share/kloom/data admin enable
ken@github`.

## Deployed

- **kai, 2026-10-06 01:43Z**, by `just deploy` (the `.sprint-deploy`
  recipe), from merged `main` at `db6bc633` (PR #61). Its own checks
  passed: both doors read, the tailnet door refuses an anonymous write and
  keeps reader data from one, frame bodies come from the library, and pages
  are compressed. The library was rebuilt (`bc6011`).
- **The migration, live:** the service's `reader.db` is at schema 9.
  `frame_visit` and `admin` are new and empty, and the 34 `seen` rows from
  before are untouched.
- **This sprint's behavior, live, on the ssh door:**
  - `/admin/traffic` answered 404 to its reader (`ken@kai`, not an admin).
  - With `ken@kai` made an admin for the check, it answered 200 with the
    heading and all 11 subject rows. The flag was then taken away.
  - `POST /api/reader/visit` with an unknown subject answered 404.
- `ken@github` is now an admin on kai (`admin.mjs --data
~/.local/share/kloom/data admin enable ken@github`). That follows Ken's
  "only ken" decision, so the grid is his to open there.
- **Not yet on the public site.** `just publish-public`, then `just
site-admin enable ken`, are Ken's to run.
