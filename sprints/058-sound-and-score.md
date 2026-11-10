# 058 — Sound and Score

## Goal

korg proposal 3549, covering korg 3545: the thirteenth subject,
`subjects/music`, _Sound and Score_, "a history of Western music, from bone
flutes to streaming". It is kloom's first arts subject, and the last of Ken's
four-subject arc (3542 → 3544 → 3543 → 3545). One leg of the overseen backlog
program korg 4368, run as a karc leg on kai from `main` at `95c16101`, the
morning after sprint 057's fifth tune of the author-subject tools.

## Decisions

- **The premise held** (checked at start): no music subject existed; western-civ
  already holds `beethoven-ninth` and `rite-of-spring`, which the brief tells
  music to connect to, not retell; kloom is not in the cross-project plan
  index; no grow branch was pending.
- **The before, recorded first** (`.scratch/058/reach-before.txt`,
  `density-before.txt`): western-civ reached, in one and two steps, 1 and 10
  of ai's 66 frames, 21 and 50 of biology's 67, 5 and 25 of blood's 62, 20
  and 44 of chemistry's 66, 5 and 16 of computing's 70, 7 and 19 of
  feynman's 62, 30 and 46 of food's 65, 9 and 20 of making's 68, 13 and 37 of
  mathematics's 65, 10 and 19 of nursing's 64, and 38 and 53 of physics's 68. The registry held 4,894 names.
- **The id is `music`**, served at `/music`; the title _Sound and Score_ (Ken's,
  2026-10-03) and the subtitle "a history of Western music, from bone flutes
  to streaming" (57 characters), kept as the proposal offered it.
