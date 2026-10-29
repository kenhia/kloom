# 056 — Printing a frame

## Goal

korg proposal 4156, covering korg 3497: one slice of the low-hanging-fruit
program korg 4162, run as a karc leg on kai. Ken printed a frame (Keeping
Watch, "Navy nursing began with twenty") and got the app rather than the
frame. The reading printed as a scrolling box, cut off at the box's height.
The HUD, the timeline, the tabs, the AI box and the hint bar all printed,
on a tinted background. The fix is a print stylesheet that prints the
scene, then the whole reading, on a white page.

## Decisions

- **Premise held** (checked at start). There was no `@media print` or
  `print-color-adjust` anywhere in `engine/` or `src/`. The reading is
  `.reading { overflow-y: auto }` inside a `100dvh` shell, which is exactly
  the cut-off Ken saw. kloom is not in the cross-project plan index, and
  `just grow-pending` found nothing pending.
- **Calls already made by the overseer:** scope exactly as 3497 spells it,
  no `publish-public` (it needs Ken's word), and 3497 is left `resolved`,
  not done, until Ken prints a frame on his inkjet.
- **A stylesheet, not a print view.** The print rules live in the three
  components whose markup they hide or reflow (`Shell`, `SpinePane`,
  `Narrative`), each beside its screen rules, plus `src/app.css` for the
  page and dialogs. There is no print button. The browser's own Print is
  the control, and the User's Guide says so.
- **The palette is overridden with `!important`.** The shell and the spine
  pane each set `--background`, `--ink` and the rest inline, and only an
  important declaration beats an inline one. Overriding the variables,
  rather than restyling every element, keeps everything painted from them
  consistent: the drawing's `--line` and the accent words become ink.
- **A chart keeps its colour through `--print-accent`.** That is the
  accent of the frame's light palette, set on the shell. A dark palette's
  accent is pale and would vanish on white, and every dark palette in every
  subject has a light counterpart (checked), so `paletteFor(…, 'light')`
  always gives one that reads on white.
- **Citations open in two ways.** CSS cannot open a `<details>`, but
  Chrome's `::details-content` can be made visible, which also covers
  headless print-to-PDF, where `beforeprint` never fires. Other browsers get
  the `<details>` opened on `beforeprint` and closed again on `afterprint`.
- **The header prints on page 1 only**, at the top, not as a repeating
  running head. A `position: fixed` header repeats in Chrome but would
  overlap the reading unless the page margins were reserved for it. The
  item allows a header or a footer, and one at the top does the job.
- **The reader's layer does not print**, as 3497 says: annotation
  highlights and their ✎ buttons, kept answers (`.qa`) and a name's open
  card. Trail buttons are left off too, because they are controls and not
  content. Connections print, since they are content with a _why_.
- **Pages are Chrome's.** Below 760px the phone layout's rules apply,
  because a printed page is about 720px wide. The print block comes after
  those rules and undoes the heights and the extra border they add.

## What shipped

- `@media print` in `engine/ui/Shell.svelte`, which stacks the panes, sets a
  white page and dark ink, hides the tab row, hint line, AI pane, notes and
  dividers, and adds a print-only header with the subject, title and URL.
- `@media print` in `engine/ui/SpinePane.svelte`. The scene prints as it
  stands once it has entered: no animation, the drawing fully drawn at
  3 in, and the headline and counter at fixed sizes. The brackets, the HUD
  tools, the index and the timeline are left off.
- `@media print` in `engine/ui/Narrative.svelte`. The reading prints whole,
  with no controls, trail buttons, kept answers, annotation marks or name
  cards. Citations and edits print opened, figures keep their colour, the
  chart accent comes from `--print-accent`, and there are no page breaks
  inside figures, tables, code, quotations, citations or connections, or
  straight after a heading. A photograph is capped at 4.5 in. Also a
  `beforeprint`/`afterprint` pair for the `<details>`.
- `src/app.css`: a white page, `color-scheme: light`, and no dialog prints.
- `just print-check` (`create-tools/print-check/print_check.mjs`): 46
  checks over four cases in print-emulated Chromium, each also saved as a
  PDF in `.scratch/print-check/`.
- docs/design.md §Printing, and a "Printing a frame" section in the User's
  Guide.

## Verification

- `just print-check`: 46/46. The cases are ai/compute in dark and in light
  (a chart and two photographs, 7 Letter pages), western-civ/beethoven-ninth
  in dark (the longest reading, 5–6 pages) and nursing/sacred-twenty in
  light (Ken's frame, 5 pages).
- **Negative-tested.** I planted three faults one at a time: the reading
  back to `overflow-y: auto`, the tab row no longer hidden, and the
  citations' `content-visibility` removed. Each run exited 1 with the
  expected failures (8 of 46 for the first two together, 4 for the third),
  and the run went back to 46/46 once the code was restored.
- **Looked at, not only asserted.** I took print-emulated full-page
  screenshots at 720px. The header line comes first, then the scene with
  its drawing in black, one rule, and the reading in black on white. The
  TPU photograph is in full colour. The training-compute chart has dark
  bars and its last bar in the light palette's purple. Sources and the
  opened citations follow. Looking at them turned up three fixes the
  assertions had passed: a doubled rule under the scene (the phone layout's
  `border-top`), a photograph taking most of a page, and Sources' two-digit
  numbers off the left edge. All three are fixed.
- `just check` green (1,715 tests). `just hud-check` 145/145, since Shell
  and SpinePane changed.
- Not done here, as the brief says: Ken printing a frame on his colour
  inkjet. 3497 stays `resolved` until he has.

## Repaired in passing

Nothing.

## Follow-ups

- None filed. "Print with my notes" is named in 3497 as a later idea, not
  a defect, and stays in Ken's hands.

## Deployed

2026-10-28 19:20 PDT, from merged `main` (`940db247`, PR #66) by
`just deploy` (the `.sprint-deploy` recipe) to the kai service. `just
verify` passed all ten of its checks (both doors read, writes and reader
data gated, the library served, compressed pages); `DEPLOYED` reads
`940db247`. Then `print_check.mjs --url http://127.0.0.1:4891`, run against
the live service rather than a dev server, passed 46/46 over the same four
cases.

**Not published to the public reader site** (kloom.kenhiatt.us). `just
publish-public` waits for Ken's word, as the overseer's clearance said.
3497 stays `resolved` until Ken prints a frame on his inkjet.
