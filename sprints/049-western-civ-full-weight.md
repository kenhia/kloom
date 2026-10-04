# 049 — Western civ at full weight

## Goal

korg proposal 3546, covering korg 3542: bring western-civ, the POC
subject, to the weight of the other nine (it had 25 frames and two
trails; they have 62 to 70 and three to seven), and broaden it from a
spine that was mostly science into law, faith, philosophy, art, politics
and empire. Every existing frame id is kept, because every other subject
links into this one: names, connections, bookmarks, notes, annotations and
kept answers all point at them. It goes first of four subject sprints
(3542 → 3544 → 3543 → 3545), so that Daily Bread, Story of Life and Sound
and Score can link into the broadened frames.

## Decisions

- **The premise held** (checked at start): 25 frames, two trails
  (`measure`, `printing`), a main spine of 20 that ran Prometheus,
  writing, Greek inquiry, Eratosthenes, the Pantheon, the scriptorium,
  Magna Carta, the Renaissance and Reformation frames, the Royal Society,
  then steam, Faraday, Maxwell, DNA, the Moon and JWST. kloom is not in
  the cross-project plan index. No grow branch was pending.
- **The before, recorded first** (`.scratch/049/reach-before.txt`,
  `density-before.txt`): western-civ reached, in one and two steps, 0 and
  6 of ai's 66 frames, 0 and 5 of blood's 62, 13 and 33 of chemistry's
  66, 4 and 12 of computing's 70, 7 and 14 of feynman's 62, 7 and 18 of
  making's 68, 8 and 29 of mathematics's 65, 1 and 2 of nursing's 64, and
  32 and 48 of physics's 68. It stored 13 connections and was touched by
  96 (83 stored on other subjects' frames, 40 of them physics's); 178
  marks on 128 names, 7.12 a frame. The registry held 3,143 names.

### Shape

The plan is `create-tools/subject-plan/western-civ.json` (written by
`.scratch/049/mkplan.py`): 58 main-spine frames and five trails of 14, 72
in all, 47 of them new. The POC's arc, myth to cosmos, stays the
backbone, and every era is widened around it. Ten segments, the old ones
kept by id where they still fit (`myth`, `antiquity`, `middle-ages`,
`rebirth`, `machines`, `code-and-cosmos`) and four added:

| Segment                    | Palette     | Frames | New | Years          |
| -------------------------- | ----------- | -----: | --: | -------------- |
| Myth                       | `night`     |      1 |   0 | (category)     |
| The ancient world          | `marble`    |     11 |   7 | 3200 BC–AD 126 |
| Late antiquity             | `porphyry`  |      4 |   4 | AD 50–529      |
| The long middle            | `parchment` |      7 |   5 | 800–1347       |
| Rebirth                    | `fresco`    |      5 |   3 | 1341–1513      |
| Reformation and new worlds | `fresco`    |      6 |   2 | 1516–1648      |
| Reason and revolution      | `candle`    |      7 |   6 | 1665–1789      |
| Machines and the masses    | `brick`     |      8 |   5 | 1776–1884      |
| The modern world           | `steel`     |      6 |   6 | 1913–1989      |
| Code and cosmos            | `night`     |      3 |   0 | 1953–2022      |

Three new `date` trails, the three the proposal named, of three frames
each, beside the two old ones (_The measure of things_, _The printing
press_):

| Trail                            | Anchor              | Palette      | Frames                                                             |
| -------------------------------- | ------------------- | ------------ | ------------------------------------------------------------------ |
| Rome, from Republic to Byzantium | `augustus`          | `marble`     | `twelve-tables`, `cicero`, `fall-of-constantinople`                |
| Revolutions                      | `french-revolution` | `candle`     | `glorious-revolution`, `haitian-revolution`, `revolutions-of-1848` |
| The idea of rights               | `magna-carta`       | `broadsheet` | `us-bill-of-rights`, `vindication`, `womens-suffrage`              |

- **72, not about 65.** Each era in 3542's gap list has its frames, and
  each era has at least one frame that is not politics or science
  (tragedy, the cathedral, painting, Beethoven, the serial novel, _The
  Rite of Spring_). Getting to 65 meant dropping one of these, and the
  others run 62 to 70.
