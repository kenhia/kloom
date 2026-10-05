# 052 — Keys that always work

## Goal

korg proposal 3567, covering korg 3561, 3562, 3563 and 3564: the character
shortcuts (Z, B, N…) went dead whenever focus left the spine, the narrative
or the notes. That happened after Home → Begin, a Begin on another subject,
a deep link, or a click on the drawing or a paragraph. Enter on the start
screen also did nothing unless focus was on Begin or the subject list.

## Decisions

- **Premises held** (checked at start). `pageKey` still gated character
  shortcuts on `within(SHORTCUT_PANES)` (keys.ts:312). The Shell's focus
  effect still needed `wasActive === false`, so a shell that mounted begun
  never took focus. StartScreen's `keydown` handled only Escape. kloom is not
  in the cross-project plan index, and no grow branch was pending.
- **3564: option 3, as the proposal decided.** Character shortcuts act
  anywhere in the shell. They stand down only in a text field, in
  `[data-own-keys]` (dialogs, the settings, the AI results) and in the
  reading while words are being chosen. `SHORTCUT_PANES` is gone. WCAG 2.1.4
  now rests on rebinding and turning a key off (sprints 011 and 037).
  docs/design.md §Interaction says so and records why the scoping existed.
  This also makes 3562 a gate case only, with no pointerdown or tabindex
  work.
- **One help-bar run.** Each shortcut acts anywhere now, so the help bar's
  "…, in the spine or narrative" and "…, anywhere" runs became one list. The
  keys dialog's "anywhere" marker per row and the `modified()` helper went
  with them. The dialog's note and the User's Guide now say "anywhere on
  the page but a text box or an open dialog".
- **Begin and Continue focus the spine; only Esc returns to Home.** The
  proposal left this to the implementer. Begin and Continue start reading,
  so a screen reader should land on the frame. Esc is a cancel, so it goes
  back to the control that opened the start screen. `StartScreen`'s
  `onbegin(closed)` carries which one happened, and the page calls the
  shell's new `reading()` before the shell comes forward.
- **3561: the shell takes the spine focus on mount when it is begun**
  (`active && !wasActive`). A deep link, another subject opened from the
  list or by a resume link, and the map's jump from the start screen now all
  land on the slider.
- **3563: Enter begins from anywhere on the start screen.** It does not
  begin on another control (button, link, input, select, textarea, summary)
  or inside `[data-own-keys]`, and not with a modifier or during IME
  composition.

## Found on the way: SvelteKit's focus reset

The gate's negative run against main turned up a related bug that none of
the work items named. After Home, focus sat on `<body>`, not on Begin.
SvelteKit's `goto` resets focus to the body once it has navigated, and that
undid the start screen's own `button.focus()`. So after every trip home the
start screen was keyboard-dead: Esc and Enter reached nothing until the
reader tabbed in. The same reset undid the new shell's spine focus after
opening another subject. This is the same bug class and inside this
sprint's scope, so it is fixed here. `home()`, `open()` and the map's jump
from the start screen pass `keepFocus: true`, and the cross-subject resume
link carries `data-sveltekit-keepfocus`. Jumps (`follow`) already re-focused
the spine in `afterNavigate`, so they are unchanged.

## What shipped

- `engine/keys.ts`: `SHORTCUT_PANES` and `modified` removed. `pageKey`
  returns a matched shortcut anywhere outside `OWN_KEYS`.
- `engine/ui/Shell.svelte`: focus on mount when begun, `reading()`, and one
  help-bar run.
- `engine/ui/StartScreen.svelte`: Enter anywhere, `onbegin(closed)`, and the
  resume link keeps focus.
- `engine/ui/KeysDialog.svelte`: the note reworded, and the "anywhere"
  marker removed.
- `src/routes/[subject]/[[frame]]/+page.svelte`: `keepFocus` on Home, on
  opening another subject and on the map's jump. Begin and Continue tell the
  shell that reading starts.
- `create-tools/focus-check/focus_check.mjs` and `just focus-check`, 17
  checks. Each entry route (deep link, Begin on this subject, Home then Esc,
  Begin on another subject, Enter on the list, Continue) lands focus where
  the design says. Z opens the drawing after each, or C opens the contents
  on another subject's first frame, which may have no drawing. Z and B work
  after a click on the scene or a paragraph. Enter after a click on the
  start screen's background begins. Z typed in the AI box types and opens
  nothing. The check runs outside `just check`, like home-check and
  hud-check.
- Tests: `engine/keys.test.ts` now asserts the shortcuts act from a button,
  the bare page and no target. `page.test.ts` checks the one help-bar run.
  keys-check no longer expects "anywhere".
- docs/design.md: §Interaction (character shortcuts, modified bindings),
  §Start screen (Enter anywhere; focus after Begin, Continue and Esc; the
  focus reset), §Keyboard shortcuts, and the five "scoped like the others"
  mentions. The User's Guide's keyboard paragraph changed to match.

## Verification

- `just check` is green.
- `just focus-check` passes 17/17 on the branch. Negative-tested against
  `origin/main` (a worktree served on :5416): 4/17, exit 1. Main failed every
  entry route but Continue, both clicks, B, and Enter on the background.
- keys-check passes 70/70, home-check 11/11, hud-check 145/145 and
  start-fit 856/856.

## Repaired in passing

- The focus reset after Home (above). It is in the same bug class and the
  same files, and focus-check covers it.

## Follow-ups

None.

## Deployed

2026-10-05, from merged `main` (`6a32bd1c`, PR #59), by `just deploy` on
kai. Its verify passed 10/10: both doors read, the tailnet door refuses an
anonymous write and keeps reader data and notes, frame bodies come from the
library, and pages go compressed. Library `f88c6e`.

Verified live: `focus_check.mjs --url http://127.0.0.1:4890` (the tailnet
door, anonymous, so nothing was written to a reader's data) passed 14/14.
Continue and B after a click were skipped because they need a reader.

The public reader site (kloom.kenhiatt.us) was not published in this ship.
It still runs sprint 051's build until `just publish-public`.
