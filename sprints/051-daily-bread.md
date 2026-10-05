# 051 — Daily Bread

## Goal

korg proposal 3547, covering korg 3544: the eleventh subject,
`subjects/food`, _Daily Bread_, "how humanity learned to feed itself". It
is the first subject that is neither a science nor a profession, and it
runs from foraging and the first farmers through grain and empire, spice
and sugar, the agricultural revolutions, keeping food, Haber–Bosch and the
Green Revolution, to the table. It is the second of four subject sprints
(3542 → 3544 → 3543 → 3545), so it links into western-civ's broadened
frames, and records its links to the coming biology subject as pending.

## Decisions

- **The premise held** (checked at start): no food subject existed,
  western-civ's expansion (3546) had shipped as sprint 049, kloom is not
  in the cross-project plan index, and no grow branch was pending.
- **The before, recorded first** (`.scratch/051/reach-before.txt`,
  `density-before.txt`): western-civ reached, in one and two steps, 1 and
  10 of ai's 66 frames, 5 and 23 of blood's 62, 20 and 43 of chemistry's
  66, 5 and 16 of computing's 70, 7 and 18 of feynman's 62, 9 and 20 of
  making's 68, 13 and 37 of mathematics's 65, 10 and 17 of nursing's 64,
  and 38 and 53 of physics's 68. The registry held 3,665 names.
- **The id is `food`**, served at `/food`; the title _Daily Bread_ (Ken's,
  2026-10-03) and the subtitle "how humanity learned to feed itself".

### Shape

The plan is `create-tools/subject-plan/food.json` (written by
`.scratch/051/mkplan.py`): 49 main-spine frames and four trails of 16, 65
in all. The spine is dates, in eight segments that each restart time:

| Segment                  | Palette    | Frames | Years             |
| ------------------------ | ---------- | -----: | ----------------- |
| Before farming           | `ember`    |      3 | c. 1 Ma–12,400 BC |
| The first farmers        | `barley`   |      6 | 9600–6000 BC      |
| Grain and empire         | `amphora`  |      7 | 2500 BC–1640      |
| Spice, tea and trade     | `saffron`  |      5 | 1498–1839         |
| Agricultural revolutions | `hayrick`  |      7 | 1701–1846         |
| Keeping food             | `frost`    |      7 | 1500 BC–1924      |
| The modern harvest       | `nitrogen` |      7 | 1909–2025         |
| The table                | `linen`    |      7 | 1782–2009         |

| Trail            | Anchor               | Palette   | Frames |
| ---------------- | -------------------- | --------- | -----: |
| The first drinks | `gobekli-tepe`       | `amphora` |      3 |
| Bread            | `oldest-bread`       | `barley`  |      4 |
| The potato       | `columbian-exchange` | `hayrick` |      4 |
| Famine           | `irish-famine`       | `amphora` |      5 |

- **The three candidate trails** the proposal named (Bread, Famine, The
  potato) are all here, and a fourth, _The first drinks_ (wine, Sumerian
  beer, the Reinheitsgebot), hangs from Göbekli Tepe, where the feasting
  and beer debate starts. Sen's entitlement point is the Famine trail's
  theme, told in full in `bengal-1943`.
- **Keeping food** is the one segment that runs from deep time (salt, sort
  −1500) to the 1920s; its story is the problem of keeping, not a period.
- **The voice** is the collective "we", humanity feeding itself, with the
  caution from sprint 049: on the sugar islands, the Banda Islands, opium,
  enclosure and the famines, a headline must not fold the victims into a
  "we" that did it.

### Theme

Four dark/light pairs, one palette per section, every pair used:

| Palette  | Scheme | For                                  | Ink  | Muted | Accent | Line |
| -------- | ------ | ------------------------------------ | ---- | ----- | ------ | ---- |
| ember    | dark   | before farming                       | 14.9 | 7.6   | 9.9    | 11.6 |
| barley   | light  | the first farmers; Bread             | 14.4 | 6.4   | 5.5    | 12.6 |
| amphora  | dark   | grain and empire; drinks; Famine     | 14.7 | 7.7   | 7.1    | 11.4 |
| saffron  | light  | spice, tea and trade                 | 15.0 | 6.6   | 5.6    | 12.9 |
| hayrick  | light  | agricultural revolutions; the potato | 14.1 | 6.2   | 5.6    | 12.3 |
| frost    | dark   | keeping food                         | 15.7 | 8.2   | 10.7   | 11.9 |
| nitrogen | dark   | the modern harvest                   | 15.2 | 8.0   | 11.0   | 11.6 |
| linen    | light  | the table                            | 15.1 | 6.6   | 6.3    | 13.3 |

The lowest contrast is 5.5:1, `barley`'s accent
(`.scratch/051/palettes.py`). The sections run dark, light, dark, light,
light, dark, dark, light.

### The hand frames

_Before farming_, written by hand as the bar:

- `cooking` (c. 1 million years ago, CHEWING): Wonderwerk Cave's burned
  bone and ash (Berna et al. 2012, read in full: 30 m in, grasses, brush
  and leaves), Gesher Benot Ya'aqov's cooked fish (Zohar et al. 2022),
  a table of what cooking does (Evenepoel's egg protein, Carmody's mice,
  Koebnick's raw-food survey), Wrangham's cooking hypothesis with Organ's
  feeding-time test (4.7 percent against 48 predicted; chimpanzees 37),
  and the case against (Roebroeks and Villa). The plate is the feeding-time
  gap on log axes, the primate line marked schematic.
- `foragers` (c. 21,000 BC, WILD): Ohalo II (Weiss 2004, read in full: 142
  taxa, nearly 19,000 grass grains, the slab on pebbles), Piperno's starch,
  the composite sickles, the Hadza (Marlowe and Berbesque; Pontzer's
  energetics, read in full, as a table), and the original affluent society
  with Lee's own larger count and Kaplan's critique.
- `oldest-bread` (c. 12,400 BC, FARMED): Shubayqa 1 from Arranz-Otaegui et
  al. 2018, read in full: the hearths, the 24 bread-like fragments, a table
  of voids that tells dough from flat and leavened bread, the particle
  sizes, the five-step recipe, and the feasting argument. The plate draws
  four crumbs with their voids at the paper's sizes and shares.

### Authoring at scale

- **Twenty-four authors**, one per part of two to four frames, each a
  subagent given the shared brief (`.scratch/051/brief.md`) and a
  paragraph of its own (`.scratch/051/parts/`, written by
  `.scratch/051/mkparts.py` from the plan: frames with topic, sort and
  palette, at most five must-tell points, the shared names it owns and
  borrows, connection candidates checked against the other subjects'
  readings, and its checking commands). The session allows 20 subagents at
  once, so four parts started as the first finished. The plan's `owners`
  named 54 shared names, every id from `names.py lookup`.
- **Committed as each part reported**, not in the planned order: a part
  whose borrowed names were drafted by a later part brought those drafts
  in with it, without their `home` (`.scratch/051/borrowed.py` found them;
  `commit.sh`'s `BORROW`), and the home was set when the home frame
  landed (`phytophthora-infestans`, `mcdonalds`, `amartya-sen`,
  `vitamin-c`, `catalhoyuk`). Review per part was `.scratch/051/review.sh`
  (a copy with that part's drafts, marks placed, the subject tests, word
  counts, accent, topic and image clashes) and a contact sheet; then
  `commit.sh`: names added, marks placed, staged with `stage_segment.py`,
  and the exported index tested before every commit. Twenty-five content
  commits, none of which failed its index check.
- **What it came to**: 65 frames, 55,095 words of prose (698 to 899 a
  frame), about 200 pages; 56 images, each looked at and none repeated
  in the repository; 13 charts and 141 tables; 951 citations; 11 frames
  with `asOf`; every accent unique. The registry grew from 3,665 names to
  4,293.
- **Fixed at review**:
  - Four names drafted by two parts at once (`chicago`, `dorian-fuller`,
    `kolkata`, `enriched-flour`): the later part deleted its draft and
    borrowed. One of my messages about it went to the wrong author.
  - `pompeii-bakery`'s connection to `making/roman-plane`, which its own
    author doubted, was a rhyme and was dropped.
  - `chuno`'s headline said "freeze-dried", which its reading says chuño
    is not; it now reads "We froze the harvest at ALTITUDE."
  - Two _whys_ reworded at review to say only what a reading states
    (`pasteurization` → `first-herds`, `escoffier` → `restaurant`).
- **Left as written, for Ken's eye**: `famine-1876`'s headline, "The Raj
  saved rupees; millions STARVED.", is pointed but sourced (Lytton's
  instructions put "severe economy" first); its author offered to soften
  it.
- **The paragraphs were wrong somewhere in nearly every part**, and each
  error was caught by an author reading the source. Among them: Black
  Sunday's storm did not reach Washington (the storms of May 1934 and
  March 1935 did); the McDonald brothers chalked their kitchen on a tennis
  court in 1952–53, not 1948; Rohwedder's slicer used endless bands, not
  reciprocating blades; the 1756 Kartoffelbefehl was Silesia's, about the
  fifteenth such order; Appert's 12,000 francs was a reward on condition
  he publish, not a prize; the _Frigorifique_ carried chilled meat, not
  frozen; Tambora erupted in 1815, not 1315; India's official toll of
  1876–78 was 5¼ million; lime "freeing niacin" in maize is debated;
  the chinampas predate the Aztecs; service à la russe reached Paris in
  1810, not with Escoffier; SOFI 2026 had replaced the 2025 report the
  brief named. The leads-not-sources rule held for a seventh run.