- **Where the old frames already tell a gap**, it gets no frame of its
  own. `scriptorium` tells Benedict's Rule, Charlemagne's learning and
  Caroline minuscule, so neither Benedict nor Charlemagne has a frame;
  `greek-inquiry` tells the Presocratics and Plato's _Timaeus_, so the
  philosophers' frame is `socrates`, from the trial to Aristotle's
  _Politics_. Montesquieu is told inside `american-revolution` (Madison's
  Federalist No. 47 cites him), Voltaire inside `encyclopedie`, the wars
  of religion inside `westphalia`, the Cold War inside
  `fall-of-the-wall`, the UN inside `udhr`, Toledo's translators inside
  `aquinas`.
- **The science frames stay**, all of them on the original arc, and the
  new frames that touch science (Baghdad, the cathedral, perspective)
  tell this subject's side and connect to the subject that tells the
  science: `mathematics/perspective`, `physics/ibn-al-haytham`,
  `mathematics/al-khwarizmi`, `chemistry/jabir`.
- **Every existing id kept**, and every existing frame still on the main
  spine or its trail. Six moved into new segments (`erasmus-greek-nt`,
  `ninety-five-theses`, `voyages`, `shakespeare` into _Reformation and
  new worlds_; `royal-society` into _Reason and revolution_), which
  changes no link.
- **The voice** stays the collective "we", with a caution in the brief:
  on the frames about conquest, slavery, empire and genocide a headline
  must not fold the victims into a "we" that did it.

### Theme

The subject had one pair, `night` and `parchment`, and its frames
alternated inside sections: sprint 038 left it so at Ken's word, the one
subject not re-paletted. 3546 asked for it to be brought into line. It
now has seven pairs, each tied to an era, and every frame wears its
section's palette (15 frames re-paletted; a palette is presentation, so
no `edits`). `night` and `parchment` keep their values, so the myth, the
long middle and the cosmos read as before.

| Palette    | Scheme | For                                | Ink  | Muted | Accent | Line |
| ---------- | ------ | ---------------------------------- | ---- | ----- | ------ | ---- |
| night      | dark   | myth; code and cosmos              | 15.5 | 6.4   | 8.7    | 8.7  |
| parchment  | light  | the long middle; the old trails    | 13.4 | 5.0   | 5.3    | 10.4 |
| marble     | light  | the ancient world; Rome            | 14.7 | 6.1   | 5.9    | 12.6 |
| basalt     | dark   | its counterpart                    | 14.9 | 7.3   | 6.8    | 11.2 |
| porphyry   | dark   | late antiquity                     | 14.9 | 7.8   | 8.5    | 11.1 |
| alabaster  | light  | its counterpart                    | 15.5 | 7.1   | 8.3    | 13.9 |
| fresco     | light  | rebirth; reformation               | 13.5 | 6.0   | 5.8    | 12.0 |
| lapis      | dark   | its counterpart                    | 15.1 | 7.9   | 9.3    | 11.3 |
| candle     | dark   | reason and revolution; Revolutions | 15.1 | 7.4   | 11.0   | 11.8 |
| broadsheet | light  | the idea of rights                 | 15.4 | 6.8   | 7.7    | 13.5 |
| brick      | light  | machines and the masses            | 14.4 | 6.4   | 6.1    | 12.8 |
| soot       | dark   | its counterpart                    | 14.7 | 7.3   | 6.2    | 11.0 |
| steel      | dark   | the modern world                   | 14.9 | 7.6   | 8.8    | 11.1 |
| newsprint  | light  | its counterpart                    | 14.8 | 6.3   | 7.5    | 12.7 |

The lowest contrast is 5.0:1, `parchment`'s muted, unchanged
(`.scratch/049/palettes.py`); `engine/colour.test.ts` holds every palette
over 4.5 across the brightness sliders' range. The sections run dark,
light, dark, light, light, light, dark, light, dark, dark.

### The hand frame

`hammurabi` (c. 1753 BC, STONE): the Louvre stele from its catalogue record
(225 × 79 × 47 cm, Susa 1901–02), L. W. King's 1910 translation for the
laws, quoted as a table of cases (1, 196, 199, 215, 218, 229, 230), and the
revision of _Code of Hammurabi_ for the scholarship: Van De Mieroop's
"opposition" and "pointillism", Landsberger's silence of the court records,
the Covenant Code. The plate puts the stele to scale beside laws 196–199
drawn as a tree, one variable changed at each branch. The plan's date moved
from 1754 to 1753 BC to match the revision. The 25 older frames run 350 to
700 words with almost no images, so they were named in the brief as what
the subject already tells, not as the bar; `hammurabi` and two frames of
_Keeping Watch_ (`hospitallers`, `basiliad`) were the bar.

