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
- **An old work cannot be dated.** `published` takes a four-digit year,
  so neither the papyrus (c. 1550 BC) nor, later, a manuscript of AD 888
  could be; their dates went into the title or the reading.

### Authoring at scale

- **Twenty authors in parallel**, in two waves launched minutes apart,
  each a subagent with a shell and the web. Each got a shared brief
  (`.scratch/math/brief.md`: what to read, the voice, the palettes by
  era, the demand that every reading do one piece of mathematics, marks
  by spec, how to check alone, the report) and its own paragraph: frames
  in order, each with its topic, date, palette, what it owns and what it
  must leave to a neighbour, and connection candidates. Anchor authors
  (`euclid-elements`, `diophantus`, `cantor`) finished the anchor first,
  and each anchor was committed before its trail.
- **Review, per part:** the part checked in a copy with every author's
  drafts, word counts, the plates and charts on a contact sheet, claims
  from this month checked against their sources, names added, marks
  placed, then staged with `stage_segment.py` and the exported index
  tested before the commit. Twenty-one commits, one per part plus the
  hand segment, each validated on its own.
- **Claims from after my training** were checked at source, not trusted
  to the report: OpenAI's Navier–Stokes announcement of 8 September 2026
  (Quanta's report read; the frame gives it as contested), Anthropic's
  post of 10 August on the zeta zeros and Lamzouri's arXiv paper of 2
  September, Anthropic's and Buzzard's posts of 4 September on the Lean
  proof of Fermat's Last Theorem, and the factoring of RSA-896 on 19
  September, whose published factors multiply back to the challenge number
  (checked here, against Weis's page and Wikipedia's list).
- **What review changed:**
  - `rigour` ran two words over 900 and was trimmed.
  - `cardano-cubic` lost its connection to Copernicus: the same printer,
    Petreius, is a shared name, not a connection.
  - Four within-mathematics _whys_ claimed more than a reading said (the
    year Cantor began, the strong law, "Algoritmi", Brahmagupta's books
    in Baghdad) and were rewritten to what the readings state.
  - `georg-cantor` went into the registry early, for geometry2's marks,
    without its `home`, which it regained with `cantor`.
  - 21 shared names written from one subject's angle were widened (Euler
    without number theory, Newton without the calculus, Poincaré as a
    relativist only, von Neumann as bomb and computer only, Eratosthenes
    without the sieve, Wiener without Brownian motion), and
    `rsa-cryptosystem` gained its home.
- **Where sources disagreed, the readings give both**, well over a hundred
  times: the Ishango bone as arithmetic or fable, Plimpton 322 as a
  teacher's list or trigonometry, Hippasus as legend, Liu Hui's last π,
  the Bakhshali dates, Kerala's series reaching Europe or not, Gauss or
  Legendre for least squares, Galois's last night, Cauchy's ε, Gödel and
  Hilbert's Königsberg, the Kac–Feynman story, the Mandelbrot set's first
  pictures, Weil's name on modularity, Wiles's seven years or six, and the
  classification of finite simple groups declared done in 1980, 1981 or 1983.
- **The brief was wrong seven times**, each caught by an author reading
  the source: Hilbert's "Wir müssen wissen" came the day after Gödel's
  announcement, not before; _Principia Mathematica_'s page 379 only
  promises 1 + 1 = 2; Wiener's 1923 paper did not prove nowhere
  differentiability (Paley, Wiener and Zygmund, 1933); Florence's 1299
  "ban" was a guild's bookkeeping rule (Nothaft, 2020); Poincaré paid for
  the pulped printing, not a reprint; one Millennium Problem is now
  "active", not open; and the twin-prime bound and RSA records had moved
  in September 2026. The author-subject skill now says to check a brief.
- **What it came to:** 65 frames and about 54,500 words of prose; 64
  images, each looked at before use and none repeated in the repository;
  5 charts and many tables; twelve frames dated with `asOf`; every accent
  unique; 296 new names (the registry has 1,757).

