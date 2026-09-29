# 015 — Fourth subject: the History of Computing

## Goal

korg proposal 3427 (Ken, 2026-09-28), covering korg 3398: the fourth
subject, computing from counting boards and gears to the cloud. It is the
second test of `skills/author-subject/SKILL.md`, written in sprint 014, and
must complement the AI subject rather than repeat it: where both touch an
event, this subject's frame is about the machine.

## Decisions

- **Premises held.** There was no `subjects/computing`, and the
  author-subject skill and its tools were in place as sprint 014 left them.
  kloom is not in the cross-project plan index.

### Shape

- **Dates, then technologies.** The plan is
  `create-tools/subject-plan/computing.json`. Its 37 main-spine frames run
  through six `date` segments, from counting boards to the Altair:
  1. Counting and gears;
  2. Engines of arithmetic;
  3. Cards, gears and relays;
  4. The electronic machine;
  5. Transistors and mainframes;
  6. The microprocessor.

  Then come three `technology` segments, where threads run side by side
  and a year is the wrong label (Networks; Software, shared; Computing
  everywhere). A closing `category` segment, Open questions, holds
  security and where computing is now.

- **Six trails of five frames**, on the proposal's candidates:

  | Trail                     | Anchor              | Label kind |
  | ------------------------- | ------------------- | ---------- |
  | Babbage's engines         | `difference-engine` | date       |
  | Bletchley and Colossus    | `colossus`          | date       |
  | Transistor to Moore's law | `transistor`        | date       |
  | The personal computer     | `altair`            | date       |
  | The internet stack        | `internet`          | technology |
  | Unix and C                | `unix`              | date       |

  The internet stack is labelled by layer, not by year: its frames explain
  one layer after another.

- **Complementing AI.** The AI subject tells Lovelace's notes, Boole and
  Shannon, Turing's 1936 paper, the Turing test, Dartmouth, Lisp machines,
  and GPUs and TPUs. This subject gives the machine side of each: the
  Babbage trail's `mill-and-barrels` is the engine's mechanism, not the
  notes; `edvac-report` is the stored-program design, not the 1936 paper.
  Where a story is AI's or Feynman's to tell, a frame mentions it in a
  sentence rather than retelling it.

- **The voice** is the collective "we" of the field, as in western-civ
  and ai, with a machine as the subject where a frame is about one
  machine.

### Theme

Three pairs of palettes, one for each era of the machine. Every ink,
muted, accent and line colour was checked against its background:

| Palette   | Scheme | For                                | Ink  | Muted | Accent | Line |
| --------- | ------ | ---------------------------------- | ---- | ----- | ------ | ---- |
| walnut    | dark   | counting, gears and cards, to 1941 | 14.6 | 7.3   | 9.4    | 10.7 |
| cardstock | light  | counting, gears and cards, to 1941 | 12.8 | 5.7   | 5.6    | 10.5 |
| console   | dark   | valves, transistors and mainframes | 13.8 | 7.1   | 8.0    | 10.6 |
| teletype  | light  | valves, transistors and mainframes | 15.1 | 6.3   | 7.1    | 12.7 |
| circuit   | dark   | the microprocessor, networks, now  | 14.4 | 8.0   | 9.8    | 11.2 |
| schematic | light  | the microprocessor, networks, now  | 16.3 | 6.5   | 6.1    | 13.0 |

The lowest contrast is 5.6:1, against a floor of 4.5.

### The first segment, by hand

Counting and gears has three frames:

- `abacus` (c. 300 BC): the Salamis tablet, Roman _calculi_, the
  Exchequer's cloth, bead frames, and the 1946 contest in Tokyo;
- `antikythera` (2nd century BC): gear trains as multiplication, the
  Metonic train drawn from its tooth counts (64/38 × 53/96 × 15/53 = 5/19),
  and the mechanism read as a program;
- `logarithms` (1614): Napier's table against a modern computation,
  Briggs's base 10, and the slide rule.