### Authoring at scale

- **Seventeen authors in parallel**, one per part of two or three frames,
  each a subagent given the shared brief (`.scratch/049/brief.md`) and a
  paragraph of its own (`.scratch/049/parts/`): frames in order with
  topic, sort and palette from the plan, at most five must-tell points,
  the owners of shared names (45, all looked up), and connection
  candidates. Every registry id and frame the paragraphs named was checked
  before they went out.
- **Review, per part, as each reported** (`.scratch/049/review.sh`: a copy
  with every author's drafts, the marks placed, the subject tests, word
  counts, accent, topic and image clashes), and the report's unsure claims
  read against their sources (notes in `.scratch/049/reports/`). Then
  `.scratch/049/commit.sh` in the planned order: names added, marks
  placed, staged with `stage_segment.py`, and the exported index tested
  before every commit. Eighteen content commits, none of which failed its
  index check. A borrowed name from a part due later (`edward-gibbon`,
  drafted by `late2`, marked by `rome`) went in with the earlier part.
- **What it came to:** 47 new frames, 40,385 words of narrative (762 to
  900 a frame); the subject 72 frames and 52,122 words, about 190 pages;
  46 images, each looked at and none repeated in the repository; 11 charts
  and 79 tables; 897 citations; 2 frames with `asOf`; every accent unique.
  The registry grew from 3,143 names to 3,665.
- **Fixed at review:**
  - Four accent clashes, each found only when the second frame went
    live: BALLOT (`unification` became PLEBISCITE), DEAD (`black-death`
    became MORTALITY), PEOPLE (`american-revolution` became TRUTHS),
    DOWN (`fall-of-the-wall` became OPEN). My message about BALLOT went
    to the wrong author; `unification`'s found it and changed anyway.
  - Three names drafted twice (`bill-of-rights-1689`, `edmund-burke`,
    `olympe-de-gouges`): the later part deleted its drafts and borrowed.
  - `catholic-church` and `pope`, drafted by their owner and marked by no
    one, were dropped; `constantinople` was added to `constantine`'s and
    `crusades`'s marks once `rome` had drafted it.
  - Homes set on names whose home frame is new: `hagia-sophia` and
    `corpus-juris-civilis` (`justinian`), `house-of-wisdom`, `petrarch`
    (`humanism`), `encyclopedie`, `french-revolution`,
    `united-states-declaration-of-independence` (`american-revolution`),
    `united-states-bill-of-rights`, `world-war-i`, `world-war-ii`,
    `the-holocaust`, `universal-declaration-of-human-rights`,
    `berlin-wall`. `friedrich-engels` was left without one: no frame is
    chiefly about him.
- **The paragraphs were wrong somewhere in nearly every part**, and each
  error was caught by an author reading the source. Among them: Avalon's
  Twelve Tables is a 1961 translation still in copyright (Thatcher's of
  1901 was used); Ai-Khanoum was a Seleucid foundation, not Alexander's;
  USHMM counts five killing centers, not six; the Seneca Falls resolutions
  passed "by a large majority", not narrowly; the Second World War's toll
  is 60 to 75 million in current sources, not 70 to 85; "a crown from the
  gutter" has no primary source (Frederick William IV's letter to Bunsen
  is quoted instead); Beethoven's "two rehearsals" is a myth by Albrecht's
  2024 account; Africa was about a fifth European in 1880 (Boahen), not a
  tenth; the enslaved were 17.8 percent of the 1790 census, not a fifth;
  the Dead Sea Scrolls were found from November 1946. The leads-not-sources
  rule held for a sixth run.
- **Told honestly.** The frames on conquest, the slave trade, the Scramble
  for Africa and the Holocaust say who did what, with their numbers and
  the spread of the estimates, quote the victims where sources allow
  (Equiano, Primo Levi, the Congolese testimony in the Casement Report),
  and show documents, not victims: the 1935 law gazette, the Brookes print,
  the General Act's map, the 1790 census return.

### An older frame corrected

