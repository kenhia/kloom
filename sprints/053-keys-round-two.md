# 053 — Keys round two

## Goal

korg proposal 3569, covering korg 3568. This follows up sprint 052 after
Ken tested it. Tab did not reach the AI box the way design.md said it did,
and no key went to the start screen or to the settings. Ken decided every
key in chat on 2026-10-05. This sprint builds those decisions.

## Decisions

- **Premises held** (checked at start). `SHORTCUTS` had no q, h or g.
  `pageKey` had no PageUp or PageDown case, so those keys did nothing on the
  spine. design.md §Interaction still said "Tab moves into and out of the AI
  pane". §Layout still said "Sending does not switch tabs" and still had the
  stale tabs-layout paragraph. kloom is not in the cross-project plan index,
  and no grow branch was pending.
- **Ken's decisions, as recorded on 3568.**
  - Q, not `/`, because `BINDABLE` takes only letters, digits and F-keys.
  - H, not a remapped Home, because Home and End are the ARIA slider's
    minimum and maximum.
  - G, not Cmd+, (Safari takes Cmd+, and comma is not bindable).
  - Tab stays the browser's own tab order.
  - Send in the tabs layout brings the AI tab forward. That reverses
    §Layout. Q only focuses the box and does not switch.
- **The three new shortcuts go last in `SHORTCUTS`.** The first shortcut in
  that order wins a clash. A reader who had already bound q, h or g to
  something else keeps it, and the dialog names the clash.
- **G returns focus where it was.** Before this sprint the settings pop-up
  always gave focus back to the gear. `Settings.show(opener)` now remembers
  where focus was when a key opened it, and Esc returns focus there. A gear
  click still returns focus to the gear. When focus was on nothing (the
  page body), focus goes back to the gear. G puts focus on the pop-up's
  first control.
- **H is the Home button.** It calls the same `goHome()`. The page's
  navigation guard already asks about an unsaved note on the way home, so H
  gets that check for free. Esc from the start screen then returns focus to
  Home, as it does after a click on Home.
- **Send switches on submit, not on the answer.** `AiPane` gains `onsend`,
  called for an ask or a grow request that is actually sent. Stop and an
  empty box do not call it. Focus stays in the box. The dot and "Show it"
  stay, for an answer that lands after the reader has gone back to
  Narrative partway through the answer.
- **PageUp/PageDown on a trail (the choice left to the implementer):**
  they follow the trail's own segments, by the same rule as on the main
  spine (`navigation.ts` `segmentStep`). 47 of the 48 trails have one
  segment, so on most trails PageUp goes to the trail's first frame and
  PageDown does nothing. The one trail with three segments steps through
  them. One rule everywhere is simpler to explain than "nothing on a
  trail", and PageUp to a trail's start is useful in its own right. At
  either end of a spine the keys do nothing.
- **"Section" in the reader's words.** Both the help bar and `FIXED_KEYS`
  say "section", the word the colours already use (§Colours by section).
  "Segment" is the authoring word.

## What shipped

- `engine/keys.ts`: the `ask` (Q), `home` (H) and `settings` (G) shortcuts,
  and the fixed keys PageUp and PageDown (`segment-next`,
  `segment-previous`), which stand down under modifiers and in text fields
  as the arrows do. `FIXED_KEYS` gains PageUp/PageDown, and its Tab row now
  reads "move to the next control, in page order".
- `engine/navigation.ts`: `segmentStep(path, index, direction)`.
- `engine/ui/Shell.svelte` acts on the new keys. The help bar names Q (only
  where there is an ask box), H (only where there is a Home button), G and
  PgUp/PgDn. The "Tab into and out of the AI pane" hint is gone. In the tabs
  layout, `onsend` switches to the AI tab.
- `engine/ui/AiPane.svelte`: `onsend` and `focusInput()`.
- `engine/ui/Settings.svelte`: `show(opener)`, and Esc returning focus to
  the opener.
- docs/design.md:
  - §Layout: Send brings the AI tab forward, and Q does not.
  - §Interaction: Q, H, G, a PageUp/PageDown bullet, and Tab described as
    ordinary tab order (WCAG 2.1.2).
  - The lists of fixed keys gain PageUp/PageDown.
  - §Keyboard shortcuts' `FIXED_KEYS` line.
- The User's Guide and the keys dialog list the new keys, because both read
  `SHORTCUTS` and `FIXED_KEYS`.

## Verification

- `engine/keys.test.ts`: Q, H and G in every scope, standing down in a text
  field and in `data-own-keys`, rebound and turned off. PageUp and PageDown
  in every scope, under each of Alt, Ctrl and Meta, and in `FIXED_KEYS`.
- `engine/navigation.test.ts`: `segmentStep` forward, back, at both ends,
  and on a one-segment trail.
- The page tests: the help bar's run with Q, H and G, and Q left out with no
  AI pane.
- `just focus-check` has five new cases:
  - Q from the scene lands in the ask box, the Narrative tab is still
    showing, and no q is typed.
  - Send brings the AI tab forward with focus still in the box. The ask
    route is stubbed, so no model is called.
  - H opens the start screen.
  - G opens the settings with focus inside them, and Esc closes them and
    returns focus to the spine.
  - PageDown and PageUp land on the right section starts.
- **Negative test.** I stashed the engine changes and ran the check against
  the code from before this sprint. 8 cases failed: Q, both Send checks, H,
  both G checks, PageDown and PageUp-within-a-section. The new code passes
  30/30. Run against the old code, the new unit tests failed 7 of 38.

## Repaired in passing

- The tabs-layout paragraph in design.md §Layout said the character
  shortcuts "do nothing" on the tab list. Sprint 052 made that stale. It now
  says they act there as anywhere else in the shell.
- The `engine/keys.ts` header still described the scoping that sprint 052
  removed: shortcuts acting only in the spine, narrative or notes, and a
  fixed list of twelve letters. It is rewritten to match the code.

## Follow-ups

None.
