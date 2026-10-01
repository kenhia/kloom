# 025 — Seventh subject: the History of Chemistry

## Goal

korg proposal 3463, covering korg 3430: the seventh subject, chemistry
from the first smelted copper to AlphaFold and the Keeling curve, written
with links into western-civ (writing on clay, the scriptorium's inks,
printing's type metal, the DNA frame), physics (atoms, quantum
chemistry), computing (silicon, lithography) and the making subject
(korg 3431, not yet written). It is the second of three back-to-back runs
of `skills/author-subject/SKILL.md` whose issues are reported to korg
3461, and success includes that report.

## Decisions

- **Premises held.** There was no `subjects/chemistry`; connections
  (korg 3399) shipped in sprints 017–019; the making subject is not
  written, so links to it are recorded as pending. kloom is not in the
  cross-project plan index.
- **The before, recorded first**, as sprint 024 found simplest:
  `names.py density` and `names.py reach western-civ --steps 3` at the
  start of the sprint (`.scratch/chem/density-before.txt`,
  `reach-before.txt`). Western-civ then reached 6 ai, 9 computing and 14
  feynman frames in two steps (29 of the tech cluster's 198) and 51 in
  three.

### Shape

The plan is `create-tools/subject-plan/chemistry.json`: 53 main-spine
frames and three trails of 13, 66 in all.

- **Dates to 1898, then categories.** Four `date` segments (Fire and
  earth; Elements and alchemy; The chemical revolution; Atoms and the
  table, which ends with the Curies' radium), then five `category`
  segments where the threads run side by side: Industry, The chemical
  bond, Materials, The chemistry of life, and Chemistry now.
- **Three trails**, each a detour a reader may skip:

  | Trail                  | Anchor           | Frames |
  | ---------------------- | ---------------- | -----: |
  | Alchemy's last century | `boyle`          |      3 |
  | Finding the elements   | `periodic-table` |      5 |
  | From dyes to drugs     | `mauveine`       |      5 |

- **Every reading does one piece of chemistry** in front of the reader:
  a balanced equation with its masses worked, an isotope pattern read, a
  recipe read as a ratio, a law checked against the original numbers.
  This is the subject's own demand, set in the brief, as sprint 024 set
  one piece of mathematics.
- **Shared stories are owned once.** Physics' `x-rays` keeps Becquerel,
  so `radium` tells the Curies' chemistry; physics' `fission` keeps
  Hahn and Meitner, so `transuranium` tells Seaborg; western-civ's `dna`
  keeps 1953, so `dna-chemistry` tells Miescher to Chargaff; computing's
  `silicon-valley` keeps the planar process, so `photolithography` tells
  the resists.
- **The voice** is the collective "we" of the other subjects.

### Theme

Four dark/light pairs, each tied to a part of the story:

| Palette | Scheme | For                                   | Ink  | Muted | Accent | Line |
| ------- | ------ | ------------------------------------- | ---- | ----- | ------ | ---- |
| furnace | dark   | fire, metal and alchemy, to 1600      | 14.8 | 7.6   | 6.2    | 10.9 |
| alum    | light  | fire, metal and alchemy, to 1600      | 14.2 | 6.7   | 6.3    | 11.8 |
| retort  | dark   | the laboratory, 1600–1900             | 14.9 | 7.9   | 9.8    | 11.8 |
| filter  | light  | the laboratory, 1600–1900             | 15.0 | 6.4   | 5.8    | 12.2 |
| coaltar | dark   | industry, dyes, drugs and materials   | 15.0 | 7.6   | 7.1    | 11.0 |
| enamel  | light  | industry, dyes, drugs and materials   | 15.3 | 6.9   | 7.0    | 13.2 |
| helix   | dark   | the bond, life, the twentieth century | 15.2 | 7.8   | 9.3    | 11.9 |
| agar    | light  | the bond, life, the twentieth century | 14.7 | 6.6   | 5.6    | 12.2 |

The lowest contrast is 5.6:1, against a floor of 4.5.

### The first segment, by hand

Fire and earth has three frames:

- `copper-smelting` (c. 5000 BC): the slag crumbs from Belovode, fourteen
  years in a box labelled "copper minerals"; ores chosen by colour; the
  roasting and reduction of malachite worked (57% of its weight is
  copper); the 2013 smelt at Pločnik with six blowpipes and a drummer;
  Çatalhöyük's "slag" reread as burnt pigment. Read in Radivojević and
  Roberts's open 2021 review, since the 2010 paper is on ScienceDirect.
- `tyrian-purple` (c. 1800 BC): Friedländer's 12,000 snails for 1.4
  grams, dibromoindigo drawn, Pliny's vat read as a reduction, bromine's
  1 : 2 : 1 mass triplet worked from its isotopes, and the Timna wool,
  found in a copper-smelting camp.
- `clay-recipes` (c. 1200 BC): Tapputi's perfume and whether it was
  distilled, the Nineveh glass text read in Oracc's edition (10 minas of
  quartz to 15 of plant ash, soda as a flux), and the Sippar dyeing
  tablet.

**What writing them found** (each also a comment on korg 3461): the plan
still holds only ids (recurred); a fifth identical plate collector
(recurred); Tyrian purple not named in its own prose (recurred); the
before recorded first (recurred); one mark written by hand from habit,
by the reviewer; ScienceDirect again, with OpenAlex, Europe PMC and
`curl -k` for Oracc as the ways round (the grow skill now names them);
Wikipedia placing Belovode on the wrong mountain.

### Authoring at scale

- **Twenty-one authors in parallel**, each a subagent with a shell and the
  web, given a shared brief (`.scratch/chem/brief.md`) and a paragraph of
  its own (`.scratch/chem/parts.md`): frames in order, each with its
  topic, date, palette, what it owns and what it must leave to a
  neighbour, and connection candidates. The brief says its facts are
  leads, not sources (author-subject §3, from sprint 024). Anchor authors
  (`boyle`, `periodic-table`, `mauveine`) finish the anchor first.
- **Review, per part:** each part checked in a copy holding every
  author's drafts (`.scratch/chem/review.sh`: completeness, the subject
  tests with the marks placed, word counts, accent, topic and image
  clashes), claims spot-checked at source (the August 2026 Mauna Loa
  mean against NOAA's own file, 427.55 ppm), then committed by
  `.scratch/chem/commit.sh`: names added, marks placed, staged with
  `stage_segment.py`, and the exported index tested before the commit.
- **Names borrowed across parts.** Authors' marks used each other's
  drafts (Midgley, silver, Mendeleev, antimony, Berzelius …), so each
  borrowed draft went in with the first part that marked it, without a
  `home` naming a frame still to come, which was given back with
  `names.py add --update` when the frame landed (Mendeleev with
  `periodic-table`). Duplicate drafts (Haber, BASF, Pasteur, Pauling,
  penicillin, the Nobel Prize in Chemistry) shared ids, so the registry
  kept the first.
- **One commit holds five parts.** revolution2, atoms1, bond1 and bond2
  each failed the index check alone, on names and marks crossing between
  them; the review script stopped without unstaging, and materials1's
  commit took all five. They passed together (537 tests), and the commit
  says so. The commit script now unstages on failure, and the
  author-subject skill says to.
- **What it came to:** 66 frames and about 54,900 words of prose; about
  78 images, each looked at before use and none repeated in the
  repository; 15 charts and many tables; ten frames dated with `asOf`;
  every accent unique; 380 new names (the registry has 2,137).
- **Where sources disagreed, the readings give both**, scores of times:
  Belovode's date (5500 or 5000 BC), Tapputi's distillation, the
  Leiden papyri as alchemy or craft, the size and date of the Jabirian
  corpus, the Summa's authorship, Scheele or Priestley for oxygen,
  Davy's date for potassium, Kekulé's dream, Loschmidt's rings,
  Mendeleev's dream and cards, the gas toll of 1915, Clara Immerwahr's
  death, the ozone satellite story, Eichengrün against Hoffmann, Fleming's
  window, the oganesson atom count, Miller's archived vials.

### What the tools and skills assumed

Every author reported where the skills, the brief or a tool was wrong,
silent or in the way (raw notes: `.scratch/chem/findings.md`); the
roll-up is on korg 3461, beside Mathematics', for the third run and the
revision. What recurred most:

- **The brief was wrong about forty times**, and each was caught by an
  author reading the source: Moseley's three gaps, not four; no
  gunpowder recipe in Roger Bacon; Davy's potash damp and solid, not
  molten; Heitler and London never computing 3.14 eV; Lathrop at Texas
  Instruments; Freon's "1928" a patent filing date; Alexander not the
  first given penicillin. The rule sprint 024 added (a brief's facts are
  leads) did its job.
- **Marks landing on another word than the bold one** (six authors: a
  quotation or epigraph first, a capital, a word inside a longer one),
  and **marks written by hand from habit** (four authors and the
  reviewer). Both are left as decisions on 3461 (what `mark --check`
  should print; whether `just check` should run it).
- **Commons citations rewritten by hand** (thirteen authors): boilerplate
  `container`, authors as one string, the licence tag hidden behind
  "Public domain". Left on 3461.
- **Routes to sources:** Europe PMC answering 500, Wayback copies
  gzipped, archive.org page images for scans whose OCR fails; the grow
  skill now names them.
- **The stand-in anchor, checking a draft, the before** — each read two
  ways or incomplete; the subject-plan README and the author-subject
  skill now say.
- **Recurred from sprint 024:** wide contact sheets, the tight word
  band, sites refusing scripts, translations cited with `editors`, the
  plan holding only ids, one plate collector per subject.

### Connections, and the bridge

- **108 connections are stored on chemistry frames**: 58 into other
  subjects (22 physics, 14 western-civ, 7 computing, 6 mathematics, 5
  feynman, 4 ai) and 50 between chemistry frames, 41 of those added at
  review from the authors' lists, each _why_ checked against a reading
  (`.scratch/chem/conns.py` refuses one whose terms no reading holds).
  38 of the 66 frames connect to another subject.
- **The links the proposal asked for:** writing on clay (`clay-recipes`
  → `western-civ/writing`), the scriptorium's inks (`iron-gall-ink` →
  `western-civ/scriptorium`), printing's type metal (`type-metal` →
  `printing-press`, `gutenberg-bible`), the DNA frame (`dna-chemistry`,
  `protein-structure` → `western-civ/dna`); atoms (`dalton`, `karlsruhe`
  → `physics/atoms-real`) and quantum chemistry (`quantum-chemistry` →
  `physics/wave-mechanics`, `feynman/forces-in-molecules`); silicon
  (`silicon` → `computing/transistor`, `silicon-valley`, `physics/solids`)
  and lithography (`photolithography` → `computing/integrated-circuit`,
  `end-of-scaling`).
