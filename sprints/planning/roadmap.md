# Roadmap

> The general plan for this project. Keep it current; detail lives in the
> sprint records. Design decisions: [docs/design.md](../../docs/design.md).

## Now — POC: History of Western Civilization

- ~~Sprint 001~~: scaffold with real gates (korg 3356), content model (3357)
  and the three-pane shell with keyboard control and Sync Narrative (3358) —
  [record](../001-scaffold-three-pane-shell.md).
- ~~Sprint 002~~: look and feel first (Ken, 2026-09-26). Chicago-style
  citations (3371), the palette fade (3370), 16 curated frames and a trail
  (3361) and the loom start screen (3359) —
  [record](../002-poc-content.md).

- Sprint 003: user settings (proposal 3374). A gear and pop-up backed by
  a settings registry (3373), the Dark / Light / Mixed palette mode and the
  staged scene entrance (3372) —
  [record](../003-user-settings.md). Ken signed off on the entrance timings
  as first set.

- Sprint 004: ask (proposal 3368). A transient answer in the AI pane,
  behind the provider interface, first adapter headless `claude -p`, with
  "keep this" and the kept-answer format grow reads (3360). It added the app
  config file (`kloom.config.json`) and the ask-model setting (Sonnet 5 by
  default), and scoped S/T for WCAG 2.1.4 (3366) —
  [record](../004-ask.md).

- Sprint 005: grow (proposal 3369). Queued jobs that add frames and trails
  in the curated frames' style, check them and commit them (3364), written
  by `skills/grow/SKILL.md`, after the allowlist SVG sanitiser (3365). Web
  search for ask, with web sources carried into kept answers (3376), and a
  grow-model setting (Opus 5.5 by default) —
  [record](../005-grow.md).

- Sprint 006: a second subject (proposal 3400). The narrative follows the
  spine by default (3391). One app serves several subjects, with a chooser
  on the start screen (3396). The subject is the History and Current State
  of AI (3395): 41 frames and four trails on a category → date →
  technology → category spine, written by following the grow skill. The
  skill's western-civ assumptions were generalised on the way —
  [record](../006-second-subject-ai.md).

- Sprint 007: kloom runs as a service on kai (proposal 3416). Ask, keep
  and grow are gated on the tailnet identity behind `tailscale serve`, and
  an ssh door stays open for kwork demos (3388). The service grows into its
  own content clone and pushes `grow/kai`, and a PR brings the content back
  (3412) —
  [record](../007-service-on-kai.md), [operations](../../docs/deploying.md).

- Sprint 008: the content model and authoring, before Feynman (proposal
  3417). Citations gain `doi`, `chapter`/`report` kinds and `circa`, and a
  frame's Sources list is derived from citations flagged `key` (3405).
  Charts are inlined through the sanitiser, so they follow the palette mode
  (3406). `create-tools/read-source` reads PDFs and scans (3404). Both
  subjects are migrated —
  [record](../008-content-model-authoring.md).

- Sprint 009: reader data (proposal 3418). Each reader's own state has a
  SQLite store behind a storage interface, keyed by reader and subject,
  with JSON export and import (3413). Its first consumers are the last
  place, overall and per subject, offered on the start screen, and
  bookmarks, with a spine mark, a B key and a jump list across subjects
  (3414). Deep links (`/<subject>/<frame>`) came with them —
  [record](../009-reader-data.md).

- Sprint 010: the AI pane's layout (proposal 3419). Four layouts built and
  compared as a reader setting; Ken's pick is two panes with Narrative and
  AI tabs, three columns the alternative (3377). Draggable pane dividers,
  and one Ask/Grow control (3411) —
  [record](../010-ai-pane-layout-one-control.md).

- Sprint 011: the reader's layer on a frame (proposal 3420). Notes written
  in place of the scene, with a Notes tab, an unsaved-changes guard and an
  "Agent review" flag the review-notes skill works through (3409). Kept
  answers move into the reader store and are seen again, as a spine mark and
  a Q&A section (3390). The character shortcuts become remappable (3363) —
  [record](../011-readers-layer.md).

- Sprint 012: annotations (proposal 3421). A note on selected words of the
  narrative, anchored by a W3C text-quote selector so it finds its words
  after grow or an edit and shows as detached when it cannot. The A key and
  an Annotate button take the selection or let the keyboard choose it, and
  the Notes tab and the review-notes skill carry the quoted words (3415) —
  [record](../012-annotations.md).

- Sprint 013: the start screen (proposal 3425). A Home button left of the
  gear goes back to it without leaving the reader's place. A subject list
  scales it past two subjects, and the selected subject's own illustrations
  ring the loom (3424) — [record](../013-start-screen.md).

## Next

- Nothing queued in korg for kloom after the start screen; the framework
  (below) is the next large step.

## Later

- **Framework**: turn the POC into starter code, skills and agent
  instructions that generate a kloom for any subject. Its input is sprint
  006's list of what the grow skill assumed, and the authoring pipeline that
  wrote the AI subject: a plan, parallel authors, and segment-by-segment
  commits.
- More subjects: Richard Feynman (korg 3397) and the History of Computing
  (3398), and links between subjects (3399). Sprint 006 lists candidate
  links.
- Drop the README's POC banner once the framework has generated a subject.

## Ideas

- Collapsible left nav listing chapters and trails.
- A Claude API provider adapter (streamed ask answers).
