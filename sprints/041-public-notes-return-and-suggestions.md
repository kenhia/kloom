# 041 — The public site's notes return trip, the detached-note check, and suggested subjects

## Goal

korg proposal 3507, covering 3504 and 3459: the third and last slice of
program korg 3508, the public reader site. Notes readers flag for Agent
review on kloom.kenhiatt.us are answered in the live store without ever
pushing a database back; notes a publish leaves detached are reported after
each publish; and a reader can suggest a subject, which Ken reviews.

The sprint ran as a karc leg, overseen. The overseer's notes (comment 3393)
set the round trip with the throwaway reader `kloom-test` as the slice's
same-day trigger, ruled HSTS on `/_app/immutable` not needed, asked that
"Suggest a subject" not add to the crowded start screen (korg 3514), and
said a publish goes out from merged `main` with `just publish-public`.

## Premise, checked at start

- **3504 holds.** `admin.mjs` had no note commands; `review-notes.mjs` read
  only a local `--data` store; `verify-public` had no detached check.
- **3459 holds**, and its blocker is gone: reader data lives in `reader.db`
  on the Fly volume (3458 comment 3355), so suggestions go where notes go.
- **Nothing pending.** `just grow-pending` listed nothing, and kloom is not
  in the cross-project plan index.

## What shipped

**The admin CLI** (`admin.mjs`) gained the review side:

- `flagged [--reader R] [--json]`: the flagged notes, each with its
  reader's display name (looked up in the accounts) as `readerName`.
- `handle-note READER ID RESPONSE... [--seen UPDATED]`: one answer, refused
  with the reason when the note is gone, no longer flagged, or, given
  `--seen`, edited since it was read. `handle-notes JSON` answers a list
  of `{reader, id, response, seen?}` and prints a result for each.
- `detached [--library FILE] [--json]`: every note whose frame the library
  no longer has, and every annotation whose words its reading lost.
- `suggestions [--status S] [--json]` and `mark-suggestion READER ID
STATUS`.
- `--args-b64`: the arguments as a base64 JSON list, so a response with
  quotes and spaces passes `fly ssh console -C`, which splits on spaces,
  whole.
- `delete` now reports suggestions too. A READER is a username or a login.

**The store.** `handleNote` takes an optional `seen`, the note's `updated`
when the agent read it, and refuses when it differs, so an answer never
lands on words it did not answer. `everyNote()` lists every reader's notes
for the detached check. The sixth migration adds the `suggestion` table
(reader, id, the reader's name at the time, title, cover, why, status,
created, updated), with `suggest`, `suggestions`, `allSuggestions` and
`markSuggestion`. `deleteReader` removes a reader's suggestions as well.

**review-notes** (`skills/review-notes/review-notes.mjs`) is now a front
end to the admin CLI with two targets. `--data DIR` runs `admin.mjs` here;
`--public` runs it on the Fly machine through `deploy/fly.sh ssh console`,
with the arguments base64'd. `list` shows the display name and the
`--seen` value to answer with; `handle` takes `--seen`, and `handle --file`
sends a batch in one call. `suggestions` and `mark-suggestion` follow the
same targets. `SKILL.md` says which target to use, how a refusal reads, and
how to promote a suggestion into a korg "Future subject" item that credits
whoever suggested it (search first; comment on an existing one).

**The detached check after each publish.** `just verify-public` ends with
`admin detached` on the machine, against the library it serves, and prints
each detached note as a `note` line. A detached note does not fail the
recipe; failing to run the check does. It reads a reading's text off the
rendered HTML without a DOM, through `htmlText` in `engine/anchor.ts`,
and finds the words with the same `findQuote` the page uses. The
Dockerfile copies `engine/anchor.ts`, which imports nothing, into the image
for it.

**Suggest a subject**, in the About panel (`engine/ui/Suggest.svelte`),
after the note on accuracy, for a reader only. A _Suggest a subject…_
button opens a form in place, focused on its first field: the subject
(required), what it should cover, and, optionally, why. Send closes the
form, returns focus to the button and says "Sent: …" in a status line; a
refusal is an alert and the form stays. _Your suggestions_ lists theirs with
the status in words (Sent, Planned, Written, Declined). The route is
`GET`/`POST /api/reader/suggestions`, behind the same reader gate as every
reader-data route, and refuses a 21st suggestion still waiting.

Docs: `docs/design.md` §Suggestions (new), §Annotations, §Reader data and
§About; `docs/deploying.md` §The admin CLI, §Publishing and §Readers' notes
and the backup.

