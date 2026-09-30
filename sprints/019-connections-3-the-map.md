# Sprint 019 — Connections 3: the map

korg proposal 3445, covering 3441. Branch `019-connections-3-the-map`.
Phase 3 of the connections design (korg 3399), after phase 2 (sprint 018),
so the layout could be tuned on real density.

## Goal

The graph index (sprint 017) has 222 frames, 107 connections and 1,111
names, and until now a reader saw it one frame at a time. The map draws it:
a full-screen overlay on the current frame's neighbourhood, with the
library of subjects and a name's frames as other views, that a keyboard
and a screen reader can use as well as a pointer.

## Premise check

- **Holds.** Phase 2 shipped (sprint 018), with density figures for the
  map's defaults. The contents control (3433) that the map's button sits
  beside is in the HUD. No cross-project plan lists kloom.

## Decisions

- **The whole graph goes to the browser, once.** A page loads only its
  own subject's links, but a neighbourhood crosses subjects and the
  library needs them all. `GET /api/map` serves `mapDataOf(servedGraph())`
  (about 340 KB of JSON), fetched when the map first opens and dropped
  after a grow. Each view is then computed in the browser, in under 25 ms
  for the largest (a subject's 69 nodes). Cutting the payload (frame
  indices in place of keys, descriptions on demand) can wait until it
  shows.
- **The two-step default, with names ranked by rarity.** Sprint 018's
  figures: two steps of connections reach a median of 2 frames (max 18),
  but one step through a shared name reaches a median of 22 (Richard
  Feynman is in 63). So a neighbourhood shows only the centre's own names.
  Frames sharing them are ranked by the sum, over the shared names, of one
  over the other frames each name is in, and only 8 are kept, with a note
  saying how many more there are. The densest case, `ai/turing-machine` at
  two steps, has 31 nodes, and `feynman/nobel` 21: 60 frames share a name
  with it, and the rarest-first rank picks Watson and the double helix over
  Feynman himself.
- **Still, not animated.** The layout runs to rest (300 ticks, seeded by
  the view) before anything is drawn. So "static under reduced motion"
  holds for every reader: nothing on the map ever moves. A test makes
  `Math.random` throw, so a layout that reached for it would fail the gate.
- **d3-force is the one new dependency** (3.0.0, with `@types/d3-force`).
  It was the WI's suggestion and gives `randomSource`. Its three small
  d3 dependencies come with it.
- **A shape for every subject.** The subjects' own accents are all golds
  (dark palettes) and reds (light), so they cannot tell subjects apart.
  The map takes its own surface, light or dark after the palette it opens
  over, and the dataviz reference palette's categorical hues. The
  validator, all-pairs as a node-link map needs: blue, orange, aqua and
  violet pass on the light surface. On the dark one, violet and blue fall
  to ΔE 9.8 (1.9 for protanopia), and no fourth validated hue passes all
  four checks. So colour is never the only cue. Each subject has a shape
  (circle, square, diamond, triangle, then hexagon and star), the legend
  names both, and the list says the subject in words.
- **A fourth view, the subject.** The WI's library says "click a subject
  to open its neighbourhood of frames". Its frames that have connections
  are drawn, with where they lead. The 29 of Computing's 70 with none are
  counted in a note, not drawn: unconnected, they would only float.
- **Click centres, Enter goes, Space is a click.** As the WI has it. For
  the pointer, the details under the map carry Go and Centre. A
  double-click also goes.
