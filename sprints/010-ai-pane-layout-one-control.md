# Sprint 010 — AI pane layout, and one ask/grow control

korg proposal 3419, covering 3377 (explore the AI pane's layout) and 3411
(one control for ask and grow). Branch `010-ai-pane-layout-one-control`.

## Goal

Sprint 004's ask streamed its answer into a strip along the bottom, where it
competed with the reading for height. Try the layouts side by side and record
Ken's pick. In the same sprint, make ask and grow one control, because the
layout decides where that control sits and the control decides what the pane
has to hold.

## Premise check

- **3377 holds.** The AI pane was still the full-width bottom strip
  (`Shell.svelte`: `.ai` spanning both columns). Ken's comment on the item
  (2026-09-28) had already settled the direction: option 3 (two panes with
  tabs), with a control to switch to option 2 (three columns). In the tabs
  layout the AI control must stay visible while the reader reads the
  narrative, and a status must say when the answer is back.
- **3411 holds.** Ask and grow were two forms, with grow's verb in its own
  `<select id="grow-verb">` and a Queue button.
- No cross-project plan lists kloom.

## Decisions

- **Layout is a reader setting**: "Layout" (`kloom.layout`), tabs by default.
  All four options are built, because Ken wanted to see them before cutting
  any: tabs, three columns, bottom strip, and right-hand split. Dropping the
  last two later is a settings-list edit.
- **One DOM order, placed by CSS grid.** The shell always renders the spine,
  then the tab row (tabs only), then the narrative, then the AI pane. Each
  layout is a class on `.shell` that places them. Switching layouts never
  remounts the AI pane, so an answer streaming at the time survives the switch.
- **In the tabs layout, the control stays at the foot under both tabs**, and
  only the results region is the AI tab's panel. Sending does not switch
  tabs, per Ken's note. A result landing unseen puts a dot on the AI tab, says
  "Answer ready, on the AI tab" in the status line, and offers a "Show it"
  link, which saves a keyboard user a trip back up to the tab list.
- **The results region replaces the answer's own scroller.** One focusable
  `#ai-results` (`data-own-keys`) holds the answer, its actions and the grow
  jobs. It is a `tabpanel` in the tabs layout and a labelled `region`
  elsewhere. In tall layouts it takes the height; in the strip it keeps the
  old 35vh cap and hides when empty.
- **The tab keys go to the tab, not the page.** `tabKey` (`engine/keys.ts`)
  maps Left/Right (wrapping) and Home/End. The tab handles the key and
  prevents its default. The shell already ignores prevented keys, so the
  spine stays put without adding the tab list to `OWN_KEYS`, and Esc still
  works there. S brings the Narrative tab forward.
- **The gear moves to the tab row in the tabs layout**, so it can be reached
  from either tab.
- **The one control** (`engine/ai/control.ts`): the verb select comes first,
  with "Ask a question" as the default, then "Grow: …" ×3 when grow is
  configured. Without grow there is no select. The verb sets the button's
  word (Ask/Grow), the placeholder, the label and the model setting.
  "Include web" shows for ask only.
- **No confirm for grow.** It reads bigger instead: an outlined, bold button,
  and a line naming the grow model and saying it commits. **The verb resets to
  Ask after each grow**, which is 3411's recommendation. The reset is also the
  quick way back to Ask, so there is no separate shortcut.
- **No answer history.** A taller pane invites one, but it would be a design
  change that nobody asked for here. The pane still holds only the latest
  answer, and design.md §Ask says so.
- **The AI pane reports its state through a callback** (`onactivity`), not a
  bindable prop. ESLint's `no-useless-assignment` reads a bindable prop that
  is only written inside an effect as a dead store.

## Ken's review (2026-09-28)

After seeing the first screenshots, Ken asked for three tweaks to every
layout, and for draggable dividers if they were cheap:

- **"Web" stacked over the send button**, relabelled from "Include web", and
  **a smaller button**. Both give the text box more room before it wraps. The
  control is now a grid: the verb on its own row, then the text box beside a
  narrow column of Web over the button.
- **The keyboard help moves to a bar along the foot of the whole page.** The
  shell became a flex column: the panes' grid (`.panes`, which now carries
  the layout class), then the bar. The bar keeps `id="ai-hint"`, so the text
  box's `aria-describedby` still reaches it.