- **Pending, for the making subject** (korg 3431, not yet written):
  sixteen frames, from `copper-smelting` and `type-metal` to
  `bessemer-steel`, `aluminium`, `silicon` and `polymers`, listed on
  3431 for its authors to store.
- **Left unmade:** rhymes (the Solvay Conference as a shared name,
  `standard-model` as "a second periodic table"), and every candidate
  whose _why_ no reading states (`ai/self-attention`,
  `feynman/plenty-of-room`, `computing/moores-law`).
- **Density** (`names.py density`), after:

  | Subject     | Frames | Marks per frame | Connections per frame |
  | ----------- | -----: | --------------: | --------------------: |
  | ai          |     66 |           11.24 |                  1.15 |
  | chemistry   |     66 |            7.73 |                  1.64 |
  | computing   |     70 |           10.33 |                  1.20 |
  | feynman     |     62 |            8.65 |                  1.63 |
  | mathematics |     65 |            7.71 |                  2.22 |
  | physics     |     68 |            7.37 |                  3.26 |
  | western-civ |     24 |            7.04 |                  3.58 |

- **Western-civ's reach** (`names.py reach`), before (recorded at the
  start) and after:

  | To        | Frames | Within 1 | Within 2    | Within 3    |
  | --------- | -----: | -------: | ----------- | ----------- |
  | ai        |     66 |        0 | 6           | 13 → 14     |
  | computing |     70 |        4 | 9 → 12      | 17 → 19     |
  | feynman   |     62 |        7 | 14          | 21          |
  | total     |    198 |       11 | **29 → 32** | **51 → 54** |

  One step out, western-civ now reaches 13 chemistry frames, 33 in two
  and 48 in three. As with physics and mathematics, the gain into the
  tech cluster is small: chemistry's old frames link to western-civ and
  its modern ones to computing, and only silicon, Avogadro's constant
  and the metre survey sit on both sides. In two steps chemistry itself
  reaches 44 physics, 25 mathematics, 21 feynman, 14 computing and 9 ai
  frames.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint
  and 962 tests; every subject is loaded and validated, every SVG
  sanitised, and the links test finds every connection's frame and every
  mark's name.
