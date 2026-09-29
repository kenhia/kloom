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
`create-tools/` (authoring scripts: plates, citations, charts, traced art),
`skills/` (agent instructions: `grow/SKILL.md` writes content,
`review-notes/SKILL.md` works through flagged notes).

**Rules that are easy to break:**

- `engine/` never names a subject; subject content and theme live under
  `subjects/<subject>/`.
- Don't assume the spine is time — segments carry their own label kind.
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
- The repo is public.
