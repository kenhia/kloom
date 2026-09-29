# Sprint 011 — The reader's layer on a frame: notes, kept Q&A, remappable shortcuts

korg proposal 3420, covering 3409 (frame notes), 3390 (show kept Q&A) and
3363 (remappable shortcuts). Branch `011-readers-layer`.

## Goal

Everything personal on a frame, in one place in the right-hand pane. The
reader writes notes on a frame, and the scene becomes the editor while they
do. Answers they kept are visible again, as a spine mark and a Q&A section.
With the new N key in, the shortcut set has settled, so it becomes
remappable.

## Premise check

- **3409 holds.** No notes exist anywhere. Its dependencies shipped: the
  reader store (3413, sprint 009) and the layout (3377, sprint 010).
- **3390 holds.** Kept answers are still `data/<subject>/kept/<id>.json`,
  nothing in the UI reads them back, and grow reads them by id
  (`grow-service.ts` `readKept`). Grow leaves the file where it is after
  using it, and the job records `kept` and `result.frames`.
- **3363 holds.** The character keys are fixed in `engine/keys.ts`.
- No cross-project plan lists kloom.
- Measured before migrating: the service on kai has **no** kept answers
  (`~/.local/share/kloom/data/*/kept` does not exist). Its store holds places
  for one reader, `ken.hiatt@gmail.com`. The six kept files are in this
  checkout's dev `data/`.

## Decisions

- **One tab row heads the right-hand pane in every layout.** Its tabs are
  Narrative, Notes (with a reader) and AI (in the tabs layout), and the gear
  moved into it for good, out of the narrative toolbar. Notes had to sit
  beside the narrative in all four layouts, and one row placed the same way
  in each was simpler than a second tab list inside the narrative. A layout
  with one tab shows no tab list, just the gear.
- **Q&A lives in the reading, notes on their own tab.** 3390 asked for a
  collapsed section in the narrative, and 3409 for a Notes tab sitting with
  it. Both are in the right-hand pane, side by side, which is the
  proposal's "one place".
- **A note goes on the frame in the reading pane**, the one the reader is
  reading. That is the spine's frame unless following is off, and the
  editor's heading names it either way.
- **Leaving the frame closes the editor.** With changes not saved it asks
  first, via `confirm()`: a native dialog is accessible for free and modal
  where it should be. With no changes it just closes. Leaving the subject
  asks through `beforeNavigate`, and a reload gets the browser's own
  `beforeunload` question.
