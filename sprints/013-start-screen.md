# Sprint 013 — The start screen: a Home control, a subject list, the subject's frames around the loom

korg proposal 3425, covering 3424. Branch `013-start-screen`.

## Goal

Once a reader was inside a subject, nothing led back to the start screen.
The screen itself offered other subjects only as an "Or open" row of links,
which works for two subjects and not for ten. This sprint adds a Home control
left of the settings gear and a keyboard-selectable subject list. The
selected subject shows its title and _Continue where you were_, and small
copies of its own frame illustrations are drawn around the loom.

## Premise check

- **3424 holds.** There was no route back from inside a subject. The only
  chooser was the "Or open" row in `StartScreen.svelte`, and the five icon
  candidates were still only in `.scratch/start-icons/`.
- No cross-project plan lists kloom.

## Decisions

Ken's two, recorded on 3424 before it was proposed:

- **The ring shows the selected subject's own illustrations.** It is redrawn
  when the selection changes, and a large subject shows a sample.
- **Home opens the start screen over the current subject, with it
  selected.** Begin or Esc returns to exactly where the reader was, and
  `/` still redirects.

Made in the sprint:

- **The shell is not remounted.** Home sets `begun = null`, and the shell
  (keyed by subject, as before) goes inert behind the dialog. Nothing about
  the place, the narrative or an unsaved draft has to be saved and restored.
  The URL stays on the frame too, because the place effect only writes while
  started.
- **Focus comes back to Home**, the control that opened the dialog, rather
  than to the spine, which is where it goes after a first Begin. Shell knows
  which case applies: `goHome` sets a flag that the reactivation effect reads.
- **Opening another subject does not fade out first.** Its Begin calls
  `onopen`, which marks the subject begun and navigates. If the reader
  cancels at the unsaved-note guard, the start screen stays as it was. With
  a fade it would have been left invisible over an inert shell.
- **A subject chosen in the list opens begun.** The reader has already
  chosen it on a start screen, and showing a second one would be a stutter.
  A bare `/<subject>` link from outside still opens on its start screen.
- **One _Continue_ offer, for the selection.** The server now loads the
  reader's place in every served subject (`readerData.places`), one
  `lastVisited` per subject. That replaced `here`. The second _Last read ·
  other subject_ offer became a _Last read_ note on that subject in the
  list. The current subject's offer is left out once the reader has begun
  it, because Begin already returns them there and the place loaded with
  the page would be stale.
- **The palette follows the selection.** The subject's start look carries
  its palettes and first frame's palette name, so this cost nothing, and a
  subject list that changes the title but not the colours read wrong.
- **The look endpoint is a read under `/api`**: `GET /api/start/<subject>`.
  A `/[subject]/…` route would have shadowed a frame with the same name.
  It goes through `servedSubject`, so an unknown or path-like id is a 404,
  and `subject-scope.test.ts` covers it with the other APIs.
- **The sample is evenly spread along the main spine**, first frame first
  (`engine/start.ts`, `RING = 10`). AI's 66 frames show their whole sweep,
  not the 1840s. Western civ has 16 and shows 10 of them.
- **A listbox, not a list of buttons.** Selection and activation are
  different acts here: selecting changes what the screen shows, and Enter
  or Begin opens it. That is the listbox pattern
  (`aria-activedescendant`, focus stays on the list). ←/→ move as well as
  ↑/↓, because the list lies flat on a phone.
- **One button style for the gear and Home**: `engine/ui/IconButton.svelte`,
  which forwards the rest of its props and exposes `focus()`. Settings'
  gear moved onto it. There is no copy of `.gear`.

## What shipped

- **Engine:** `engine/start.ts` (`startLook`, `RING`) and its test;
  `engine/ui/IconButton.svelte`; `engine/ui/icons/` (home, loom, shuttle,
  return, title-card). StartScreen has the subject listbox, the ring, and a
  Begin that opens the selection; the "Or open" row is gone. Settings uses
  IconButton. Shell has `onhome`, the Home button in a `.corner` with the
  gear, and focus back to Home.
- **Route:** `GET /api/start/[subject]`.
- **Page:** `readerData.places` replaces `here` in the load. The page adds
  the selection, looks fetched once and cached, the palette of the selected
  look, the list with _Last read_, the selection's resume offer, `home()`
  and `open()`.
- **Docs:** design.md §Start screen (Home, the list, the selection's look),
  §Several subjects (the chooser), §Reader data (last visited); the
  roadmap; CLAUDE.md and its Copilot mirror.

## Verification

- `just check`: svelte-check (0 warnings), prettier and eslint, and vitest.
- **New tests:** the start look's palette, an even sample of AI reaching its
  last tenth, a small subject shown whole, the endpoint's 404s and a served
  look, the listbox (this subject selected, `aria-activedescendant`, above
  the title), the ring inside the `aria-hidden` stage, no list with one
  subject, Home named, before the gear and in its style, no Home on a
  shell without `onhome`, and the selection's _Continue_ with _Last read_
  in the list.
- **Negative test:** a first-ten sample (`drawn[i]`) fails "samples a long
  subject evenly along the spine".
- **In a real browser** (Playwright, Chromium, the dev server, keyboard
  only, `.scratch/s013.mjs`):
  - Shift+Tab from Begin focuses the listbox.
  - ↑ selects AI: the title, palette and ring change.
  - Esc returns to the shell, with focus on the spine.
  - After two →, Home opens the start screen on western civ. Esc returns to
    `/western-civ/greek-inquiry`, unchanged, with focus on Home.
  - Home, ↑ and Enter open `/ai/…` begun, with no dialog.
  - Screenshots at 1400×900 and 390×800 show the list down the left and
    flat above the title respectively.

## Repaired in passing

- **`bind:this={tabEls[i]}` warned on every page load** (Svelte's
  `binding_property_non_reactive`, in the dev console). `tabEls` was a plain
  array. It is now `$state`, and the warning is gone.

## Follow-ups

- None filed. The four runner-up icons are in the repo for later use, as
  3424 asked. Nothing uses them yet.
