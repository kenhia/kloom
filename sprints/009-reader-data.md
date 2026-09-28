# Sprint 009 — Reader data: a store, resume where I was, bookmarks

korg proposal 3418, covering 3413 (the reader-data store) and 3414 (last
visited and bookmarks). Branch `009-reader-data`.

## Goal

Give the reader's own state a home. The AI subject, at 66 frames, made the
first need plain (Ken, 2026-09-28): getting back to where you left off. The
store is designed for every later consumer (notes, kept answers and
annotations), and only places and bookmarks get tables now.

## Premise check

- **3413 holds.** Its dependency, the tailnet identity (3388), shipped in
  sprint 007. `readerOf` already gives every request that may write a
  login, and the ssh door and the dev server map to the host's `user@host`.
  So the "fixed local reader" fallback in the proposal's notes was not
  needed. The real identity is used from the start.
- **3414 holds.** Sprint 006's routes (3396) named only the subject, so
  deep links were added here, as the proposal's notes said to.
- No cross-project plan lists kloom.

## Decisions

- **`node:sqlite` over better-sqlite3.** Node 22.13 is already the engines
  floor, and `node:sqlite` is unflagged there. On kai's Node 24.21 it
  prints no experimental warning, and it ships SQLite 3.53.4. No
  dependency, no native addon, and nothing to rebuild on a Node upgrade.
  Rollup leaves the `node:` import external, so the adapter-node build is
  unchanged.
- **An async interface over a sync adapter.** `ReaderStore` is async, so a
  Postgres adapter can come later without touching callers. SQLite answers
  synchronously underneath.
- **Records name frames, never trails.** Validation already puts each frame
  on exactly one spine, so the frame says which trail it is on. The deep
  link is `/<subject>/<frame>` for the same reason. A stored trail could
  only go stale.
- **A label is stored with each record.** It is the frame's title when the
  record was written. A jump list that spans subjects can then name a frame
  without loading every subject. Titles in the current subject come from
  the content and override it.
- **Offered, not forced.** The resume offers sit under Begin, and Begin
  keeps the focus. A deep link skips the start screen, since the reader
  asked for a frame.
- **No reader, no reader data.** Reader-data routes refuse a request with
  no reader, reads included. On such a page (a tagged tailnet node), the
  controls are absent rather than broken.
- **A stale frame link redirects** to the subject rather than 404ing, so an
  old bookmark lands on the start screen.
- **What B bookmarks:** the frame on the spine, not a pinned narrative
  frame. The toggle lives in the spine pane, and so does the mark.
- **No localStorage cache.** The page load brings the reader's data with
  the page, so a cache would only add a second truth. 3414 allowed one;
  nothing needed it.

## What shipped

- `engine/reader-data.ts` holds the `ReaderStore` interface and the record
  and export types. `parseExport` checks every record, and one bad record
  refuses the file.
- `src/lib/server/reader-store.ts` is the SQLite adapter: migrations by
  `user_version`, WAL, newer-wins upserts, and export and import.
- `src/routes/api/reader/` holds `place`, `bookmarks` (GET/POST/DELETE),
  `export` and `import`. A record must name a served subject and a frame on
  disk.
- The subject page moved to `src/routes/[subject]/[[frame]]/`. Its load
  adds `frame`, `reader` and `readerData`, leaving out records whose
  subject or frame is gone. The URL follows the reader by `replaceState`,
  and the place is written 800ms after they stop.
- Shell has `goTo(frame)`, `startAt`, `onplace` and a bookmark offer. The
  spine HUD carries the toggle and the jump list
  (`engine/ui/Bookmarks.svelte`). Ticks carry a flag, and the words go in
  `aria-valuetext`, the tick title and the announcement. The B key is
  scoped like S and T, and the AI pane's hint bar names it.
- The start screen shows _Continue where you were_ and _Last read ·
  <subject>_.
- `just verify` also checks that the tailnet door refuses an anonymous
  reader-data read (401) and that the ssh door serves one (200).
- Docs: design.md §Reader data, plus the deep-link, key and write-gate
  lines; deploying.md (where `reader.db` lives, and how to back it up);
  the roadmap; CLAUDE.md and its Copilot mirror.

## Verification

- `just check`: svelte-check with no warnings, prettier and eslint, and 382
  vitest tests.
- New tests cover the store (per-subject and overall places, readers kept
  apart, bookmarks, export/import round trip, never moving back in time,
  and migrating and reopening a file, including a newer file refused), the
  export parser, the routes (401 with no reader, 404 for an unknown
  subject, 400 for a missing frame, export as an attachment, import under
  another reader), the B key's scope, and the page. The page tests cover
  no controls without a reader, the toggle and jump list in the spine, the
  mark in words, the resume offers after Begin, and deep links, including
  a trail frame.
- Negative test: removing the tick's `marked` class fails the page test
  that checks the mark.
- **Keyboard only, in a real browser.** Playwright drove Chromium against
  `node serve.js` on test ports. Enter begins; → three times moves the URL
  to `/western-civ/eratosthenes`; B presses the toggle, says "Bookmarked:
  Then we MEASURED." and puts ", bookmarked" in the slider's value text. A
  reload lands on the same frame, past the start screen. The jump list
  opens with Enter, → inside it leaves the spine alone, and Esc closes it
  and returns focus to its button. `/ai`'s start screen offers "Last read ·
  The History of Western Civilization", and Tab then Enter lands on the
  frame. Continue resumes; B again removes the bookmark. No console
  errors. Screenshots at 1400px and 390px showed the list and flags
  clear of the HUD.
- The browser run caught one bug: following an in-app link to a deep link
  (the last-read offer) showed the start screen, because the page
  component is reused. Fixed with an `$effect.pre` on `data.frame`.

## Follow-ups

- Nothing filed. Notes (3409), kept Q&A (3390) and annotations are already
  items, and they depend on this store. An import button in the UI waits
  on a reader wanting one, since the route covers backup and moving hosts.

## Deployed

- **2026-09-28, kai, `just deploy` from merged main `79036cf`** (sprint-ship
  Phase 7, the `recipe: deploy` line). `npm ci` did not re-run, since the
  lockfile was unchanged. The content clone was on `grow/kai` at main, and
  the sync needed nothing. All six `just verify` checks passed, including
  the two new ones: the tailnet door refuses an anonymous reader-data read
  (401), and the ssh door serves its reader's (200).
- **This sprint's behaviour, live on :4891.** `/western-civ/printing-press`
  serves (200) with the bookmark toggle and no start-screen dialog, and
  `/western-civ/nope` redirects (307) to `/western-civ`. A bookmark was
  added, listed and deleted through `/api/reader/bookmarks`, leaving the
  list empty. `~/.local/share/kloom/data/reader.db` was created on first use
  (WAL), and the journal shows no errors.
