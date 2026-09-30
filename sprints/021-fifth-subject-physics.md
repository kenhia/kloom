# 021 — Fifth subject: the History of Physics, the first written with links

## Goal

korg proposal 3451, covering korg 3428: the fifth subject, physics from
the Greeks to cosmology, chosen as the **bridge** between western-civ and
the densely linked tech cluster (ai, computing, feynman). It is the first
subject written with names, connections and topics from the start: sprint
018 ran author-subject's link steps as a backfill, and this is their first
authoring run. Success is measured as bridge density: connections from
Physics into each subject, and western-civ's two-step reach into the tech
cluster, before and after.

## Decisions

- **Premises held.** korg 3446 (`topic`) shipped in sprint 020 and the
  author-subject brief already names a `topic` per frame; there was no
  `subjects/physics`. kloom is not in the cross-project plan index.

### Measuring the bridge

- **`names.py reach <subject>`** (new) counts, for each other subject,
  its frames within one and within two connections of any frame of the
  given subject. Connections are shown on both ends, so the graph is
  undirected, and a path may pass through any subject: that is what a
  bridge is for. Checked by hand against the one-step figures before
  Physics existed (western-civ stores connections only among its own
  frames; four computing frames and seven feynman frames connect in).
- **Before**, western-civ reached 21 of the tech cluster's 198 frames in
  two steps:

  | To        | Frames | Within 1 | Within 2 |
  | --------- | -----: | -------: | -------: |
  | ai        |     66 |        0 |        4 |
  | computing |     70 |        4 |        7 |
  | feynman   |     62 |        7 |       10 |

### Shape

The plan is `create-tools/subject-plan/physics.json`: 45 main-spine
frames and four trails of 23, 68 in all.

- **Dates to 1900, then categories.** Five `date` segments (The Greeks;
  Light and motion; The new science; Heat, light and charge; Cracks in the
  classical), then five `category` segments where the threads run side by
  side and a year is the wrong label (Relativity; The quantum; The
  nucleus; Particles; The cosmos), and a closing Open questions.
- **Four trails**, the proposal's candidates:

  | Trail                             | Anchor              | Label kind |
  | --------------------------------- | ------------------- | ---------- |
  | The field, Ørsted to Hertz        | `the-field`         | date       |
  | Heat and information              | `entropy`           | date       |
  | The quantum revolution, 1900–1927 | `quantum-mechanics` | date       |
  | The Standard Model                | `standard-model`    | date       |

- **Faraday and Maxwell are western-civ's.** Its `faraday-induction` and
  `maxwell` tell the 1831 ring and the 1865 paper. Physics' field trail
  takes the physics around them (Ørsted, Ampère, Faraday's lines of force
  as real things, Maxwell's vortex model and the displacement current,
  Hertz), and connects to both. Duplication across subjects is allowed
  (docs/design.md §Connections); here a connection turns it into the
  other angle.
- **The voice** is the collective "we" of western-civ, ai and computing.

### Theme

Four dark/light pairs, one for each era:

| Palette      | Scheme | For                                 | Ink  | Muted | Accent | Line |
| ------------ | ------ | ----------------------------------- | ---- | ----- | ------ | ---- |
| bronze       | dark   | the Greeks to Newton                | 14.5 | 7.6   | 8.1    | 11.2 |
| papyrus      | light  | the Greeks to Newton                | 12.5 | 5.8   | 6.1    | 10.3 |
| gaslight     | dark   | heat, light and charge, 1700–1910   | 14.1 | 7.4   | 9.5    | 10.5 |
| foolscap     | light  | heat, light and charge, 1700–1910   | 14.9 | 6.2   | 6.0    | 12.8 |
| cloudchamber | dark   | the quantum, the nucleus, particles | 15.8 | 8.3   | 10.4   | 11.9 |
| photoplate   | light  | the quantum, the nucleus, particles | 15.3 | 6.2   | 6.3    | 13.3 |
| deepfield    | dark   | relativity and the cosmos           | 16.0 | 8.0   | 9.7    | 11.9 |
| starchart    | light  | relativity and the cosmos           | 16.2 | 6.6   | 8.1    | 13.7 |

The lowest contrast is 5.8:1, against a floor of 4.5.

### The first segment, by hand

The Greeks has three frames:

- `aristotle-motion` (4th century BC): natural places and forced motion,
  the case against the void (Physics IV.8, where Aristotle states the first
  law of motion as an absurdity), Philoponus and Galileo, and Rovelli's
  2015 reading of Aristotle's physics as Newton's at terminal speed;
