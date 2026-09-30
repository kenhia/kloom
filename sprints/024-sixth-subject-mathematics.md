# 024 — Sixth subject: the History of Mathematics

## Goal

korg proposal 3462, covering korg 3429: the sixth subject, mathematics
from the Ishango bone to proofs checked by machine. It is the second
subject written with names, connections and topics from the start, after
Physics, and it is meant to link western-civ and physics to the tech
cluster (Boole, logic, Gödel and Turing, probability and statistics,
linear algebra; path integrals for Feynman; calculus and group theory for
Physics). It is also the first of three back-to-back runs of
`skills/author-subject/SKILL.md` whose issues are reported to korg 3461,
and success includes that report.

## Decisions

- **Premises held.** There was no `subjects/mathematics`; connections
  (korg 3399) shipped in sprints 017–019. kloom is not in the
  cross-project plan index.
- **The before, recorded first.** `names.py density` and `names.py reach
western-civ --steps 3` were run at the start of the sprint, before any
  mathematics frame existed, instead of on an archive of the base commit
  afterwards. Western-civ then reached 27 of the tech cluster's 198
  frames in two steps and 47 in three.

### Shape

The plan is `create-tools/subject-plan/mathematics.json`: 49 main-spine
frames and three trails of 16, 65 in all.

- **Dates to 1736, then categories.** Four `date` segments (Counting; The
  Greeks; Beyond Greece; The new mathematics, which ends with Euler's
  bridges of Königsberg), then six `category` segments where the threads
  run side by side: Algebra, Analysis, Geometry, Probability, Logic and
  foundations, and Mathematics now. The proposal named five categories;
  Logic comes after Probability so that the spine runs from Gödel and
  Turing straight into proofs by computer and the present.
- **Three trails**, each a story a reader may skip:

  | Trail                 | Anchor            | Frames |
  | --------------------- | ----------------- | -----: |
  | Fermat's Last Theorem | `diophantus`      |      6 |
  | The primes            | `euclid-elements` |      6 |
  | Infinity              | `cantor`          |      4 |

- **Every reading does one piece of mathematics** in front of the reader
  (a proof sketched, a worked example, a construction the plate draws).
  This is the subject's own demand, set in the brief.
- **Shared stories are owned once.** Physics' `archimedes` tells the
  lever, buoyancy and _The Method_, so `archimedes-circle` tells π and
  exhaustion and connects to it; ai's `laws-of-thought` and
  `turing-machine` tell Boole's hope and Turing's machine, so `boole` and
  `entscheidungsproblem` take the mathematics' angle and connect to them.
- **The voice** is the collective "we" of western-civ, ai, computing and
  physics.

### Theme

Four dark/light pairs, each tied to a part of the story:

| Palette    | Scheme | For                                    | Ink  | Muted | Accent | Line |
| ---------- | ------ | -------------------------------------- | ---- | ----- | ------ | ---- |
| clay       | dark   | counting to 1500                       | 14.3 | 7.5   | 6.7    | 11.1 |
| vellum     | light  | counting to 1500                       | 13.0 | 6.1   | 5.5    | 10.8 |
| oakgall    | dark   | 1500–1850, the printed treatise        | 14.5 | 7.3   | 9.0    | 10.9 |
| quarto     | light  | 1500–1850, the printed treatise        | 15.0 | 6.6   | 7.4    | 12.7 |
| blackboard | dark   | algebra, analysis, geometry after 1850 | 14.8 | 7.8   | 11.3   | 11.7 |
| graphpaper | light  | algebra, analysis, geometry after 1850 | 15.7 | 6.4   | 5.5    | 13.0 |
| terminal   | dark   | probability, logic and machines        | 15.8 | 7.6   | 10.8   | 11.7 |
| printout   | light  | probability, logic and machines        | 16.5 | 7.0   | 8.3    | 14.1 |

The lowest contrast is 5.5:1, against a floor of 4.5.

### The first segment, by hand

Counting has three frames:

- `ishango-bone` (c. 18,000 BC): the three columns of notches, unrolled
  on the plate one tick per notch with their sums (60, 48, 60); the
  readings as primes, doubling, base 12 and a lunar calendar; Keller's
  "fables" as Pletser and Huylebrouck's reply quotes them; the second
  bone read both ways; Baur's 2025–26 permutation test and its
  exploratory adjustments.
- `ybc-7289` (c. 1800–1600 BC): base 60 place by place, 1;24,51,10
  against √2 (one part in about 2.4 million), the missing zero that makes
  30 either 30 or a half, the student's hand tablet, and Plimpton 322's
  two live readings (Robson's teacher's list, Mansfield and Wildberger's
  ratio trigonometry).
- `rhind-papyrus` (c. 1550 BC): multiplication by doubling, unit
  fractions and the 2/n table, problem 50's circle as a square of eight
  ninths (π = 256/81), the seked of problem 56, and problem 79's seven
  houses, which Peet traced to Fibonacci and St Ives. Read in Peet's 1923
  edition, from archive.org's full text.

**What writing them found** (each also a comment on korg 3461):

- **`PD-Art` covers a flat work only.** Commons tags a photograph of
  Plimpton 322, a clay tablet, as `PD-Art-100-1923`, and `commons_media`
  calls it `ok`. It was left out, and the grow skill now says so.
- **ScienceDirect refuses both a script and the Wayback route**, so
  Fowler and Robson's 1998 paper on YBC 7289 was cited through the
  Wikipedia revision that summarises it. The grow skill now names
  ScienceDirect, and archive.org's `_djvu.txt` full text for old
  editions.
- **The plan holds only frame ids.** Topics, dates and palettes live in
  the prose brief, where nothing checks that sorts rise or palettes
  alternate. Left for korg 3461 to decide.
- **A fourth identical plate collector**: `mathematics.py` is
  `physics.py` with the name changed.
- **A frame's own name** had no first mention: "Ishango" in prose is the
  place, so a sentence now names "the Ishango bone".
- **An ancient work cannot be dated** in a `media` citation, whose
  `published` takes only years AD; the papyrus's has none.