`erasmus-greek-nt` said Western Christendom "had forgotten the Greek
itself". The Greek New Testament was copied and read in the Greek East
throughout the Middle Ages, and Greek was taught in Italy from 1397; the
passage was rewritten, with an `edits` correction. Its "eight Greek
manuscripts" checked out (the _Novum Instrumentum omne_ revision). The
older readings' pointers onward were read once the spine changed, and
`greek-inquiry`'s "next frame" (now `alexander`) was reworded to name
Eratosthenes.

### Names and connections

- **Names:** 522 new, every Wikidata id from `names.py lookup`; 25 old
  ones widened that were written from one subject's angle (Jerusalem known
  for glassblowing, Plato for the five solids, Aristotle for physics,
  Rome for its ruins teaching builders, Napoleon for losing to the
  chess-playing Turk, the French Revolution for the meter, the EU for its
  AI law, and others), and `toledo-spain` widened to its translators.
- **Connections:** 60 from western-civ to the other subjects (13 before),
  every one supported by a reading: 13 to chemistry and to physics, 12 to
  nursing, 9 to mathematics, 5 to blood, 4 to computing, 3 to making and 1
  to ai. 90 between western-civ's own frames, 50 of them added at review
  from the authors' lists, each checked against the reading that states
  it (`.scratch/049/within.json`); one why was reworded where the reading
  said less than it claimed. 83 connections stored on other subjects still
  point in (none were broken: every id was kept).
- **Density** (`names.py density`, `.scratch/049/density-after.txt`):
  western-civ now has 849 marks on 704 names, 11.79 a frame (7.12
  before), and 233 connections touching it, 3.24 a frame.
- **Reach**, in one and two steps (`names.py reach western-civ --steps
2`):

  | To          | Before (1 / 2) | After (1 / 2) |
  | ----------- | -------------- | ------------- |
  | ai          | 0 / 6          | 1 / 10        |
  | blood       | 0 / 5          | 5 / 23        |
  | chemistry   | 13 / 33        | 20 / 43       |
  | computing   | 4 / 12         | 5 / 16        |
  | feynman     | 7 / 14         | 7 / 18        |
  | making      | 7 / 18         | 9 / 20        |
  | mathematics | 8 / 29         | 13 / 37       |
  | nursing     | 1 / 2          | 10 / 17       |
  | physics     | 32 / 48        | 38 / 53       |

### What the tools and skills assumed

Every author reported where the skills, the brief or a tool was wrong,
silent or in the way (raw notes: `.scratch/049/reports/`).

- **Two tools had been broken since earlier sprints, and nothing
  noticed** because no subject had been written since:
  - since sprint 032, the test setup compiled the live `subjects/`
    strictly whatever `KLOOM_TEST_SUBJECTS` said, so an author's checking
    copy failed on any other author's half-written frame
    (`vitest.content.ts` now reads both variables);
  - since sprint 033, a second `def drafts` in `names.py` shadowed the
    helper `add` read its files with, so every `names.py add` raised a
    TypeError (renamed `draft_files`; `add` has tests now).
