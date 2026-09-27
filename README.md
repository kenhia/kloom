# kloom

> **Status: proof of concept / work in progress.** Nothing here is stable —
> not the content format, not the UI, not the skills. That stays true until
> kloom has at least **two subjects** built on it and **tested skills** for
> generating a new one.

kloom is an interactive, growable timeline for learning a subject. Scrolling
moves a cursor along a "spine" of richly illustrated frames; a reading pane
holds the narrative, charts, images and sources for the frame you are on; and
an AI pane lets you ask for more detail or *grow* the story — new frames on
the main spine, or a side trail to explore.

The first subject is **the History of Western Civilization**. The longer aim
is a framework — starter code, agent skills and instructions — for generating
a kloom on any subject.

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
SvelteKit + TypeScript (being scaffolded in sprint 001).

## License

MIT — see [LICENSE](LICENSE).