## Decisions

- **Answers go to the live store, one guarded write each.** A database is
  never pushed back, and a pulled copy is never written to: an answer
  written there would never reach the site. `just pull-notes` stays as the
  backup.
- **How review-notes picks its target** (the open question in the
  proposal's notes): a flag, `--data DIR` or `--public`, never inferred.
  `--public list` reads the live store rather than the newest pulled copy,
  so nothing is reviewed stale and no pull is needed first.
- **Batching the `fly ssh` calls:** `handle --file` sends many answers in
  one call. A single `handle` is a batch of one, so both go through one path
  (`handle-notes`). Each `fly ssh console` costs a few seconds, and that is
  the whole saving; a list call is already one.
- **One implementation, two transports.** review-notes never opens the store
  itself any more. It calls `admin.mjs` locally or over ssh, so the public
  site and kai's service are answered by the same code.
- **`--seen` guards against edits**, not only deletion or unflagging. A
  reader may edit a flagged note between the listing and the answer; the
  answer is then refused, and the agent lists again. Re-flagging changes
  nothing that matters here, because the response is cleared and the note
  is flagged again.
- **Suggestions live in About**, per the overseer's note on start-screen
  crowding (korg 3514). They are not in the export: a suggestion is a note to
  Ken, not reading data. They are kept with the reader's display name at
  the time, so the credit survives a rename. 20 waiting is enough for a
  family site, and it stops a stuck key filling the table.
- **Only the review side moves a status.** `declined` waits for Ken's say,
  and the skill says so.
- **The HSTS ruling** (static assets need none) is taken as given:
  `serve.js` is untouched.

## Verified

- **`just check` is green**: svelte-check (0 warnings), prettier and
  eslint, 1,392 tests, the tools' tests, the reader gate (88 files clean)
  and the mark check. New: the store (the `seen` guard, `everyNote`,
  suggestions, the schema-5 file moving forward), the admin CLI and
  review-notes run for real under plain Node (`src/lib/server/admin.test.ts`),
  `htmlText` and `detachment`, the suggestions route, and About's form
  rendered with and without a reader.
- **Negative test:** with the `seen` clause defeated
  (`? IS NULL OR 1 OR …`), two tests fail: the store's and the admin CLI's.
- **`htmlText` against the DOM:** on all 616 frames of the staged public
  library, `htmlText` equals the page's own text-node walk in Chromium
  (DOMParser, svg, style and script skipped) byte for byte. Negative
  control: a naive tag strip with no entity decoding matched 0 of 616.
- **Keyboard only, 1280×800 and 390×844** (Playwright, dev server): About
  opens with Enter, the toggle opens the form with focus in Subject,
  Tab reaches Send, Enter sends, the status line says "Sent: …", focus
  returns to the toggle, the list shows the new suggestion, an empty
  subject is refused by the browser and the form stays open, and Esc
  closes About with focus on its button. The panel stays inside a 390px
  screen.
- **The round trip against the real image, locally** (`docker build` of
  this commit, run with a scratch volume): a reader was added and invited,
  signed in with the link, flagged a note and made an annotation on words no
  reading has, and suggested a subject, all through the HTTP API. `flagged`
  named them "Kloom Test". A stale `--seen` was refused. `handle-notes`
  through `--args-b64` answered with a response full of quotes and an em
  dash, which reached the reader intact, and `my-notes` counted it as 1
  unseen. `detached` reported exactly the annotation. `mark-suggestion
planned` showed in the reader's own list. `delete --yes` removed the
  account, 2 notes and 1 suggestion.

## Left for the ship turn

The reader edition's code changed, so it publishes, from merged `main`:

1. `just publish-public`. `verify-public` should pass the 18 checks it had
   and then print the detached line (`note N notes, 0 detached` expected).
2. **The live round trip with `kloom-test`** (comment 3393): `just invite
kloom-test` for a fresh password, sign in with the link, flag a note on
   the live site; `just pull-notes`; `review-notes.mjs --public list`, then
   `handle … --seen …`; check the answer is unseen for `kloom-test`
   (`/api/reader/my-notes`); `admin detached`; then `admin delete kloom-test
--yes`. `jkh` is not touched.

## Repaired in passing

- `engine/anchor.test.ts` kept its own copy of reading-text extraction, which
  handled five entities. It now uses `htmlText`, so the tests exercise the
  code the detached check runs.

## Follow-ups

None filed.
