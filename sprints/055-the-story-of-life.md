# 055 — The Story of Life

## Goal

korg proposal 3548, covering korg 3543: the twelfth subject,
`subjects/biology`, _The Story of Life_, "a history of biology, from
Aristotle's animals to CRISPR". Biology was the largest gap among the
sciences, and blood, chemistry, nursing, food and western-civ already
point at it. It is the third of four subject sprints (3542 → 3544 → 3543
→ 3545), and it picks up the links Daily Bread (sprint 051) left pending
for it.

## Decisions

- **The premise held** (checked at start): no biology subject existed,
  all 26 food frames the pending-links comment on 3543 names exist, all 11
  shared names it lists are in the registry, kloom is not in the
  cross-project plan index, and no grow branch was pending.
- **The before, recorded first** (`.scratch/055/reach-before.txt`,
  `density-before.txt`): western-civ reached, in one and two steps, 1 and
  10 of ai's 66 frames, 5 and 24 of blood's 62, 20 and 43 of chemistry's
  66, 5 and 16 of computing's 70, 7 and 18 of feynman's 62, 30 and 45 of
  food's 65, 9 and 20 of making's 68, 13 and 37 of mathematics's 65, 10
  and 19 of nursing's 64, and 38 and 53 of physics's 68. The registry held
  4,293 names.
