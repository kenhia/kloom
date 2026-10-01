# 026 — Eighth subject: How We Build

## Goal

korg proposal 3464, covering korg 3465 and 3431: a per-subject subtitle,
then the eighth subject, _How We Build_, subtitled "creating the objects
around us": carpentry, forge work, machining and 3D printing, and the
crafts beside them. It links on purpose into chemistry (metals, heat
treatment, glass, plastics), physics (mechanics, heat), computing
(numerical control, G-code, open source) and western-civ (steam, the
metre survey, precision measurement). It is the third of three
back-to-back runs of `skills/author-subject/SKILL.md` whose issues are
reported to korg 3461, and the run most likely to stress it, because its
spine is not one timeline.

## Decisions

- **Premises held.** `subject.json` had no subtitle and the route passed
  the app's tagline; there was no subject about making; chemistry's
  sixteen pending links were waiting on korg 3431. kloom is not in the
  cross-project plan index.
- **Ken's answers at the start (2026-09-30):** the branch is
  `026-how-we-build`; **every reading walks through one real technique**,
  history-first, as chemistry's readings each do one piece of chemistry
  (not history only, and not a separate how-to kind of frame); about 65
  frames, with trails including materials science, and room left for grow.
  He had already said (on 3431) that the crafts named were a starting
  point and that he expects to grow this subject a good deal.
- **The id is `making`**, served at `/making`, with the title _How We
  Build_.
- **The before, recorded first**: `names.py density` and `names.py reach
western-civ --steps 3` before any frame (`.scratch/build/density-before.txt`,
  `reach-before.txt`). Western-civ then reached 6 ai, 12 computing and 14
  feynman frames in two steps, 32 of the tech cluster's 198, and 54 in
  three.

### The subtitle (korg 3465)

`subject.json` takes an optional `subtitle`, a line of at most 60
characters (`SUBTITLE_MAX`), validated beside the title. The loader and
the subject listing carry it. On the start screen it stands under the
selected subject's title in place of kloom's tagline, which a subject
without one keeps; the subject list says it under the title, and so does
About's table of subjects. Labels that name a subject in passing (the
back chip, a name card, the map) keep the title alone. design.md §Files
and §Start screen, the author-subject skill and the grow skill's file
table say so. Tests: validation (length, type, blank), the listing (a
non-string subtitle is dropped), and stats.

### Shape

The plan is `create-tools/subject-plan/making.json`: 46 main-spine frames
and five trails of 22, 68 in all.

- **By craft, each craft a `date` segment that starts time again.** The
  proposal pictured "`category` segments with dates inside". But a
  segment's `labelKind` says what its frames' labels are, and the
  validator checks rising sorts only within a segment, so a spine by craft
  whose frames are dated is a run of `date` segments: Stone and fire
  (3.3 million years ago to 200,000), Clay and glass (3500 BC to 1959),
  Wood (5100 BC to 1942), Metal by fire (4000 BC to 1881), Machines that
  make machines (1774–1900), Making many (1803–1961), Code and machine
  (1952–80) and Layer by layer (1984–2015). Only the last segment, Making
  now, is a `category` segment. The author-subject skill now says this.
- **Five trails**, each a detour a reader may skip:

  | Trail                | Anchor               | Kind       | Frames |
  | -------------------- | -------------------- | ---------- | -----: |
  | Joinery              | `egyptian-carpentry` | `category` |      3 |
  | At the forge         | `bloomery`           | `category` |      4 |
  | Materials science    | `japanese-sword`     | `date`     |      7 |
  | Lathe work           | `maudslay`           | `category` |      4 |
  | Slicers and supports | `fdm`                | `category` |      4 |

- **Every reading walks through one real technique**: where to strike
  and at what angle, how a soft hammer thins an edge, how bark is
  distilled without air, and so on through dovetails, temper colours,
  three-plate scraping, change gears and slicing. History stays most of
  each frame.
- **The voice** is the collective "we" of the other subjects.
- **Ken's own work as a source.** Three of his public repositories are
  cited where they show a technique: `openscad_exploration` for
  parametric design, `kCheatSheet` for mesh export settings and
  `kTaskLight` for designing a printed part to fit.

### Theme

Five dark/light pairs, each tied to a family of crafts:

| Palette   | Scheme | For                                   | Ink  | Muted | Accent | Line |
| --------- | ------ | ------------------------------------- | ---- | ----- | ------ | ---- |
| flint     | dark   | stone, clay and glass                 | 14.8 | 7.5   | 9.1    | 11.2 |
| chalk     | light  | stone, clay and glass                 | 15.1 | 6.5   | 6.3    | 12.8 |
| oak       | dark   | wood                                  | 14.7 | 7.9   | 8.4    | 11.1 |
| shavings  | light  | wood                                  | 14.7 | 6.6   | 5.9    | 12.4 |
| ember     | dark   | metal by fire                         | 14.9 | 7.8   | 6.0    | 11.0 |
| scale     | light  | metal by fire                         | 14.7 | 6.7   | 6.0    | 12.7 |
| blueprint | dark   | machine tools, measurement, materials | 14.9 | 7.7   | 9.5    | 11.6 |
| drafting  | light  | machine tools, measurement, materials | 14.7 | 6.5   | 6.4    | 12.0 |
| filament  | dark   | plastics, robots, printing            | 15.5 | 8.2   | 10.8   | 12.0 |
| resin     | light  | plastics, robots, printing            | 15.3 | 6.8   | 6.9    | 13.1 |

The lowest contrast is 5.9:1, against a floor of 4.5
(`.scratch/build/palettes.py`).

### The first segment, by hand

Stone and fire has three frames:

- `knapping` (c. 3.3 million years ago): Lomekwi 3, found after a wrong
  turn, read in Harmand et al. 2015; the technique of knapping from the
  Dibble experiments as synthesised by Li et al. 2023 (platform angle and
  depth settle a flake, force is a threshold); Lomekwi's failed blows read
  as too much platform depth; the Oldowan pushed back to Nyayanga, with
  _Paranthropus_ beside it (Plummer et al. 2023).
- `handaxe` (c. 1.76 million years ago): John Frere's letter of 1797,
  read in _Archaeologia_ 13; Kokiselei 4 (Lepre et al. 2011); the soft
  hammer and Bordes's ratios, with refinement (width over thickness)
  worked from invented numbers; Stout et al. 2015's six students, whose
  hand axes were no thinner after 167 hours; Boxgrove's elephant-bone
  hammer (Parfitt and Bello, January 2026).
- `birch-tar` (c. 200,000 years ago): the first synthetic material;
  Kozowyk et al. 2017's three methods with their temperatures and yields,
  and the Campitello lump worked as runs and grams of bark; the
  condensation method and the Königsaue tar's underground origin (Schmidt
  et al. 2023); the Zandmotor flake, Ötzi and a chewed lump with a genome.

**What writing them found** (each also a comment on korg 3461): the
spine-by-craft question above (repaired in the skill); HAL's PDF links
answer scripts with a JavaScript challenge and `/document` serves the
file; Europe PMC serves only the open-access subset, so PNAS papers come
back empty; a transparent PNG turns black as a JPEG unless composited onto
white; a thing with no English Wikipedia article gets no name; Wikipedia's
Acheulean article sends Frere's flints to the wrong society; and the
recurring ones: the plan holds only ids, a sixth identical plate collector,
Commons citations rewritten by hand, wide contact sheets.

### Authoring at scale

- **Twenty-one authors in parallel**, each a subagent with a shell and the
  web, given a shared brief (`.scratch/build/brief.md`) and a paragraph of
  its own (`.scratch/build/parts.md`): frames in order, each with its
  topic, label, sort, palette, the technique to walk through, what it owns
  and what it leaves to a neighbour, and connection candidates. The brief
  says its facts are leads, not sources, and names the five anchors to
  finish first. Twenty ran at once (the limit), and the twenty-first
  (`now`) started when the first finished.
- **Review, per part, as each reported:** `.scratch/build/review.sh` (a
  copy with every author's drafts: completeness, the subject tests with the
  marks placed, word counts, accent, topic and image clashes), a contact
  sheet of the plates, the report's unsure claims read, then
  `.scratch/build/commit.sh`: names added, marks placed, staged with
  `stage_segment.py`, the exported index tested before every commit, and
  unstaged on failure. Twenty-two content commits; none failed its index
  check.
- **Within-subject connections** were added at review from the authors'
  lists by `.scratch/build/conns.py`, which refuses one whose terms
  neither reading holds; 41 went in. Two written onto frames committed
  earlier were left unstaged by the first commit script, found by
  `git status` and committed (`afa5a6f`); the script now stages any
  committed frame a connection changed.
- **What it came to:** 68 frames and about 60,200 words of narrative
  (219 pages at 275 words a page); 115 images, each looked at before use
  and none repeated in the repository; 8 charts and many tables; six
  frames dated with `asOf`; every accent unique; 373 new names (the
  registry has 2,510).