- **Every content commit was validated on its own**, the index exported
  and the subject tests run on it; the one five-part commit was
  validated as five.
- **All 50 mark specs pass `--check`**, every subject's.
- **Negative tests, each seen failing:** the index check on four parts
  whose names crossed (above); `conns.py` on a _why_ whose terms no
  reading held (the first draft of `paracelsus` → `boyle`, until the
  Boyle reading's "three principles of the chymists" was found);
  `review.sh`'s accent check on SALT, held by two frames mid-sprint.
- **Reproducibility:** `draw-plates/chemistry.py` redraws every plate;
  the fifteen chart specs are in `create-tools/bar-chart/examples/`.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on a
  scratch data directory, `.scratch/025/walk.mjs`):
  - `/chemistry`: the start screen titled "The History of Chemistry",
    Enter to begin;
  - → through all 53 main-spine frames in plan order, with the right
    accent and HUD label at each;
  - T into each of the three trails at its anchor, → through every trail
    frame, Esc back to the anchor: 66 stops, no mismatch;
  - Home and End reach STONE. and DAY.;
  - a deep link to a trail frame (`/chemistry/aspirin`);
  - no broken images, console errors or failed requests, and no
    horizontal overflow at 390px;
  - the start screen lists the History of Chemistry among seven
    subjects.
