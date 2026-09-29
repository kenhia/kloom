# Sprint 016 — Navigation: a table of contents, and a Continue that continues

korg proposal 3434, covering 3432 and 3433. Branch `016-navigation-toc-continue`.

## Goal

Long subjects (Feynman, and the AI subject's 66 frames) had no way to move
directly to a frame. The only ways to move were stepping the spine, the
timeline bar and the bookmarks. And Home mid-subject offered no _Continue
where you were_ for the place just left. This sprint adds a table of
contents and makes the start screen's two buttons mean different things.

## Premise check

- **3432 holds.** The `seen` guard was still at `+page.svelte:271`
  (`if (!f || seen === data.subject.id) return [];`), and `places` still
  came only from the page load.
- **3433 holds.** Nothing in `engine/`, `src/` or `docs/` listed a
  subject's frames; the roadmap still had it as an idea.
- No cross-project plan lists kloom.

## Decisions

Ken's, recorded on 3432 before the sprint:

- **Begin starts from the first frame; Continue returns to the last place in
  that subject**, read from the reader-data store rather than stale page
  data. The `seen` guard is dropped.

Made in the sprint:

- **The page keeps a live mirror of the places**, not a re-read. Each move
  writes the mirror at once, and the store 800ms later as before. So Home
  inside the debounce still names the frame just left. A fresh load (another
  subject, say) may race the pending write, so the page keeps whichever copy
  of each subject's place is newer (`newerPlaces`, engine/reader-data.ts),
  with a tie going to the load.
- **Without a reader there is no mirror.** Nothing is kept for an anonymous
  reader, so nothing is offered, as before.
- **Esc still returns to where the reader was.** Only Begin moves: dismissing
  a dialog should not move the reader. StartScreen gains `onfirst`, which
  Begin on the subject behind calls before closing, and Esc does not.
- **The contents are a popover, not a dialog**, matching the gear and the
  bookmarks. Focus is not trapped, a click outside closes it, and Esc
  returns to the button.
- **Nested lists with disclosure buttons, not a treeview.** The entries are
  links (each frame has a deep link, so open-in-new-tab works), and a
  treeview would announce them as tree items. The treeview's keys are added
  anyway: ↑/↓ through the filter, entries and disclosures, Home/End, and
  →/← on a trail. The reasoning is in design.md §Contents.
- **Trails: collapsed and indented.** Ken asked whether they should be
  indented or collapsed, and this does both, as 3433 recommended. The trail
  the reader is on, or those branching from their frame, open expanded.
- **The type-to-filter box is in.** It was "recommended, not required", but
  at 66 frames it is the quick path. A trail whose title matches stays
  whole. While filtering, matched trails show open as plain labels rather
  than as disclosure buttons, because there is nothing to disclose.
- **C is the shortcut**, the sixth in `SHORTCUTS`, so it is remappable under
  Settings › Keys and scoped like the others (WCAG 2.1.4). It sits last, so
  it never wins a clash with an older one.
- **Marks in words.** A frame's marks are said after its position ("c. 240
  BC · 1 kept answer"), in `marksText`'s words, so they read the same to
  the eye and to a screen reader. Annotations count as notes there, as they
  do on the spine.
- **After a pick, focus returns to the contents button**, not the body. It
  is inside the spine, so the shortcuts still act.
- **On a phone it is a full-screen sheet**, with its title, close button and
  filter sticky at the top.
- **No reuse of the bookmarks' item markup.** The proposal suggested it
  "where it fits". The contents copy its look (label over a muted context
  line), but a bookmark item carries a remove button and cross-subject
  context, so sharing a component would have cost more than it saved.

## What shipped

- **Engine:** `engine/contents.ts` (`contentsOf`, `filterContents`,
  `contentsCount`, `openTrails`) and its test; `engine/ui/Contents.svelte`;
  the `contents` shortcut in `engine/keys.ts`; `newerPlaces` in
  `engine/reader-data.ts`. Shell puts Contents before Bookmarks in the
  spine's tools, handles C, and names C in the help bar. It takes `hrefOf`
  for the links. StartScreen has `onfirst`.
- **Page:** `places` (the mirror) replaces the loaded `places` in the resume
  offer, `seen` is gone, Begin goes to the first frame, and `hrefOf`.
- **Docs:** design.md §Contents (new), §Interaction (C), §Reader data
  (last visited), §Start screen (Home); the roadmap; CLAUDE.md and its
  Copilot mirror.

## Verification

- `just check`: svelte-check (0 warnings), prettier and eslint, vitest.
- **New tests:** `newerPlaces` (newer per subject from either copy, a tie to
  the load); the contents (every frame once by segment, trails under their
  anchors, all 66 of AI, the filter by title and position ignoring case,
  a trail frame keeping its anchor, a trail kept whole by title, empty
  segments dropped, which trails open); C scoped like the other shortcuts;
  on the page, the contents closed in the spine left of the bookmark,
  every frame linked under its segment with one `aria-current`, a trail
  collapsed under its anchor, and a mark in words. The hint-bar tests now
  name C.
- **Negative tests:** `>` for `>=` in `newerPlaces` fails "prefers the fresh
  load"; `anchor !== id` in `contentsOf` fails four contents tests; dropping
  `aria-current` fails "lists every frame … with the current one marked".
- **In a real browser** (Playwright, Chromium, the dev server with its local
  reader, keyboard only, `.scratch/s016.mjs`):
  - Begin, → ×3, and Home within 250ms (inside the write's debounce): the
    offer is _Continue where you were: Then we MEASURED. · c. 240 BC_, the
    frame just left.
  - Begin goes to `prometheus`, the first frame.
  - → ×2, Home, then _Continue_ returns to `greek-inquiry`.
  - Home then Esc stays at `greek-inquiry`.
  - After a reload, the offer comes from the store and names `greek-inquiry`.
  - C on the spine opens the contents focused on the current frame, and ↓
    moves to the next. Esc closes them and focuses the button, without
    moving.
  - Enter reopens them. Home then ↑ reaches the filter. Typing "press"
    shows "2 frames". ↓ then Enter goes to `printing-press`, closes the
    list, and focus is on the button.
  - C again opens with the printing trail expanded (`aria-expanded=true`)
    and the other trail collapsed. ↓↓ then Enter enters the trail at
    `gutenberg-bible`, and the Main story crumb shows. C again opens with
    focus on that trail frame.
  - AI (66 frames) and Feynman (62), at End: the current frame is focused
    and scrolled into view, at 1400×900 and at 390×800. On the phone the
    sheet is 374px wide and the page never scrolls sideways.

## Repaired in passing

- **The Copilot mirror had fallen behind.**
  `.github/copilot-instructions.md`'s Project section was missing sprints
  014 and 015 and the author-subject skill. It is now the same as CLAUDE.md
  again.

## Follow-ups

- None filed.
