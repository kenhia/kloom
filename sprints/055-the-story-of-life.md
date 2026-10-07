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

| Segment                  | Palette     | Frames | Years       |
| ------------------------ | ----------- | -----: | ----------- |
| Naming and ordering life | `herbarium` |      7 | 345 BC–1753 |
| Seeing small             | `stain`     |      8 | 1665–1888   |
| Deep time and change     | `strata`    |      8 | 1667–1860   |
| Inheritance              | `garden`    |      7 | 1866–1950   |
| The molecule             | `helix`     |      7 | 1928–1961   |
| Reading and writing life | `gel`       |      8 | 1973–2012   |
| Ecology and the whole    | `canopy`    |      7 | 1807–2026   |

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

| Palette   | Scheme | For                            | Ink  | Muted | Accent | Line |
| --------- | ------ | ------------------------------ | ---- | ----- | ------ | ---- |
| herbarium | light  | naming and ordering life       | 14.0 | 6.1   | 5.6    | 12.2 |
| stain     | dark   | seeing small; Germ theory      | 15.2 | 7.6   | 8.1    | 11.2 |
| strata    | light  | deep time and change           | 14.7 | 6.6   | 5.7    | 12.9 |
| ocean     | dark   | The Beagle                     | 15.6 | 8.3   | 10.3   | 12.0 |
| garden    | light  | inheritance; What we got wrong | 14.7 | 6.4   | 6.4    | 12.7 |
| canopy    | dark   | ecology and the whole          | 15.4 | 8.3   | 11.1   | 12.0 |
| gel       | light  | reading and writing life       | 15.5 | 6.5   | 6.2    | 13.1 |
| helix     | dark   | the molecule                   | 15.2 | 8.0   | 10.4   | 11.8 |

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
One author (`time1`) stopped on an API error after claiming its accents
and was started again.

- **Committed as each part could be**, not in the planned order: a part
  waited only for the anchor of its trail and for the names it borrowed
  from parts still at work. Review per part was `.scratch/055/review.sh`
  (a copy with that part's drafts, marks placed, the subject tests, word
  counts, accent, topic and image clashes) and a contact sheet; then
  `commit.sh`: names added, marks placed, staged with `stage_segment.py`,
  and the exported index tested before every commit. Twenty-seven content
  commits (the hand segment and 26 parts), none of which failed its index
  check. Two changes to the scripts mid-run: a borrowed draft is now
  _copied_ into the registry, not moved, so a running author's files are
  never disturbed; and when the owner's part commits, any `home` a
  borrowed copy went in without is restored (`megatherium`, `pangenesis`,
  `charles-sutherland-elton`).
- **What it came to**: 67 frames, 56,747 words of prose (679 to 900 a
  frame); 78 images, each looked at and none repeated in the repository;
  16 charts and about 100 tables; 994 citations; 4 frames with `asOf`
  (CRISPR, Woese, _Silent Spring_, the biodiversity crisis); every accent
  unique. The registry grew from 4,293 names to 4,894.
- **Fixed at review**:
  - Three connections dropped as rhymes: `linnaeus` → `blood/race-serology`
    (neither reading ties Linnaeus's varieties to blood groups),
    `piltdown` → `making/knapping`, and `silent-spring` →
    `ross-malaria`.
  - Names no part drafted: `pasteur-institute` (its owner never marked
    it; `mol3` did) and `principles-of-geology` (each of two parts left it
    to the other), drafted at review with their parts.
  - Three names drafted by two parts at once (`carnegie-institution-for-science`,
    `friedrich-loeffler`, `ferdinando-ii-de-medici`): the later part
    deleted its draft and borrowed. None was in the plan's `owners`.
  - Homes set on names their frames are chiefly about: `conrad-gessner`,
    `carl-linnaeus`, `georges-cuvier`, `george-beadle`, `photo-51`,
    `hms-beagle`, `alexander-von-humboldt`.
- **The paragraphs were wrong somewhere in most parts**, and each error
  was caught by an author reading the source, the leads-not-sources rule
  holding for an eighth run. Among them: Griffith's four groups of mice
  are a textbook composite of his Table VII; Hershey and Chase stripped
  75–80 percent of the sulfur and 21–35 percent of the phosphorus; Avery's
  1944 paper used crude enzyme preparations, purified DNase coming in
  1946; Nirenberg and Matthaei tested amino acids in groups, not one to a
  tube; Clear Lake's poison was DDD, not DDT, and Lindeman's paper has no
  "10 percent rule"; Enewetak's drill reached basalt at 1,267 m through
  limestone, not 1,300 m of coral; the _Beagle_'s _Toxodon_ skull came
  from Uruguay, not Punta Alta; Pasteur's glacier flasks were sealed-point,
  not swan-necked; Brown named the nucleus with a single lens; 155 people
  were at Asilomar, and P1–P4 were the NIH's 1976 terms, not Asilomar's;
  Muller's 1939 manifesto called for eugenics after social equality rather
  than rejecting it; Ivanovsky worked in the Crimea and Beijerinck at
  Delft; Weismann's mice ran to January 1889.
- **Wikipedia was wrong or vandalized several times**, and the readings
  follow the sources: Agassiz's catfish "confirmed in 1890" (he died in
  1873), the Thomas Hunt Morgan and Spontaneous generation articles
  vandalized at their current revisions (earlier revisions cited), the
  Robert Koch article wrong in three places, and the Oxford debate,
  Linnean papers and Ali Wallace articles each contradicting themselves.