- **Draggable dividers.** These were cheap enough to take in this sprint.
  - `Splitter.svelte` is the ARIA window splitter: a focusable separator, a
    pointer drag with capture, arrows ±2%, Home/End to the limits, and
    Enter or double-click to reset.
  - `engine/panes.ts` holds the fractions, the limits (the narrative keeps a
    fifth in three columns) and the per-layout memory in `kloom.panes`.
  - The grid tracks come from those fractions as `fr`, set inline as
    `--cols`/`--rows`, so the phone's one-column rule still overrides them.
  - A divider shares its pane's grid cell, which is why every pane is now
    placed explicitly. Otherwise auto-placement would push a pane into the
    next free cell.
  - A size is not a pick from a list, so it stays out of the settings
    registry.
- **Focus on a divider** is its accent line. The shell's focus outline rule
  now skips separators; the two drew a double box.

## What shipped

- `engine/settings.ts`: the `layout` setting and `Layout` type. It is added to
  the page's settings list.
- `engine/ai/control.ts`: the verb table (`aiVerbs`, `isGrow`), with tests.
- `engine/keys.ts`: `tabKey`, with tests.
- `engine/ui/Shell.svelte`: the four layout grids, the tab row (ARIA tabs,
  roving tabindex, the result dot), the gear placement, and the phone
  collapse to one column.
- `engine/ui/AiPane.svelte`: rewritten around the results region and the one
  control. The ask and grow logic is unchanged.
- `engine/ui/Narrative.svelte`: becomes a `tabpanel` in the tabs layout.
  Adds `[hidden]` support.
- `engine/ui/Splitter.svelte`, `engine/panes.ts` and `splitKey` in
  `engine/keys.ts`: the dividers, with tests.
- The keyboard help, moved to the shell's bottom bar.
- `docs/design.md`: §Layout (the four layouts, Ken's pick, the tab keys, the
  phone behaviour), a new §The AI control, and §Ask, §Web search, §Grow,
  §Interaction and §Settings brought in line.
- Page tests: the one control, the layout setting, the tab list and its
  panels, and the gear's placement in both layout families.

## Verification

- `just check`: svelte-check (0 warnings), prettier and eslint, and vitest
  (31 files, 405 tests; all green).
- **Dividers in a real browser** (`.scratch/split.mjs`), in all four layouts:
  - ← ← narrows the spine (768 → 717 px) without moving the spine's frame;
  - Home goes to a quarter (320 px) and Enter resets;
  - a mouse drag lands at 500 px and survives a reload;
  - in three columns, the AI divider drags wider (320 → 475 px), and End
    stops with the narrative at 256 px (a fifth);
  - in the split, ↓ ↓ grows the narrative;
  - at 390 px no divider shows.

  All passed. The keyboard pass below was re-run after the change and still
  passes.

- **Screenshots** at 1280×800 and 390px for all four layouts, before and
  after an answer, plus the tabs layout's AI tab. The answer is a
  Playwright-intercepted NDJSON stream, not a model call. They are published
  for Ken as a private comparison page:
  <https://claude.ai/artifact/RqsbdfsWxXqfL86dBucuvG>.
- **A keyboard-only pass in all four layouts** (Playwright, real chromium,
  dev server). It checked:
  - the Tab order reaches verb → text box;
  - in the tabs layout, Tab reaches only the selected tab, the hidden panel
    is not a stop, → moves to the AI tab without moving the spine
    (04 → 04), Home/End and wrapping ← work, and S from the spine brings the
    Narrative tab back;
  - Esc from the text box returns to the spine (`slider`);
  - S and T typed into the box stay there;
  - ↓ on the verb picks the first grow verb, the button reads Grow, and
    the Web box goes away;
  - Enter queues the grow (request intercepted) with the verb and text, and
    the verb resets to Ask.

  All passed. The scripts are `.scratch/keys.mjs` and `.scratch/shots.mjs`,
  which are git-ignored.

## Follow-ups

- **Ken to look at the four layouts and confirm the pick** (the comparison
  page above). If tabs and three columns are the keepers, drop `strip` and
  `split` from the `layout` choices. A stored value that is no longer a
  choice falls back to the default, so readers need no migration.