- **Where sources disagreed, the readings give both**, scores of times:
  the first stone tools' makers, Frere's society, Huntsman's dates and
  heat, the Japanese sword's core carbon, the Iron Bridge's part counts,
  Nasmyth's own telling of the steam hammer, Benardos's year, Whitney's
  milling machine, Johansson's patent, Hendry against Willert, Bézier
  against de Casteljau, the Unimate's plant and axes, the 45° overhang
  rule, ASML's and Zeiss's mirror smoothness.
- **Ken's repositories** are cited in `openscad` (six lines of
  `drawer_nameplate.scad`, read line by line; the repository has no
  licence, and the quotation is short), `stl-meshes` (kCheatSheet's mesh
  settings and kTaskLight's STL files, measured) and `printed-fits`
  (kTaskLight, MIT).

### What the tools and skills assumed

Every author reported where the skills, the brief or a tool was wrong,
silent or in the way (raw notes: `.scratch/build/findings.md`); the
roll-up is on korg 3461 beside the two earlier runs'. What recurred most:

- **One broken plate module stopped every author** (nine reported it):
  `making.py` imported every module before looking at the frames named,
  and a stray `\n` in one stopped everyone's drawing. Repaired here.
- **Marks typed by hand from habit** (eight), copied from the
  hand-written frames, whose marks the tool had placed. The grow and
  author-subject skills now say so.
- **Namesake articles** pass `wiki_cite` and `lookup` silently (four: a
  politician, a senator, a priest and a footballer). The grow skill now
  warns; whether `lookup` should check is left on 3461.
- **The brief was wrong in sixteen of twenty-one paragraphs**, each
  caught by an author reading the source (Boulton's shilling, not Watt's;
  Johansson's 1896 steps of 0.01 mm; Willert, not Hendry; RS-274-D in
  1979; the _Schenectady_ a tanker at her pier; a strap lathe at
  Petosiris; the dovetail's slope rule uncited). The leads-not-sources rule
  held for a third run. One gap was mine: mass1's paragraph listed no
  connection candidates.
- **Recurred from 024 and 025:** `mark --check` exiting 1 on success,
  sites refusing scripts, wide contact sheets, the tight word band,
  Commons citations rewritten by hand, the plan holding only ids.

### Connections, and the bridge

- **83 connections are stored on making frames**: 42 into other subjects
  (20 chemistry, 10 computing, 7 western-civ, 2 mathematics, 2 physics, 1
  feynman) and 41 between making frames. 37 of the 68 frames connect to
  another subject.
- **The links the proposal asked for:** chemistry's metals and heat
  treatment (`lost-wax`, `bloomery` → `copper-smelting`; `japanese-sword`,
  `huntsman-steel`, `chinese-cast-iron`, `iron-carbon`, `heat-treatment` →
  `bessemer-steel`; `duralumin` → `aluminium`; `arc-welding` →
  `davy-electrolysis`), glass and plastics (`glassblowing` →
  `clay-recipes`, `float-glass` → `leblanc-solvay`, `injection-moulding`,
  `fdm`, `carbon-fibre`, `moulded-plywood` → `polymers`,
  `stereolithography`, `euv` → `photolithography`); physics' mechanics
  and heat (`galileo-beams` → `falling-bodies`, `coalbrookdale` →
  `carnot`); computing (`numerical-control` → `whirlwind`, `bezier-curves`
  → `macintosh`, `reprap`, `slicing` → `free-software`, `openscad` →
  `open-source`, `maudslay`, `whitworth`, `interchangeable-parts`,
  `screw-cutting` → `clement-fragment`, `euv` → `end-of-scaling`);
  western-civ (`wilkinson-boring`, `coalbrookdale`, `steam-hammer`,
  `wind-sawmill`, `block-mills` → `steam`; `gauge-blocks` →
  `metre-survey`; `westminster-hall` → `florence-dome`).
- **Chemistry's pending links:** eight of its fourteen frames are now
  linked (`copper-smelting`, `type-metal`, `bessemer-steel`, `aluminium`,
  `photolithography`, `polymers`, `leblanc-solvay`, `clay-recipes`). Left
  unmade, because no reading on either side states the link:
  `alexandrian-alchemy`, `agricola`, `mineral-acids`, `bottger-porcelain`,
  `silicon`, `lithium-battery`, `haber-bosch`, and the weaker `gunpowder`
  and `newton-alchemy`.
- **Physics is thin** (two links): its frames are about laws, and only
  Carnot's steam engines and Galileo's book touch a maker's craft in their
  readings.
- **Density** (`names.py density`), after:

  | Subject     | Frames | Marks per frame | Connections per frame |
  | ----------- | -----: | --------------: | --------------------: |
  | ai          |     66 |           11.24 |                  1.15 |
  | chemistry   |     66 |            7.73 |                  1.94 |
  | computing   |     70 |           10.33 |                  1.34 |
  | feynman     |     62 |            8.65 |                  1.65 |
  | making      |     68 |            7.21 |                  1.22 |
  | mathematics |     65 |            7.71 |                  2.25 |
  | physics     |     68 |            7.37 |                  3.29 |
  | western-civ |     24 |            7.04 |                  3.88 |

- **Western-civ's reach** (`names.py reach`), before (recorded at the
  start) and after:

  | To        | Frames | Within 1 | Within 2    | Within 3    |
  | --------- | -----: | -------: | ----------- | ----------- |
  | ai        |     66 |        0 | 6           | 14          |
  | computing |     70 |        4 | 12          | 19 → 20     |
  | feynman   |     62 |        7 | 14          | 21 → 22     |
  | total     |    198 |       11 | **32 → 32** | **54 → 56** |

  One step out, western-civ now reaches 7 making frames, 18 in two and 32
  in three. As with the earlier subjects, the gain into the tech cluster
  is small: making's links to western-civ run through steam and the metre,
  and into computing through numerical control and Clement, but the two
  sets of frames rarely meet within two steps. In two steps making itself
  reaches 20 chemistry, 16 physics, 12 computing, 10 mathematics, 9
  western-civ, 6 ai and 4 feynman frames.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint
  and 1,042 tests; every subject is loaded and validated, every SVG
  sanitised, and the links test finds every connection's frame and every
  mark's name.
- **Every content commit was validated on its own**, the index exported
  and the subject tests run on it.
- **All 90 mark specs pass `--check`**, every subject's.
- **Negative tests, each seen failing:** the subtitle validation (blank,
  wrong type, 61 characters); `making.py` with a planted broken module
  (skipped and named, the asked-for frame still drawn; a missing frame
  still exits 1); `commons_media`'s date on five BC strings; `names.py
add --check` on a name already held; `review.sh`'s accent check (FLAT,
  taken by two authors mid-sprint, caught in a copy); `conns.py` on whys
  whose terms no reading held (seven candidates refused).
- **Browser pass** (Playwright, headless Chromium, keyboard only, on an
  export of the committed tree, `.scratch/build/walk.mjs`):
  - `/making`: the start screen titled "How We Build" with "creating the
    objects around us" under it, Enter to begin; the subject list says the
    subtitle under the title; selecting a subject without one brings back
    kloom's tagline; About's table carries it
    (`.scratch/build/subtitle.mjs`);
  - → through all 46 main-spine frames in plan order, with the right
    accent and HUD label at each;
  - T into each of the five trails at its anchor, → through every trail
    frame, Esc back to the anchor: 68 stops, no mismatch;
  - Home and End reach HIT. and MAKING.; a deep link to a trail frame
    (`/making/dovetail`); no broken images, console errors or failed
    requests, and no horizontal overflow at 390px.
- **The counter overlap** (korg 3469), measured as sprint 025 did
  (`.scratch/build/overlap.mjs`): one making frame overlapped at
  1400×900, `wootz`, whose headline was shortened; none now.

## Repaired in passing

- **The skills**, from the hand segment: the author-subject skill on
  `date` segments by craft; the grow skill on HAL's `/document`, Europe
  PMC's open-access subset, compositing a transparent PNG before JPEG, and
  names with no English article.
- **`making.py`** names and skips a module that fails to import, so one
  author's half-written plates stop only their own frames.
- **`commons_media`** leaves out a BC date and an "AnonymousUnknown
  author"; **`names.py add --check`** names the drafts it leaves alone.
- **The reading pane** styles inline code and preformatted programs, and
  a long line scrolls instead of widening the pane on a phone (sixteen
  readings already used inline code).
- **The skills and the subject-plan README**, from the authors' reports:
  the mark form never typed, namesake articles, emphasis beside sub- and
  superscripts, code blocks, more routes to sources, Prettier on drafts, a
  live anchor before a stand-in, who drafts a shared name, and what
  `--only` keeps.
- **Fourteen shared names** widened or homed.
- **The roadmap** had no entries for sprints 024 and 025; they are added
  beside 026's.