- **The id is `biology`**, served at `/biology`; the title _The Story of
  Life_ (Ken's, 2026-10-03) and the subtitle "a history of biology, from
  Aristotle's animals to CRISPR" (56 characters).

### Shape

The plan is `create-tools/subject-plan/biology.json` (written by
`.scratch/055/mkplan.py`): 52 main-spine frames and three trails of 15,
67 in all. The spine is dates, in seven segments that each restart time,
following the seven-part arc in 3543:

| Segment                  | Palette     | Frames | Years        |
| ------------------------ | ----------- | -----: | ------------ |
| Naming and ordering life | `herbarium` |      7 | 345 BC–1753  |
| Seeing small             | `stain`     |      8 | 1665–1888    |
| Deep time and change     | `strata`    |      8 | 1667–1860    |
| Inheritance              | `garden`    |      7 | 1866–1950    |
| The molecule             | `helix`     |      7 | 1928–1961    |
| Reading and writing life | `gel`       |      8 | 1973–2012    |
| Ecology and the whole    | `canopy`    |      7 | 1807–2026    |

| Trail             | Anchor              | Palette  | Frames |
| ----------------- | ------------------- | -------- | -----: |
| Germ theory       | `swan-neck-flask`   | `stain`  |      5 |
| The Beagle        | `origin-of-species` | `ocean`  |      5 |
| What we got wrong | `mendel-peas`       | `garden` |      5 |

- **The three candidate trails** in 3543 are all here. _Germ theory_ does
  not retell nursing's Semmelweis and Lister, which it connects to; it runs
  Fracastoro, Snow, Koch, Ross and the discovery of viruses. _What we got
  wrong_ mirrors In the Blood's trail of the same name: preformation,
  pangenesis, Piltdown, eugenics and Lysenko. Spontaneous generation, the
  fourth wrong idea 3543 named, is on the main spine, where Redi and
  Pasteur end it.
- **The modern era stays dated**, not `category`: 3543 offered a split
  (genetics / molecular / ecology), and the three segments _The molecule_,
  _Reading and writing life_ and _Ecology and the whole_ make it while
  keeping their dates.
- **Told elsewhere, connected here**: the double helix itself
  (`western-civ/dna`), the chemistry of DNA, PCR, protein structure,
  AlphaFold and crystallography (chemistry), Harvey and Leeuwenhoek's red
  cells (blood), Semmelweis and Lister (nursing), pasteurization, Malthus
  and Lysenko's famine (food). AlphaFold, which 3543's arc names, is
  chemistry's frame and gets no second one here.
- **The voice** is the collective "we", humanity coming to understand life,
  with sprint 051's caution: on eugenics, Lysenko, race science and
  Piltdown a headline says who did what.

### Theme

Four dark/light pairs, one palette per section, every pair used
(`.scratch/055/palettes.py`):

| Palette   | Scheme | For                                   | Ink  | Muted | Accent | Line |
| --------- | ------ | ------------------------------------- | ---- | ----- | ------ | ---- |
| herbarium | light  | naming and ordering life              | 14.0 | 6.1   | 5.6    | 12.2 |
| stain     | dark   | seeing small; Germ theory             | 15.2 | 7.6   | 8.1    | 11.2 |
| strata    | light  | deep time and change                  | 14.7 | 6.6   | 5.7    | 12.9 |
| ocean     | dark   | The Beagle                            | 15.6 | 8.3   | 10.3   | 12.0 |
| garden    | light  | inheritance; What we got wrong        | 14.7 | 6.4   | 6.4    | 12.7 |
| canopy    | dark   | ecology and the whole                 | 15.4 | 8.3   | 11.1   | 12.0 |
| gel       | light  | reading and writing life              | 15.5 | 6.5   | 6.2    | 13.1 |
| helix     | dark   | the molecule                          | 15.2 | 8.0   | 10.4   | 11.8 |

The lowest contrast is 5.6:1, `herbarium`'s accent. The main spine runs
light, dark, light, light, dark, light, dark.

### The hand frames

_Naming and ordering life_'s first three frames, written by hand as the
bar (commit `1121dfc0`):

- `aristotle-animals` (c. 345–343 BC, LAGOON): Lesbos and the lagoon of
  Pyrrha; the _History of Animals_ read in D'Arcy Thompson's translation
  (Wikisource): facts before causes, his great genera as a table and the
  plate, Laurin and Humar's 2022 matrix of 147 animals by 161 characters,
  and three claims confirmed only in the nineteenth century (the
  hectocotylus, the smooth-hound's placenta, the catfish's guarding male).
- `theophrastus` (c. 300 BC, INQUIRY): the _Enquiry into Plants_ in Hort's
  1916 translation (Wikisource): the four classes and how cultivation blurs
  them (the plate draws each from his definition), date-palm hand
  pollination and the caprified fig, Camerarius's proof of plant sex in
  1694, Alexander's observers, and the difficulty of knowing which plant a
  Greek name meant.
- `herbals` (1542, LIFE): Dioscorides, pictures copied from pictures,
  Brunfels and Weiditz's "living pictures", and Fuchs's _De historia
  stirpium_ with his preface in Arber's 1912 translation (Gutenberg), the
  three craftsmen as a table, the relief block in section as the plate, and
  the chili pepper and maize from the Americas.

What the hand frames found:

- **Wikipedia was wrong twice**: _History of Animals_ says Agassiz
  confirmed the catfish in 1890 (he died in 1873; his paper is 1857), and
  gives Cuvier's naming of the hectocotylus as 1817 where the 2024 _Marine
  Biology_ paper and the article on the organ give 1829. The readings
  follow the sources and say so where it matters.
- **Two accounts of Fuchs's draughtsmen disagree** (Arber: Füllmaurer drew,
  Meyer copied; Wikipedia the reverse); the reading gives both.
- **The Internet Archive was offline** on the day; Wikisource's parse API
  served both classical translations whole, and Gutenberg's plain text
  served Arber. Folded into the brief.

## Authoring at scale

Twenty-six authors, one per part of two or three frames, each a subagent
given the shared brief (`.scratch/055/brief.md`) and a paragraph of its own
(`.scratch/055/parts/`, written by `.scratch/055/mkparts.py` from the plan).
The plan's `owners` names 98 shared names, every id from `names.py lookup`
(checking the brief's ids found five already in the registry, among them
`photo-51`, `genentech` and `g-h-hardy`, and corrected two). Twenty
started at once, the session's limit; the last six as the first finished.
