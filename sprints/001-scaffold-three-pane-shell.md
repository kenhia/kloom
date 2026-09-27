# 001 — Scaffold + three-pane shell

## Goal

korg proposal 3362, which covers three work items:

- korg 3356: a SvelteKit + TypeScript scaffold with real `just check` gates.
- korg 3357: the subject-agnostic content model, with placeholder Western Civ
  frames.
- korg 3358: the three-pane shell (spine scroller with HUD, narrative, AI
  placeholder), with full keyboard control and a configurable Sync Narrative.

Out of scope: deployment, the AI backend (3360), real content (3361) and the
start screen (3359).

## Decisions

- **Premises held.** At the start the repo had only the harness and a
  deliberately failing `just check`, and kloom is not in the cross-project
  plan index.
- **Toolchain copied from koverwatch 001:** Svelte 5 runes, adapter-node,
  strict TS, vitest, prettier + eslint, and dev/preview bound to loopback.
  The one addition is `svelte-check --fail-on-warnings`. The Svelte a11y
  lints arrive as warnings, and accessibility is a requirement here, so a
  warning has to fail the gate.
- **`engine/` sits at the repo root, not under `src/`,** so extracting the
  framework later means moving a directory. It gets a `$engine` alias, and
  the kit TypeScript hook adds it to the tsconfig includes. `src/` is the
  SvelteKit wiring and is the only code that picks a subject
  (`src/lib/server/config.ts`, overridable by `KLOOM_SUBJECT` /
  `KLOOM_SUBJECTS_DIR`).
- **Content is read from disk per request** rather than bundled at build
  time. The grow jobs coming later write files, and the running site should
  show them without a rebuild.
- **File format:** JSON for structure (`subject.json`, `spine.json`,
  `trails/<id>.json`, `frames/<id>/frame.json`), markdown for the reading,
  SVG for the illustration. JSON rather than YAML front-matter keeps the
  parser in the standard library. The only runtime dependency is `marked`,
  for the reading pane. docs/design.md §Files has the full shape.
- **Frames live in one flat `frames/` directory,** and spines refer to them
  by id. Each frame sits on exactly one spine (main or a trail), and
  validation enforces that. A trail's anchor must be a frame on the main
  spine.
- **Validation collects every problem** as `where: what` lines, and
  `loadSubject` refuses to build an invalid subject. The unit tests load the
  real `western-civ` subject, so a content error fails `just check`.
- **Markdown is hardened; the SVG check is only a tripwire.**
  - Markdown shows raw HTML as text. Links and images are dropped unless the
    URL is http(s) or has no scheme, judged after decoding entities and
    stripping the control characters and whitespace a browser ignores.
  - The illustration check is a regex. It catches honest mistakes (script,
    style, embedding elements, links, handlers, character references), but
    it is not a sanitiser, and an adversarial SVG could still get past it.
    That is fine while every frame is hand-authored. A real allowlist
    sanitiser must be in place before 3360's grow jobs may write an
    illustration; that is recorded on korg 3360 as a precondition, and which
    dependency to use is that sprint's decision.
  - The two `{@html}` uses carry an eslint suppression that says why.
- **Interaction details the work items left open:**
  - A `WheelGate` makes one wheel gesture move one frame: deltas build up to
    a threshold, then a cooldown swallows trackpad inertia.
  - Home and End jump to the ends of the spine.
  - T enters the trail at the current frame. Esc leaves it, and also returns
    to the spine from anywhere in the AI pane.
  - Arrow keys typed into the AI field stay in the field.
  - Sync mode is remembered in `localStorage`, wrapped in try/catch.
  - The timeline is an ARIA slider. Clicking it or using the prev/next
    buttons gives pointer and touch users a way through without a wheel.

- **`cookie` advisory (GHSA-pxg6-pf52-xh8x): overridden, Ken's decision on
  korg 3350.** Kit 2.70.3, the latest release, declares `cookie: ^0.6.0`. On
  a 0.x version the caret allows only `<0.7.0`, so no upstream release can
  pick up the fix yet, and npm's `audit fix --force` would downgrade Kit to
  0.0.30. `package.json` scopes `overrides: {"@sveltejs/kit": {"cookie":
"^0.7.0"}}`, which resolves to 0.7.2. 0.7 keeps the parse/serialize API
  Kit uses (`src/runtime/server/cookie.js`) and only adds validation. Stay
  on 0.7, not 2.x, whose API changed. Drop the override once Kit's own range
  reaches 0.7. Evidence:
  - `npm audit` reports 0 vulnerabilities.
  - `just check` and `just build` pass.
  - The browser pass is unchanged.
  - A temporary `+server.ts` probe (since removed) exercised Kit's cookie
    code against the built server. It parsed `probe=abc; other=x%20y` to
    `x y` and set `probe=v%3D1%3B%20ok; Path=/; HttpOnly; Secure;
SameSite=Lax`.

