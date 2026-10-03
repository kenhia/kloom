# 037 — Keyboard shortcuts get their own dialog: key capture with modifiers, and a settings pop-up that can't be squeezed

## Goal

korg proposal 3494, covering 3493. Ken reported on 2026-10-02 that the
settings pop-up's dropdowns had shrunk until their values were cut off
("Ligh", "Follo", "Sonr", "Opu"). This sprint fixes the pop-up so that
cannot happen again. It also moves the shortcuts out of the pop-up into a
dialog of their own that captures keys, modifiers included.

## Premise, checked at start

- **The cause holds.** `engine/ui/Settings.svelte` was one grid,
  `auto 1fr`, at `width: max-content` capped at 24rem, with
  `select { min-width: 0 }`. The longest label, "Go to a random frame in
  this subject" (`SHORTCUTS` in `engine/keys.ts`), set the label column.
- **The migration premise drifted.** 3493 asked to migrate stored
  single-key settings "in the browser and in the reader store". The reader
  store has never held settings. `ReaderStore` keeps places, bookmarks,
  notes and kept answers, and nothing under `src/lib/server` reads a
  `kloom.key.*` value. So only the browser's `localStorage` needed
  migrating. That narrowed the item without changing its direction.
- No grown content was pending (`just grow-pending`). kloom is not in the
  cross-project plan index.

## Decisions

- **Stored format: the binding's text, under the same names.** A binding
  is `{key, shift, alt, ctrl, meta}` in memory (`Binding`, `engine/keys.ts`).
  It is stored as `ctrl+alt+shift+meta+m`, modifiers in that fixed order,
  or `off`, under the old `kloom.key.<action>` names. A single letter,
  which is all a stored key was until now, parses as itself. The
  "migration" is therefore reading, not rewriting, and a reader's remapped
  letters keep working with nothing touched. The settings tests and
  `just keys-check` both check this. A stored binding that is unparseable
  or reserved reads as the default.
- **The shortcuts are not settings rows any more.** The registry's rule is
  that every setting is a pick from a fixed list, and a captured binding is
  not. So the shortcuts live in `UserKeys`, owned by `UserSettings` as
  `settings.keys` and loaded by the same `load()`. That gave Shell, the
  start screen and the dialog one source without a new prop. `keySettings`
  and `keymapOf` are gone.
- **Page-wide means outside the panes, not inside a text field.** A
  binding with Alt, Ctrl or Meta acts anywhere on the page, the AI pane's
  buttons included. It still stands down in a text field and under
  `data-own-keys`. On a Mac, Option with a letter types a character, so
  taking it from the ask box would break typing.
- **Shift is let off a plain binding, never added.** N has always meant
  n, and Caps Lock users rely on that. Matching tries the exact modifiers
  first, then the same press without Shift, so a reader can still bind
  Shift+Y apart from Y.
- **The fixed keys stand down under Alt, Ctrl or Meta.** Before, the shell
  ignored every modified press. Now modified presses are matched, so the
  arrows needed the rule spelled out: Alt+← is the browser's Back and must
  not move the spine.
- **The physical key stands in for a character a modifier made.** Option+M
  is µ and Shift+1 is !. `pressedKey` falls back to `code` (`KeyM`,
  `Digit1`) when `key` is not a letter, digit or F-key.
- **Bindable keys: a–z, 0–9, F1–F12.** Punctuation varies too much by
  layout, and Space, Enter and the arrows belong to controls.
