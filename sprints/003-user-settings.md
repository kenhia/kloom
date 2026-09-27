# 003 — User settings: settings control, palette mode, staged scene entrance

## Goal

korg proposal 3374, which was split out of ask (3368) so that animation
tuning cannot hold up the AI work. It covers two work items, done in this
order:

- korg 3373: the settings control. A gear button and a pop-up rendered from
  a small settings registry, so that ask and grow can add their model rows
  cheaply.
- korg 3372: the Dark / Light / Mixed palette mode (the first row), and the
  staged scene entrance on prev/next.

## Decisions

- **Premises held.** `Shell.svelte` ignored page keys only in text inputs,
  textareas, selects and contenteditable, so radios were not covered. The
  draw-on was 1.4s per group at 0.25s steps, capped at 1.5s, so it ends at
  about 2.9s. The start screen wore the first frame's palette, and no
  settings code existed. kloom is not in the cross-project plan index.
- **Registry (3373).** `engine/settings.ts` holds the `Setting` type
  (`{id, label, choices, default, storageKey}`), `readSetting` and
  `writeSetting`, and the `paletteMode` setting.
  - A stored value that is no longer a choice falls back to the default. The
    same rule covers a model that the app config drops.
  - `engine/user-settings.svelte.ts` is the reactive store. The page makes it
    with the list, so ask and grow add a row by building a `Setting` from the
    app config at runtime and appending it; nothing else changes.
- **Controls.** One control kind: a native `<select>` with a visible
  label, including the palette mode. Model rows must be drop-downs, and one
  kind keeps the pop-up uniform.
- **A disclosure, not a `<dialog>`.** A modal would dim and inert the page,
  and the palette mode should show its effect live behind the panel. Esc
  closes the panel and refocuses the gear; a click outside also closes it.
  - The panel carries `data-own-keys`, which the shell now honours, so page
    keys stand down anywhere inside it.
  - Esc is handled on the gear and the selects with `preventDefault`. Those
    handlers run before the shell's window listener, so Esc inside a trail
    closes the panel and does not also leave the trail.
- **Placement:** the end of the narrative toolbar, beside "Follow the
  spine". It is clear of the corner brackets.
- **"Follow the spine" stays put.** It belongs next to the Sync button it
  modifies, and moving it would cost a click. The reasoning is in
  docs/design.md §Settings.
- **Palette mode (3372).**
  - Each palette may name a `counterpart` of the other scheme in
    `subject.json`, and validation checks it. The engine swaps a palette for
    its counterpart only when the scheme differs, so a subject with several
    dark palettes keeps their variety in Dark mode.
  - Mixed is the default, and the OS colour scheme is not consulted. This was
    my call, raised with Ken and signed off with the eyeball check.
  - The start screen follows the mode. Settings load on mount, so a
    remembered Light shows the start screen switching once on load.
- **Staged entrance (3372).** The headline is split into its words and the
  accent, and each fades in on its own delay:
  - `--headline-delay` 1s and `--headline-fade` 1s;
  - `--accent-delay` 1.5s and `--accent-fade` 1s.

  The four variables sit at the top of `.scene` in `SpinePane.svelte`. The
  scene is `{#key frame.id}`, so rapid presses restart it cleanly. Reduced
  motion shows everything at once. The metadata has no delay, and the HUD is
  outside the keyed scene, so both are there at 0s.

## Verification

- `just check` passes: svelte-check shows 0 warnings, prettier and eslint
  are clean, and vitest runs 96 tests (76 before). The new tests cover:
  - registry defaults and persistence
  - a stale stored value, and a value refused for not being a choice
  - blocked storage
  - runtime-supplied choices
  - `paletteFor` in every mode
  - counterpart validation
  - the gear's server-rendered semantics (button, name, `aria-expanded`,
    `aria-controls` pointing at a hidden `role="group"` panel with
    `data-own-keys`) and its toolbar position
  - labelled selects
  - the shell painting the first frame in its light counterpart under Light
- **Negative-tested.** Removing the same-scheme counterpart check, and
  removing `data-own-keys` from the panel, each failed its test (2 failed,
  94 passed). Both were restored.
- **Keyboard-only browser pass** (Playwright, headless Chromium):
  - Begin, then ArrowRight to 02.
  - Tab order: Next, Sync Narrative, Follow, then the gear.
  - Enter opens the panel (`aria-expanded` true), and Tab moves into the
    select.
  - ArrowDown ×2 selects Light, and the spine does not move (stayed 02/16).
    The background fades to parchment and `kloom.palette=light` is stored.
  - Esc closes the panel and focus returns to the gear. ArrowRight on the
    closed gear still moves the spine.
  - After a reload, both the start screen and the shell are parchment.
- **Phone width and reduced motion.** At 390px the panel fits with no
  horizontal scroll, and an outside click closes it. With reduced motion,
  the headline and accent are at opacity 1 within 50ms.
- **Entrance timings sampled** (opacity of words / accent): 0.3s 0 / 0;
  1.2s 0.06 / 0; 1.8s 0.89 / 0.15; 2.6s 1 / 1. The metadata was at 1
  throughout.

## Follow-ups

- **Eyeball check: signed off.** Ken passed the check on 2026-09-27 with
  the timings as first set. The final values are headline 1s delay over 1s
  and accent 1.5s delay over 1s, recorded in docs/design.md §Scene entrance.
- The first frame's entrance plays behind the start screen, so it is over
  by the time Begin is pressed. This is the same as the draw-on before this
  sprint. If Ken wants the first scene to stage in after Begin, the fix is
  to key the scene on the shell's `active` too.