- **Recordings are cited, not played** (the proposal's default). kloom has no
  audio, so every reading describes what is heard and cites the recording it
  describes. That needed a citation kind: **`recording`** (performers,
  `recorded`, label and catalog number, release, the page that holds it),
  rendered per Chicago 14.263, an album italic and a track on one quoted
  (`engine/citation.ts`, docs/design.md §Citations, the grow skill).
- **The audio question is not filed.** The proposal's notes say to file a
  public-domain-clip reader feature as a work item if it looked worth having;
  the overseer's run rule for program 4368 files no new work items, and wins.
  It is written up for decision in the wrap-up instead.
- **A third trail other than _Recorded sound_.** 3545 offered Tuning, The piano
  and Recorded sound as trail candidates. Recorded sound would retell the main
  spine's _Machines that remember_ section (phonautograph to LP) frame for
  frame, so the third trail is **_The voice_** instead: the castrati, Jenny
  Lind's tour, García's laryngoscope, the crooner's microphone and Auto-Tune,
  anchored on Monteverdi's _Orfeo_.

### Shape

The plan is `create-tools/subject-plan/music.json` (written by
`.scratch/058/mkplan.py`): 50 main-spine frames and three trails of 17, 67 in
all. The spine is dates, in ten sections that each restart time, following
3545's nine-part arc with its twentieth century split in two:

| Section                   | Palette     | Frames | Years             |
| ------------------------- | ----------- | -----: | ----------------- |
| First sounds              | `cave`      |      3 | c. 38,000–1400 BC |
| Number and harmony        | `monochord` |      4 | c. 500 BC–AD 510  |
| Writing it down           | `vespers`   |      5 | c. 900–1322       |
| Print and the Renaissance | `woodcut`   |      4 | 1501–1567         |
| The Baroque               | `gilt`      |      5 | 1607–1742         |
| Classical and Romantic    | `salon`     |      6 | 1781–1893         |
| Machines that remember    | `shellac`   |      7 | 1857–1948         |
| Songs of the New World    | `sheet`     |      4 | 1871–1925         |
| Modern and electric       | `valve`     |      5 | 1921–1964         |
| Digital                   | `pixel`     |      7 | 1957–2026         |

| Trail     | Anchor              | Palette     | Frames |
| --------- | ------------------- | ----------- | -----: |
| Tuning    | `pythagoras-ratios` | `monochord` |      6 |
| The voice | `monteverdi-orfeo`  | `gilt`      |      5 |
| The piano | `mozart-vienna`     | `salon`     |      6 |

### Theme

Five dark/light pairs, one palette per section, every pair used, the main
spine alternating dark and light by section (`.scratch/058/palettes.py`):

| Palette   | Scheme | For                               | Ink  | Muted | Accent | Line |
| --------- | ------ | --------------------------------- | ---- | ----- | ------ | ---- |
| cave      | dark   | first sounds                      | 15.3 | 7.8   | 8.6    | 11.3 |
| monochord | light  | number and harmony; Tuning        | 15.0 | 6.7   | 6.5    | 12.9 |
| vespers   | dark   | writing it down                   | 15.5 | 7.9   | 9.6    | 11.3 |
| woodcut   | light  | print and the Renaissance         | 15.4 | 6.6   | 6.5    | 13.0 |
| gilt      | dark   | the Baroque; The voice            | 15.3 | 8.0   | 10.3   | 11.5 |
| salon     | light  | classical and Romantic; The piano | 15.1 | 6.7   | 7.1    | 13.3 |
| shellac   | dark   | machines that remember            | 15.9 | 8.3   | 7.4    | 11.9 |
| sheet     | light  | songs of the New World            | 14.8 | 6.2   | 6.0    | 12.5 |
| valve     | dark   | modern and electric               | 16.0 | 8.2   | 8.2    | 12.1 |
| pixel     | light  | digital                           | 15.7 | 6.7   | 5.6    | 13.3 |

The lowest contrast is 5.6:1, `pixel`'s accent.

### The hand frames

_First sounds_, written by hand as the bar (commit `3dae03c9`):

- `hohle-fels-flute` (c. 40,000 years ago, BONE): the griffon-vulture flute
  found at Hohle Fels in 2008, from Conard, Malina and Münzel in _Nature_
  (read in its abstract and captions), the 2009 press reports and Ice Age
  Europe's account of the replicas; the ivory flutes' split-and-rejoin
  making as a table and the plate; the open question of how it was played
  (an edge-blown flute, or a reed instrument with a lost mouthpiece); the
  Geissenklösterle redating to 42,000–43,000 years and the disputed Divje
  Babe "flute".
- `lyres-of-ur` (c. 2500 BC, LYRES): the Great Death Pit and Puabi's grave,
  from Woolley's own _Ur of the Chaldees_ (1929, public domain in the US
  since 2025, quoted) and _Ur Excavations II_ (1934, paraphrased); the
  plaster-of-Paris recovery; Woolley's string counts as a table; his
  bass-tenor-alto guess; the 2011 CT study of the attendants' deaths.
- `hurrian-hymn` (c. 1400 BC, CLAY): tablet h.6 from Ugarit; the
  Babylonian string names and the interval pairs, the notation's first line
  read through them, as a table and the plate; five rival decipherments; and
  the argument over whether the tuning was diatonic (Wulstan, Mirelman,
  Rahn 2022), with Kilmer's 1976 record and a 1978 broadcast cited as the
  first two `recording`s.

What the hand frames found:

- **Wikipedia was wrong once and a reporter once**: the Paleolithic flute
  article dates the Hohle Fels find to 2006 (the 2009 reports and the museum
  say 2008), and NPR called the 22-centimeter flute "about a foot long". The
  reading says both.
- **A museum's object was rebuilt**: Woolley restored Puabi's instrument as a
  harp; the British Museum rebuilt it as the Queen's Lyre in 1971–72 after
  heat in its gallery melted his wax (the museum's own record, through the
  Wayback Machine, since the British Museum refuses a script).
- **A Commons "public domain" drawing was a modern copy**: the hymn tablet's
  widely used drawing carries `PD-Art|PD-old` but is an unknown modern hand
  copy; it was left out. Folded into the brief.
