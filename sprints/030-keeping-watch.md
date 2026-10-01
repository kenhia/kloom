# 030 — Tenth subject: Keeping Watch

## Goal

korg proposal 3471, covering korg 3470: the tenth subject, _Keeping
Watch_, subtitled "care at the bedside, from infirmary to operating
room", built around Ken's mother's career as a US Navy surgical nurse and
then in hospital administration, and ending on a dedication to her. It is
the companion to _In the Blood_ (sprint 028, for Ken's father), with the
links between the two written on purpose. Its five-part arc runs from
care before nursing, through Nightingale and the profession, the
operating room and nurses at war, to the modern profession. It is the
second run of the author-subject skill since sprint 029 tuned it, and
reports its findings in a new feedback item.

## Decisions

- **Premises held** (checked at start). The subject depends on korg 3399
  (connections), 3461 and 3476 (the two tunings, sprints 027 and 029),
  3465 (the subtitle, sprint 026) and 3475 (the dedication scene, sprint
  028), and all had shipped. No nursing subject existed. kloom is not in
  the cross-project plan index.
- **Ken's answers at the start (2026-10-01):**
  - the title is _Keeping Watch_, the branch `030-keeping-watch`;
  - the subtitle is "care at the bedside, from infirmary to operating
    room". The first one offered, with "the" before each place, was 61
    characters, and the gate allows 60 (sprint 026's rule). That was the
    brief's error, caught before anything was written, and Ken chose the
    shorter form;
  - his mother will not review the frames before they ship, so accuracy
    rests on the sources alone, as for In the Blood;
  - the dedication reads "Captain Kathleen Hiatt, USN", with "Retired",
    and its reading is Ken's own text, drafted by him, checked for
    spelling and grammar, and approved by him with the corrections
    ("Mom" and "Dad" capitalised as his own usage).
- **The id is `nursing`**, served at `/nursing`.
- **The before, recorded first**: `names.py density` and `names.py reach
western-civ --steps 3` before any frame (`.scratch/nursing/density-before.txt`,
  `reach-before.txt`). Western-civ then reached 0, 5 and 13 blood frames
  in one, two and three steps, and the registry held 2,822 names.

### Shape

The plan is `create-tools/subject-plan/nursing.json`: 42 main-spine
frames and four trails of 22, 64 in all, each with its topic, sort and
palette checked by `subject_plan.py --check` before any author started.

- **Five `date` segments, each starting time again**, then two `category`
  segments:

  | Segment                        | Frames | Years     |
  | ------------------------------ | -----: | --------- |
  | Care before nursing            |      7 | 372–1836  |
  | Nightingale and the profession |      7 | 1854–1868 |
  | The operating room             |      7 | 1846–1949 |
  | Nurses at war                  |      9 | 1861–1973 |
  | The modern profession          |     10 | 1873–2004 |
  | Today                          |      1 |           |
  | Dedication                     |      1 |           |

- **Four `date` trails**, the four the proposal named:

  | Trail                 | Anchor             | Frames |
  | --------------------- | ------------------ | -----: |
  | Nightingale's numbers | `rose-diagram`     |      5 |
  | At the table          | `hampton-gloves`   |      5 |
  | Navy nurses           | `sacred-twenty`    |      6 |
  | Who was let in        | `training-schools` |      6 |

  Military nursing from the Civil War to Vietnam, which the proposal
  floated as a trail, is a main-spine segment, because the work item makes
  it one of the five parts. The Navy Nurse Corps, Ken's mother's own
  service, gets the trail instead, so that its frames can be as specific
  as In the Blood's bench. The operating room is likewise a main-spine
  segment, and its trail, _At the table_, follows the scrub nurse's own
  work: the scrub, the mask, the instrument table, the count and the
  checklist.

- **The voice** is the collective "we" of the other subjects.
- **The dedication is the last frame on the spine**: "Dedicated to
  Captain Kathleen Hiatt, USN", in `dressblue`, the Navy's navy and gold.

### Theme

Six dark/light pairs, each tied to a part of the story:

| Palette    | Scheme | For                         | Ink  | Muted | Accent | Line |
| ---------- | ------ | --------------------------- | ---- | ----- | ------ | ---- |
| cloister   | dark   | care before nursing         | 14.6 | 7.5   | 8.1    | 11.0 |
| linen      | light  | care before nursing         | 14.8 | 6.8   | 6.8    | 12.9 |
| lamplight  | dark   | Nightingale                 | 15.0 | 7.6   | 10.5   | 11.3 |
| ledger     | light  | Nightingale's statistics    | 14.3 | 6.3   | 6.3    | 11.9 |
| theatre    | dark   | the operating room          | 15.2 | 8.1   | 10.1   | 11.6 |
| gown       | light  | the operating room          | 15.0 | 6.4   | 5.7    | 12.3 |
| olive      | dark   | the Army and war            | 14.2 | 7.7   | 9.0    | 11.0 |
| canvas     | light  | the Army and war            | 13.9 | 6.2   | 5.7    | 11.9 |
| dressblue  | dark   | the Navy and the dedication | 15.4 | 8.4   | 8.3    | 11.4 |
| whites     | light  | the Navy and the dedication | 16.4 | 7.1   | 10.5   | 14.3 |
| nightshift | dark   | the modern profession       | 15.5 | 8.3   | 10.0   | 11.7 |
| chart      | light  | the modern profession       | 15.6 | 6.9   | 7.3    | 13.3 |

The lowest contrast is 5.7:1, against a floor of 4.5
(`.scratch/nursing/palettes.py`). `dressblue` is navy (#0f1a2e) with a
gold accent (#d4af37), as Ken's note on 3470 asked; its light counterpart
`whites` puts navy on white, since gold on white does not reach 4.5.

### The first segment, by hand

Care before nursing opens with three frames:

- `basiliad` (c. 372): Basil's new city outside Caesarea, from his own
  Letter 94 and his rules for monks (Clarke's 1925 translation, public
  domain), Gregory of Nazianzus's funeral oration, and Nam 2024 on the
  debate over what it was (hospital, hospice or leprosarium). The monks
  who nursed are in the Shorter Rules: "We who serve the sick in the
  hospital are taught to serve them … as if they were brothers of the
  Lord." The plan gave c. 369; the sources give 372, when Valens gave the
  land, and the plan was changed.
- `monastic-infirmary` (c. 530–830): chapter 36 of the Rule of Saint
  Benedict, and the Plan of Saint Gall. No open source details the plan's
  infirmary, so we read its inscriptions from the manuscript itself
  (e-codices' images of Cod. Sang. 1092) and give them in our translation:
  the sick monks' cloister, "the place of the very sick", the
  physicians' house with its drug cupboard, the sixteen-bed herb garden,
  and the house where "the bled, or those taking potions" ate. The image
  in the reading is cut from Commons' public-domain copy, since
  e-codices' own images are CC BY-NC.
- `hospitallers` (1113): the hospital of Saint John in Jerusalem, from the
  bull of 1113, Raymond du Puy's rule ("How our lords the sick should be
  received and served", set out as a table of the admission), Jacques de
  Vitry, and two pilgrims who disagree about its size: John of Würzburg's
  two thousand sick and Theoderich's thousand beds, with Kedar's
  reconciliation.

**What writing them found:**

- **OpenAlex now has a daily budget per network.** A request without an
  API key spends a shared allowance, and this host's ran out after a
  handful of queries, with a `Rate limit exceeded` that names the reset
  at midnight UTC. With nineteen authors working at once it would be gone
  in minutes. The brief says to use Crossref and Europe PMC's REST API
  first, and to keep OpenAlex for the one lookup that needs it.
- **MDPI refuses a script** (a 230-byte page); the Wayback `id_` form
  reads its HTML in full, as `reaching-sources.md` already says.
- **e-codices serves IIIF images** of any region at any size and
  rotation, which made the Plan of Saint Gall's small, upside-down script
  readable. Its images are CC BY-NC, so they are a source to read, never
  an image to use.

### The dedication

`dedication`: the frame Ken specified on korg 3470, laid out as In the
Blood's is, with the `scene.dedication` kind that sprint 028 added:
"Dedicated to" above "Captain Kathleen Hiatt, USN", "Retired" beneath, and
one line, "NURSE CORPS · UNITED STATES NAVY". The palette is `dressblue`,
navy and gold. Its reading is Ken's own text, word for word as he approved
it (`.scratch/nurse-dedication-corrected.md`).

The plate (`nursing_dedication.py`) puts two pieces of insignia side by
side on one line, each named beneath. On the left is a captain's sleeve:
four half-inch stripes a quarter inch apart, the lowest two inches above
the cuff, computed at twelve units to the inch, with the Nurse Corps'
single oak leaf above them in place of the line officer's star, as the
Navy Nurse Corps article's insignia section has it. On the right is the
seal of the Navy Nurse Corps. Both the leaf and the seal are traced from
the Navy's own public-domain seal (Commons) by the new
`create-tools/trace-art/navy_nurse_seal.py`. It traces only the gold, so
on the navy ground the seal reads as gold on navy. The first trace lost
the leaf's pale highlights and left a hole in it, and the stripes, drawn
as outlines, read as five bands. Both were fixed by looking: cream and
near-white tones inside the inner disc count as leaf, and the stripes are
filled as braid is. The plate is about 70 KB.

### Authoring at scale

- **Nineteen authors in parallel**, each a subagent with a shell and the
  web, given a shared brief (`.scratch/nursing/brief.md`) and a paragraph
  of its own (`.scratch/nursing/part-*.md`): frames in order, each with
  its topic, label, sort and palette from the plan, at most about five
  must-tell points, the owner of each shared name, and connection
  candidates, trails included. Every name id in the paragraphs was looked
  up before they went out, and about forty were corrected
  (`beguines-and-beghards`, `united-states-navy-nurse-corps`,
  `mabel-k-staupers`, `postpartum-infections` …), along with ten titles
  that had no article.
- **Review, per part, as each reported:** `.scratch/nursing/review.sh` (a
  copy with every author's drafts; the subject tests with the marks
  placed; word counts; accent, topic and image clashes), a contact sheet
  of every plate and chart, the report's unsure claims, and the riskiest
  readings read in full (`scutari`, `farr`, `where-nursing-is`). Then
  `.scratch/nursing/commit.sh`: names added, marks placed, staged with
  `stage_segment.py`, and the exported index tested before every commit.
  Twenty-one content commits, none of which failed its index check.
  Trail parts waited for their anchors, and borrowed names went in
  without `home` until the home frame landed (`florence-nightingale`,
  `uss-repose-ah-16`, `mary-eliza-mahoney`, `mabel-k-staupers`).
- **Fixed at review:**
  - The Magaw photograph (`nurse-anesthetist`) was dropped. It is tagged
    `PD-old-70-expired` with no photographer, came from a 2016 journal
    article, and nothing shows it was published before 1931.
  - The `staupers` plate's "quota of 1941" became 1940, as its reading
    has it.
  - CLOCK was committed on `hospice` while `surgical-scrub` held it in a
    draft; the scrub's author was told and chose ELBOW.
  - `sacred-twenty`'s headline was shortened so its counter clears the
    metadata at 1400×900 (korg 3469's measure).
  - The rose plate now labels January 1855's zymotic rate as zymotic.
  - Two names drafted twice from the brief's owner list
    (`isabel-hampton-robb`, `american-nurses-association`) were kept once.
  - The registry's alias "Walter Reed" moved off the hospital, now that
    the man has a name of his own.
  - The subject was put into American spelling outside quotations
    ("percent", "meters", "programs"), as the brief asked, and the four
    charts whose headings changed were redrawn.
- **What it came to:** 64 frames and 58,111 words of narrative (211 pages
  at 275 words a page); 59 images, each looked at before use and none
  repeated in the repository; 22 charts and 117 tables; 685 citations;
  seven frames dated with `asOf`; every accent unique; 320 new names (the
  registry has 3,142).
- **The brief was wrong again in nearly every paragraph,** and each error
  was caught by an author reading the source:
  - "The Lady with the Lamp" is Longfellow's phrase, not The Times's.
  - Dix asked for nurses of 35 to 50, not "plain, over thirty".
  - Lister's 1867 dressing was carbolic rag, putty and tin, not lint and
    foil.
  - The plates-and-speech mask test was Hübener's (1898), not Flügge's.
  - The _Mongolia_ nurses were killed by a defective shell, not by the
    enemy.
  - _Repose_'s numbers were the wrong way round.
  - Saunders gave diamorphine in the Brompton mixture, not morphine.
  - California is no longer the only state with ratio laws.
  - The Salisbury Plain quotation is two passages run together.
  - The first infection control sister was E. M. Cottrell, and the
    operating-room text is by Edythe, not Edith, Alexander.

  The leads-not-sources rule held for a fifth run. The owner list was
  wrong twice where an earlier part drafted a name first, and the brief's
  checking command for trail parts left out the anchor; the
  author-subject skill now says both.

- **Accuracy where this reader will look first.** The Navy frames rest on
  the Naval History and Heritage Command's histories, _Navy Medicine_'s
  back issues (public domain on the Internet Archive, the authors' best
  source), DANFS, the statutes themselves, and the nurses' own oral
  histories, marked as their tellings. The operating-room frames rest on
  the period's texts: Fürbringer, Halsted's 1913 account, Robb's hand
  disinfection, Schimmelbusch, Magaw's 1906 paper, the Army's 1943
  _Operating Room Technique_ and the Navy's hospital corps handbooks.
  Where the Navy's sources disagree (Duerk's promotion date, the Brinks
  nurses' ranks, _Consolation_'s first helicopter patient), the readings
  give both.

### What the tools and skills assumed

Every author reported where the skills, the brief or a tool was wrong,
silent or in the way (raw notes: `.scratch/nursing/reports/`). Sprint
029's repairs held: `--with-drafts` ended the copying of drafts by hand,
the readings stripped of marks meant no author typed a mark from habit,
per-plate contact sheets were readable, and the citation forms for
letters, diaries, excerpts and second-hand sources were used without
trouble. What recurred or was new:

- **Two tool bugs**, each found by one author and repaired:
  - `mark` placed a frame's marks even when it named a name no file
    held;
  - its bold check missed a bold mention of an italic name.
- **`lookup --expect`** warned on right items for six authors, because
  029's item check reads Wikidata's few words. The message now says to
  keep a right item, and the README says how to choose the word. Whether
  to keep the check as it is goes to korg 3478.
- **Sites refusing a script** were again the commonest cost: NHHC (a
  broken chain, and 404 to any User-Agent not starting `Mozilla/5.0`),
  `achh.army.mil`, WHO IRIS, Justia, the Joint Commission, and the
  Wayback Machine itself under nineteen authors (429). The routes the
  authors found are in `reaching-sources.md`.
- **Silences in the skills**, now filled: how to cite a statute and a
  court opinion; that a recent sculpture's photograph is not freed by its
  photographer's licence; and how to cite an Internet Archive leaf.
- **Commons citations** still needed hand work in most frames; the
  question of how far `commons_media` should go is on korg 3478.
- **The 550–900 band** was tight for a few frames heavy with tables, and
  comfortable for most. No change is proposed.

### Connections, and the links asked for

- **64 connections are stored on nursing frames:**
  - 46 between nursing frames: 44 added at review by
    `.scratch/nursing/conns.py`, which requires the words each end
    supports in that end's own reading, and two from authors;
  - 13 into In the Blood;
  - one each into mathematics (`rose-diagram` → `normal-distribution`,
    Quetelet), chemistry (`wwi-nurses` → `chemical-warfare`, mustard gas
    in July 1917), computing (`farr` → `scheutz-engine`), ai
    (`mills-school` → `word2vec`, "father : doctor :: mother : nurse")
    and western-civ (`monastic-infirmary` → `scriptorium`, the Rule of
    Saint Benedict).
- **In the Blood, as asked, the strongest:**
  - wartime blood: `pearl-harbor` → `fractionation`, `mash` →
    `korea-blood`, `vietnam-nurses` and `repose` → `vietnam-blood`,
    `hospital-ships` → `whole-blood-wwii`;
  - the identity check: `bcma` → `lis` and `tube-typing`,
    `surgical-checklist` → `lis`;
  - HIV: `ward-5b` → `hiv-blood`;
  - the rest: `vital-signs` → `hales`, `red-cross` → `drew-plasma`,
    `staupers` → `segregated-blood`, `daughters-of-charity` →
    `bloodletting`.

  Of the thirty pending on 3470, those with a nursing frame to meet are
  made. The rest (bedside transfusion in 1818, Rh and obstetric care,
  home infusion, marrow transplant nursing) meet no frame of this
  subject, and are left until one exists.

- **Left unmade, because no reading on either side states the link:**
  - chemistry's antiseptics and anesthetics: Lister's carbolic came from
    coal tar, which `mauveine` also names, but that is a shared name, not
    a connection;
  - western-civ's Crimea: it has no such frame;
  - computing's records: `bcma` → `minicomputer` through MUMPS was
    weaker than the blood links it made.
- **Density** (`names.py density`), after:

  | Subject     | Frames | Marks per frame | Connections per frame |
  | ----------- | -----: | --------------: | --------------------: |
  | ai          |     66 |           11.24 |                  1.17 |
  | blood       |     62 |            7.10 |                  1.63 |
  | chemistry   |     66 |            7.73 |                  2.18 |
  | computing   |     70 |           10.33 |                  1.37 |
  | feynman     |     62 |            8.65 |                  1.65 |
  | making      |     68 |            7.21 |                  1.22 |
  | mathematics |     65 |            7.71 |                  2.29 |
  | nursing     |     64 |            7.03 |                  1.00 |
  | physics     |     68 |            7.37 |                  3.32 |
  | western-civ |     24 |            7.04 |                  3.92 |

  The one nursing frame with no mark is the dedication, by design.

- **Western-civ's reach** (`names.py reach`), before and after: unchanged
  into every subject that existed before. Into nursing it is 1, 2 and 5
  frames in one, two and three steps. Nursing itself reaches 11, 29 and
  43 blood frames in one, two and three steps, and in three steps 20
  chemistry, 9 mathematics and 6 western-civ frames. It is In the Blood's
  companion, as its links say.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint,
  1,228 vitest tests (every subject loaded and validated, every SVG
  sanitised, every connection's frame and every mark's name found),
  `just tools-test`, and every mark spec with `--check --placed`.
- **Every content commit was validated on its own**, the index exported
  and the subject tests run on it.
- **Negative tests, each seen failing:**
  - the two `names.py` repairs' tests and `commons_media`'s span test,
    against the old code;
  - a duplicate accent planted in an author's copy (navy2, letin2);
  - the overlap measure found one scene, and then none;
  - `conns.py` refused a _why_ its readings did not support until it was
    reworded.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on the
  dev server, `.scratch/nursing/walk.mjs`):
  - `/nursing`: the start screen titled "Keeping Watch", with "care at
    the bedside, from infirmary to operating room" under it, and the
    subject in the start list with its subtitle; Enter to begin;
  - → through all 42 main-spine frames in plan order, with the right
    accent and HUD label at each; T into each of the four trails at its
    anchor, → through every trail frame, and Esc back to the anchor: 64
    stops, no mismatch;
  - Home and End reach CITY. and the dedication's name; a deep link to a
    trail frame (`/nursing/navy-pow`); no broken images, console errors or
    failed requests, and no horizontal overflow at 390px.
- **The counter overlap** (korg 3469), measured as before: one nursing
  frame overlapped at 1400×900 by 7 px; with its headline shortened, none
  does.

## Repaired in passing

- **`names.py mark`** wrote a frame's marks even when its spec named a
  name no file or draft held, though its README said it would not. It now
  leaves that frame unmarked (a test first, seen failing).
- **`names.py`'s bold check** missed the bold mention of an italic name,
  `**_Staphylococcus aureus_**`, so a mark landed on a passing mention
  with no warning. Fixed and tested. Its `--expect` item warning now says
  to keep a right item.
- **`commons_media`** wrote NARA's "between 1941 and 1945" as the exact
  year 1941. It is now a span, circa its first year, with the warning.
- **`skills/grow/reaching-sources.md`**: NHHC's certificate and
  User-Agent; _Navy Medicine_ and the CMH books on the Internet Archive;
  statutes from the Internet Archive and govinfo; court opinions;
  WHO IRIS's API; PMC's PDFs through the Wayback Machine; the OpenAlex
  budget; snippets of lending-only books; page drift in scans with
  plates; and sprint 030's refusals.
- **The skills**:
  - grow: citing a statute and a court opinion, a sculpture's
    photograph, an old anonymous photograph, and an Internet Archive
    leaf;
  - author-subject: the anchor in the brief's checking command, owner
    lists against earlier drafts, and accents taken mid-draft.
- **Seven shared names widened** from one subject's angle: `william-farr`,
  `rockefeller-foundation`, `yale-university`, `heroin`,
  `american-red-cross`, `difference-engine` and `world-health-organization`.

## Follow-ups

- **korg 3478**: eleven decisions from the authors' reports, among them a
  stand-in option, `--expect` for wiki_cite, citation kinds for statutes
  and opinions, and an OpenAlex key.
- The In the Blood links that meet no nursing frame stay listed on 3470's
  comment for a later frame (bedside transfusion, obstetric care, home
  infusion).
