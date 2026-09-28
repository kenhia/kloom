# 006 — Second subject: History and Current State of AI

## Goal

korg proposal 3400 (Ken, 2026-09-27: "the next thing to feel is a second
subject with a reasonable amount of content"). It covers three work items,
in this order:

- korg 3391: the narrative follows the spine by default. Not following
  becomes a reader setting, and the Sync Narrative button goes while its
  shortcut stays.
- korg 3396: one app serves several subjects, with a route per subject, a
  chooser, and every API scoped to a subject.
- korg 3395: the AI subject. It needs at least 36 main-spine frames and at
  least three deep trails, on a spine that moves from dates to technologies,
  with rich readings. It is authored by following `skills/grow/SKILL.md`, as
  the framework's authoring guide would be.

## Decisions

- **Premises held.** The Sync Narrative button and the `manual` default
  were in `Narrative.svelte`/`Shell.svelte`. `src/lib/server/config.ts`
  served exactly one subject (`KLOOM_SUBJECT`), and `subjects/` held only
  `western-civ`. kloom is not in the cross-project plan index.

### Narrative follows the spine (3391)

- **A registry row, not a toolbar checkbox.** `followSpine`
  (`engine/settings.ts`) is "Narrative": _Follows the spine_ (default) or
  _Stays until S_, under `kloom.followSpine`. Ken confirmed it belongs in
  the settings control, not in `kloom.config.json`. The old `kloom.sync`
  key is deliberately not read. Its stored value was mostly the old
  `manual` default, and honouring it would have kept existing readers on
  the default Ken just rejected.
- **The shell derives the mode from the setting.** While following, an
  effect keeps the pin on the spine's frame. Turning following off leaves
  the reading where it is, not on whatever frame was pinned before.
- **The toolbar keeps its status line** (`aria-live`): "Following the
  spine.", "In step with the spine." or, when the two differ, where each is
  and "S brings the reading here". The gear now follows it.
- **An ask in flight.** The answer already carried its frame (3360). With
  following on, moving the spine now moves the reading pane mid-answer, so
  the answer shows a line under its heading, "You have moved on; this
  answer stays with the frame it was asked about". Keep and Grow from this
  use the answer's own frame, as before.
- `docs/design.md` §Interaction, §Settings and §Ask were rewritten for it.