- **Told honestly**: eugenics (65,370 sterilized under US state laws, the
  _Buck v. Bell_ opinion shown as the US Reports page, Carrie Buck's
  records set against the court's pedigree), Lysenko and Vavilov's death in
  prison, Linnaeus's 1758 varieties, Agassiz and Haeckel's race science,
  De la Beche's Jamaican estate, Sloane's sugar fortune, the Fuegians the
  _Beagle_ carried, Wallace's assistant Ali, Martha Chase, Franklin's data
  and how they reached Watson and Crick (the readings give each side
  where the sources disagree), and He Jiankui's edited twins.

### Names and connections

- **Names**: 601 new, every Wikidata id from `names.py lookup`; 16 old ones
  widened that were written from one subject's angle (Lederberg known only
  for DENDRAL, Franklin for DNA only, Crick without the code, Hooke and
  Kelvin as physicists only, Caltech, Cornell and Berkeley by their
  physicists, the British Museum without Sloane, Clinton without the human
  genome, and others).
- **Connections**: 97 from biology to ten other subjects, every one
  supported by a reading: 22 to western-civ, 20 to food, 18 to chemistry,
  12 to blood, 10 to physics, 5 each to mathematics and nursing, 2 to ai,
  and one each to making, computing and feynman. 75 within biology, 68 of
  them added at review by three checkers who read both ends of each of 87
  candidates (`.scratch/055/within-*.txt`); 18 were dropped as rhymes or as
  pairs a trail already joins. No other subject's frames were changed.