**What writing them found:**

- **Reading the revision you cite needed a tool.** The grow skill says to
  read the Wikipedia revision a citation pins, but `wiki-cite` could not
  print it, and I wrote a throwaway script to read the wikitext.
  `wiki-cite --text DIR` now writes each cited revision's readable text.
  The parallel authors got it before they started.
- **A primary source reversed a draft.** The first draft said the
  Antikythera makers found their planetary cycles by _anthyphairesis_.
  Freeth et al. (2021) say the opposite: that route fails for Saturn, and
  they propose another. The reading now gives both.
- **Sources disagree about the Salamis tablet.** Two Wikipedia articles
  give 1846 and 1899 for its discovery, and one calls it a gaming board.
  The reading gives both.
- **Unsupported flourishes.** Several were cut in review: who staged the
  Tokyo contest, "ratio-numbers" as the meaning of _logarithm_, and a
  claim that the bead frame is Asian (the 11th-century European abacus
  had beads on wires).
- A quotation seen only in Wikipedia (the Tokyo newspapers, Kepler on
  Bürgi) is cited as the article that quotes it, with a note, as the grow
  skill says.

### Authoring at scale

- **Fourteen authors in parallel**, one per segment or trail. The authors
  of `transistor` and `colossus` also wrote the trail or kept to the
  machine while the trail's author told the story. Each worked from:
  - the grow skill, the author-subject skill and the three hand-written
    frames;
  - a shared brief, kept with the sprint's working notes, whose substance
    is in this record: the voice, the palettes by era, what the AI and
    Feynman subjects already tell, the sources that are free, and how to
    validate alone;
  - its own paragraph naming its frames, each frame's palette, what its
    neighbours and its trail cover, and what it must leave to others.

  Each wrote only its own frame directories, its own plate module
  (`create-tools/draw-plates/computing_<part>.py`) and its own chart
  specs.

- **Review, per segment.** For each report:
  - the plates were checked on a contact sheet in their palettes;
  - the flagged claims were spot-checked, and the recent ones read at
    their source (LineShine as TOP500's No. 1 in June 2026, on TOP500's
    own page);
  - the segment was committed on its own, staged with `stage_segment.py`,
    after the index was exported to a scratch directory and the subject
    tests run there.

  There are fifteen commits of content. Trails waited for their anchors.

- **What review changed:**
  - `unix-wars` gave the 1975 university licence as $200 and `unix` as
    $150. RFC 681 (1975) says $150; `unix-wars` now says so and cites it.
  - `ibm-360` converted the 350's price per megabyte into 2020 dollars
    by the author's own arithmetic. No source did, and it was cut.
  - `colossus` first retold its trail's Heath Robinson and Mark 2; its
    author trimmed it to the machine once the trail's drafts were
    readable.
  - The unsure bibliographic details were checked where cheap: the
    imprint of Babbage's _Passages_ against Gutenberg's title page.
- **Where sources disagreed, the readings give both**, over sixty times.
  Among them:
  - the Salamis tablet's discovery;
  - the 1890 census's saving;
  - the Z1's end;
  - Colossus Mark 1's valves;
  - ENIAC's valves (17,468, 18,000 or 19,000);
  - who invented the stored program;
  - the Baby's first runs;
  - UNIVAC's delivery;
  - the hairdressers of Prony's tables;
  - Kilby against Noyce;
  - who invented packet switching;
  - ransomware's losses (the FBI's $32 million against Chainalysis's
    $820 million);
  - the share of web traffic that is encrypted.
- **Wikipedia was wrong or divided against primary sources** several
  times:
  - it dates the PDP-8 to 1964 in one article;
  - the Census Bureau misnames CTR;
  - one article says 1BSD was released in 1978, against McKusick's 1977.