### What the tools and skills assumed

The authors reported every place the skills, the brief or a tool was
wrong, silent or in the way; each finding is also on korg 3461, where the
next two subject runs add theirs before the skill is revised. What
recurred most:

- **Marks.** Most authors could not tell that `mark --check` had placed
  every word (it had: a word it cannot place is named), so they marked
  their copies by hand with `--root`, and two wrote marks into the live
  subject by mistake, because `mark` defaults to it. `mark` now says what
  it places and what would place, and the skills and READMEs say how to
  mark a copy. Five hit a first mention they did not mean (a possessive,
  a quotation, an italic title, a passing mention before the bold one);
  the grow skill now says what counts as first.
- **Images outside `commons_media`.** Eight authors used a page of a book
  scan: a PDF or DjVu on Commons, which the tool refuses, or an Internet
  Archive item. Four converted large PNGs to JPEG with Pillow. The grow
  skill now says how, and to check the licence of the particular scan.
  A `--page` option and a JPEG route in the tool are left for 3461.
- **Commons metadata** was wrong for almost every image (uploader boiler
  plate as author, upload dates, a 1915 date on an 1895 page, a
  retypeset page as the 1879 _Begriffsschrift_, `PD-Art` on a photograph
  of a tablet).
- **The 550–900 band** was tight for every author: the brief's own
  must-tell lists came near 900 words before any mathematics.
- **Sites that refuse a script:** ScienceDirect (and its Wayback copy),
  Project Euclid, the Euler Archive, AMS _Notices_, the Royal Society,
  MAA, phys.org; archive.org's full text, the Wayback `id_` form and
  authors' own copies were the ways round.
- **The stand-in for an uncommitted anchor** needed running
  `subject_plan.py` on the copy, which read as forbidden; the README now
  says it is not.
- **Intraword emphasis** (`3_x_`, `_x_²`) is not emphasis in CommonMark,
  and Prettier breaks it; the grow skill now says to write `*x*`.
- **A four-digit `published`** cannot date anything before AD 1000.
  Whether the citation schema should accept older dates is a decision,
  left for 3461.

### Connections, and the bridge

- **138 connections are stored on mathematics frames**: 68 into other
  subjects (26 physics, 18 ai, 11 computing, 9 western-civ, 4 feynman) and
  70 between mathematics frames, 66 of those added at review from the
  authors' lists, each _why_ checked against a reading. 41 of the 65
  frames connect to another subject. Left unmade: rhymes (Petreius as
  Cardano's and Copernicus's printer, Pascal as the calculator's maker
  and the probabilist), and every candidate whose _why_ no reading states.
- **Two bridges were added at the end**, each with its source read:
  Legendre's 1805 appendix first shows least squares on the Dunkirk to
  Barcelona arc of the metre survey (`normal-distribution` →
  `western-civ/metre-survey`, and on to `ai/adaline`), and Book VII of
  the _Elements_ opens with Euclid's algorithm, the route earlier studies
  took to the Antikythera mechanism's Venus cycle (`euclid-elements` →
  `computing/antikythera`).
- **Density** (`names.py density`), after:

  | Subject     | Frames | Marks per frame | Connections per frame |
  | ----------- | -----: | --------------: | --------------------: |
  | ai          |     66 |           11.24 |                  1.09 |
  | computing   |     70 |           10.33 |                  1.09 |
  | feynman     |     62 |            8.65 |                  1.55 |
  | mathematics |     65 |            7.71 |                  2.12 |
  | physics     |     68 |            7.37 |                  2.94 |
  | western-civ |     24 |            7.04 |                  2.96 |

  Mathematics marks 7.7 names a frame, inside the brief's 4–8.