- **Nodes are HTML buttons over an SVG of lines.** Focus rings, labels and
  the accessible names come from the platform. The lines are `aria-hidden`,
  and what they say is in the details (a connection's _why_) and in the list.
- **A native `<dialog>`**, so the page is inert behind it and Esc is the
  browser's own. It is `data-own-keys`, so the page's shortcuts stand down
  inside it (checked: the spine did not move on → or S).
- **The list is the phone default** (below 40rem), as the WI allowed. The
  map still works at 390px, with long labels waiting for focus.

## What shipped

- `engine/map.ts`: `mapDataOf`, `MapIndex`, `viewOf` (neighbourhood,
  library, subject, name, each with list sections), `layoutView` (seeded,
  rings that widen with their nodes), `placeLabels`, `stepFrom` (arrow keys)
  and `subjectSlot`. 15 tests.
- `src/routes/api/map/+server.ts`, with a test against the real subjects.
- `engine/ui/MapOverlay.svelte`: the dialog, its four views, the step
  control, "Show as list", the details, the legend, the map's own Back
  (and Backspace).
- The HUD's map button, right of the contents, and M (`kloom.key.map`),
  the eighth remappable shortcut, in the hint bar. "Map of the library" on
  the start screen. "Show on the map" on a name card that appears in more
  than one frame.
- design.md §The map, and M in §Interaction.

## Verification

- `just check`: svelte-check clean, prettier and eslint clean, 695 tests.
- Negative tests, each seen failing: an uncapped shared-name list, an
  arrow step with no angle limit, and a `Math.random` random source. The
  last passed the first determinism test (d3 only draws random numbers for
  nodes that coincide), so the gate gained the `Math.random` test.
- In Chromium (Playwright, dev server), at 1400×900 and 390×844:
  - `ai/turing-machine` (the densest), `western-civ/printing-press`
    (sparse) and `feynman/nobel` at one and two steps; the library, the
    Computing subject and Alan Turing's name view. Screenshots are in
    `.scratch/shots/` (turing-2, printing-press-2, nobel-2, library,
    subject, name, turing-phone, turing-phone-map).
  - **Keyboard only:** M from the spine opens on the centre, "you are
    here". The arrows move between neighbours, Home returns to the centre,
    Space on a subject opens its view, Backspace steps back, and Esc
    returns focus to the button that opened the map. Enter on a Computing
    frame jumped there with the "↩ Back to We built a machine of PAPER"
    chip, and focus landed on the spine. From a name card, Show on the map
    opened Alan Turing's view, and Esc returned focus to the name.
  - The same neighbourhood opened twice laid out identically. No page
    errors.

## Repaired in passing

- **The roadmap's Next still listed phase 2**, which shipped in sprint 018,
  and 018 had no entry. Both are fixed.

## For Ken: the look

The proposal suggested showing you the neighbourhood before building the
other views. This session ran without you, so all four are built. Your
reaction is still the next step, and the screenshots above are the quickest
way in. The open questions of look, none of them blocking:

- **Frame labels are headlines** ("We built a machine of PAPER."). On the
  map most of them start with "We", so the position label or the accent
  word alone might identify a frame faster.
- **The subject view is busy** at Computing's 41 connected frames, even
  with the rings widened. Dropping the other subjects' frames, or showing
  only one segment, would thin it.
- **The two-step default and the cap of 8** are from sprint 018's figures,
  not from use.

## Follow-ups

- None filed. The look questions above are for Ken's reaction on the
  branch, and change nothing another item depends on.

## Deployed

2026-09-29, `just deploy` (the `recipe: deploy` in `.sprint-deploy`) to the
kloom service on kai. It ran from merged main `161fd30`, then again from
`67af638` after a one-line fix (PR #22). Verifying the first deploy found
that screen readers heard the library's first subject called "centre"; an
edit to the announcement had missed after formatting. Both runs built the
app, restarted `kloom.service`, and `just verify` passed all eight door
checks. The content clone is at `67af638` on `grow/kai`.

Verified live on the ssh door (:4891), on this sprint's own behaviour:

- `GET /api/map` serves 4 subjects, 222 frames, 107 connections and 1,111
  names. `/ai/turing-machine` carries the map button, `Map (M)`.
- Keyboard only, in Chromium against the service:
  - The start screen's "Map of the library" opens the library, with no
    centre announced.
  - The arrows and Home move between subjects, and Space opens the
    Computing subject. Backspace steps back, and Esc returns focus to the
    button.
  - M on `ai/turing-machine`, then Space on Alan Turing, opens his name
    view. Enter on a Computing frame jumps to `/computing/tunny` with the
    "↩ Back to We built a machine of PAPER" chip, and focus lands on the
    spine.
- No page errors, and no errors in the service's journal since the restart.
