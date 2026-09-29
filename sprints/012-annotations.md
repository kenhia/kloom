# Sprint 012 — Annotations: notes on words of the narrative, anchored to survive edits

korg proposal 3421, covering 3415 (annotations). Branch `012-annotations`.

## Goal

A reader selects words in a frame's narrative and writes a note on them,
with the same "Agent review" flag as a frame note, so an agent can be
pointed at the exact wording that confused them. The hard part is the
anchor: grow and later sprints change narratives, and an annotation has to
find its words again, or say it cannot, and never sit on the wrong ones.

## Premise check

- **3415 holds.** Its dependency, frame notes (3409), shipped in sprint 011:
  the `note` table, the Notes tab, the editor and the review-notes skill.
  Nothing annotation-shaped existed, only two forward references
  (`engine/reader-data.ts`'s header and design.md §Reader data).
- No cross-project plan lists kloom.

## Decisions

- **An annotation is a note with an anchor**, not a new kind of record. 3415
  calls it "a frame note that also records a range", and one nullable
  `anchor` column (the third migration) gives it the note's editor, Notes
  tab, review states, export and skill without a second copy of each.
- **The anchor is the W3C text-quote selector**: `exact`, `prefix` and
  `suffix` (32 characters each) and a `start` hint, in `engine/anchor.ts`.
  It works on the reading's text as its text nodes give it, with inlined
  charts left out and whitespace collapsed. Collapsing is needed, not
  polish: readings are soft-wrapped markdown, so a paragraph's text is full
  of newlines that a re-wrap would move.
- **No fuzzy matching.** The quote must be found exactly (give or take
  whitespace), and a place is taken only when 8 or more characters of
  context agree, or the quote is 24 or more characters and appears once.
  Rewording the quoted words detaches the annotation. The alternative,
  diff-match-patch-style fuzzy search as Hypothesis does, needs a
  dependency, and it is exactly how an annotation ends up "silently wrong"
  on words the reader never wrote about. A detached annotation keeps its
  quote, so nothing is lost.
- **Keyboard selection by sentence and word.** A reading is not editable, so
  a keyboard user has no selection without caret browsing. A (or the
  Annotate button) with nothing selected starts choose mode: ↑/↓ by
  sentence, ←/→ the start by a word, Shift+←/→ the end, Enter to annotate,
  Esc to cancel. The choice is the real DOM selection, so the mouse path
  (select, then A or the button) and the keyboard path meet in one place:
  annotate the selection. Sentences come from `Intl.Segmenter` per block, so
  a heading is not glued to its paragraph.
- **Highlights are `<mark>`s plus a ✎ button**, not the CSS Custom
  Highlight API. That API is invisible to assistive technology. A `<mark>`
  is announced as highlighted, and a real, named button after the words
  puts every annotation in the tab order, like a footnote reference. The
  glyph is CSS `content` with empty alt text, so the button's name is its
  `aria-label` and it adds nothing to the reading's text.
- **The DOM is touched only inside the reading's own elements.** Svelte owns
  the `{@html}` block's top-level nodes, so a highlight never wraps a text
  node that sits directly in `.body`, and clearing un-wraps and normalises
  each mark's parent, never the whole body.
- **An edit keeps its anchor**, as it keeps its frame: the store's edit
  statement does not touch the column, whatever the request sends.
- **Export version 3**, because an older app would silently drop anchors
  from a file with them. Versions 1 and 2 still import.
- **A is the key** (remappable, "Annotate the reading"), acting where the
  other character shortcuts act. From the spine or the notes it brings the
  narrative tab forward first.

## What shipped

- **`engine/anchor.ts`:** `quoteOf`, `findQuote`, `sentences`, `words`,
  `moveStart`/`moveEnd` and `anchorOf`, all pure.
- **`engine/ui/reading-text.ts`:** the reading's text nodes end to end
  (`readingText`), DOM range to offsets and back (`spanOf`, `rangeOf`), and
  `highlight`/`clearHighlights`.
- **Store:** migration 3 (`note.anchor`), anchors read and written as JSON,
  kept on edit, carried by `flaggedNotes`, export v3 and import.
- **Route:** `POST /api/reader/notes` takes an `anchor` on a new note and
  refuses a malformed one (400).
- **UI:** Narrative (highlights, the Annotate button, choose mode, the
  detached line), NoteEditor (the quote, "New annotation", detached),
  Notes (the quote, Show in reading, detached), Shell (the A key, drafts
  with anchors, show and annotate), and the A key in `engine/keys.ts`.
- **Skill:** `review-notes.mjs list` marks an annotation and quotes its
  words, and SKILL.md says what an annotation asks and that rewording its
  words detaches it.
- **Docs:** design.md §Annotations (new), §Interaction, §Reader data,
  §Notes; the roadmap; CLAUDE.md and its Copilot mirror.

## Verification

- `just check`: svelte-check (0 warnings), prettier and eslint, and vitest
  (34 files, 456 tests, all green).
- **The proposal's test, on real content:** `anchor.test.ts` annotates three
  ranges of `printing-press`'s rendered reading and edits it the way grow
  would: a paragraph inserted above, the sentence after one reworded, and
  one annotated sentence deleted. They re-find, re-find and detach.
- **New tests** also cover: context choosing between repeated words, a
  re-wrapped paragraph, a short quote in new surroundings detaching, a long
  unique one staying, quotes at the text's ends, sentences per block, word
  moves, anchor validation, the store (anchor kept on edit, in the flagged
  list, through export and import), migrating a schema-2 file, the route's
  400s, export v2 and v3 parsing, the A key, the Annotate button with and
  without a reader, the help line, the Notes tab's quote and Show button,
  and the skill's `list` output run under plain Node.
- **Negative tests:** accepting a quote with no agreeing context
  (`AGREE = 0`) fails "detaches a short quote…". Never detaching (a missing
  quote returning a span) fails "detaches when the quoted words are gone"
  and the real-reading test.
- **Keyboard only, in a real browser** (Playwright, Chromium, dev server on
  a copy of `data/`), in all four layouts, 39 checks each, all passing
  (`.scratch/annotate.mjs`):
  - A from the spine puts focus in the reading, selects the first sentence
    in view, shows the keys and says the words;
  - ↓ moves by sentence, Shift+← and → trim a word from each end, and the
    spine does not move;
  - Enter opens "New annotation" quoting the words, with focus in the text
    box; Tab, Space and Ctrl+Enter save it flagged;
  - the highlight is exactly the chosen words, its button is named, focus
    returns to the reading, and "Annotation saved" is said;
  - Esc cancels choosing with nothing opened;
  - Enter on the ✎ button opens "Editing an annotation", and Esc returns
    focus to the button;
  - a mouse selection plus the Annotate button takes those words, and a
    click on a highlight opens its annotation;
  - the Notes tab quotes both, and Show in reading brings the narrative
    forward and focuses the right button;
  - after a reload both are highlighted again;
  - an annotation whose words are not in the reading is reported in the
    reading, marked detached on the Notes tab with no Show button, and its
    editor says so;
  - another frame shows no highlights, and coming back redraws them;
  - no sideways scroll at 390px, and no console errors.

## Repaired in passing

- **Cancelling a note never returned focus to where it was opened from.**
  `cancelNote` called `mayLeave()`, which clears the draft, before
  `closeEditor` read `draft.from`. So Esc or Cancel always sent focus to the
  slider, although design.md §Notes says focus goes back. The browser check
  caught it through an annotation's ✎ button. `cancelNote` now reads the
  origin first, and §Notes says "saving or cancelling".

## Follow-ups

- Buttons named with a visually hidden suffix ("Edit", "Delete", now "Show
  in reading") get the accessible name "Edit : …" in Chromium, with a space
  before the colon. It reads fine, but it is sprint 011's pattern and a
  one-line change for all three if Ken wants it tidier. Not filed: it is
  cosmetic and no decision hangs on it.

## Deployed

2026-09-29 03:36 UTC, on kai. `just deploy` (the `recipe: deploy` line in
`.sprint-deploy`) ran from merged `main` at `4245c42`. It built the app,
restarted `kloom.service`, and passed all eight of `just verify`'s door
checks. No content changed: the content clone is still on `grow/kai`.

- **The migration, before and after** (read-only counts): `reader.db` went
  from schema 2 to 3, and `note` gained its `anchor` column. It held 2
  places, 0 bookmarks, 0 notes and 0 kept answers before and after. The
  journal has no errors.
- **Checked live on the ssh door (`127.0.0.1:4891`):**
  - a flagged annotation POSTed to `/api/reader/notes` came back with its
    anchor, was listed with its quoted words, and was deleted, leaving the
    list empty;
  - a malformed anchor is refused (400);
  - `/western-civ/printing-press` serves the Annotate button and the
    "Annotate the reading" key setting.
