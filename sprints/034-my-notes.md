# 034 — My notes

## Goal

korg proposal 3482, covering korg 3481: one place to see every note and
annotation a reader has, across subjects, with each one's agent-review
state, a way to go to it, and ways to clear it, one at a time or in bulk.
Before this, a note could be found only on its own frame's Notes tab, and
after the first round of agent-review fixes (kloom#35) the handled
annotations stayed behind, detached, with nowhere to clear them.

## Decisions

- **Premise, checked at start.** It held. The store listed notes per
  subject only (`notes(reader, subject)`), had `deleteNote` and
  `handleNote`, and recorded nothing about whether an answer had been
  seen. The proposal ran after content.db (032), as it asked: a note's Go
  to fetches its frame like any other jump. kloom is not in the
  cross-project plan index.
- **A modal dialog, not a pop-up like the bookmarks.** It holds filters,
  per-entry actions, confirms and bulk clears, so it is built like the map:
  a `<dialog>` opened modal, `data-own-keys`, Esc closes, and the page
  behind is inert. Closing leaves focus to the dialog itself, which returns
  it to wherever it was when the dialog opened: the control, or the pane O
  was pressed in.
- **O for "open my notes".** S, T, B, N, A, C, R, M, D and W were taken. It
  is remappable and scoped like the rest (`engine/keys.ts`).
- **"Detached" is worked out in the browser, as the reading pane does.**
  It depends on the reading's text as its rendered text nodes give it, so
  the dialog fetches each annotated frame's body (`/api/frame`, with this
  subject's bodies taken from the page's cache), parses its HTML with
  `DOMParser` (inert: no images load) and runs the same `readingText` and
  `findQuote`. Doing it on the server would have meant a second idea of
  the reading's text that could disagree with the pane. An annotation on a
  frame the library no longer has is detached, and one whose frame could
  not be fetched is left unjudged rather than guessed at.
- **"Seen" is a flag on the note**, a fourth migration (`unseen INTEGER`),
  set by `handleNote` and cleared by seeing it or by flagging the note
  afresh. A per-reader "last looked" timestamp would have needed a handled
  time on the note as well; the flag is one column and says exactly which
  answers wait. Answers given before the migration are counted as unseen,
  since nothing recorded that they were seen. The count clears when the
  dialog opens (its entries keep saying _Answered (new)_ while it stays
  open) and when the Notes tab shows the note.
- **The flag toggle has its own route** (`PATCH /api/reader/notes`,
  `flagNote`), rather than re-saving the note's text through `POST`. It
  follows the editor's box exactly: ticked flags afresh and clears the
  answer, unticked unflags a flagged note and leaves a handled one handled.
  Its label says what it will do: _Flag for agent review_, _Withdraw agent
  review_, _Ask the agent again_.
- **Bulk clears send the ids the reader saw**, not a filter for the server
  to apply (`DELETE /api/reader/notes` with `ids`, capped at 1,000). The
  confirm says how many, and that is what is deleted, even if a note
  changed state since.
- **A note whose subject or frame is gone stays listed.** The list is the
  one place to clear it, so it shows the label it was saved with and _No
  longer in the library_, and can be cleared but not gone to.
- **The list endpoint is its own route** (`/api/reader/my-notes`), not
  `GET notes` without a subject: it answers a different shape (the notes
  with where each is now, and the unseen count), and its `POST` is the
  "seen" write.
- **"Works on the public reader site too" (3458)** holds by construction.
  Everything goes through the reader's own routes and the hook's reader
  gate, so wherever there is a reader, there is My notes. The public site
  itself is not built yet.

## What shipped

- `ReaderStore` gains `allNotes`, `flagNote`, `deleteNotes`,
  `unseenAnswers` and `seeNotes`; `Note` gains `unseen`; the SQLite adapter
  its fourth migration. Export carries `unseen`, and import keeps it.
- Routes: `GET`/`POST /api/reader/my-notes`, `PATCH /api/reader/notes`, and
  `DELETE /api/reader/notes` with `ids`. The page load carries the unseen
  count.
- `engine/my-notes.ts`: an entry's states in words, the filters and their
  counts, grouping by subject, the annotated frames, `detachedIn`, and the
  bulk confirm's question.
- `engine/ui/MyNotes.svelte`: the control (with its badge and "My notes, 2
  new answers") and the dialog. The shell hosts it in the spine's HUD,
  binds O, names it in the help bar, and gains `showNote`, which opens the
  Notes tab focused on a note; the Notes tab marks answers seen.
- `docs/design.md` §My notes, with §Reader data's routes and migrations
  and §Interaction's keys; the review-notes skill says where its answers
  now show.

## Verified

- `just check`.
- Driven in Chromium against a dev server with a throwaway data dir
  (`.scratch/mynotes/drive.mjs`): four notes seeded through the routes, two
  handled with `review-notes.mjs handle`. The control read "My notes, 2 new
  answers" with a badge of 2. O from the spine opened the dialog with focus
  on the first entry, whose description read "Note · Answered (new) | Look
  again at this. Agent: Fixed the date." The annotation whose words were
  gone read "Annotation · Answered (new) · Detached", and the one whose
  words were there was not detached. The badge cleared on opening. ↓ and
  End moved between entries, and the spine did not move. The radios
  filtered to 1, 2 and 1. Delete on an entry asked "Delete this note?",
  removed it and focused the next. _Withdraw agent review_ said "No longer
  flagged." _Clear answered_ asked "Delete the answered note?" and deleted
  it. Esc closed the dialog with focus back on the spine's slider, where O was pressed. O again, then Enter on a note in another subject went to
  `/ai/alexnet` with the Notes tab selected, focus on that note and the
  Back chip naming where it came from. At 390 px the dialog was 357 px
  wide with nothing scrolling sideways.

## Repaired in passing

- `sprints/planning/roadmap.md` stopped at sprint 028; 029 to 033 are
  listed now, from their records.

## Follow-ups

- The live test is the deploy's: Ken's three handled annotations from
  kloom#35 are on the service, detached and answered, and _Clear answered_
  should remove all three.