- **What it came to:**
  - 67 frames and about 52,400 words of prose;
  - 90 images, all public domain, CC0 or CC BY(-SA), each looked at
    before use, none repeated;
  - 26 charts and 90 tables;
  - fourteen frames dated with `asOf`;
  - every accent unique.

  Every chart rebuilds byte for byte from its spec, and
  `draw-plates/computing.py` redraws all 67 plates identically under two
  hash seeds.

### The method test: what the skills assumed

The authors reported every place the skills, the brief or a tool was
wrong, silent or in the way. As in sprints 006 and 014, each finding was
generalised in a skill, fixed in a tool, or noted.

**Generalised in `skills/grow/SKILL.md`** (§Authoring with tools):

- read the Wikipedia revision you cite (`wiki-cite --text`);
- Wikisource and Project Gutenberg for old texts, and the Wayback
  Machine's `id_` form for sites that refuse a script, cited by their own
  URL;
- how to cite an RFC, a thesis, a patent, and a work read in a copy;
- a number an author worked out is said to be theirs;
- Commons' `published` can be the upload date, and "public domain" can be
  claimed for a company's photograph;
- the prose count leaves out headings, and Prettier does not format
  Python.

**Added to `skills/author-subject/SKILL.md`**, on what a brief settles:

- an anchor's author is told what each trail frame covers, not only its
  id;
