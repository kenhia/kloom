# kloom

> **Status: proof of concept / work in progress.** Nothing here is stable —
> not the content format, not the UI, not the skills. That stays true until
> kloom has at least **two subjects** built on it and **tested skills** for
> generating a new one.

kloom is an interactive, growable timeline for exploring a subject. Scrolling
moves a cursor along a "spine" of richly illustrated frames; a reading pane
holds the narrative, charts, images and sources for the frame you are on; and
an AI pane lets you ask for more detail or _grow_ the story — new frames on
the main spine, or a side trail to explore.

There are twelve subjects so far, all served by one app:

- **the History of Western Civilization**, 58 main-spine frames from
  myth to cosmos, through law, faith, philosophy, art, politics and
  empire, with five trails (the measure of things, the printing press,
  Rome, revolutions, the idea of rights);
- **the History and Current State of AI**, 41 main-spine frames and four
  trails, on a spine that runs from myths through dates to technologies;
- **Richard Feynman**, a life on 34 dated frames with five trails (the path
  integral, the diagrams, Los Alamos, computing and the Challenger
  commission), written with the author-subject skill;
- **the History of Computing**, 37 main-spine frames from counting boards
  to the cloud, on dates that give way to technologies, with seven trails
  (Babbage's engines, beyond counting, Bletchley and Colossus, the
  transistor to Moore's law, the personal computer, the internet stack,
  Unix and C);
- **the History of Physics**, 45 main-spine frames from Aristotle to
  cosmology, on dates to 1900 and then categories (relativity, the quantum,
  the nucleus, particles, the cosmos), with four trails (the field, heat and
  information, the quantum revolution, the Standard Model); the first
  subject written with names and connections from the start, and the
  bridge between western-civ and the other three;
- **the History of Mathematics**, 49 main-spine frames from the Ishango
  bone to proofs checked by machine, on dates to 1736 and then categories
  (algebra, analysis, geometry, probability, logic and foundations), with
  three trails (Fermat's Last Theorem, the primes, infinity); every
  reading does one piece of mathematics in front of the reader;
- **the History of Chemistry**, 53 main-spine frames from the first copper
  smelting to AlphaFold, on dates to 1898 and then categories, with three
  trails (alchemy's last century, from dyes to drugs, finding the
  elements); every reading does one piece of chemistry;
- **How We Build**, 46 main-spine frames on a spine by craft, each craft
  starting time again, with five trails (the forge, joinery, the lathe,
  materials science, slicers and supports); every reading walks through
  one real technique;
- **In the Blood**, 40 main-spine frames, what we believed, what we
  learned, transfusion, what we do with blood, and the bench by hand and
  by machine, with four trails (what we got wrong, beyond ABO, blood at
  war, clotting), built around Ken's father's career in Army blood banking
  and ending on a dedication to him;
- **Keeping Watch**, 42 main-spine frames, care before nursing, Nightingale
  and the profession, the operating room, nurses at war and the modern
  profession, with four trails (Nightingale's numbers, the scrub nurse's
  work, the Navy Nurse Corps, who was let in), built around Ken's
  mother's career as a Navy surgical nurse and ending on a dedication to
  her; the companion to In the Blood;
- **Daily Bread**, 49 main-spine frames on how humanity learned to feed
  itself, from fire and foraging through the first farmers, grain and
  empire, spice and trade, the agricultural revolutions, keeping food and
  the modern harvest to the table, with four trails (the first drinks,
  bread, the potato, famine);
- **The Story of Life**, 52 main-spine frames on the history of biology,
  from Aristotle's animals through the microscope, deep time, inheritance
  and the molecule to reading and writing genomes and ecology, with three
  trails (germ theory, the Beagle, what we got wrong).

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
just check    # types + a11y lints, prettier/eslint, unit tests, content validation, reader gate
just build    # Node server in build/; run with `node serve.js`
just build-reader  # the reader edition in build-reader/; `KLOOM_EDITION=reader node serve.js`
```

On kai it runs as a service behind `tailscale serve`, where ask, keep and
grow need a signed-in tailnet user. The public site runs the reader
edition: no ask, grow or keep, and invited readers who sign in. See
[docs/deploying.md](docs/deploying.md).

Code lives in four places. `engine/` is the subject-agnostic model, loader,
validation and UI. `subjects/<subject>/` holds one subject's content, one
directory per frame, and `names/` the people, places and things the subjects
share, one file each (`KLOOM_NAMES_DIR`, by default beside the subjects).
`src/` is the SvelteKit wiring that serves every
subject under `KLOOM_SUBJECTS_DIR` (default `subjects`) at `/<subject>`;
`/` opens `KLOOM_SUBJECT` (default `western-civ`), and the start screen
links the others. `create-tools/` holds the authoring scripts that made the
content (plates, citations, charts, traced art); see its README. `skills/`
holds the instructions a model writes content by: `skills/grow/SKILL.md` is
what grow jobs follow, and they commit to the git repository the subject
lives in. As a service, that is the service's own content clone, on a grow
branch that it pushes.

Ask runs headless `claude -p` on the host, so the server needs a logged-in
Claude Code on its `PATH`. It can also run on the Claude API with an API
key, `ANTHROPIC_API_KEY`, which logs what each ask costs (`just ask-costs`).
The providers, the models on offer and which one ask defaults to are in the
app config `kloom.config.json` (`KLOOM_CONFIG` to use another). Kept answers are written under `data/` (`KLOOM_DATA_DIR`), which is
git-ignored.

## License

MIT — see [LICENSE](LICENSE).
