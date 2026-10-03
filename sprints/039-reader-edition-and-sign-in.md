# 039 — The reader edition: a stripped public build, invite-only sign-in, and the Welcome page

## Goal

korg proposal 3505, covering 3500, 3501 and 3502. This is the first of
three slices of program korg 3508, the public reader site at
`kloom.kenhiatt.us` on Fly.io. The plan is in brainstorm 3458 (comment
3378), and Ken's decisions of 2026-10-02 are in the work items:

- every page needs sign-in
- readers have display names
- notes are private per reader
- Ken's parents share one login, `J-n-K`
- the welcome link lands on a Welcome and How-To page that says plainly
  what Agent review does

This slice is everything testable on kai with no Fly. Packaging and the
first publish are 3506; the notes' return trip is 3507. The sprint ran as a
karc leg, overseen.

## Premise, checked at start

- **Holds.** The code anchors in the proposal are where it says:
  - `reader.ts` has the doors and `readerOf`
  - `serve.js` marks the doors
  - `hooks.server.ts` has init and handle
  - `sqlite-reader-store.ts` has `node:sqlite` with numbered migrations
- **No native dependencies.** `node:crypto` has scrypt, so sign-in adds no
  npm dependency. None was added.
- **Nothing pending.** No grown content was waiting (`just grow-pending`),
  and kloom is not in the cross-project plan index.
- **The overseer's notes** (comment 3382) were read first and followed:
  - check by category
  - link About rather than duplicate it
  - write for a shared login
  - quote the Welcome copy in the wrap-up
  - leave the kai service alone unless shared paths changed its behaviour
    (they did; see Deploy)

## What shipped

### The reader edition (3500)

- **An edition is a build.** `KLOOM_EDITION=reader` at build time does three
  things:
  - It points a new alias, `$edition`, at `src/lib/edition/reader/` rather
    than `src/lib/edition/full/`.
  - It defines `__KLOOM_EDITION__`.
  - It builds into `build-reader/`, so the full build in `build/` is never
    replaced.
- **What moved behind `$edition`:**
  - The ask, grow, keep and kept-answer route handlers, now in
    `src/lib/edition/full/`. In the reader edition they are one shared 404
    (`src/lib/edition/absent.ts`).
  - The hooks: the full edition's doors, content sync, grow queues and kept
    migration, or the reader's session hooks.
  - What the page offers the AI pane.
  - Sign-in, the welcome link and sign-out, which are 404s in the full
    edition.
- **Dropped by `__KLOOM_EDITION__`, so the bundler removes it:**
  - `library()` building the content.db, in `subject.ts`
  - the AI pane, in `Shell.svelte`
  - the Q&A section, in `Narrative.svelte`
  - the page's kept-answer calls and model settings
- **`serve.js`'s third mode.** `KLOOM_EDITION=reader node serve.js` loads
  `build-reader/` and opens one listener on `0.0.0.0:$PORT` (8080) with no
  door marks. Any mark a client sends is dropped.
- **Start-up** only opens the library (`KLOOM_CONTENT_DB`, read-only) and
  `reader.db`. Media come from `KLOOM_MEDIA_DIR`.