- **The tools stamped two different days**: `commons_media` (and `bar_chart`
  and `subject_plan`'s stand-in) stamped the host's local date, `wiki_cite`
  the UTC date (sprint 049); on kai, in PST, one frame's citations disagreed
  by a day after 16:00. Repaired: all stamp UTC.

## Authoring at scale

Twenty-seven authors, one per part of two or three frames, each a subagent
given the shared brief (`.scratch/058/brief.md`) and a paragraph of its own
(`.scratch/058/parts/`, written by `.scratch/058/mkparts.py` from the plan and
`.scratch/058/paras*.py`). The plan's `owners` names the 21 shared names,
computed from the paragraphs as each name's earliest-committing part. Every
name id the brief gives was checked against Wikipedia's search before it went
out: 213 matched, and 33 were wrong or had no article (`4-33` for `433`,
`gramophone-record` for `phonograph-record`, `manuel-garcia-ii` for
`manuel-garcia-baritone`, `andy-hildebrand`, a redirect to AutoTune, dropped),
and seven the brief called new were already in the registry
(`hildegard-of-bingen`, `arnold-schoenberg`, `simon-stevin`, `basf`,
`polyvinyl-chloride`, `stanford-university`, `memphis-tennessee`). Twenty
started at once, the session's limit; the last seven as the first finished.

- **Committed as each part could be**, not in the planned order: a part
  waited only for its trail's anchor and for names it borrowed from parts
  still at work. Review per part was `.scratch/058/review.sh` (a copy with
  that part's drafts, marks placed, the subject tests, word counts, accent,
  topic and image clashes) and a contact sheet; then `commit.sh`: names
  added, marks placed, staged with `stage_segment.py`, and the exported
  index tested before every commit. Twenty-seven part commits and the hand
  segment, none of which failed its index check. Three pairs of parts
  borrowed from each other (tune1 and harm2, tune2 and baroque2, baroque2
  and classic1); the first of each brought the other's draft in without
  `home`, and the owner's commit gave it back. The authors took 14 to 38
  minutes each; all 27 reported within two hours of the brief.
- **What it came to**: 67 frames, 57,419 words of prose (691 to 898 a
  frame); 75 images, each looked at and none repeated in the repository; 7
  charts and 77 tables; 1,041 citations, 59 of them recordings; 3 frames
  with `asOf` (Bayreuth's festival today, streaming, music made by AI);
  every accent unique. The registry grew from 4,894 names to 5,512.
- **Fixed at review**:
  - **A press photograph left out**: Berliner with his gramophones is a
    National Photo Company print; the Library of Congress says "no known
    restrictions", but nothing records it was published without a notice,
    which the grow skill's rule asks for, so it was dropped.
  - **Measured times dropped**: `hot-five`'s table and plate gave "West End
    Blues" chorus by chorus in minutes and seconds, measured from an
    Internet Archive upload of a 1928 recording still in copyright; the
    times came out, the bars and what is heard stayed (from Pearson's
    notes). Folded into the grow skill.
  - **One connection dropped as a rhyme**: `aristoxenus` →
    `biology/aristotle-animals` (teacher and student each describing first).
  - **One _why_ narrowed** to what its reading says: Orfeo's castrati, one
    borrowed from the Medici court (the reading does not name Magli).
  - **Homes set** on names a later frame is chiefly about: `les-paul`,
    `arnold-schoenberg`, `hildegard-of-bingen`, `compact-disc`.
- **The paragraphs were wrong somewhere in every part**, and each error was
  caught by an author reading the source, the leads-not-sources rule
  holding for a ninth run. Among them: Philolaus is c. 470–385 BC; the
  Ptolemaic _helikon_ is a ratio device, not an eight-string instrument;
  Zarlino's 1558 temperament is 2/7-comma, his quarter-comma 1571; Ellis
  defined the cent in 1880, not 1875; the Council of Trent never passed the
  canon about hearing the words (Monson); Petrus Castellanus edited the
  _Odhecaton_, Girolamo Donato was its dedicatee; Farinelli sang the same
  four airs to Philip V for ten years, not 22; the crooner ban was the
  BBC's of 1942; Caruso's 1902 sessions were for the Gramophone & Typewriter
  Company in Milan; Columbia's Glee Clubs record was not the first
  electrical record sold (Victor 19626 was); BASF's first tape was
  carbonyl iron; Schaeffer's 1948 études were on discs; the 1859 grand
  patent was Henry Steinway Jr.'s; Schoenberg introduced the row in 1923;
  the payola hearings were the House's; streaming led US revenue from
  2015; MUSIC I ran on a 704 in New York; the Technical Grammy for MIDI was
  2013; "Crazy Blues" is not a twelve-bar blues throughout.
- **Wikipedia was wrong or contradicted itself many times**, and the
  readings follow the sources: the Paleolithic flute's find dated 2006; the
  Odhecaton's passes in two orders across three articles; Werckmeister
  III's fifths; Ellis's cent "in 1875"; the Chowning patent's expiry; "Daisy
  Bell"'s machine; the Possente spirto's print year; Beethoven's Broadwood;
  and the Agassiz-style self-contradictions in the Jenny Lind, Paganini and
  Crosby articles.
- **Told honestly**: the boys castrated for choirs and opera (named, with
  the Sardinian code that ended it), the attendants killed at Ur (the 2011
  CT study against Woolley's "voluntarily"), the spirituals' makers and the
  students who sang them, the race-record market's pay, Wagner's _Judaism in
  Music_ and Bayreuth under Winifred Wagner and Hitler (twelve of its 51
  persecuted Jewish artists murdered), the Nazi dismissal of Schoenberg and
  the _Entartete Musik_ show, Pat Boone's covers of Little Richard, and
  Wendy Carlos throughout by her name.

### Names and connections

- **Names**: 618 new, every Wikidata id from `names.py lookup`; 23 old ones
  widened that were written from one subject's angle (Helmholtz known only
  for energy and nerves, Ptolemy for the _Almagest_, Pythagoras with no
  music, Nicomachus for arithmetic, Stevin for his falling balls, Chicago
  for grain and meat, BASF and PVC without tape and records, Java for its
  plantations, the IBM 7090, Stanford, Sony, Fraunhofer and others); the
  Republic of Venice gave up its "Venice" alias to the city's own name.
- **Connections**: 77 from music to nine other subjects, every one
  supported by a reading: 36 to western-civ, 10 to physics, 9 each to
  computing and mathematics, 4 to ai, 3 each to chemistry and making, 2 to
  food and 1 to feynman. 70 within music, 61 added at review from the
  authors' lists, each checked against the reading the author named. No
  other subject's frames were changed. None of biology, blood or nursing
  has a direct link: music's arc does not cross them.
- **Density** (`names.py density`, `.scratch/058/density-after.txt`): music
  has 846 marks on 718 names, 12.63 a frame, and 147 connections, 2.19 a
  frame; western-civ now touches 331 connections, 4.6 a frame.
- **Reach**, in one and two steps (`names.py reach`): western-civ reaches
  27 and 47 of music's 67 frames, and its two-step reach into the others
  rose for computing (16 → 17) and mathematics (37 → 38). Music reaches 22
  and 55 of western-civ's 72, 7 and 26 of physics's, 4 and 19 of
  mathematics's, 7 and 15 of computing's and 3 and 20 of chemistry's.

### What the tools and skills assumed

Every author reported where the skills, the brief or a tool was wrong,
silent or in the way.

- **Repaired here** (each in "Repaired in passing" below): a `book`'s
  `volume` silently dropped (46 citations in seven subjects), the UTC/local
  date split between `wiki_cite` and the other tools, `names.py drafts
--part`'s silence, `contact_sheet`'s stale per-plate PNGs, and
  `reaching-sources.md`'s line that there is no `lecture` kind.
- **Folded into the skills**: a `recording` kind and how to cite one an
  author cannot hear (grow skill, design.md); an unauthorized upload of a
  recording in copyright is not used, not even measured (grow skill); a
  search for an id's words is not the lookup, and committed owners and
  mutual borrowing in checking commands (author-subject); a section on
  music and sound recordings, with the routes the authors found to the
  Library of Congress, DAHR, UCSB's cylinders, the Internet Archive's 78s
  and scores, treatises, old journals and patents, museums and the sites
  that refused (reaching-sources).
- **Left for a decision** (described in the wrap-up, not filed, at the
  overseer's rule for program 4368): see below.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint,
  1,803 vitest tests (every subject loaded and validated, every SVG
  sanitized, every connection's frame and every mark's name found), `just
tools-test`, `just reader-gate`, every mark spec with `--check
--placed`, and the American-spelling check.
- **Every content commit was validated on its own**, the index exported
  and the subject tests run on it.
- **Negative tests, each seen failing first**: the recording kind's
  rendering and its misplaced `recorded`; a book's volume (failed before
  the fix). `contact_sheet`'s cleanup was seen removing a planted stale
  PNG, and `names.py drafts --part nosuch` now says so.
- `just scene-fit music`: 0 misfits in 67 frames at 1280×800, 1400×900
  and 390×844.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on the
  dev server, `.scratch/058/walk.mjs`): the start screen titled "Sound and
  Score"; → through all 50 main-spine frames with the right accent and HUD
  label at each; T into each of the three trails at its anchor, → through
  every trail frame and Esc back: 67 stops, no mismatch; Home and End
  reach BONE. and PROMPT.; a deep link (`/music/castrati`); no broken
  images, console errors or failed requests, and no horizontal overflow at
  390px; the subject list shows "Sound and Score".

## Repaired in passing

- **Accessed dates in UTC**: `commons_media`, `bar_chart` and
  `subject_plan`'s stand-in stamped the host's local date where `wiki_cite`
  stamps UTC (sprint 049); on kai, in PST, one frame's citations disagreed
  by a day after 16:00. All stamp UTC (`4eece37a`).
- **A book's volume** was accepted and never rendered; it reads "Vol. N."
  after the title (Chicago 14.119), with a test seen failing first.
- **`names.py drafts --part`** printed nothing for a part with no drafts,
  which four authors read as a failure to run; it now says so.
- **`contact_sheet`** left per-plate PNGs of an earlier run beside the
  current ones, and two authors looked at stale plates; it removes the
  PNGs it named before that it does not draw now.
- **`reaching-sources.md`** said to cite a lecture as `web`; the `lecture`
  kind exists since sprint 057.
- **Two music drafts respelled** for the spelling gate (catalog, theater).

## Decisions for Ken (not filed)

- **Audio in the reader**: the proposal asked the sprint to decide how to
  cite recordings (done: the `recording` kind) and to file a public-domain
  clip feature if one looked worth having. It does: the Library of
  Congress's National Jukebox and UCSB's cylinders hold pre-1925 recordings
  now in the US public domain, and 16 of these frames already cite one, and every reading
  already describes the sound. Whether kloom plays audio is a product
  decision; not filed, at the overseer's rule.
- **Publishing**: music is not in `publish.json`, so the public reader site
  will not carry it until Ken adds it.
- **The `recording` kind's next fields**, if wanted: a matrix or take
  number, an archive's call number, roles (conductor, ensemble, soloist),
  and wording for `read: "record"` on a recording ("Read in its catalog
  record only" reads oddly for audio). Authors put these in `note`.
- **Tool features** the authors asked for, each a design choice: a line or
  curve chart in `bar-chart` (tune2 hand-drew one), a rotate-about-a-point
  helper in `plates.py` (three mechanism authors wrote their own), a
  Fotothek reader in `commons_media`, quieter `mark --check` warnings after
  titles and place names ("Cardinal", "Duke", "California"), a gate for "the
  chart below", and whether the spelling gate should cover `skills/`.
- **The 15-mark cap** was the binding limit on several history frames
  (blues, Petrucci, neumes); the brief could say which yields, a planned
  borrow or an owned name.