- **Western-civ's reach into the tech cluster** (`names.py reach`), before
  (recorded at the start) and after:

  | To        | Frames | Within 1 | Within 2    | Within 3    |
  | --------- | -----: | -------: | ----------- | ----------- |
  | ai        |     66 |        0 | 5 → 6       | 11 → 13     |
  | computing |     70 |        4 | 8 → 9       | 15 → 17     |
  | feynman   |     62 |        7 | 14          | 21          |
  | total     |    198 |       11 | **27 → 29** | **47 → 51** |

  One step out, western-civ now reaches 8 mathematics frames, 29 in two
  steps and 53 in three. Into the tech cluster the gain is small, for
  the reason Physics found: a two-step path needs one mathematics frame
  linked to both sides, and the frames western-civ touches (Ishango, YBC
  7289, the Rhind papyrus, Euclid, the sieve, perspective, Riemann's
  curved space) are ancient or geometric, while those the tech cluster
  touches (matrices, gradient descent, Markov, Monte Carlo, Boole, Gödel,
  Turing, RSA) are modern. Before the two bridges above, the two-step
  figure had not moved at all. Mathematics itself is densely linked into
  the cluster: in two steps it reaches 21 ai, 21 computing and 17 feynman
  frames.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint
  and 879 tests; every subject is loaded and validated, every SVG
  sanitised, and the links test finds every connection's frame and every
  mark's name.
- **Every content commit was validated on its own**: the index exported
  and the subject tests run on it. One was refused and fixed before it
  landed (geometry2, on a borrowed name's `home`).
- **All 46 mark specs pass `--check`**, every subject's.
- **Negative tests, each seen failing:** `mark --check` on a planted spec
  word no reading holds (named, exit 1); the index check on a name whose
  home frame was not yet committed; `prose_words.py` on `rigour` at 902
  and `normal-distribution` at 909 words.
- **Reproducibility:** `draw-plates/mathematics.py` redraws every plate;
  the five chart specs are in `create-tools/bar-chart/examples/`.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on a
  scratch data directory):
  - `/mathematics`: the start screen titled "The History of
    Mathematics", Enter to begin;
  - → through all 49 main-spine frames in plan order, with the right
    accent and HUD label at each;
  - T into each of the three trails at its anchor, → through every trail
    frame, Esc back to the anchor: 65 stops, no mismatch;
  - Home and End reach COUNT. and ALONE.;
  - a deep link to a trail frame (`/mathematics/banach-tarski`);
  - no broken images, console errors or failed requests, and no
    horizontal overflow at 390px;
  - the start screen lists the History of Mathematics among six subjects.

## Repaired in passing

- **`names.py mark`** printed nothing when it placed marks, and `--check`
  said "not marked yet" without saying every word had been found; both
  now say what they place.
- **21 shared names** written from one subject's angle, widened.
- **The grow skill**: `PD-Art` and flat works, ScienceDirect and
  archive.org full text, intraword emphasis, what a first mention is,
  book pages scanned outside Commons.
- **The author-subject skill and READMEs**: checking the brief, commands
  named per frame, staging names changed since the last commit, the
  stand-in for an anchor, marking a copy.

## Follow-ups

None filed. What the authors found that needs a decision (a `--page`
option and a JPEG route in `commons_media`, dates before AD 1000 in
`published`, per-frame topics and palettes in the plan, one plate
collector for every subject) is on korg 3461, which exists to weigh this
run's findings with the next two before the skill changes.

## Deployed

2026-09-30, by `just deploy` (the `recipe: deploy` in `.sprint-deploy`),
from merged `main` at `998ce70`, to the kloom service on kai. The
service's content clone is at the same commit.

- `just verify` passed all eight door checks: the tailnet door refuses
  anonymous writes and reader-data reads, and the ssh door lets its reader
  through.
- **The sprint's work, live on both doors (:4890 and :4891), each 200:**
  - `/mathematics`;
  - `/mathematics/ybc-7289` (main spine), whose page carries "TWO.";
  - `/mathematics/banach-tarski` (a trail frame), whose page carries
    "BALL.";
  - `/media/mathematics/ybc-7289/ybc-7289.jpg`;
  - `/api/start/mathematics` (the start screen's look, with the clay and
    vellum palettes).