- **The reserved list grew past 3493's examples.** Writing the tests
  showed that nearly every Ctrl letter is taken somewhere: G (find again),
  U (view source), J (downloads), K and E (search), and Ctrl+Shift+M
  (Chrome's profile switcher, through M). Ctrl+B and Ctrl+I remain. Alt and
  Shift combinations are where a reader has room, and the dialog's intro
  says so by naming them first.
- **A clash asks rather than warns.** Keys another shortcut already has
  bring up Swap (focused), Use for both, or Cancel. Swap gives the other
  shortcut this one's old binding, or turns it off when there was none. A
  binding left shared is named under the rows, as the pop-up used to.
- **The dialog renders its content only while open.** Rendering a closed
  dialog's rows put "Home, End" and "my-notes" into every page's server
  HTML, and three page tests that check for their absence failed. It also
  kept about 4 KB of markup out of every page for something rarely opened.
- **The pop-up's grid** is `minmax(0, auto) minmax(9rem, max-content)`,
  with selects at `width: 100%; min-width: 9rem` and labels wrapping. The
  layout check makes every label very long and measures each select.

## What shipped

- `engine/keys.ts`: `Binding`, `bindingText`/`parseBinding`, `keyName`
  (Cmd and Option on a Mac), `bindingOf`/`pressedKey`, `reserved`,
  `FIXED_KEYS`, `modified`, `onMac`. `pageKey` takes a press with
  modifiers, and `keyClashes` compares bindings.
- `engine/settings.ts`: `readKeymap`, `writeKey`, `keyWarnings` over
  bindings. `engine/user-settings.svelte.ts`: `UserKeys` (set, reset,
  resetAll, load) under `UserSettings.keys`.
- `engine/ui/KeysDialog.svelte`: the dialog. It has rows with keycaps,
  Change/Off/Reset, capture with a status line, refusals with reasons,
  clash Swap / Use for both / Cancel, "Reset all to defaults", Done, and
  the fixed keys.
- `engine/ui/Settings.svelte`: the "Keyboard shortcuts…" button and the
  grid that cannot squeeze a select.
- `engine/ui/Shell.svelte`: keys from `settings.keys`, modified presses
  passed to `pageKey`. The help bar names modified bindings in a run of
  their own, ending "anywhere".
- `just keys-check` (`create-tools/keys-check/keys_check.mjs`) runs 33
  checks at each of 1280×800 and 390×844, all keyboard-only:
  - every select at least 9rem with every label made long, and the pop-up
    on screen;
  - Enter on the gear opens the pop-up, and the dialog opens on the first
    row;
  - the dialog fits with no sideways scroll;
  - capture is announced in a `role="status"` line;
  - Esc cancels a capture and the dialog stays open;
  - Ctrl+T is refused with its reason;
  - Alt+Y is captured;
  - a clash focuses Swap, and Swap works;
  - Esc closes the dialog onto its button, then the pop-up onto the gear;
  - the bindings are stored;
  - the help bar shows "Alt+Y map, anywhere", and Alt+Y opens the map from
    the gear;
  - a stored letter from before still binds.

  The Playwright finder moved from scene-fit into
  `create-tools/lib/browser.mjs`, which both checks import.

- design.md: §Interaction (modified bindings are exempt from 2.1.4, the
  matching rules), §Settings (Keys moved out, the no-squeeze grid) and a
  new §Keyboard shortcuts.

## Verification

- `just check` green: svelte-check with no warnings, prettier, eslint,
  vitest (1,300+ tests, 13 new in `keys.test.ts`, 6 new in
  `settings.test.ts`, page tests updated), and the tools' tests.
- `just keys-check`: 66/66. **Negative-tested twice:**
  - With the old CSS back (`auto 1fr`, `min-width: 0`), it failed 10
    checks: every select measured 15px with long labels, at both sizes.
  - With the dialog's reserved check disabled, it failed from "Ctrl+T is
    refused" onward.
- `just scene-fit feynman` still runs on the shared finder: 0 misfits in 62
  frames.
- **Not verified with a real screen reader.** The capture prompt is checked
  as the text of a `role="status"` line, which is what a screen reader
  announces, but no screen reader was run.

## Follow-ups

None filed.

## Deployed

2026-10-03, on kai, by `just deploy` from merged `main` (`5b861a0`, PR #44).
`just verify` passed all ten checks: both doors read, writes are gated, reader
data is kept from an anonymous read, frame bodies come from the library, and
pages go compressed. The sprint's own behaviour was then checked live:
`keys_check.mjs --url http://127.0.0.1:4891` passed 66/66 against the
deployed service at 1280×800 and 390×844. That covers the pop-up's selects
at 9rem or more with long labels, the dialog keyboard-only (capture, refusal,
swap, Esc), Alt+Y opening the map, and a stored single letter still binding.
