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