- who owns a figure two frames will want to chart (two authors wanted
  ENIAC's trajectory time);
- each frame's palette, so the spine alternates however it is shared out.
  Here it did, all the way down the main spine;
- accents are grepped again before reporting (two authors chose FREE
  within minutes);
- how to check a draft before its `frame.json` goes live, and a trail
  before its anchor lands.

**Fixed in the tools:**

- **`wiki-cite --text DIR`** (new) writes each cited revision's text. It
  also gives one citation for titles that redirect to one article. They
  printed twice.
- **`subject_plan.py --complete`** left the finished frames of a trail
  with no anchor in the copy, where they failed every author's check. It
  now leaves them out and names them. Three authors hit it; the copy was
  seen failing on the five PC-trail frames, and passing once they were
  named and left out.
- **`bar-chart`** labelled a whole number "56.0". Three authors worked
  round it, and the Linux TOP500 chart shipped with 1.0, 28.0 and 67.0
  machines. It now writes 28. Every other chart rebuilds byte for byte.
- **`plates.py`'s `D.text`** did not escape. Two authors wrote AT&T or
  `<TITLE>` into a label and got invalid SVG; one escaped by hand. It now
  escapes. Every plate of every subject redraws identically, except the
  AI `rlhf` plate's bare `>`, now `&gt;`.
- **`prose_words.py`** (new) counts a reading's prose. Four authors had
  each written their own.
- **`contact_sheet.py --scale`** renders a sheet large enough to read the
  labels. Three authors screenshot it by hand at 2.5×.
- The bar-chart README's table now lists every spec, as it says it does.

**Noted, not changed:**

- **`commons-media`** writes straight into a frame directory, gives the
  uploader's words as author, can't recompress a large PNG, and marks a
  doubtful "public domain" `ok`. The skill now says to check, and every
  image was rewritten and looked at. A preview mode would help, but
  nothing went wrong for want of it.
- **Accent reservations.** Grepping narrows the race but does not close
  it; review caught the one clash. Not worth machinery.
- **Wikipedia revisions dated after `accessed`.** Revisions are dated in
  UTC, and an evening in Pacific time is already the next day there. One
  author dropped such a citation. The validator does not compare the two,
  and should not.
- **Sites that refuse scripts** (IEA, GSMA, ACM, RAND, TOP500's
  statistics, Cloudflare Radar) were read through archives or their data
  files. The skill now names the Wayback route.

### Candidate links to other subjects (for korg 3399)

Reciprocal to sprints 006 and 014's lists:

- **To `ai`:**
  - `jacquard-loom` and `mill-and-barrels` → `analytical-engine`:
    Lovelace's notes against the machine;
  - `pascaline` → `leibniz`: the stepped reckoner;
  - `differential-analyzer` and `z3` → `laws-of-thought`: Shannon ran the
    analyzer; Zuse's switching logic;
  - `z3` → `turing-machine`: universal in principle (Rojas 1998);
  - `edvac-report` → `turing-machine` and `mcculloch-pitts`: the First
    Draft builds its circuits from McCulloch–Pitts neurons;
  - `manchester-baby` → `turing-test`;
  - `whirlwind` → `adaline`: a 1953 Widrow memo on testing core memory;
  - `fortran` and `univac` → `samuel-checkers`: the IBM 701 and 704;
  - `time-sharing`, `multics` and `arpanet` → `eliza`: Project MAC;
  - `bsd` and `minicomputer` → `expert-systems`: the VAX;
  - `xerox-alto`, `bsd` and `free-software` → `lisp-collapse`;
  - `microprocessor` → `adaline`: Hoff;
  - `cloud`, `where-computing-is` and `end-of-scaling` → `compute`;
  - `colossus-d-day` → `governance`: Bletchley Park, then and now.
- **To `feynman`:**
  - `hollerith`, `eniac` and `harvard-mark-i` → `punched-cards`: the Los
    Alamos machines and human computers;
  - `moores-law` → `plenty-of-room`, and `physics-of-computation`
    (Mead, who named Moore's law);
  - `xerox-alto` and `microprocessor` → `physics-of-computation` (Conway
    at PARC, silicon gates);
  - `where-computing-is` → `lectures-on-computation` (Landauer's bound);
  - `tls` and `security` → `quantum-computing-now` (Shor, ML-KEM);
  - `arm` → `connection-machine`: TOP500's first No. 1 was a CM-5.
- **To `western-civ`:** `macintosh` → `printing-press`: desktop
  publishing.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint,
  and 635 tests. Every subject is loaded and validated, and every SVG
  of every subject is sanitised.
- **Every content commit validated on its own.** The index was exported
  to a scratch directory and the subject tests were run there.
- **Negative tests, each seen failing:**
  - `prose_words.py` exits 1 with a limit below the real counts, and
    flagged `security` at 908 words while its author was still at work;
  - the complete copy failed on the PC trail's five frames before the fix
    and names them after it;
  - two authors planted a duplicate accent in their scratch copies and
    watched the validator fail.
- **Reproducibility:** all 50 chart specs rebuild their committed charts
  byte for byte, and the computing plates redraw identically under two
  hash seeds. After the escaping fix, all four subjects' plates redraw
  identically but one (`rlhf`, above).
- **Browser pass** (Playwright, headless Chromium, keyboard only, on a
  scratch data directory):
  - `/computing`: the start screen titled "The History of Computing",
    Enter to begin;
  - → through all 37 main-spine frames in plan order, with the right
    accent and HUD label at each;
  - T into each of the six trails at its anchor, → through every trail
    frame, and Esc back to the anchor: 67 stops in all;
  - Home and End reach the two ends;
  - a deep link to a trail frame (`/computing/tls`);
  - no broken images, no console errors, no failed requests;
  - no horizontal overflow at 390px;
  - the start screen's list offers the History of Computing among the
    four subjects.

## Repaired in passing

- **Tools:** `wiki-cite`'s duplicate citations, `--complete`'s
  anchorless trail frames, `bar-chart`'s "28.0", and `D.text`'s escaping
  (above). None of them was part of the item, and every one had failed an
  author.
- **The bar-chart README** said every spec was in its table; 26 new ones
  were not.
- **Stale docs:** the README, CLAUDE.md, the design doc and the roadmap
  said there were three subjects.

## Follow-ups

None filed. Every finding is fixed here or noted with its reason. The
candidate links go to korg 3399 as a comment. The AI subject shows two
Commons images twice each (`Full_GPT_architecture.svg`, and a t-SNE plot
of word embeddings). Sprint 014 noted that reuse can be deliberate, so
they are left as they are.
