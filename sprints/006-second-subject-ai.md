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

### Several subjects (3396)

- **`/<subject>` for every subject, with `/` redirecting.** The page
  moved to `src/routes/[subject]/`, and `src/routes/+server.ts` redirects
  `/` (307) to `$KLOOM_SUBJECT`, or to the first served subject if that one is gone.
  A subject is a directory under `$KLOOM_SUBJECTS_DIR` whose name matches
  `[a-z0-9][a-z0-9-]*` and that holds a readable `subject.json`
  (`listSubjects`, `src/lib/server/config.ts`). `subjectDirFor` checks an
  id against that listing, not only the pattern, so `..`, a hidden
  directory or an upper-case name is simply unknown: a 404.
- **The chooser is the start screen.** It adds an "Or open" row of links
  under Begin, inside the dialog and after Begin in tab order. The engine
  component takes resolved `{title, href}` pairs, so it never builds an app
  route. The page wraps the shell in `{#key}` by subject, and "begun" is
  remembered per subject. Opening another subject, or going Back to one,
  therefore starts at that subject's start screen with a fresh spine, not
  at the old index.
- **Every API names its subject explicitly**, in the body. The other option
  was nesting the APIs under `/[subject]/api/…`. A body field keeps
  subjects and fixed routes out of each other's namespace, and it matches
  the item's wording. Ask builds its context from the named subject. Keep
  refuses an answer asked under another subject (the negative test was
  seen failing without the check). Grow's list takes `?subject=`. Media
  moved to `/media/<subject>/<frame>/<file>`, and the loader's existing
  `mediaBase` option carries the prefix into the rendered reading.
- **Grow: a queue per subject, one runner slot for the host.** Each subject
  keeps its jobs under `<dataDir>/<subject>/grow/` as before. Every served
  subject's queue is loaded at start, so a restart resumes all of them. The
  runners share one slot, so two subjects never run `claude -p` grow jobs
  at once. A job waiting on another subject's job reports "waiting for
  another subject's grow job". The subject gate (`exclusive`) stays
  global, which is over-broad but harmless with one runner.
- **Settings stay global.** None of palette mode, narrative following, ask
  model or grow model is about a subject.
- A second request for the answer-in-flight check (3391) was made live: an
  ask on "We stole FIRE.", then → while it streamed. The answer kept its
  heading and showed the "moved on" line, and the reading moved to
  "We learned to WRITE.".