- **Daily Bread's pending links** (the comment on korg 3543): made from
  `woese-archaea` (`food/salt`), `swan-neck-flask` and `koch-postulates`
  (`food/pasteurization`), `virus` and `humboldt` (`food/fertilizer`),
  `mcclintock` and `neanderthal-genome` (`food/maize`), `neanderthal-genome`
  (`food/first-herds`, `food/potato-blight`), `koch-postulates`
  (`food/potato-blight`), `origin-of-species`, `darwin-wallace`,
  `notebook-b` and `predator-prey` (`food/malthus`), `lysenko`
  (`food/great-chinese-famine`), `recombinant-dna` and `crispr`
  (`food/gm-crops`), and `beagle-voyage` (`food/lind-scurvy`). Left
  unmade, because no biology frame tells crop domestication genetics or
  nutrition: `founder-crops`, `rice`, `chuno`, `first-wine`, `chocolate`,
  `coffeehouse`, `reinheitsgebot`, `chorleywood`, `appert-canning` (made
  from `beagle-voyage` instead, on the ship's tinned meat), `bengal-1943`,
  `four-course`, `green-revolution`, `vitamins`, `catalhoyuk` and
  `chinampas`.
- **Density** (`names.py density`, `.scratch/055/density-after.txt`):
  biology has 946 marks on 739 names, 14.12 a frame (the most of any
  subject), and 172 connections, 2.57 a frame.
- **Reach**, in one and two steps (`names.py reach`): western-civ reaches
  21 and 50 of biology's 67 frames, and its two-step reach into the
  others rose for blood (24 → 25), chemistry (43 → 44), feynman (18 → 19) and food (45 → 46). Biology reaches 11 and 34 of western-civ's 72,
  12 and 33 of food's, 10 and 35 of chemistry's, 9 and 25 of physics's,
  and 8 and 20 of blood's.

### What the tools and skills assumed

Every author reported where the skills, the brief or a tool was wrong,
silent or in the way (`.scratch/055/reports/`).

- **`mark --check` passed a mark on an unfinished draft** (an empty kind
  or description, as `lookup --write-draft` leaves it) that the checking
  copy leaves out, so the copy refused the frame; five authors met the two
  disagreeing. Repaired: `mark` now says the draft is unfinished and
  exits 1.
- **`--complete` printed one line per unfinished draft** of every
  directory passed (37 from one part), burying the author's own output.
  Repaired: one line a directory.
- **The brief said "today" in local time**, and `wiki_cite.py` stamps
  UTC by design (sprint 049): eight authors rewrote dates by hand after
  midnight UTC. Folded into author-subject: the brief gives the UTC date.
- **Unlisted shared names were drafted twice** despite 98 owners; folded
  into author-subject (look in every part's drafts before drafting).
- **Folded into the grow skill**: block quotes count as prose; a paper
  published online early takes its issue's year; a frame about an
  experiment marks the experiment by name.
- **Folded into reaching-sources**: a section on natural history and the
  life sciences (Darwin Online, Wikisource's parse API, BHL's challenge and
  its Internet Archive mirrors and IIIF pages, PNAS and _Genetics_ through
  the Wayback Machine, NLM Profiles in Science, Nobel lectures, Cambridge
  Core, IUCN's tables, R packages' datasets, Wikipedia's extlinks) and
  this run's refusals.
- **Left for a decision** (korg 3576): `commons_media`'s licence choice on
  photographs of old artworks, and its authors and titles; a
  `--skip-missing` for marking in a checking copy; `lookup`'s slug
  collisions; grouped bars; citation kinds for a letter to an unknown
  recipient, a lecture, a modern UK act and DataCite DOIs; plate helpers
  (clipping, hidden lines, coastlines); the 15-mark cap for method-and-history
  frames; rights rules for posthumously published manuscripts and press
  photographs; and how a brief asks for a laboratory frame's method.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint,
  1,715 vitest tests (every subject loaded and validated, every SVG
  sanitized, every connection's frame and every mark's name found), `just
tools-test`, `just reader-gate`, every mark spec with `--check
--placed`, and the American-spelling check.
- **Every content commit was validated on its own**, the index exported
  and the subject tests run on it.
- **Negative tests, each seen failing first**: `mark --check` on an
  unfinished draft (`test_an_unfinished_draft_is_not_yet_known`), and five
  unfinished drafts in one directory
  (`test_many_unfinished_drafts_in_one_directory_are_one_line`).
- `just scene-fit biology`: 0 misfits in 67 frames at 1280×800, 1400×900
  and 390×844.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on the
  dev server, `.scratch/055/walk.mjs`): the start screen titled "The
  Story of Life"; → through all 52 main-spine frames with the right accent
  and HUD label at each; T into each of the three trails at its anchor, →
  through every trail frame and Esc back: 67 stops, no mismatch; Home and
  End reach LAGOON. and LOSSES.; a deep link (`/biology/snow-pump`); no
  broken images, console errors or failed requests, and no horizontal
  overflow at 390px. The subject list shows it as "Story of Life", the
  leading "The" dropped by design (sprint 047); the walk's own check
  expected the full title.
- Plates looked at on contact sheets beyond the authors' own: the hand
  plates, `gesner`, `cabinet`, `mendel-peas`, `rediscovery`,
  `beagle-voyage`.

## Repaired in passing

- **`mark --check` and unfinished drafts**, **`--complete`'s warnings**:
  above.
- **Two files committed unformatted** (`cabinet/frame.json` after a
  review edit, and a chart spec): formatted.
- **`caesium chloride`'s description** respelled for the spelling gate.
- **README** counted eleven subjects; it now counts twelve and gives The
  Story of Life's shape.

## Follow-ups

- korg 3576: the tool and rule changes above that need a decision.
- **Publishing**: biology is not in `publish.json`, so the public reader
  site will not carry it until Ken adds it; that is his call.