- **Notes are plain text**, shown `pre-wrap` and never rendered as markup.
  They come whole with the page, since there are few and they are short.
  Kept answers come as counts per frame, with the bodies fetched when the
  Q&A section opens (3390's "cheap enough to mark the whole spine").
- **Review states:** none, flagged or handled, with the agent's response.
  Ticking the box again re-flags a note and clears the old response.
  Unticking a flagged note unflags it, and a handled note stays handled. The
  reader sees the response under their note.
- **The review skill reaches the store through its adapter.** The adapter
  moved to `sqlite-reader-store.ts`, which imports only `node:` modules and
  types, so plain Node 24 loads it with its types stripped.
  `skills/review-notes/review-notes.mjs` imports it, so there is no second
  way into `reader.db`, and no new dependency (no tsx). It runs from a
  checkout with `--data`, and it sees every reader's flagged notes: the
  agent works for the host, and Ken reads as `ken.hiatt@gmail.com` on the
  tailnet while an agent on kai is `ken@kai`. A test runs the script for
  real.
- **Kept answers are stored whole**, in the `kloom.kept-answer` v1 format,
  so grow reads exactly what it read before. **Grow reads only the queuing
  reader's own** (`job.by`), and the grow route checks the reader too. A
  job with no `by` (pre-007) can no longer name a kept answer; none are
  queued.
- **The migration's owner** is `KLOOM_KEPT_OWNER`, else the host's own
  reader, because the files never said who kept them. Files move to
  `kept-migrated/`, never deleted. If they land under the wrong identity,
  export and import move them.
- **3390's open question: a grown answer stays**, marked "Grown into
  <frame>" with a link to each frame. It is still what the reader asked.
  Grow now records the frames on the kept answer when a job commits, and
  the migration carries over what finished jobs had already made.
- **Numbering a kept answer's sources without a format change.** Keeping
  stored the citations in first-use order, so pairing that order with the
  answer's own `[n]` markers recovers each number (`keptReferences`). When
  the frame's list has changed and they no longer pair up, the sources are
  listed unnumbered. No `refs` field, and the format stays v1.
- **Marks:** fixed rows under the line (flag, dot, ruled lines), so a
  kind's place never shifts with the others (design.md §Marks).
  `marksText` puts them in words everywhere a frame is named.
- **Shortcuts:** each character key is a setting, any letter or Off, under
  a "Keys" group (a new optional `group` on `Setting`). The registry stays
  pick-from-a-list, with no free-text key capture. A letter set for two
  shortcuts is allowed, with the settings saying which one acts, rather than
  refused mid-edit. The arrows, Home/End, Esc and Tab stay fixed: they are
  not character keys, and they are the ARIA widgets' own keys. "Narrative:
  Stays until S" became "Stays until synced", since S may not be S.
- **Export is version 2** (notes and kept answers). A version 1 file still
  imports.

## What shipped

- **Store:** `sqlite-reader-store.ts` has migration 2 (the `note` and `kept`
  tables), the notes methods (`notes`, `saveNote`, `deleteNote`,
  `flaggedNotes`, `handleNote`), the kept methods (`keep`, `keptCounts`,
  `keptOn`, `kept`, `grew`, `forget`) and export/import v2.
  `reader-store.ts` keeps the shared instance and re-exports the adapter.
- **Kept answers:** `keep()` writes to the store. `kept-files.ts` is the
  one-time move, run from `hooks.server.ts` `init`. `grow-service.ts` reads
  from the store and records what a job grew into. The grow route checks
  the reader's own kept answer.
- **Routes:** `/api/reader/notes` (GET/POST/DELETE) and `/api/reader/kept`
  (GET/DELETE). The page load adds the subject's notes and kept counts.
- **UI:** `NoteEditor.svelte` (in the scene's place), `Notes.svelte` (the
  tab), `KeptQa.svelte` (the Q&A `<details>`), the spine's marks, and the
  shell's tab row, draft, guard, N key and keymap. The page adds the layer
  offer and `beforeNavigate`. "Keep this" bumps the frame's count.
- **Keys:** `engine/keys.ts` gains `SHORTCUTS`, `Keymap`, `keyClashes` and
  the N key. `pageKey` takes a keymap. `engine/settings.ts` gains
  `keySettings` and `keymapOf`, and `Settings.svelte` gains group headings
  and warnings.
- **Skill:** `skills/review-notes/` (SKILL.md, review-notes.mjs).
- **`just verify`:** two more door checks for notes.
- **Docs:** design.md §Layout, §Ask, §Grow, §Interaction, §Reader data,
  §Settings, and new §Marks, §Notes and §Kept answers; deploying.md;
  roadmap; CLAUDE.md and its Copilot mirror.

## Verification

- `just check`: svelte-check (0 warnings), prettier and eslint, and vitest
  (33 files, 433 tests; all green).
- **New tests** cover:
  - the store: notes per reader and subject, edits, review states, flagged
    across readers, kept counts, grown, forget, export v2 round trip and
    import newer-wins;
  - migrating a schema-1 file (sprint 009's schema, as it shipped) to 2;
  - moving kept files, once, with what grow made of them;
  - the routes: 401 with no reader on every new route, per-reader
    isolation, and refusing empty or oversized notes, bad ids and missing
    frames;
  - the export parser on v1 and v2;
  - `keptReferences` and `marksText`;
  - keys: N, remapped letters, off, and clashes;
  - page renders: the Notes tab in all four layouts and none without a
    reader, the list's review states, marks in words and shape, the closed
    Q&A, the Keys group, remapped help, and the clash warning;
  - the review-notes script run under plain Node.
- **Negative tests:**
  - A value import planted in the adapter fails the script test with
    `ERR_MODULE_NOT_FOUND`.
  - Removing the kept mark from `SpinePane` fails its page test.
- **The kept-file move, for real:** the dev server on a copy of this
  checkout's `data/` logged "moved 6 into ken@kai's store". It left the
  files in `kept-migrated/`, and the counts were western-civ
  `{eratosthenes: 1, jwst: 4}` and ai `{turing-test: 1}`.
- **Keyboard only, in a real browser** (Playwright, Chromium, dev server),
  in all four layouts, all checks passing (`.scratch/layer.mjs`):
  - the slider says "1 kept answer";
  - Tab reaches the Q&A summary, Enter opens it and loads the answer;
  - it shows "Grown into Knowledge went VIRAL." (recorded by hand on the
    copy);
  - N opens the editor in the scene with focus in the text box, and S and
    T typed there stay there;
  - Tab, Space ticks Agent review, and Ctrl+Enter saves, brings the picture
    back and returns focus to the slider;
  - the slider then says ", 1 kept answer, 1 note", and the Notes tab
    counts it;
  - with unsaved changes, → asks: No stays on the frame with the draft
    kept, Yes moves and closes it;
  - Esc on a clean editor closes it without asking;
  - → on the tab list reaches Notes, and Edit and Delete (which asks) work;
  - a saved note survives a reload, and a reload with unsaved changes gets
    `beforeunload`;
  - with the note key remapped to M, N does nothing, M opens the editor,
    and the help says "M note";
  - no console errors.
- **Screenshots** at 1280×800 (the editor in tabs, the Q&A in columns) and
  at 390px (the editor, the Notes tab and the marks): no sideways scroll.

## Repaired in passing

- The Copilot mirror (`.github/copilot-instructions.md`) was missing
  sprint 010's status line; restored with this sprint's.
- The roadmap still listed the AI pane's layout under Next, and had no
  sprint 010 entry. Both are fixed, and Next is annotations (3415).

## Follow-ups

- Ken wanted to try notes "and see how it feels before calling it settled"
  (3409). The editor-in-the-scene, the guard's wording and the marks'
  shapes are the things to judge.