- `archimedes` (c. 250 BC): the lever proved from postulates (the plate
  draws the proof's row of seven equal weights), the principle of
  buoyancy, Vitruvius's wreath against the Latin poem's balance, and the
  palimpsest read at the Walters and at SLAC;
- `ptolemy` (c. AD 150): deferent, epicycle and equant, with the plate
  tracing Mars from the Almagest's own parameters (R 60, e 6, r 39;30,
  read in Toomer's translation, X.7–8), R. R. Newton's fraud charge, and
  the 2022 Hipparchus fragments.

**What writing them found**, as the link steps' first authoring run:

- **The author's own check had been broken since sprint 017.**
  `subject_plan.py --complete` copied only the subject, and the test reads
  the name registry beside the subjects, so every mark and every
  connection to another subject failed in the copy. The copy now holds the
  other subjects and the registry at `DIR/.names`, with `--drafts`
  merged in, and the test reads `KLOOM_TEST_NAMES`. Seen failing on a mark
  to an unknown name in the copy, and passing on the real ones.
- **`names.py mark` placed a mark on a name no file held**, and only
  vitest noticed. It now names such an id (not in the registry or a
  `--drafts` directory) and exits 1. Seen failing on a planted
  `tycho-brahe` mark, and every existing spec still passes.
- **An italic title needs its underscores in the spec** (`"_Physics_"`):
  the words are matched as written, and `mark` refused the bare word. The
  ai subject already marks `[_cybernetics_]` this way; the names README
  now says so.
- **A hub's description was written from one subject's angle.**
  `aristotle.json` described him by the syllogism alone, for the AI
  subject. It now names his physics too. Physics will mark many names
  another subject added first; the brief asks authors to report such a
  description rather than edit it, and review widens it.
- **A connection's why has to be in a reading.** A draft connected
  `ptolemy` to `eratosthenes` by the Earth radius as a unit of distance;
  neither reading says so, and it was cut. Three claims were cut or
  rewritten for want of a source (the iron in the palimpsest's ink, the
  equant and Kepler's empty focus, a Maragha "school").
- **Sources disagree** and the readings say so: Aristotle wrong or right
  in his domain; Mach against Dijksterhuis on the lever's proof; the
  wreath by bath or by balance; Ptolemy's "fishy numbers".

### Authoring at scale

- **Nineteen authors in parallel**, one per segment or trail part, in two
  waves launched minutes apart. Each got the grow and author-subject
  skills, the three hand-written frames, a shared brief (voice, palettes
  by era, the rights rules, marks by spec, how to check alone) and its own
  paragraph: frames in order, each with its topic, date and palette, what
  its neighbours and its trail tell, and the connection candidates to
  check. Each wrote only its frame directories, its plate module
  (`create-tools/draw-plates/physics_<part>.py`), its chart specs, its
  name drafts and its mark spec.
- **Review, per part:** word counts, the plates and charts on a contact
  sheet in their palettes, the flagged claims spot-checked (Goodstein's
  drop counts against his 2000 paper; Ptolemy's Mars against Toomer), the
  names added and a sample read, the marks placed, then the part staged
  with `stage_segment.py` and the index exported and tested before the
  commit. Anchors went in before their trails.
- **What review changed:**
  - `szilard-engine` and `landauer` both chose PRICE.; Szilard's became
    LOOK.
  - `entropy` sorted 1850 after `spectra`'s 1859, the plan's error: it
    now sorts by 1865, when Clausius named it, the year its story lands.
  - `cmb` never said "cosmic microwave background" in prose; it does, and
    marks it.
  - The black-hole plate's integrated rays made a 127 KB drawing; thinned
    to a point every 1.5 units it is 40 KB and looks the same.
  - Four readings said "by my arithmetic"; the subject says "our".
  - Three chart headings ran off their charts and a value label sat on
    one; widened, or the axis raised.
  - 22 shared names written from one subject's angle were widened (Kepler
    known only by the Platonic solids, Hilbert only by his programme,
    Oppenheimer without his black hole, Maxwell without gases, Kelvin
    without the second law, Bell Labs without the microwave background),
    and ten names gained a physics home.
- **Where sources disagreed, the readings give both**, well over a
  hundred times, among them: Aristotle wrong or right in his domain;
  Ørsted's discovery by plan or by chance; Mayer's priority; Kelvin's
  1848 and 1854 scales; S = k log W as Boltzmann's or Planck's; whether
  Michelson–Morley led Einstein; Planck quantising in 1900 or not; the
  1919 eclipse plates; Millikan's selection of drops; the Bohr–Einstein
  clash at Solvay; Meitner's share of fission; the evolving-dark-energy
  signal (DESI's 2.8–4.2σ against a 2026 recalibration's 3.2σ); and the
  Hubble tension, given both ways.
- **Wikipedia was wrong or divided against primary sources** often:
  Hertz's room (Wikipedia 12 m, Hertz 13 m); Hubble's sample (46
  galaxies, but distances for 24); Penzias and Wilson's excess (4.2 K
  against the paper's 3.5 K); Commons' dates for Kepler's, Millikan's and
  Coulomb's figures; a file named for Perrin's tracings that shows an
  X-ray tube; and the 1927 Solvay photograph, nominated for deletion as
  still in copyright, which no frame uses.
- **What it came to:** 68 frames and about 56,200 words of prose; 83
  images, each looked at before use and none repeated in the repository;
  19 charts and 66 tables; twelve frames dated with `asOf`; every accent
  unique; 350 new names (the registry has 1,461).

### The link steps' first authoring run: what the tools and skills assumed

The authors reported every place the skills, the brief or a tool was
wrong, silent or in the way. Each finding was fixed, generalised in a
skill, or noted.

**Fixed in the tools** (each seen failing, then passing):

- **`subject_plan.py --complete`** had failed every author since sprint
  017: the copy lacked the registry and the other subjects. It now carries
  both, merges `--drafts`, drops a draft's `home` on a frame not in the
  copy, defaults to the repository's registry wherever the subject sits,
  and takes `--only FRAME …` so another author's half-written frame
  cannot fail the check (five authors pruned their copies by hand).
- **`names.py`:** `mark` refuses a name no file or draft holds, and
  `--check` names a mark written by hand; `lookup`'s ids split on an en
  dash (Church–Turing had become `churchturing`), and the seven ids it
  had run together are renamed with every mark and spec; `reach` is new.
- **`prose_words.py`** counted a mark's target as words: a reading grew
  about twenty words when its names were marked.
- **`bar_chart.py`** refuses a heading wider than the chart, overlapping
  neighbour labels, and a value label under the heading. It found the
  same faults in five charts already live (computing's `cloud-q2` and
  feynman's `muon-gap` headings were clipped), now repaired; every other
  chart rebuilds byte for byte.
- **`contact_sheet.py`** shows a frame's charts (`--charts`), colours a
  plate before its `frame.json` exists (`--palette`), and writes its page
  beside its PNG: two authors got each other's plates back.

**Generalised in `skills/grow/SKILL.md`:** marks by spec for an author
with tools (seven of nineteen wrote them by hand from habit, and the
spec's words must be the first mention as written); look at every chart;
Commons' public-domain claims (laboratory contractors, `PD-USGov` on
others' photographs, deletion nominations); "our arithmetic"; more sites
to read through the Wayback Machine; a plate may label its own geometry.

**Added to `skills/author-subject/SKILL.md`:** check marks with the
drafts; report a name written from one angle, and review widens it; dated
sorts in the brief; the anchor first; each other's drafts and `--only`;
the index check and staging by path; connections between authors' frames
at review; `names.py reach`.

**Noted, not changed:**

- **`commons_media`** still gives the uploader's words as title and
  container, the upload date as `published`, and no retry on HTTP 429;
  every author rewrote its citations, as its README says to. A retry
  would help; nothing went wrong for want of it.
- **Wikisource and Commons rate-limit quickly**, and archive.org's DjVu
  text of collected papers was the reliable route for Faraday, Maxwell and
  Hertz.
- **A `wiki-cite` revision can be dated after `accessed`** (UTC against
  Pacific time). The validator does not compare them, and should not.
- **No bar chart for close values or error bars**: two authors drew
  charts by hand in their plate modules (the H₀ dot-and-whisker, the Z
  line shape), regenerated by running the module.
- **An English Wikipedia title as a name's id** forced the PTB's item for
  the Reichsanstalt, which has its own Wikidata item but no English
  article. The alias carries it.

### Connections, and the bridge

- **174 connections are stored on physics frames**: 108 into the other
  subjects (48 to feynman, 40 to western-civ, 12 to computing, 8 to ai)
  and 66 between physics frames, 45 of those added at review from the
  authors' lists, each _why_ checked against a reading. 63 of the 68
  frames connect to another subject; left unmade were rhymes (Ethernet's
  ether, Bell Labs as a shared employer), and every candidate whose _why_
  no reading supports.
- **Density** (`names.py density`), after:

  | Subject     | Frames | Marks per frame | Connections per frame |
  | ----------- | -----: | --------------: | --------------------: |
  | ai          |     66 |           11.24 |                  0.82 |
  | computing   |     70 |           10.33 |                  0.94 |
  | feynman     |     62 |            8.65 |                  1.48 |
  | physics     |     68 |            7.37 |                  2.56 |
  | western-civ |     24 |            7.04 |                  2.62 |

  Physics marks 7.4 names a frame, inside the brief's 4–8; sprint 018's
  subjects ran 8.7–11.2.

- **Western-civ's reach into the tech cluster** (`names.py reach`), the
  proposal's success measure, before (the base commit) and after:

  | To        | Frames | Within 1 | Within 2    | Within 3    |
  | --------- | -----: | -------: | ----------- | ----------- |
  | ai        |     66 |        0 | 4 → 5       | 6 → 11      |
  | computing |     70 |        4 | 7 → 8       | 9 → 15      |
  | feynman   |     62 |        7 | 10 → 14     | 12 → 21     |
  | total     |    198 |       11 | **21 → 27** | **27 → 47** |

  One step out, western-civ now reaches 32 physics frames. Two steps into
  the tech cluster it gained six, three steps twenty. The two-step gain is
  small because a two-step path needs one physics frame on both sides,
  and only eleven are (the field, Ampère, Hertz, Young's slits, the prism,
  the Principia, Boltzmann, the electron, the photon, real atoms,
  superconductivity), and their tech-side ends are mostly the same few
  Feynman frames. The physics western-civ touches (steam, Faraday,
  Maxwell, the SI, JWST) is classical and cosmological; what touches the
  tech cluster is quantum and computational, and the bridge between those
  runs through physics' own connections, which is the three-step figure.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint
  and 788 tests; every subject is loaded and validated, every SVG
  sanitised, and the links test finds every connection's frame and every
  mark's name.
- **Every content commit was validated on its own**: the index exported
  and the subject tests run on it, with one exception. `fd76753` (the
  field anchor) went in with `line-of-force`'s home on a frame the next
  commit added, because my wrapper lost the test's exit code in a pipe;
  the next commit is green, the wrapper now stops, and the squash merge
  folds both. Separately, `19aee55` swept five authors' unfinished mark
  specs into a tool commit through `git add create-tools/names`; the
  gate does not read specs, and each part's own commit set its spec.
- **Negative tests, each seen failing:** `mark` on an unregistered name
  and on a hand-written mark; the complete copy on an unregistered mark,
  and on a broken planned frame without `--only` (passing with it);
  `bar_chart.py` on the 250 K bar under its heading; all 25 mark
  specs still pass `--check`.
- **Reproducibility:** all 67 bar-chart specs rebuild their charts byte
  for byte (the six repaired ones from their new specs), and
  `draw-plates/physics.py` redraws every physics plate.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on a
  scratch data directory):
  - `/physics`: the start screen titled "The History of Physics", Enter
    to begin;
  - → through all 45 main-spine frames in plan order, with the right
    accent and HUD label at each;
  - T into each of the four trails at its anchor, → through every trail
    frame, Esc back to the anchor: 68 stops;
  - Home and End reach VOID. and OPEN.;
  - a deep link to a trail frame (`/physics/uncertainty`);
  - no broken images, console errors or failed requests, and no
    horizontal overflow at 390px;
  - the start screen lists the History of Physics among five subjects.

## Repaired in passing

- **Seven name ids** that `lookup` had run together, in ai, computing,
  feynman and the gravity segment, renamed with their marks and specs.
- **Five live charts** with clipped headings or crowded labels
  (computing's `cloud-q2`, BSD and TOP500; feynman's `muon-gap` and
  wobble ratio).
- **The names README** had an ordered list Prettier made of "exits 1".
- **The author's check** (`--complete`), broken since sprint 017.
- **Word counts:** with link targets no longer counted, four readings in
  other subjects now count just under 550 (ai's `talos` 530, computing's
  `anzan` 517 and `cranmer-abacus` 508, feynman's `return-to-flight`
  549). The count is a measure, not a gate; they are left as written.

## Follow-ups

None filed. Every finding is fixed here or noted with its reason. The
reach figures are a result, not a defect: whether a later sprint should
add frames that sit on both sides of the bridge is a question for the
next planning session, and the numbers above are its input.
