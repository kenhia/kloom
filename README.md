# kloom

> **Status: proof of concept / work in progress.** Nothing here is stable —
> not the content format, not the UI, not the skills. That stays true until
> kloom has at least **two subjects** built on it and **tested skills** for
> generating a new one.

kloom is an interactive, growable timeline for learning a subject. Scrolling
moves a cursor along a "spine" of richly illustrated frames; a reading pane
holds the narrative, charts, images and sources for the frame you are on; and
an AI pane lets you ask for more detail or _grow_ the story — new frames on
the main spine, or a side trail to explore.

There are two subjects so far, both served by one app:

- **the History of Western Civilization**, 18 frames and two trails;
- **the History and Current State of AI**, 41 frames and four trails, on a
  spine that runs from myths through dates to technologies.

The longer aim is a framework (starter code, agent skills and instructions)
for generating a kloom on any subject.

## Inspiration

The look and feel come from a short video made with Claude:
["i asked claude to make a video on western civilization"](https://x.com/IterIntellectus/status/2103212539895017864)
(@IterIntellectus, September 2026). kloom is not a video — it borrows that
visual language (era-tracking palettes, big serif headlines with one accent
word, line drawings that draw themselves, a persistent timeline HUD) for a
page you scroll, read and extend.

## Layout

```
+---------------------------+---------------------------+
|  spine scroller           |  narrative                |
|  (the visual hook)        |  (read, dive in)          |
+---------------------------+---------------------------+
|  AI: ask / grow the story / add a trail               |
+-------------------------------------------------------+
```

See [docs/design.md](docs/design.md) for the content model and interaction
rules, and [sprints/planning/roadmap.md](sprints/planning/roadmap.md) for
where it is going.

## Development

This repo uses the [kprojects](https://github.com/kenhia/kprojects) minimal
harness: `just` lists recipes, `just check` runs the gates. The app is
SvelteKit + TypeScript on Node 22.13+ or 24:

```sh
npm ci
just dev      # http://127.0.0.1:5173, loopback only
just check    # types + a11y lints, prettier/eslint, unit tests, content validation
just build    # Node server in build/; run with `node build`
```

Code lives in four places. `engine/` is the subject-agnostic model, loader,
validation and UI. `subjects/<subject>/` holds one subject's content, one
directory per frame. `src/` is the SvelteKit wiring that serves every
subject under `KLOOM_SUBJECTS_DIR` (default `subjects`) at `/<subject>`;
`/` opens `KLOOM_SUBJECT` (default `western-civ`), and the start screen
links the others. `create-tools/` holds the authoring scripts that made the
content (plates, citations, charts, traced art); see its README. `skills/`
holds the instructions a model writes content by: `skills/grow/SKILL.md` is
what grow jobs follow, and they commit to the git repository the subject
lives in.

Ask runs headless `claude -p` on the host, so the server needs a logged-in
Claude Code on its `PATH`. The models on offer, and which one ask defaults
to, are in the app config `kloom.config.json` (`KLOOM_CONFIG` to use
another). Kept answers are written under `data/` (`KLOOM_DATA_DIR`), which is
git-ignored.

## License

MIT — see [LICENSE](LICENSE).
