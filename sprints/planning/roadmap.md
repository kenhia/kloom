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

- Sprint 014: the third subject, Richard Feynman (proposal 3426). The
  method sprint 006 used, written down as `skills/author-subject/SKILL.md`
  and followed: a plan, a segment by hand, eleven parallel authors, review
  and a commit per segment. 62 frames, a life on a dated spine with five
  trails (3397) — [record](../014-third-subject-feynman.md).

- Sprint 015: the fourth subject, the History of Computing (proposal
  3427). The author-subject skill's second test: a segment by hand,
  fourteen parallel authors, review and a commit per segment. 67 frames,
  dates giving way to technologies, with six trails, complementing the AI
  subject (3398) — [record](../015-fourth-subject-computing.md).

- Sprint 016: navigation (proposal 3434). A table of contents in the spine's
  HUD, left of the bookmark: frames by segment, trails collapsed under their
  anchors, the reader's marks, a filter, and C to open it (3433). This was
  the "collapsible nav" idea, made as a popover. The start screen's
  _Continue_ now continues: Begin starts from the first frame, and Continue
  comes from a live mirror of the reader's places (3432) —
  [record](../016-navigation-toc-continue.md).

- Sprint 017: connections, phase 1 (proposal 3443). A name registry shared
  by every subject, keyed by Wikidata ID, with first-mention marks that
  open a card ("Appears in…"). Connections from frame to frame, each with
  a _why_, shown on both ends. Jumps across subjects that land on the
  frame, with the browser's Back and a stacking "↩ Back to…" chip. 45
  connections from the recorded candidates, and western-civ's names as
  the proof (3439) — [record](../017-connections.md).

- Sprint 018: connections, phase 2 (proposal 3444). Names marked across
  AI, Feynman and Computing (1,111 in the registry), 62 more connections
  (21 touching western-civ), and grow and author-subject writing names and
  connections (3440) — [record](../018-connections-2.md).

- Sprint 019: connections, phase 3, the map (proposal 3445). A full-screen
  map on a frame's neighbourhood (one or two steps, names ranked by how
  rare they are), the library of subjects, a subject's connected frames and
  a name's frames; a seeded layout that never moves, keyboard moves between
  neighbours, and "Show as list" (3441) — [record](../019-connections-3-the-map.md).

- Sprint 020: a map you can read (proposal 3450). A `topic` on every
  frame, backfilled across the four subjects and written by grow and
  author-subject (3446); map labels by topic, shown whole, lines dimmed at
  rest and brought forward for the hovered or focused node, and a details
  panel that never resizes the graph (3447); no text selected on a
  double-click (3448) — [record](../020-a-map-you-can-read.md).

- Sprint 021: the fifth subject, the History of Physics (proposal 3451,
  covering 3428). 68 frames, the first written with names, connections and
  topics from the start, by the author-subject skill's link steps; 174
  connections stored on its frames (108 into the other subjects), and
  western-civ's reach into the tech cluster raised from 21 to 27 frames in
  two steps and 27 to 47 in three — [record](../021-fifth-subject-physics.md).

- Sprint 022: About kloom (proposal 3457). The library counted live from
  the narratives (`engine/stats.ts`, `/api/stats`, `just stats`: about 819
  pages at 275 words a page) (3455), and the start screen's corner, with
  About and the settings gear (3456) — [record](../022-about-kloom.md).

- Sprint 023: exploring for fun (proposal 3452). The whole library as a 3D
  force graph behind the map's "3D" switch, `3d-force-graph` loaded only
  when it opens (3449), and two dice: a random frame in this subject (D)
  and anywhere in the library (W), never the one you are on (3437) —
  [record](../023-exploring-for-fun.md).

- Sprint 024: the sixth subject, the History of Mathematics (proposal
  3462, covering 3429). 65 frames, every reading doing one piece of
  mathematics; the first of three author-subject runs reporting to 3461 —
  [record](../024-sixth-subject-mathematics.md).

- Sprint 025: the seventh subject, the History of Chemistry (proposal
  3463, covering 3430). 66 frames, every reading doing one piece of
  chemistry; 108 connections stored on its frames; the second run
  reporting to 3461 — [record](../025-seventh-subject-chemistry.md).

- Sprint 026: a per-subject subtitle (3465), and the eighth subject, _How
  We Build_, "creating the objects around us" (proposal 3464, covering
  3431). 68 frames on a spine by craft (each craft a `date` segment that
  starts time again) and five trails, every reading walking through one
  real technique; 83 connections on its frames, 42 into other subjects;
  the third run reporting to 3461 — [record](../026-how-we-build.md).

