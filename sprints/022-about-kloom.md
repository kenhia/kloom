# 022 — About kloom: the book it would make, library stats, and settings on the start screen

## Goal

korg proposal 3457, covering korg 3455 and 3456. Ken asked, "if kloom was a
book, how many pages would it be?", and wanted the answer in the app. Also,
the settings could only be reached from inside a subject. So: count the
narratives live (3455), and give the start screen an About control and the
settings gear in its upper right (3456).

## Decisions

- **Premises held.** The start screen had no gear and no settings.
  `engine/ui/reading-text.ts` is browser-only (it walks the DOM), so the
  count needed a server-side equivalent. kloom is not in the cross-project
  plan index.
- **Counting as the reader sees it, without a DOM.** `engine/stats.ts`
  renders each reading with the reader's own markdown renderer and strips
  the HTML to text. Block tags become breaks and inline tags are removed,
  so `_cathode_s` stays one word. Charts are inlined as empty markup, so
  their labels are not counted; that matches `reading-text.ts`, which skips
  `svg`. A picture's credit is never rendered, and alt text goes with its
  tag. A word is a whitespace token with a letter or digit in it, so a lone
  em dash does not count. The frame's scene and citations are never read.
- **Live, and no cache.** The item's premise was that the server loads
  every subject per request. It does, but only the subject being opened
  and a light graph read of the others, so there was no subject index to
  hang a cache on. Counting from the raw subjects (`readSubject`: no
  validation, no SVG sanitising) takes about 150 ms for the whole library
  on kai, and only when About is first opened (`GET /api/stats`). A cache
  would only add a way to be stale. It waits on the grow gate, as
  `servedGraph` does.
- **A frame counts when a spine walks it** (main or trail) and it has a
  reading. A stray directory on no spine is not a frame the reader can
  reach, and is not counted.
- **Library pages are the whole library's words over 275**, not the sum of
  each subject's rounded pages: it is one book.
- **`just stats` runs the engine's TypeScript through Vite's module runner**
  (`runnerImport`, already a dependency). Node's type stripping cannot load
  `engine/`, whose imports have no extensions, and adding `tsx` for one
  recipe would break the no-dependencies-for-a-gate rule. `statsReport`
  prints a Markdown table for sprint records.
- **About is a pop-up like the gear's, not a modal.** The start screen is
  already a modal dialog. About uses the settings pattern: an
  `aria-expanded` button, a `role="group"` panel after it in the tab
  order, Esc closing it with focus returning to the button, and a pointer
  press outside closing it. It also closes when Tab moves focus out of it,
  so it never sits over the gear. The per-subject figures are a real
  `<table>` with row headers and a (visually hidden) caption. The library
  figures are a `<dl>` labelled by its heading.
- **Esc on the start screen.** The start screen begins on Esc. It now
  ignores an Esc a pop-up already handled (`defaultPrevented`), so closing
  About or Settings does not also leave the start screen.
- **One set of key-clash warnings.** The "B is set for bookmark and note"
  text moved from `Shell.svelte` into `keyWarnings` in `engine/settings.ts`,
  so the gear says the same thing on both screens.
- **The build stamp** is `git log -1 --format='%h · %cs'`, read by
  `vite.config.ts` and `define`d as `__KLOOM_BUILD__`. `just deploy` builds
  from the commit it ships, so the stamp names the deployed app. The
  subjects come from the content clone, which the stamp does not describe.
  The stamp is empty outside git, and About then leaves the line out.

## The figure

`just stats` on 2026-09-30, on this branch (the repo's content, not the
service's grow branch):

| Subject     | Frames | On trails | Trails |   Words | Pages |
| ----------- | -----: | --------: | -----: | ------: | ----: |
| ai          |     66 |        25 |      4 |  49,619 |   180 |
| computing   |     70 |        33 |      7 |  58,509 |   213 |
| feynman     |     62 |        28 |      5 |  46,804 |   170 |
| physics     |     68 |        23 |      4 |  59,181 |   215 |
| western-civ |     24 |         5 |      2 |  11,213 |    41 |
| **Library** |    290 |       114 |     22 | 225,326 |   819 |

**About 819 pages** at 275 words a page, narratives only: 225,326 words.
The planner's crude estimate was about 231k words and 840 pages; the
difference is the markup, alt text and credits the real extraction leaves
out. The library also holds 286 images, 69 charts, 274 tables, 2,874
citations, 281 connections and 1,461 names.

## Verification

- `just check`: svelte-check (no warnings), prettier and eslint, vitest.
  New tests are `engine/stats.test.ts` and `src/routes/api/stats/stats.test.ts`.
  The fixtures cover the exclusions: a citation-heavy frame's twelve
  citations add no words, a scene's headline and metadata add none, a
  frame on no spine is not counted, alt text and a chart's labels are
  left out, and a table and a caption count.
- **Negative test:** with the `<svg>` strip removed from `wordCount`, the
  "leaves out … drawings" test fails. Restoring it passes.
- In Chromium (Playwright, dev server), at 1400×900 and 390×844, keyboard
  only:
  - The tab order from Begin is: Map of the library, About kloom,
    Settings, Image credit.
  - Enter on About opens it and loads the figures ("…a 819-page book").
    Esc closes it, returns focus to About, and leaves the start screen
    open.
  - Tab from About lands on Settings, which opens with Enter. Esc from
    inside a select closes it, returns focus to the gear, and leaves the
    start screen open.
  - Changing the palette mode there recolours the start screen.
  - Esc with nothing open still begins.
  - There were no page errors.
  - No page scrolls sideways. At 390px About spans x 24–382 and Settings
    x 24–382. Screenshots are in `.scratch/022/`.

## Repaired in passing

- **The settings pop-up was 34px wider than its cap** at phone width. Its
  `max-width` did not include its padding and border (content-box), so at
  390px the panel started off the screen's left edge, in the shell as well
  as on the start screen. It is now `box-sizing: border-box`, with the cap
  raised from 22rem to 24rem so its wide width is unchanged (384px). At
  390px it now fits (x 24–382).

## Follow-ups

- None filed.

## Deployed

2026-09-30, by `just deploy` from merged `main` (`79a78be`, PR #26) to the
kai service. `just verify` passed all eight door checks. The content clone
is on `grow/kai` at `79a78be`.

Verified live:

- `GET /api/stats` returns 200 on both doors in about 0.16 s, so it is an
  open read on the tailnet door. It reports 225,326 words and 819 pages:
  ai 180, computing 213, feynman 170, physics 215, western-civ 41. The
  service's content matches the repo's.
- The About panel shows "Build 79a78be · 2026-09-30".
- The keyboard walk from Verification was rerun against the ssh door at
  1400×900 and 390×844, and each step behaved the same:
  - About opened on "…a 819-page book".
  - Esc in About or in Settings closed the pop-up and left the start
    screen open.
  - The palette mode, changed from the start screen, recoloured it.
  - A second Esc began.
  - There were no page errors.
