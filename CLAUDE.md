<!-- kproject:begin — managed by kprojects; do not edit inside this block -->

## kproject conventions

This project uses the kproject minimal harness
(<https://github.com/kenhia/kprojects>). Keep context small; prefer doing
over ceremony.

### Layout

- `sprints/` — the project's evolution, one record per PR-sized unit of
  work (a "sprint")
  - `planning/` — planning docs; at minimum `roadmap.md` (the general plan)
  - `review/` — more formal reviews as the project matures
  - sprint records: `###-<short-name>.md` for small projects, or a
    `###-<short-name>/` directory of files for larger/more formal ones
  - a sprint record is one informal narrative: goal, decisions, what
    shipped, follow-ups — written during the sprint, not after
  - projects that deploy end the record with a `## Deployed` section:
    what shipped, where, when, and what was verified live — appended
    after the deploy, not predicted before it
- `docs/` — project documentation, architecture, usage
- `.scratch/` — git-ignored scratch space for user or agent ephemera;
  use it instead of /tmp
- `justfile` — dev recipes; default recipe is `@just --list`; `just check`
  runs the CI gates; `just deploy` (or variants) if the project deploys
- `.env` — git-ignored; tokens and environment vars

### Workflow

- One sprint ≈ one PR. Sprint proposals and work items are managed in
  `korg`; durable cross-project knowledge goes in `klams`.
- Mark each work item resolved as its work completes — don't batch the
  resolutions into sprint-ship. A proposal's progress should be readable
  while the sprint is running, which is the only time it is useful.
- If the korg or klams MCP tools are unavailable in your session, say so
  up front — don't silently work around missing infrastructure.
- A few projects share contract surfaces with siblings and have a
  **guiding plan** constraining how those change; most have none, and one
  grep is the whole cost of finding out. Grep the `index.md` routing
  table in `kai:~/src/tools/cross-project-planning` — a local path on
  kai, read through kaed from any other host (`root: "kai:src"`, path
  `tools/cross-project-planning/…`); don't clone a second copy. Not
  listed → nothing applies. Listed → read the mapped plan folder before
  planning sessions and before changing a contract surface it names, and
  amend the plan in the same ship when what you build diverges from it.
- TDD preferred: write the failing test first when practical.

### Tooling preferences

- No stack the harness could name, so `just check` is yours to write. Ask
  what this repo can actually get wrong — a documents repo's failure mode is
  a stale cross-reference, not a type error
- Add no dependency to make a gate: a stdlib script or a shell one-liner
  keeps a repo that had no dependencies still having none
- Skip what isn't yours to verify — external URLs, machine-local paths
- **Negative-test it.** Plant the error the gate exists to catch and watch it
  exit 1. A gate never seen to fail is not a gate, and the seeded placeholder
  fails on purpose until you replace it
- License is MIT unless specifically directed otherwise

<!-- kproject:end -->

## Project

kloom is an interactive, growable timeline for learning a subject: a spine
scroller (left), a narrative reading pane (right) and an AI pane (bottom) that
answers questions (ask) or adds frames and side trails (grow). POC subject:
the History of Western Civilization. Later: a framework (starter code, skills,
instructions) that generates a kloom for any subject, proven on a second
subject, AI. korg project `kloom` (id 72). Status: sprint 001 shipped the scaffold,
content model and three-pane shell; sprint 002 the curated POC content (16
frames and a trail, with Chicago-style citations) and the loom start screen;
sprint 003 user settings (a gear and pop-up over a settings registry, the
Dark / Light / Mixed palette mode) and the staged scene entrance; sprint 004
ask (the provider interface, a headless `claude -p` adapter, "keep this",
the `kloom.config.json` app config and the ask-model setting); sprint 005
grow (queued jobs that commit frames and trails, written by a skill in
`skills/grow/`), the allowlist SVG sanitiser, and optional web search for ask;
sprint 006 the second subject, `subjects/ai` (66 frames), served beside
western-civ at `/<subject>`, with the narrative following the spine by
default;
sprint 007 the service on kai (`tailscale serve` :4890 with tailnet identity
gating writes, an ssh door on :4891, and grow into a service-owned content
clone that pushes `grow/kai`; `docs/deploying.md`);
sprint 008 the content model for a paper-heavy subject (citations gain
`doi`, `chapter`/`report` kinds and `circa`, and the Sources list is derived
from citations flagged `key`), charts inlined so they follow the palette
mode, and `create-tools/read-source` for PDFs and scans;
sprint 009 reader data (a SQLite store behind `ReaderStore`, keyed by
reader and subject, with export and import), the last place offered on the
start screen, bookmarks, and deep links (`/<subject>/<frame>`);
sprint 010 the AI pane's layout as a reader setting (two panes with
Narrative and AI tabs by default, three columns the alternative), draggable
pane dividers, and one Ask/Grow control (a verb, one text box, a send
button);
sprint 011 the reader's layer on a frame: notes written in place of the
scene (a Notes tab, an unsaved-changes guard, and an "Agent review" flag
that `skills/review-notes/` works through), kept answers moved into the
reader store and shown again (a spine mark and a Q&A section), and
remappable character shortcuts (S, T, B and the new N);
sprint 012 annotations: notes on selected words of a narrative, anchored by
a W3C text-quote selector so they find their words again after an edit and
show as detached when they cannot, made with A (a selection, or words chosen
with the keyboard) and listed with the notes.
Sprint 013 the start screen as a place to come back to: a Home button
left of the gear, a keyboard subject list, and the selected subject's
illustrations in a ring around the loom.
Sprint 014 the third subject, `subjects/feynman` (62 frames: a life on a
dated spine, five trails), written by following the new
`skills/author-subject/SKILL.md` (plan, a segment by hand, parallel authors,
review and commit per segment).
Sprint 015 the fourth subject, `subjects/computing` (67 frames: dates giving
way to technologies, six trails), the author-subject skill's second test,
written to complement the AI subject rather than repeat it.
Sprint 016 navigation: a table of contents in the spine's HUD (frames by
segment, trails under their anchors, the reader's marks, a filter, C to
open it), and the start screen's Continue fed by a live mirror of the
reader's places, with Begin starting from the first frame.
Sprint 017 connections, phase 1: a name registry (`names/`, keyed by
Wikidata ID) whose first mentions in a reading open a card, connections
from frame to frame with a _why_ shown on both ends, and jumps across
subjects with the browser's Back and a "↩ Back to…" chip (R).
Sprint 018 connections, phase 2: names marked across every subject (1,111
in the registry), 62 more connections (21 touching western-civ), grow
and author-subject writing names and connections (grow may add names but
never change one), and `names.py add` and `density`.
Sprint 019 connections, phase 3: the map, a full-screen overlay (M, or the
HUD beside the contents) on a frame's neighbourhood, the library of
subjects, a subject's connected frames or a name's frames; a seeded layout
that never moves (`engine/map.ts`), arrow keys between neighbours, and
"Show as list".
Sprint 020 a map you can read: a plain `topic` on every frame (required,
backfilled, written by grow and author-subject; design.md §Topics says
which surfaces name a frame by it), map labels by topic and whole, lines
dimmed at rest and brought forward for the node under the pointer or
focus, and a details panel of one height.
Sprint 021 the fifth subject, `subjects/physics` (68 frames: dates to 1900,
then categories, four trails), the bridge between western-civ and the tech
cluster, and the first written with names and connections from the start
(174 connections on its frames); `names.py reach` measures a subject's
reach, and the authoring tools refuse more of what authors could not see
(an unregistered or hand-written mark, a chart's text that will not fit).
Sprint 022 About kloom: the library counted live from the narratives
(`engine/stats.ts`, `/api/stats`, `just stats`: about 819 pages at 275
words a page), and the start screen's corner, with About (the book, the
stats, credits and the build) and the settings gear.
Sprint 023 exploring for fun: the whole library as a 3D force graph
(the map's "3D" switch; `3d-force-graph` and three.js loaded only when
it opens, decorative, with the 2D map as the accessible route), and two dice for a random frame in this subject (D) or anywhere (W).
Sprint 024 the sixth subject, `subjects/mathematics` (65 frames: dates
to 1736, then categories, three trails), every reading doing one piece of
mathematics, and the first of three author-subject runs reporting to
korg 3461.
Sprint 025 the seventh subject, `subjects/chemistry` (66 frames: dates
to 1898, then categories, three trails), every reading doing one piece
of chemistry, the second author-subject run reporting to korg 3461.
Sprint 026 a per-subject `subtitle` in `subject.json` (shown under the
title on the start screen, in the subject list and in About), and the
eighth subject, `subjects/making`, _How We Build_ (68 frames: a spine by
craft, each craft a `date` segment that starts time again, five trails),
every reading walking through one real technique, the third
author-subject run reporting to korg 3461.
Sprint 027 the author-subject skill tuned from those three runs: one
plate collector (`draw-plates/plates_for.py`), topic, sort and palette
in the plan checked by `subject_plan.py --check`, every mark spec run by
`just check` (`mark --check --placed`), the create-tools' own tests
(`just tools-test`), `skills/grow/reaching-sources.md`, and citations for
older, translated and second-hand sources (`1550 BC`, `translators`,
`edition`, `language`, `letter`, `encyclopedia`, `citedIn`,
`abstractOnly`).
Sprint 028 the ninth subject, `subjects/blood`, _In the Blood_ (62
frames: what we believed, what we learned, transfusion, what we do with
blood, and the bench by hand and by machine; four trails, one of them
military blood), built around Ken's father's career in Army blood banking
and ending on a dedication to him; the first author-subject run after the
tuning, with its decisions left on korg 3473.
Sprint 029 the author-subject skill tuned a second time, from In the
Blood's findings (korg 3473): citations gain `read` (abstract, first page,
excerpt; replacing `abstractOnly`), `citedIn` standing without a link on a
checked chain, a `diary` kind, `mirror` and JSTOR stable urls; the tools
gain `subject_plan.py --with-drafts`, a contact sheet PNG per plate,
`commons_media crop` and its Flickr and PD-self credits, and `names.py
lookup`'s set-index and item-class checks; authors are shown readings
stripped of marks (`names.py strip`), and each shared name has one owner.
Sprint 030 the tenth subject, `subjects/nursing`, _Keeping Watch_ (64
frames: care before nursing, Nightingale and the profession, the operating
room, nurses at war and the modern profession; four trails, among them
the Navy Nurse Corps and the scrub nurse's work), built around Ken's
mother's career as a Navy surgical nurse and ending on a dedication to
her, the companion to In the Blood with 13 links written into it; the
second author-subject run after the tuning, with its findings filed for
decision.
Sprint 031 ready for readers: the scene keeps to its row of the spine, the
drawing giving way and long headlines set smaller, so nothing meets the
HUD (`just scene-fit`, every frame at desktop and phone sizes), and
About's note on accuracy with a Content feedback issue form.
Sprint 032 content.db: the subjects compiled into one SQLite library
(`engine/content-db.ts`; strict for the gate, incremental by subject,
swapped in by rename) that the app serves from, the page carrying every
frame's head and the frames around it, the rest fetched per frame with
neighbours ahead (`/api/frame`), compressed responses, and `just bench`,
which measured every target met at 5× today's content.
Sprint 033 the author-subject skill tuned a third time, from Keeping
Watch's findings (korg 3478): `case` and `statute` citations in legal form
(22 migrated), `read: "record"`, a chart's data DOI rendered with its
credit; `subject_plan.py --stand-in`, `names.py drafts` with name owners
and parts in the plan, `lookup --expect` split from `--expect-item` and
shared with `wiki_cite.py --expect` (`create-tools/lib/`), `crop
--rotate`, commons_media reading NARA, Navy and Wellcome files; and
Internet Archive snippets as supporting evidence only.
Sprint 034 My notes: every note and annotation across subjects in one
dialog (O, or the HUD), each with its state in words (agent review
pending, answered, detached), filters, Go to, Clear, the flag, Clear
answered and Clear detached, and a count of agent answers not yet seen
(an `unseen` flag that `handle` sets).
Sprint 035 the RA for ask, evaluated and declined: `just ask-eval`
(`bench/ask-eval/`) asks 29 frame-tied questions the way ask does and has
Opus grade the answers blind. Sonnet 5 beat kvllm's resident model
(qwen3.8-27b) with and without web (a Wikipedia shim for the RA), and beat
Haiku 4.5, which `claude -p` runs with thinking on and which left the models
list. Ask's 250-word limit is soft.

Inspiration: <https://x.com/IterIntellectus/status/2103212539895017864>.

**Read first:** `docs/design.md` (content model, ask vs grow, interaction
rules — all decided, change the doc with the code), then
`sprints/planning/roadmap.md`.

**Stack:** SvelteKit (adapter-node) + TypeScript; toolchain modelled on
`kai:~/src/tools/koverwatch` (its sprint 001 is the scaffold template).
`just check` runs svelte-check (warnings fail — that is where the a11y lints
land), prettier + eslint, and vitest, which also loads and validates every
subject under `subjects/`. Layout: `engine/` (model, loader,
validation, Svelte UI; alias `$engine`), `subjects/<subject>/` (content),
`src/` (SvelteKit wiring — the only code that picks a subject),
`names/` (the name registry every subject shares),
`create-tools/` (authoring scripts: plates, citations, charts, traced art),
`skills/` (agent instructions: `grow/SKILL.md` writes content,
`author-subject/SKILL.md` authors a whole subject, `review-notes/SKILL.md`
works through flagged notes).

**Before a sprint's own work, review grown content** (korg 3442): run
`just grow-pending`. If it lists a pending grow branch (the service's
`grow/kai`, a dev server's `grow/dev-<host>`, an older `grow-*`), run
`skills/review-grown/SKILL.md` first and ship that review as its own PR,
then start the sprint. Nothing pending (exit 0) costs one command.

**Rules that are easy to break:**

- `engine/` never names a subject; subject content and theme live under
  `subjects/<subject>/`.
- Don't assume the spine is time — segments carry their own label kind.
- A reading marks a name's first mention only (`[words](kloom:e/<id>)`),
  and only a name in `names/`; a connection names `<subject>/<frame>`, is
  stored on one end, and says why. The gate refuses a dangling one.
- Every frame flags at least one key-source citation (`"key": true`; the
  Sources list is built from them, never written); every image or chart in
  a reading carries a `media` citation with its licence; Wikipedia is cited
  by revision (`oldid=`) and a DOI goes in `doi`.
- Model calls go through the provider interface only; `claude -p` is one
  adapter, not the architecture.
- Keyboard and screen-reader support are requirements; verify keyboard-only
  when you change interaction.
- Every request that is not a read needs a reader (`src/hooks.server.ts`); a
  new write path goes through that gate, never around it. Reader data is
  keyed by that reader, and its routes refuse a request with none, reads
  included.
- Reader data (places, bookmarks, notes, kept answers) goes through `ReaderStore`,
  never straight to SQLite; a schema change is a new migration, never an
  edit to a shipped one.
- Grown content reaches `main` only through `skills/review-grown`: a grow
  commits to a grow branch (`grow/kai`, `grow/dev-<host>`), never to `main`
  or a sprint branch, and a review's squash carries the `Grow-reviewed`
  trailer.
- The repo is public.
