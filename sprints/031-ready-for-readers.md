# 031 — Ready for readers

## Goal

korg proposal 3479, covering korg 3469 and 3477: polish that anyone
outside the house would see on day one, done before the weekend's
public-site brainstorm (3458). The scene's counter can never overlap the
metadata, and About ends with an accuracy disclaimer and a way to report
an error.

## Decisions

- **Premises held and widened** (checked at start). 3469 filed 13 frames
  outside chemistry at 1400×900, and Ken's comment found 49 of
  chemistry's 66 at 1280×800. Measured across the whole library, before
  any change, with the new checker: the counter sat over the metadata on
  **292 frames at 1280×800, 15 at 1400×900 and 361 at 390×844**. Counting
  the drawing riding up into the top HUD as well, that was 2014 misfits in
  615 frames. kloom is not in the cross-project plan index.
- **The cause was not where 3469 put it.** The counter was never laid out
  independently. It already has its own row of the spine's grid (the
  bottom HUD). The scene was centred in a `1fr` row and free to overflow
  it, and nothing in it gave way, so a tall scene spilled into both HUDs.
  Ken's decision (2026-10-01, "put the counter in the flow": headline,
  metadata and counter in one grid, the counter in its own row) is met by
  keeping the scene inside its row. Moving the counter into the scene
  would not have helped, since the scene would then have spilled into the
  timeline instead.
- **The drawing is what gives way.** The scene is a flex column that fills
  its row (`minmax(0, 1fr)`). The headline and metadata take their height,
  and the drawing shrinks (`flex: 0 1 auto`, the SVG's `max-height: 100%`)
  into what is left. A scene that already fitted lays out exactly as
  before, centred.
- **Headline type by length** (Ken's `clamp()`): a `--fit` factor of 1 up
  to 26 characters (headline, space, accent; the median is 28, and 43 of
  615 headlines are under 20), then `sqrt(26 / length)`, floored at 0.7.
  The longest headline, feynman `last-days` at 52 characters, gets 0.71.
  It scales both the viewport term and the 4.75rem ceiling, with a 1.5rem
  floor (it was 1.75rem).
- **The check is a recipe, not part of `just check`.** It needs a browser
  and a running app, and the repo has no browser dependency. Adding one to
  make a gate is what the conventions rule out. `just scene-fit` finds
  the machine's Playwright and Chromium the way `contact_sheet.py` finds
  its Chromium, and starts its own dev server unless one is answering. The
  author-subject skill now runs it before a subject is called done.
- **The disclaimer is for a stranger.** Ken's wording, lightly edited and
  keeping all five points, written for a reader who is not Ken, because
  the public site (3458) will show the same About. It names the in-app
  route concretely: select the words, press A, tick _Agent review_.
- **The `content-feedback` label was created on GitHub** (`gh label
create`), because an issue form applies only labels that already exist.

## What shipped

- `engine/ui/SpinePane.svelte`: the scene keeps to its row, and the
  headline has a `--fit` scale.
- `engine/ui/About.svelte`: "A note on accuracy" after Credits, with a
  link to the issue form.
- `.github/ISSUE_TEMPLATE/content-feedback.yml` (subject, frame, the
  quoted text, what is wrong, a source if known) and `config.yml`, which
  keeps blank issues open for code bugs.
- `create-tools/scene-fit/scene_fit.mjs` and `just scene-fit [subject…]`:
  every frame at 1280×800, 1400×900 and 390×844, with motion reduced,
  four pages at once, in about four minutes for the library.
- `docs/design.md`: §Scene fit is new, and §About gains its last bullet.
  `skills/author-subject/SKILL.md` runs the check.

## Verification

- `just scene-fit` on all 615 frames reports **0 misfits** at all three
  sizes (2014 before). It is also 0 for feynman, chemistry and
  mathematics at 1024×600 and 360×640, two sizes outside the gate.
- **Negative test:** with the regression planted (the drawing set to
  `flex: none`), `just scene-fit feynman` reported 82 misfits and exited
  1. With the code restored it reported 0.
- Screenshots of the worst frame, feynman `last-days`, before and after,
  at 1280×800 and 390. The staged entrance runs with motion on: at 0.4s on
  chemistry `pcr` the drawing is part drawn and the headline is still at
  opacity 0, with its space held so nothing shifts. At 3.4s both are at 1.
  Reduced motion is the state the checker measures.
- About, keyboard-only at 390×844: Tab reaches About, Enter opens it, Tab
  runs through the two existing links and then "report it on GitHub", and
  Tab past the last link closes the panel (as before). Esc closes it and
  returns focus to the About button. The panel spans x 24–382 of 390 with
  no horizontal scroll, and the link targets
  `issues/new?template=content-feedback.yml`.
- `just check` green.
- The issue form's preview on GitHub waits for the merge, since GitHub
  reads templates from the default branch.

## Repaired in passing

Nothing outside the covered items.

## Follow-ups

- None filed. Running `just scene-fit` in CI would mean a browser in the
  workflow. That is worth weighing with the public site (3458), not
  before it.