## What shipped

- `engine/model.ts`, `validate.ts`, `load.ts`, `markdown.ts`,
  `navigation.ts`: the types, validation, loader and markdown renderer, plus
  the pure navigation logic (stops, HUD index and cursor, the wheel gate).
- `engine/ui/Shell.svelte`: the state, page-wide keys, wheel handling, frame
  palette as CSS variables with a transition, and a live region announcing
  each frame. `SpinePane.svelte` holds the HUD (corner brackets, chapter,
  index, position, counter) and the timeline with segment boundaries, trail
  branch markers and the red cursor. `Narrative.svelte` has the Sync button,
  the "Follow the spine" setting, reading, trails and sources.
  `AiPane.svelte` is a placeholder form that says it isn't connected yet.
- `subjects/western-civ` has three placeholder frames and one trail:
  - writing (c. 3200 BC, night palette)
  - printing press (c. AD 1440, parchment palette)
  - Moon landing (1969, night palette)
  - a one-frame trail, "The printing press", holding the Gutenberg Bible
    frame.

  Every frame has real sources, and each reading says it is a placeholder.

- The tests are 43 vitest cases in total:
  - 18 are validation cases, including a missing sources key, an unknown
    anchor, out-of-order and unsorted date segments, a frame on two spines,
    an orphan frame, a scripted SVG and a `javascript:` source.
  - 3 cover the real subject.
  - 9 cover markdown sanitising, including a `javascript:` scheme hidden by
    a tab, a newline, a leading control character, an entity or upper case.
  - 7 cover navigation.
  - 6 are server-render tests of the page.
- Docs: README development section, design.md §Files and interaction
  details, roadmap, and the project section of both instruction files.

## Verification

- `just check` and `just build` both pass.
- **Negative tests.** Each planted error below made `just check` exit 1, and
  it returned to 0 once they were removed:
  - a type error in `engine/`, which proves svelte-check sees files outside
    `src/`
  - an a11y warning in an engine component
  - a failing test
  - an unused variable (eslint)
  - an unformatted file (prettier)
  - `sources: []` on a real frame. I checked that this one failed on
    validation and not formatting: lint passed, and the subject suite
    reported "sources are required".
- **In the browser.** Playwright drove headless Chromium against the built
  server on 127.0.0.1:5310. Playwright was installed in the session
  scratchpad, not in the repo.
  - Tab order runs slider → next → Sync → follow → reading → sources → AI
    field → Send.
  - → moves the spine and the palette changes from night to parchment. The
    narrative stays put in manual mode and says so; S syncs it.
  - ↓ scrolls the narrative and leaves the spine alone.
  - T enters the trail and the breadcrumb reads "Main story › The printing
    press". Esc returns to the anchor frame, with focus on the slider.
  - Home and End both work.
  - ← typed in the AI field leaves the spine alone. Enter shows the
    not-connected status, and Esc returns focus to the slider.
  - One wheel notch over the spine moves one frame, and so does a burst of
    small trackpad deltas. The wheel over the narrative scrolls only the
    narrative.
  - Follow mode tracks the spine and survives a reload.
  - With reduced motion, the SVG animation and palette transition are off.
  - At 390px there is no horizontal overflow.
  - The console shows no errors.
- Screen-reader output was **not** heard. The ARIA roles, labels and live
  region are asserted in the server-render tests and were seen in the DOM,
  but not tried with a real screen reader.

## Pre-ship review (cleo, comment on korg 3362)

- **Finding 1, sanitising weaker than claimed.**
  - The markdown bypasses are repaired, with the new tests watched failing
    first. The fixed bypasses are a tab-split scheme, a leading control
    character, an entity-spelled scheme, and `javascript:` in an image
    `src`.
  - The SVG regex now also catches the four bypasses the review found
    (`<g/onclick=`, an entity-spelled scheme, `<style>`, `<embed>`), plus
    `<use>`/`href`. All five new cases were seen failing against the old
    regex.
  - The record's claim is reworded above.
  - The real sanitiser is a precondition on 3360.
- **Finding 2, WCAG 2.1.4.** The single-character shortcuts S and T are
  filed as korg 3363, because the choice between a toggle,
  remapping and focus-scoping changes the documented keyboard design.
- **Nit, a pinned narrative takes the spine frame's palette.** Left as it
  is: the whole page follows the cursor, as design.md says.

## Repaired in passing

- The browser check found two problems, both now fixed. At 1280×560 the
  scene overflowed into the bottom HUD, so it now scales with viewport
  height as well as width. Esc from the AI pane's Send button did nothing,
  so Esc is now handled for the whole pane.
- A favicon was missing, which caused the one console 404.

## Follow-ups

- There are no touch swipe gestures on the spine yet; touch users have the
  prev/next buttons and tapping the timeline. That can wait until touch
  matters.
