# 038 — Colours by section: calmer palettes, the scene and the reading coloured apart, brightness sliders, and every subject re-paletted

## Goal

korg proposal 3498, covering 3495. Ken, 2026-10-02: mixed palettes switch
between dark and light on nearly every step, which is distracting. Dark
readings can be hard to read, and light is a bit bright for him. He wants
this in before he shares kloom with family. The decisions are his, on
3495: colour by section, colour the scene and the reading apart, add
brightness sliders, stop the authoring rule that made frames alternate, and
re-palette every subject by section in content. One or two subjects are to
be shown to him before the rest are committed.

## Premise, checked at start

- **The cause holds.** `skills/grow/SKILL.md` said neighbouring frames
  should "keep alternating". `skills/author-subject/SKILL.md` said the
  plan's palettes make "dark and light alternate along the spine".
  `subject_plan.py --check` warned where "a palette repeats".
- **The counts hold.** `create-tools/palette-switches/palette_switches.py`,
  written for this sprint, measured the same figures as 3495's table. The
  one difference is western-civ at 32% (6 of 19), which 3495 rounded to 33%.
- No grown content was pending (`just grow-pending`). kloom is not in the
  cross-project plan index.

## Decisions

- **Which side is which.** The scene pane wears the scene's palette. That
  covers the scene, its HUD and the HUD's pop-ups (contents, bookmarks, my
  notes), and the note editor that takes the scene's place. The shell wears
  the reading's palette: the narrative, the notes, the tab row with the
  gear and its pop-up, the AI pane in every layout, and the hint line. Text
  goes with the reading, which is what a reader fixing it to light wants
  calm. The map takes the scene's scheme when opened from the HUD, and the
  reading's when opened from a name card.
- **By section maps the frame's own palette.** By section, a frame wears
  its own palette in its section palette's scheme, through `counterpart`,
  as 3495 specified. Once a subject is re-paletted, every frame in a section
  wears the section's palette, so _By section_ and _Each frame_ look the
  same. The engine mode still matters for content not yet re-paletted, and
  for grown frames.
- **The dedications need no special case.** Blood's and nursing's
  dedication frames are each a one-frame segment, so their section is
  themselves.
