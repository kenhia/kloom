# 023 — Exploring for fun: a 3D library graph, and random jumps

korg proposal 3452, covering 3449 (the 3D library graph) and 3437 (two
Random buttons). Branch `023-exploring-for-fun`.

## Goal

Two ways to wander the library rather than read it in order: the whole
library at once as a 3D force graph you can turn and fly through, and two
dice that jump to a random frame, in this subject or anywhere.

## Premise check

- **3437 holds.** The contents control is in the spine's HUD. Home and the
  gear share the tab row's corner. The page's `follow` is the one jump path
  (Back chip, browser Back). Shortcuts are remappable through `SHORTCUTS`.
- **3449 holds.** The 2D map and the start screen's "Map of the library"
  exist (sprint 019), every frame has a `topic` (sprint 020), and
  `3d-force-graph` was not yet a dependency. It is at 1.80.1, MIT, with
  `three` 0.186.1 (MIT) under it.
- kloom is not in the cross-project plan index.

## Decisions

- **3D is a switch on the map, not its own overlay.** The WI asked for it
  from the 2D map and from the start screen's library map, and both are
  the same `MapOverlay`. One "3D" switch beside Show as list covers both.
  It is off whenever the map opens, since the 2D map is the everyday tool.
  Show as list, or the switch again, returns to 2D. A node's "Show on the
  2D map" opens the 2D map centred on it.
- **Lazy twice.** The overlay imports `Library3d.svelte` only when the
  switch turns on, and the component imports `3d-force-graph` and `three`
  in `onMount`. **Measured** (`vite build`, the JS a subject page loads
  through its static imports):

  |                 | files |         raw |      gzip |
  | --------------- | ----: | ----------: | --------: |
  | eager, before   |    10 |   283,025 B |  99,698 B |
  | eager, after    |    12 |   287,524 B | 101,724 B |
  | 3D chunks, lazy |     3 | 1,545,836 B | 412,612 B |

  The 4.5 KB of eager growth is the dice, the two shortcuts, the switch and
  Vite's two small lazy-load helpers. No eager file contains three.js
  (grepped for `WebGLRenderer` and `three-forcegraph`), and in the browser
  the 3D chunks arrive only when the switch is turned.

- **`three` is a direct dependency** (with `@types/three`) because the
  component builds the solids itself. `3d-force-graph` only takes three
  as its own dependency. npm dedupes to one copy (0.186.1).
- **A solid for each subject's shape**, so colour is never the only cue in
  3D either. The mapping is sphere, cube, octahedron, tetrahedron,
  hexagonal prism and icosahedron, for the 2D circle, square, diamond,
  triangle, hexagon and star. The map's legend stays as it is, in 2D
  shapes. A name is a small grey sphere. Nodes are sized by their links.
- **Labels on the pointer, not sprites.** The WI allowed `three-spritetext`.
  290 floating topic labels would bury the graph, and would add a
  dependency. So the pointer's label says the frame's topic, title, subject
  and position (or a name and its description), and a click puts the same
  in the details with Go and Show on the 2D map.
- **The camera fit is our own.** `zoomToFit` measures node objects by their
  world matrices, which only a render updates. `onEngineStop` fires before
  the nodes are moved, so the first attempts fitted a ±1.3 box and parked
  the camera inside the graph. The fit runs a frame later, with
  `updateMatrixWorld` first. Even then, the library's fit takes in the
  nearest points, which left the graph a small knot mid-screen. `fit()`
  faces the middle of the frames and backs off only as far as their width
  and height need at that depth.
- **Motion.** 160 warm-up ticks (about half a second) before first paint,
  then a fit. Without reduced motion, the layout drifts four more seconds
  to rest, the camera eases out to it, and the graph turns slowly. A "Turn
  slowly" toggle stops it (WCAG 2.2.2), as does taking hold of the graph.
  The hovered node's links come forward with particles. **Under reduced
  motion** the layout stops at first paint, nothing turns, there are no
  particles, and flying to a node has no transition. Checked: two
  screenshots 1.5 s apart are byte-identical.
- **Decorative, and said so.** The canvas is `aria-hidden` and not a tab
  stop. A sentence of counts, and a table by subject under "Counts by
  subject", say what it holds, and every control is an ordinary button.
  Esc closes the map as ever.