- **`just reader-gate`, in `just check`,** builds the reader edition (about
  3 s) and fails if it finds any of these:
  - a marker from an ask, grow, keep or editor-only module (15 markers in
    four categories, plus client markers for the AI pane's requests)
  - any import of `node:child_process`

  A marker no longer in its source fails the gate too.

  **Negative-tested four ways**, each exiting 1:
  - the full build, run as if it were the reader's: every category fired
  - a planted import of `claudeArgs` into the reader hooks
  - a planted `node:child_process` import
  - a marker renamed in the gate

  Each plant was removed, and the gate passed again.

### Sign-in (3501)

- **Accounts.** `src/lib/server/accounts.ts`, loadable by plain Node, holds
  the accounts over `reader.db`. They arrive as migration 5: `account`,
  `session` and `invite` tables. Session ids and invite tokens are stored
  as their sha256 only.
- **Logins.** Usernames are case-insensitive and stored lower-case. Logins
  are `<username>@kloom.kenhiatt.us` (or `$KLOOM_LOGIN_DOMAIN`).
- **Welcome links** work once and expire after 7 days. Opening one only
  shows the form, so a message app's preview does not use it up.
- **Passwords** are scrypt, at least 8 characters.
- **Sessions** last a year and slide, moving forward at most once a day.
- **Backoff** is in memory, per username (5) and per address (20,
  `Fly-Client-IP` first): 30 s, doubling to 15 minutes.
- **Hardening.** Every response carries `X-Robots-Tag: noindex`, and
  `robots.txt` disallows everything. The reader edition's CSP is set by
  `kit.csp`, and the origin check stays on.
- **The admin CLI.** `admin.mjs` is plain Node 24 and goes through the
  accounts and the reader store, never around them. Its commands are `add`,
  `invite` (which adds when given a display name, and doubles as reset),
  `disable`, `enable`, `list` and `delete --yes`. Delete removes the
  reader's data through a new `ReaderStore.deleteReader`.
- **Pages.** `/signin`, `/welcome/<token>`, and sign-out as a plain form on
  the start screen.
- **Recipes:** `just build-reader`, `just serve-reader`, `just admin`.

### The Welcome and How-To page (3502)

`/welcome` is one page, in both editions. It is where a welcome link lands,
and the start screen links to it from under Begin. Its copy is quoted in
full in the wrap-up handoff on korg 3505, for Ken's review. The note
editor's "Agent review" hint now says the same thing at the box, in the
reader edition: "Sends this note to Ken and the agents he works with, who
read it and may answer it here."

## Decisions

- **The disclaimer is linked, not moved** (3502's open question). About
  keeps "A note on accuracy", and the Welcome page points to it.
- **A reset voids the password too,** not only sessions and links. Then the
  new link is unambiguously the one way in. The cost: a link minted by
  mistake signs the reader out until they use it.
- **A disabled reader's link does not work.** `invite` refuses until
  `enable`.
- **The reader edition's start-screen line** is "A timeline you can read
  and annotate". The full edition keeps "…read, question and grow".
- **With no AI pane the shell is two panes,** Narrative and Notes as tabs,
  with no Layout setting.
- **The edition is chosen by which build runs.** `serve.js` takes
  `KLOOM_EDITION` at run time and loads that edition's own directory. A full
  build therefore can never be opened on the public listener.
- **CSP only in the reader edition,** so the kai edition is unchanged.
- **Reads ask the library, not the files** (a change in both editions):
  - The media route serves only a file the library lists for that frame,
    read from `KLOOM_MEDIA_DIR` (by default the subjects).
  - A place, bookmark or note must name a frame the library has.
  - `/` lists subjects from the library.

  The reader edition has no subjects directory, and on kai these are the
  same set.

## Verified

- **`just check` is green:** svelte-check, lint, 1370 tests and the reader
  gate. New tests:
  - **accounts.** A link works once. A link runs out after 7 days. A reset
    ends sessions and voids the password. A disabled reader is refused
    every way in. Sessions slide. Delete goes through the store.
  - **rate limit.**
  - **reader hooks and routes.** An anonymous page is redirected to sign
    in. Anonymous API reads are refused. Sign-in and welcome links are
    open. Door marks are ignored. The four agent routes return 404. Sign-in
    backs off at 429 after five. A welcome link lands on `/welcome`.
  - **the page with no AI pane, and the start screen's links.**
  - **the Welcome page's promises.**
  - **a schema-4 `reader.db` moved forward.**
- **The reader edition, run on kai and driven with curl and headless
  Chromium:**
  - An anonymous `/` redirects 303 to `/signin`. An invite link greets "Hi
    Joel and Kathy", works once, and lands on `/welcome` signed in.
  - Ask, grow and kept answers return 404 when signed in. A bookmark is
    stored under `j-n-k@kloom.kenhiatt.us`.
  - A cross-origin form post is refused 403.
  - Sign-out ends one session, and a disabled reader is sent to sign in.
  - The page hydrates under the CSP with no console errors. The spine
    moves, the tabs are Narrative and Notes, there is no AI pane, and the
    map opens.
  - **Keyboard only:** sign in, then Tab to the Welcome link and to Sign
    out, and Enter on each.
- **The full edition, built and run on spare ports (4990/4991):**
  - Every check `just verify` makes gave the same results as before.
  - The new routes return 404 there, and `/welcome` returns 200.
  - The dev server serves.

## Repaired in passing

- **`sprints/planning/roadmap.md`** listed sprints only to 034. It now has
  035–038 from their records, beside 039. Proven by the records it links.
- **`reader-store.test.ts`'s schema-3 fixture** rewound only the column
  that schema 4 added. It now drops the tables that schema 5 adds too, so it
  stays a file from schema 3.

## Deploy owed at ship

The shared paths changed kai's behaviour, though only slightly: media are
checked against the library, and records against its frames. The ship
therefore runs `just deploy` on kai and `just verify`, per the overseer's
note. The kai edition is otherwise unchanged.

## Follow-ups

None filed. What this slice leaves to 3506 is already that item's scope:

- the Dockerfile copying `build-reader/`, plus `admin.mjs` with
  `src/lib/server/{accounts,sqlite-reader-store}.ts`
- `ORIGIN`, `KLOOM_CONTENT_DB`, `KLOOM_MEDIA_DIR` and
  `KLOOM_DATA_DIR=/data` in `fly.toml`
- the `just invite` and `just pull-notes` wrappers