- **Told honestly**: the frames on sugar, the Banda Islands, opium,
  enclosure and the five famines say who did what, give the estimates and
  their spread, and present the debates as debates (the Irish famine and
  genocide, the Holodomor and genocide, Churchill's part in Bengal, the
  Great Leap's toll). They show documents, not victims: Ligon's plan of a
  sugar works, a soup-kitchen ration, the decree of 7 August 1932, Sen's
  wage series, _Peking Review_'s claimed harvests, the grain landed at
  Madras.

### Names and connections

- **Names**: 628 new, every Wikidata id from `names.py lookup`; 18 old
  ones widened that were written from one subject's angle (tuberculosis
  as a disease of the past, Charlemagne known only for learning,
  Manchester without the Corn Law League, the Soviet Union without its
  famine, borax without its use as a preservative, ammonia without
  refrigeration, the Dutch East India Company as a trader only, common
  salt as a crystal only, James Cook known by Harrison's watch, Liebig
  without the law of the minimum, the Rockefeller Foundation without the
  Mexican wheat program, and others).
- **Connections**: 75 from food to the other subjects, every one
  supported by a reading: 40 to western-civ, 18 to chemistry, 5 to
  making, 4 to nursing, 3 to blood, 3 to mathematics and 2 to physics. 50
  between food's own frames, 34 of them added at review from the authors'
  lists, each checked against the reading that states it
  (`.scratch/051/within.py`). No other subject's frames were changed.
- **Pending links to biology** (3543, the next subject sprint): 25 frames'
  worth, from domestication genetics to lactase persistence, lager yeast
  and Lysenko, left as a comment on korg 3543 with the names already in
  the registry to borrow.
- **Density** (`names.py density`, `.scratch/051/density-after.txt`):
  food has 854 marks on 736 names, 13.14 a frame (the most of any
  subject), and 125 connections touching it, 1.92 a frame. western-civ's
  connections touching it rose from 233 to 273.
- **Reach**, in one and two steps (`names.py reach`): western-civ now
  reaches 30 and 45 of food's 65 frames, and its reach into the others is
  unchanged but for blood (5/23 → 5/24) and nursing (10/17 → 10/19),
  which it now reaches through food. Food reaches 26 and 50 of
  western-civ's 72, 12 and 25 of chemistry's 66, 4 and 14 of making's,
  4 and 13 of nursing's, 3 and 13 of mathematics's, 2 and 12 of
  physics's, 2 and 11 of blood's, and 0 and 5 of computing's.

### What the tools and skills assumed