- **Random is a jump.** Both dice go through the page's `follow`, so the
  Back chip, R and the browser's Back return from a random jump.
  `walkedFrames` is every frame a spine walks, trails included.
  `pickOther` drops the current frame before the draw, so every other
  frame is equally likely. "Anywhere" draws over the map's frame list
  (fetched once, as the map does), so it may land in the same subject, as
  the WI allows.
- **Placement and keys.** The one die sits left of the contents in the
  HUD, and the two dice sit left of Home, the first of Ken's two sketched
  spots. That keeps Home and the gear together, as on the start screen.
  The new shortcuts are D (dice) and W (wander), the ninth and tenth.
  They are remappable and scoped like the rest, and shown in the hint bar.

## What shipped

- `engine/random.ts` (`walkedFrames`, `pickOther`) with 5 tests.
- `engine/library3d.ts` (`library3dOf`: nodes, links, per-subject counts)
  with 6 tests.
- `engine/ui/Library3d.svelte`: the WebGL view, the fit, the details, the
  counts and "Turn slowly".
- `engine/ui/MapOverlay.svelte`: the "3D" switch, the lazy component and
  "Show on the 2D map".
- `engine/ui/Shell.svelte`: the two dice, the `random` and `anywhere`
  shortcuts, and the hint bar.
- The page: `random()`, a jump through `follow`.
- `engine/keys.ts`: D and W, tested with the other shortcuts.
- `vite.config.ts`: `server.fs.allow: ['engine']`. SvelteKit's dev server
  serves only its own directories, and the lazily imported engine
  component is requested on its own, so it was refused (403) until the
  engine was allowed. The production build was unaffected.
- design.md §The library in 3D and §Random, the map's 3D bullet, and D/W in
  §Interaction.

## Verification

- `just check`: svelte-check with no warnings, prettier and eslint, and
  vitest (807 tests, 11 of them new).
- **Negative tests, each seen failing:**
  - `pickOther` without the exclusion fails 3 of its 5 tests.
  - `library3dOf` without the registry check fails the "leaves out a
    mention of a name the registry does not have" test.
  - Restoring each passes.
- In Chromium (Playwright, dev server, SwiftShader WebGL), at 1400×900 and
  390×844:
  - **Random.**
    - D from the spine, 25 times in Physics: 21 distinct frames, never the
      same one twice running, never outside the subject.
    - 40 more presses landed on trail frames 14 times.
    - R and the browser's Back returned along the jumps, with the "↩ Back
      to…" chip.
    - W, 12 times, landed in Physics, Computing and AI, trail frames
      included.
    - Clicking either die jumps the same way, and focus stays on the spine.
    - The hint bar reads "…M map, D random and W anywhere…".
  - **3D, keyboard.**
    - From M on `feynman/nobel`, three Shift+Tabs reach "3D: the whole
      library", and Enter opens it in about 0.6–1.2 s. Focus stays on the
      switch.
    - The details open on "The 1965 Nobel Prize in Physics · you are here".
    - The Tab order runs Show as list, Close, Counts by subject, Go to,
      Show on the 2D map, Turn slowly. The canvas has no tabindex.
    - Esc closes the map and returns focus to the Map button.
    - From the start screen, "Map of the library", then 3D, then 3D again
      returns to the library view with focus on a node.
  - **3D, pointer.**
    - Hovering finds nodes (Quarks; The path integral; Hough transform, a
      name).
    - A click flies to the node and fills the details. "Show on the 2D map"
      opens "Map · Around Quarks" with focus on its centre.
  - The dark surface was checked on `ai/turing-machine`.
  - At 390px nothing scrolls sideways, and there were no page errors in
    any run.
  - Screenshots are in `.scratch/023/`: `wide-3d`, `wide-reduced-3d`,
    `phone-3d`, `*-picked`, `dark-3d-hover` and `dark-counts`.

## Repaired in passing

- **The roadmap had no entry for sprint 022.** Added, with 023.

## For Ken: the look

- The graph is dense at the library's size: 1,750 nodes and 2,952 links.
  Hiding the names (frames and connections only) would show the subjects'
  shapes more plainly. It would be a one-line filter, if you want it as a
  switch.
- The dice icons are hand-drawn SVG, one die and two.

## Follow-ups

- None filed.
