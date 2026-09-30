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