Every author reported where the skills, the brief or a tool was wrong,
silent or in the way (raw notes: `.scratch/051/reports/`).

- **The checking copy failed on other parts' unfinished drafts**: an
  owner's draft straight from `lookup --write-draft`, its `kind` and
  `description` empty, broke every borrower's copy (table3 could not test
  until it dropped the flag; keep2's `mark --check` passed while vitest
  failed), and a drafts directory not yet made crashed `--complete`.
  Repaired: both are left out of the copy and named.
- **`names.py drafts` exited 1 on any part's problem**, so with 24 parts
  no author could read their own status (six asked for a filter).
  Repaired: `--part`.
- **`lookup`** dropped the dotless ı from slugs (Nevalı Çori → `neval-cori`)
  and cut `first_line` at the API's first "sentence", "Mary Prince (c.".
  Repaired.
- **My paragraphs' checking commands named the wrong drafts directories**
  for about a third of the parts, and the plan's `owners` listed the
  subject's own crops but not the places, institutions and scholars many
  parts shared. Folded into author-subject §3, with leads for a
  present-state frame ("the latest edition") and naming the part in a
  message.
- **Folded into the grow skill**: the `kind` of a people (`org`) and of a
  species, crop, food or chemical (`idea`); `citedIn` names the whole
  title and keeps `accessed` when the work has a url or doi; list items
  count as prose.
- **Folded into reaching-sources**: a section on food, agriculture and
  policy sources (FAO's bulk files and PDFs, FRUS, _Historical
  Statistics_, the Federal Register, patents, Chinese and Russian
  Wikisource, _Peking Review_, Fulcrum, AgHR, the Internet Archive's own
  search, 1930's copyright and the URAA), and the sites that refused a
  script this run.
- **Left for a decision** (korg 3557): two-series and negative charts,
  `bar_chart`'s rounding, `wiki_cite`'s UTC `accessed`, `commons_media`'s
  authors and sizes, mark words matching inside longer names, label
  collisions inside a plate, what `--expect` reads, and `plates.py`'s
  `arc()` and clipping.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint,
  1,610 vitest tests (every subject loaded and validated, every SVG
  sanitized, every connection's frame and every mark's name found), `just
tools-test`, `just reader-gate`, every mark spec with `--check
--placed`, and the American-spelling check.
- **Every content commit was validated on its own**, the index exported
  and the subject tests run on it.
- **Negative tests, each seen failing first**: `merge_drafts` on an
  unfinished draft and a missing directory; `slug('Nevalı Çori')`.
  `for_part` was written with its test, not seen failing first.
- `just scene-fit food`: 0 misfits in 65 frames at 1280×800, 1400×900
  and 390×844.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on the
  dev server, `.scratch/051/walk.mjs`): the start screen titled "Daily
  Bread"; → through all 49 main-spine frames with the right accent and
  HUD label at each; T into each of the four trails at its anchor, →
  through every trail frame and Esc back: 65 stops, no mismatch; Home and
  End reach CHEWING. and FORMULATIONS.; a deep link
  (`/food/bengal-1943`); food in the start screen's list; no broken
  images, console errors or failed requests, and no horizontal overflow
  at 390px.
- Plates looked at on contact sheets beyond the authors' own:
  `founder-crops`, `maize`, the three hand plates.

## Repaired in passing

- **`--complete` and unfinished drafts**, **`names.py drafts --part`**,
  **`lookup`'s slug and first line**: above.
- **README** counted ten subjects and gave western-civ as "19
  main-spine frames and two trails", stale since sprint 049; it now
  counts eleven and gives western-civ's shape.
- **A chart spec** (`food-ultra-processed-hall-intake.json`) was
  committed unformatted, failing Prettier; formatted.
- My tool commit (`2ee5b745`) swept in table1's mark spec before its
  frames, so that one intermediate commit's `mark --check --placed` would
  fail; the squash merge does not carry it.

## Follow-ups

- korg 3557: the tool changes above that need a design call.
- korg 3543 (biology): the pending links, as a comment.
- **Publishing**: food is not in `publish.json`, so the public reader
  site will not carry it until Ken adds it; that is his call.