- Sprint 027: the author-subject skill and its tools tuned from those
  three runs (proposal 3467, covering 3461): one plate collector, topic,
  sort and palette checked in the plan, `mark --check` in `just check`,
  namesake and stale-draft warnings, Commons, contact-sheet and wiki-cite
  fixes, one "reaching sources" reference, a test gate for the
  create-tools, and the citation schema for older, translated and
  second-hand sources (BC dates, translators, editions, letters,
  encyclopedia entries, "cited in") —
  [record](../027-tune-author-subject.md).

- Sprint 028: the ninth subject, _In the Blood_ (proposal 3468, covering
  3466): 62 frames from the four humours to the automated laboratory,
  every reading showing how we knew or how it was done, the bench and
  blood-bank procedures from the manuals that taught them, four trails
  (what we got wrong, beyond ABO, blood at war, clotting) and a
  dedication to Colonel Joel T. Hiatt; 88 connections on its frames, 20
  into other subjects; the authors' feedback repaired where mechanical
  and left on korg 3473 where it needs a decision —
  [record](../028-in-the-blood.md).

- Sprint 029: the author-subject skill tuned a second time, from In the
  Blood's findings (proposal 3476, covering 3473): `read` on citations,
  `citedIn` without a link, a `diary` kind, mirrors and JSTOR stable urls;
  `subject_plan.py --with-drafts`, a contact sheet per plate, `commons_media
crop`, `names.py lookup`'s checks, readings shown to authors without
  marks, and one owner per shared name —
  [record](../029-tune-author-subject-second-pass.md).

- Sprint 030: the tenth subject, _Keeping Watch_ (proposal 3471, covering
  3470): 64 frames from care before nursing to the modern profession, four
  trails, built around Ken's mother's career as a Navy surgical nurse and
  ending on a dedication to her; the companion to In the Blood, with 13
  links written into it — [record](../030-keeping-watch.md).

- Sprint 031: ready for readers (proposal 3479, covering 3469 and 3477):
  the scene keeps to its row of the spine (`just scene-fit`), and About's
  note on accuracy with a Content feedback issue form —
  [record](../031-ready-for-readers.md).

- Sprint 032: content.db (proposal 3480, covering 3460): the subjects
  compiled into one SQLite library the app serves from, frames fetched on
  demand with their neighbours ahead, compressed responses, and `just
bench` — [record](../032-content-db.md).

- Sprint 033: the author-subject skill tuned a third time, from Keeping
  Watch's findings (proposal 3485, covering 3478): `case` and `statute`
  citations in legal form, `read: "record"`, a chart's data DOI, and the
  tools' stand-ins, drafts and expectations —
  [record](../033-tune-author-subject-third-pass.md).

- Sprint 034: My notes (proposal 3482, covering 3481): every note and
  annotation across subjects in one dialog (O), with its state in words,
  filters, Go to, Clear, the agent-review flag, Clear answered and Clear
  detached, and a count of agent answers not yet seen —
  [record](../034-my-notes.md).

- Sprint 035: the RA for ask, evaluated and declined (proposal 3484,
  covering 3483): `just ask-eval` asks 29 frame-tied questions as ask does
  and has Opus grade them blind; Sonnet 5 stays ask's model —
  [record](../035-ra-for-ask.md).

- Sprint 036: grown content reviewed into main (proposal 3492, covering
  3442, 3486 and 3487): grow branches, `just grow-pending`,
  `skills/review-grown`, one grow job under a dev reload, and navy-pow's
  Guam section re-sourced —
  [record](../036-grow-review-and-guam.md).

- Sprint 037: keyboard shortcuts in their own dialog (proposal 3494,
  covering 3493): key capture with modifiers, reserved combinations refused,
  and a settings pop-up whose selects keep their width —
  [record](../037-keyboard-shortcuts-dialog.md).

- Sprint 038: colours by section (proposal 3498, covering 3495): a palette
  per section, the scene and the reading coloured apart, brightness sliders,
  and every subject re-paletted — [record](../038-colours-by-section.md).

- Sprint 039: the reader edition and sign-in (proposal 3505, covering 3500,
  3501 and 3502; the first slice of program 3508, the public reader site): a
  build with ask, grow, keep and the agent code stripped out, checked by
  `just reader-gate`; invite-only accounts with one-time welcome links,
  year-long sessions and an admin CLI; and the Welcome and How-To page —
  [record](../039-reader-edition-and-sign-in.md).

## Next

- Whatever the korg Planning queue holds for project kloom (72).

## Later

- **Framework**: turn the POC into starter code, skills and agent
  instructions that generate a kloom for any subject. Its input is sprint
  006's list of what the grow skill assumed, and the authoring pipeline that
  wrote the AI subject, now written down as `skills/author-subject/SKILL.md`
  and tested on Feynman in sprint 014.
- Drop the README's POC banner once the framework has generated a subject.

## Ideas

- A Claude API provider adapter (streamed ask answers).