- **A layout defect the walk did not catch, found by looking:** on the
  last frame the counter overlapped the metadata lines. Measured on every
  frame (`.scratch/025/overlap.mjs`, bounding boxes after the animations
  finish): 17 frames overlap at 1400×900 (4 chemistry, 11 feynman, 2
  mathematics), and at 1280×800 every frame with a counter is at risk
  (49 of chemistry's 66, 5 of western-civ's 24). Four chemistry scenes
  were tightened (`newton-alchemy`, `oxygen`, `where-chemistry-is`,
  `pcr`), which clears two at 1400×900; the fix belongs in the scene
  layout and needs a decision on how it gives way, filed as korg 3469.

## Repaired in passing

- **The grow skill:** the routes to sources the authors found
  (OpenAlex, Europe PMC and its fallbacks, Wayback with `--compressed`,
  archive.org page images, Oracc with `curl -k`), and a frame must say
  its own subject's name in prose.
- **The author-subject skill and the subject-plan README:** checking a
  draft `frame.json` in the copy, unstaging after a failed index check,
  borrowed names whose home is still to come, recording the before first,
  and the whole stand-in recipe.
- **`names.py add --check`** says what it would write; **`wiki_cite`**
  names a title cited as another article.
- **Twenty shared names** widened or homed.

## Deployed

2026-09-30, by `just deploy` (the `recipe: deploy` in `.sprint-deploy`),
from merged `main` at `f92aa30`, to the kloom service on kai. The
service's content clone is at the same commit.

- `just verify` passed all eight door checks: the tailnet door refuses
  anonymous writes and reader-data reads, and the ssh door lets its reader
  through.
- **The sprint's work, live on both doors (:4890 and :4891), each 200:**
  - `/chemistry`;
  - `/chemistry/clay-recipes` (main spine), whose page carries "CLAY.";
  - `/chemistry/aspirin` (a trail frame), whose page carries "WILLOW.";
  - `/media/chemistry/copper-smelting/plocnik-axes.jpg`;
  - `/api/start/chemistry` (the start screen's look, with the furnace
    palette).
