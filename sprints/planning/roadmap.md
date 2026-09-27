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

## Next

The curated frames are the bar grow is written against.

- Grow (proposal 3369): frames and trails written by the model, in the
  curated frames' style and with `citations` (3364), after the allowlist
  sanitiser (3365). It adds a grow-model setting (default Opus 5.5).
- Run as a service on kai.

## Later

- **Framework**: turn the POC into starter code, skills and agent
  instructions that generate a kloom for any subject.
- **Explorations into AI**: the second subject, built with the framework —
  tests the skills and the mixed-segment spine (dates, then technologies).
- Drop the README's POC banner once both subjects and the skills hold up.

## Ideas

- Collapsible left nav listing chapters and trails.
- A Claude API provider adapter (streamed ask answers).
