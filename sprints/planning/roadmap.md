# Roadmap

> The general plan for this project. Keep it current; detail lives in the
> sprint records. Design decisions: [docs/design.md](../../docs/design.md).

## Now — POC: History of Western Civilization

- Sprint 001: SvelteKit + TypeScript scaffold with real gates (korg 3356),
  the content model (3357) and the three-pane shell with keyboard control and
  Sync Narrative (3358).

## Next

- AI backend: ask/grow behind a provider interface, first adapter headless
  `claude -p` (3360) — probably an ask sprint, then a grow sprint.
- POC content: ~12 hand-curated frames following the video's arc, plus one
  trail (3361).
- Start screen: the gold-on-black loom (3359).
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