- **Brightness is a pick from a fixed list too.** The registry's rule (every
  setting is a pick from a fixed list) holds. A slider is a `range` control
  over the choices' indices, and each step is 0.025 OKLCH lightness. Light
  runs from six steps dimmer to one brighter, and dark from two darker to
  six lighter. Ken asked for light to be less bright, so most of the light
  range dims. Every colour of a palette moves by the same amount, so the
  palette keeps its look. Then a foreground under 4.5:1 is pushed away from
  the background until it holds. At baseline every palette in the library
  already meets 4.5:1 for ink, muted, accent and line (measured at the
  start: the lowest was western-civ parchment's muted at 5.01), so 0 is an
  exact identity.
- **The range is where the guarantee holds, and a test says so.**
  `engine/colour.test.ts` checks every palette of every subject at every
  step. Widening the light range to -20 failed it ("ai/drafting at -20: ink
  2.87"), which is the negative test.
- **Migration.** On load, `kloom.palette` is mapped onto `kloom.scene` and
  `kloom.reading`, once, and only when neither is stored: Mixed becomes By
  section and Same as scene, Dark becomes Always dark for both, and Light
  becomes Always light for both. The old key is left in place, unread.
- **The authoring rule.** `subject_plan.py` takes a `palette` on every
  segment, and `spine.json` keeps it. `--check` no longer warns on a
  repeat. It warns where a frame's palette is not its section's and its
  plan entry gives no `paletteWhy`, and where a segment's frames name
  palettes but the segment names none. Grow and author-subject now say: a
  palette per section, chosen for its era or theme, with the subject's
  balance kept across sections; a trail takes its anchor's section's
  palette unless its own era calls for another; never alternate.
- **Western-civ: segment palettes only.** Ken said to leave it alone unless
  a segment is genuinely mixed. Its night frames (writing, scriptorium,
  shakespeare, maxwell) begin or end runs that cross segment boundaries.
  Without segment palettes, _By section_ would take each segment's first
  frame and turn all of Antiquity dark, which is not "as it is" either. So
  each segment names its majority palette, and no frame was rewritten.
  _Each frame_ still shows the hand-curated runs.
- **The re-palette is scripted from one map.**
  `create-tools/palette-switches/sections-038.json` holds every subject's
  section and trail palettes. `repalette.py` applies it: the segment
  `palette`s, every frame in a section to match, and the subject's plan
  under `create-tools/subject-plan/` too, so `--check` reports no drift.

## The re-palette: shown first, then the rest

Physics and blood were applied first, with western-civ's segment palettes,
and shown to Ken on a review page: screenshots of every physics and blood
section, before and after strips for all ten subjects, and the seven
proposed maps (https://claude.ai/artifact/Ty3dR3rRekUQodW3u9r1k6). He
approved all of it as proposed ("Looks good, continue"), and the other
seven were applied from the same map.

Switches between dark and light along the main spine
(`palette_switches.py`), before and after. After the re-palette, _Each
frame_ and _By section_ read the same everywhere except western-civ,
whose frames kept their own palettes:

| Subject     | Before (each frame) | After (by section) |
| ----------- | ------------------- | ------------------ |
| ai          | 60% (24/40)         | 12% (5/40)         |
| blood       | 92% (36/39)         | 8% (3/39)          |
| chemistry   | 100% (52/52)        | 8% (4/52)          |
| computing   | 97% (35/36)         | 14% (5/36)         |
| feynman     | 100% (33/33)        | 12% (4/33)         |
| making      | 100% (45/45)        | 11% (5/45)         |
| mathematics | 100% (48/48)        | 8% (4/48)          |
| nursing     | 93% (38/41)         | 5% (2/41)          |
| physics     | 100% (44/44)        | 9% (4/44)          |
| western-civ | 32% (6/19)          | 11% (2/19)         |

Before the re-palette, _By section_ alone would have read blood at 0%:
every one of its sections happened to open on a dark frame, so the default
would have turned the whole subject dark. The content pass is what keeps
each subject's balance. 314 frames were rewritten, every segment and trail
of every subject names its palette, and the dedication frames kept theirs
(each is its own one-frame section).

## What shipped

- `engine/colour.ts`: OKLCH conversion, WCAG contrast and `brighten`.
- `engine/settings.ts`: Scene colours, Reading colours, Light and Dark
  brightness, `migratePaletteSetting`, `sectionPalette`, `framePalettes`.
- `Segment.palette` (`engine/model.ts`), checked by `engine/validate.ts`.
- `SpinePane` takes the scene's palette; `Shell` sets the reading's.
- The settings pop-up shows a `range` control as a slider with its label
  said, and gathers the advanced rows under a collapsed Advanced.
- The start screen takes the first section's palette, in the scene colours.
- `just colours-check` (`create-tools/colours-check/`).
- `palette_switches.py` and `repalette.py` (`create-tools/palette-switches/`).
- The grow and author-subject skills, and `subject_plan.py`.
- `docs/design.md` §Colours, and every line that named the Palette mode.

## Verification

- `just check`, after the whole re-palette: 1,329 vitest tests pass, including the contrast guarantee
  at every slider step, the migration, `framePalettes` and the rendered
  panes coloured apart. svelte-check, prettier, eslint and the tools'
  tests are clean.
- `just colours-check`, 92/92 at 1280×800 and 390×844, keyboard-only:
  - the panes are coloured apart;
  - the old Palette setting migrates for Mixed, Dark and Light;
  - both sliders, at both ends, keep 4.5:1, read off the page's computed
    colours;
  - the pop-up stays on screen with no sideways scroll;
  - the choices are remembered across a reload.

  The negative test: with the shell planted to wear the scene's palette,
  the check failed on "the scene stays dark while the reading turns light".

- `just keys-check`: 70/70. `just scene-fit`: 0 misfits in 616 frames,
  every subject at 1280×800, 1400×900 and 390×844.
- One `just check` run, made while the seven subjects were being
  rewritten, failed the frame endpoint's ETag test (a 200 where a 304 was
  expected): the library was rebuilt between its two requests. Run alone
  three times, and in a full `just check` once the content had settled,
  it passed.