- **Repaired during the run:** `names.py mark --root` crashed on a spec
  frame not in an author's copy (it skips with a note; `--placed`, the
  gate, still refuses one); `commons_media --jpeg` crashed on a PNG
  carrying megabytes of metadata (the score of Beethoven's Ninth);
  `wiki_cite` wrote a local `accessed` beside a UTC revision date, so in
  the evening `published` fell a day after `accessed`.
- **Folded into the skills** (`author-subject` §Extending a subject and
  §3, `grow` §The reading, §Names, §Sources, `reaching-sources`
  §History, law and the humanities): what changes when a subject is
  extended (ids kept, the old frames not the bar, re-palette, old
  pointers and old names' angles, tests pinning the shape); accent claims
  in one shared file; a name drafted by a later part borrowed and
  committed with the earlier one; every owner's drafts in the checking
  command; up to fifteen marks for a history frame, and none in a table;
  regnal-year and foreign statutes, treaties, a translation of a
  translation; routes for old translations (Gutenberg, LacusCurtius,
  Perseus, other Wikisources' APIs), the copyright of Avalon's newer
  translations and Fordham's errors, and the sites behind a challenge
  whose Wayback copies work.
- **Left for a decision**, the tool changes (korg 3554): accent claims
  enforced by `--check`, a check for a draft no spec marks,
  `lookup --write-draft`, `commons_media`'s author and title handling for
  four more institutions, a text-fit check for plates, a crop region for
  `read_source`, and citation kinds for treaties and non-US statutes.
- **The 550–900 band was tight for history frames**: one first draft ran
  1,343 words, and fourteen frames finished within ten words of 900. The
  band held, by cutting.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint,
  1,524 vitest tests (every subject loaded and validated, every SVG
  sanitised, every connection's frame and every mark's name found), `just
tools-test`, `just reader-gate`, every mark spec with `--check
--placed`, and the American-spelling check.
- **Every content commit was validated on its own**, the index exported
  and the subject tests run on it.
- **Negative tests, each seen failing first:** the test setup's copy
  check (failing on a half-written frame in the live tree, then passing);
  `names.py add`'s two new tests against the shadowed helper; `mark`'s
  missing-frame tests; the large-metadata PNG test, which failed only
  once its chunk was compressed, as the real file's was.
- `just scene-fit western-civ`: 0 misfits in 72 frames at 1280×800,
  1400×900 and 390×844.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on the
  dev server, `.scratch/049/walk.mjs`): the start screen titled "The
  History of Western Civilization"; → through all 58 main-spine frames in
  plan order with the right accent and HUD label at each; T into each of
  the five trails at its anchor, → through every trail frame and Esc back:
  72 stops, no mismatch; Home and End reach FIRE. and BACK.; a deep link
  (`/western-civ/haitian-revolution`); no broken images, console errors or
  failed requests, and no horizontal overflow at 390px.
- Six plates spot-checked on contact sheets beyond the authors' own
  (`scramble-for-africa`, `abolition`, `gothic-cathedral`,
  `renaissance-painting`, `athenian-democracy`, `fall-of-the-wall`).

## Repaired in passing

- **The test setup ignored an author's copy** (since sprint 032), and
  **`names.py add` was broken** (since sprint 033): both above.
- **`mark --root`**, **`commons_media --jpeg`** and **`wiki_cite`'s
  accessed date**: above.
- **Tests that pinned western-civ's old shape** (`served.test.ts`'s
  neighbors, `validate.test.ts`'s palettes and trails, `grow.test.ts`'s
  fixture insert, now in _Reformation and new worlds_) follow the new one.
- **Sprint 048's record** was committed unformatted, failing Prettier on
  `main`; formatted.
- **"per cent"** respelled "percent" in western-civ's three older readings
  (a `sed` that also caught "per century" was caught at the diff and put
  back); the other subjects' are korg 3553.

## Follow-ups

- korg 3554: the author-subject tool changes above, to decide before or
  alongside the three subject sprints queued behind this one.
- korg 3553: "per cent" in nine subjects, which the spelling gate cannot
  see.
- western-civ has no `subtitle`; the others that have one say what the
  subject covers. Now that it covers law, faith, art and empire as well as
  science, one would help on the start screen. It is Ken's line to write,
  so it is left.

## Deployed

2026-10-04, to the service on kai, by `just deploy` (`.sprint-deploy`'s
`recipe: deploy`) from merged `main` at `07b04c55` (PR #56). The content
clone is at the same commit.

- **The deploy's own verify:** all ten checks `ok` (both doors, write
  gating, reader-data and notes gating, a frame's body from the library,
  compression). `DEPLOYED` reads `07b04c551`.
- **This sprint's work, live on both doors (:4890 and :4891), each 200:**
  `/western-civ`, `/western-civ/hammurabi` (its page carries "We set the
  law in STONE."), `/western-civ/fall-of-constantinople` (a trail frame),
  `/western-civ/holocaust`, and `/media/western-civ/hammurabi/hammurabi-columns.jpg`.
- **`/api/stats`** counts western-civ at 72 frames, 14 of them in 5 trails,
  58,810 words (214 pages, by the stats' own count, which includes tables
  and captions), 48 images, 12 charts and 150 connections.
- **The public reader site** was published the same day at Ken's word,
  with `just publish-public` from `561c094`: Fly release v11, image
  `kloom-reader:561c09481-202610041619`, replacing v10 (`3c49f08`). Every
  `verify-public` check passed (TLS, HSTS, robots, the sign-in wall, the
  404s for grow and for ask and keep without ask, compression, the
  library's build `992f39`, the Fly-Client-IP overwrite). The site has two
  notes, none detached; ask has spent $0.02 of $15 this month.
  `pull-notes` backed up the readers' store first, to
  `reader-20261004-1619.db`.
