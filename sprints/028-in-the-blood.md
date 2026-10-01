# 028 — Ninth subject: In the Blood

## Goal

korg proposal 3468, covering korg 3466: the ninth subject, _In the Blood_,
subtitled "what we believed, what we learned, how we use it", built around
Ken's father's career in Army blood banking and laboratory medicine. Its
five-part arc runs from beliefs and misconceptions, through what was
learned and transfusion, to modern uses and the laboratory bench, manual
to automated. The automation frames show the manual procedure itself, not
only the machine that replaced it. It is the first subject written with
the author-subject skill since sprint 027 tuned it.

## Decisions

- **Premises held** (checked at start). The subject depends on korg 3399
  (connections, sprints 017–019), 3465 (the subtitle, sprint 026) and 3461
  (the tuning, sprint 027), and all three had shipped. The nursing subject
  it should link to (korg 3470) is not written, so those links are
  recorded as pending (below). kloom is not in the cross-project plan
  index.
- **Ken's answers at the start (2026-10-01):**
  - the branch is `028-in-the-blood`;
  - his father will not review the frames before they ship, so accuracy
    rests on the sources alone;
  - the dedication frame carries Ken's own text, which he drafted. It was
    checked for spelling and grammar, he approved the corrections, and he
    kept "Dad" capitalised as his own usage;
  - the Medical Service Corps insignia is traced as outlined letters (the
    mid-grey line tones only).
- **The id is `blood`**, served at `/blood`.
- **The before, recorded first**: `names.py density` and `names.py reach
western-civ --steps 3` before any frame (`.scratch/blood/density-before.txt`,
  `reach-before.txt`). Western-civ then reached 6 ai, 12 computing and 14
  feynman frames in two steps (32 of the tech cluster's 198, the same as
  after sprint 026), and 18 making frames.

### Shape

The plan is `create-tools/subject-plan/blood.json`: 40 main-spine frames
and four trails of 22, 62 in all, each with its topic, sort and palette
checked by `subject_plan.py --check` before any author started.

- **Five `date` segments, each starting time again**, then two `category`
  segments:

  | Segment                           | Frames | Years       |
  | --------------------------------- | -----: | ----------- |
  | What we believed                  |      3 | 400 BC–1242 |
  | What we learned                   |      7 | 1628–1959   |
  | Transfusion                       |     10 | 1665–1950   |
  | What we do with blood             |     10 | 1941–1999   |
  | The bench, by hand and by machine |      8 | 1852–1990   |
  | Today                             |      1 |             |
  | Dedication                        |      1 |             |

  The bench is a main-spine segment, not the trail the proposal floated,
  because the work item makes it the later frames' focus. Its dates
  overlap the transfusion and modern segments', which a segment that
  starts time again allows.

- **Four `date` trails:**

  | Trail             | Anchor            | Frames |
  | ----------------- | ----------------- | -----: |
  | What we got wrong | `humours`         |      5 |
  | Beyond ABO        | `abo`             |      5 |
  | Blood at war      | `robertson-depot` |      6 |
  | Clotting          | `cryoprecipitate` |      6 |

  The proposal's Landsteiner → Rh → Coombs line runs on the main spine,
  since every reader needs it in order. The trail from `abo` takes the
  groups found after it (Lattes's stains, Bernstein's alleles, Kell, Duffy
  and Kidd, the Bombay phenotype, HLA).

- **Every reading shows how we knew, or how it was done**: the
  experiment, the argument, or the procedure, step by step with its
  numbers. For the bench and blood-bank frames that is the frame's point.
- **The voice** is the collective "we" of the other subjects.
- **The dedication is the last frame on the spine**, as Ken asked: "Dedicated
  to Colonel Joel T. Hiatt, USA", in maroon, the Medical Service Corps'
  branch colour, with Ken's text as its reading.

### Theme

Six dark/light pairs, each tied to a part of the story:

| Palette | Scheme | For                               | Ink  | Muted | Accent | Line |
| ------- | ------ | --------------------------------- | ---- | ----- | ------ | ---- |
| humour  | dark   | belief and misconception          | 15.1 | 7.7   | 8.3    | 11.3 |
| vellum  | light  | belief and misconception          | 14.8 | 6.6   | 5.5    | 12.8 |
| anatomy | dark   | what we learned                   | 15.0 | 7.8   | 7.4    | 11.4 |
| folio   | light  | what we learned                   | 15.0 | 6.3   | 6.6    | 12.3 |
| vein    | dark   | transfusion and blood groups      | 15.4 | 8.0   | 5.9    | 11.4 |
| plasma  | light  | transfusion and blood groups      | 15.0 | 6.8   | 7.0    | 13.1 |
| cryo    | dark   | modern uses, screening, clotting  | 15.2 | 8.2   | 10.1   | 11.9 |
| ward    | light  | modern uses, screening, clotting  | 15.1 | 6.5   | 6.1    | 12.3 |
| bench   | dark   | the laboratory                    | 15.3 | 8.1   | 10.1   | 11.8 |
| slide   | light  | the laboratory                    | 15.6 | 7.2   | 7.2    | 13.2 |
| maroon  | dark   | military blood and the dedication | 14.2 | 8.8   | 13.5   | 11.6 |
| branch  | light  | military blood and the dedication | 16.1 | 7.9   | 9.9    | 14.6 |

The lowest contrast is 5.5:1, against a floor of 4.5
(`.scratch/blood/palettes.py`). The blood reds took care: `vein`'s accent
(#f0605e on #170d0f) is 5.9:1, and `plasma`'s (#a3161f on straw) 7.0:1.
`maroon` is a deep maroon ground (#3d0f17) with silver accent; its light
counterpart `branch` puts the branch maroon (#800000) on white as the
accent.

### The first segment, by hand

What we believed has three frames:

- `humours` (c. 400 BC): _On the Nature of Man_ read in Jones's Loeb
  translation, with the author's own tests (a drug that draws phlegm, a
  wound, the same emetic given in four seasons, worked as a table);
  Fåhræus's suggestion that the four humours were the four layers of
  blood left to stand (his 1921 paper and Haak's 2012 chapter are closed,
  so it is cited through the Humorism article with `citedIn`); Richet's
  "who has ever seen it?"; and the treatment that followed, evacuation.
- `galen` (c. AD 170): read in Brock's 1916 Loeb translation of _On the
  Natural Faculties_ III.xv: the experiment of the cut arteries that
  emptied the veins, the pits in the septum whose ends he admitted he
  could not see, and his bookkeeping of the vessels' sizes, worked as a
  table, with Brock's own note that the conclusion was right and the route
  wrong.
- `ibn-al-nafis` (c. 1242): West 2008 (read in full through the Wayback
  `id_` form) and Meyerhof's translations as West quotes them; the solid
  septum, the road through the lung and the predicted _manafidh_; the
  rediscovery in Berlin in 1924; and the open question of transmission,
  where Wikipedia's two articles disagree about what Alpago carried to
  Padua.

Each plate is drawn in `create-tools/draw-plates/blood_belief.py`: a
glass of settled blood beside the square of qualities, Galen's two
systems with the septum's pits, and the heart with a solid septum and the
road through the lung.

**What writing them found:**

- **PMC and Europe PMC now refuse a script.** The PMC site answers with a
  reCAPTCHA page and Europe PMC's PDF renderer with a Cloudflare
  challenge, both as HTML that the PDF reader rejects. The REST API still
  answers, and a publisher's page through the Wayback `id_` form read a
  paper in full. This matters most for a biomedical subject, so the brief
  says it and `skills/grow/reaching-sources.md` now does (repaired in
  passing).
- **A Wikidata ID typed from memory was wrong**: a name draft for
  pulmonary circulation carried Q645187, and `lookup` gives Q494603. `add
--check` passed it, because it checks the registry, not the item. The
  brief now says it, and every author takes IDs from `lookup`.
- **The Institute of Heraldry's DoD certificate chain** needs `curl -k`,
  noted beside the other broken chains.

### The dedication

`dedication`: the frame Ken specified on korg 3466. Its plate places two
official drawings rather than computing one (`blood_dedication.py`), since
a hand-drawn first pass had looked wrong to him:

- the colonel's eagle is the Defense Logistics Agency's drawing (Commons,
  `File:US-O6 insignia.svg`, public domain), its silhouette stroked and its
  detail filled with `currentColor`;
- the Medical Service Corps insignia is The Institute of Heraldry's image
  13862, traced by `create-tools/trace-art/msc_insignia.py` (potracer,
  pure Python, `uv run`) on the mid-grey line tones only, so the M and S
  show as outlines. The first trace came out inverted (potracer traces the
  pixels that are false), and was fixed in the script.

The plate is about 108 KB, against about 6 KB for a computed one; the
trace itself is 33 KB of path data, less than the 200 KB the comment
estimated.

**Ken's revision (korg 3475, 2026-10-01).** On reviewing the frame Ken
asked to bring it closer to his mockup:

- the name and rank in mixed case, between a smaller "Dedicated to" above
  and a "Retired" directly below, which the nursing subject will need too;
- a single line under it, "MEDICAL SERVICE CORPS · UNITED STATES ARMY";
- the two insignia side by side;
- and not the mockup's differently coloured comma.

The scene set every headline in large capitals, so this needed the engine.
It is a scene kind any subject may use, not a page for this one: an
optional `scene.dedication` of `{kicker, name, note?}`. When present, the
scene shows it in place of the headline and the metadata beneath it, and
the narrative's heading reads "Dedicated to Colonel Joel T. Hiatt, USA,
Retired". The headline and accent stay, because the contents, the map and
the spine's screen-reader label still name the frame by them. It is
validated (a test first, seen failing) and recorded in design.md §Content
model. The plate is redrawn with the eagle and the branch insignia side by
side on one line, each named beneath, as the mockup has them; checked at
1400×900 and at 390 px, with no overflow.

### Authoring at scale

- **Eighteen authors in parallel**, each a subagent with a shell and the
  web, given a shared brief (`.scratch/blood/brief.md`) and a paragraph of
  its own (`.scratch/blood/part-*.md`): frames in order, each with its
  topic, label, sort and palette quoted from the plan, at most about five
  must-tell points, who owns a shared story or name, and connection
  candidates, trails included. The brief carried the new PMC refusal and
  said its facts were leads, not sources. Three anchors (`abo`,
  `robertson-depot`, `cryoprecipitate`) were finished first by their
  authors.
- **Review, per part, as each reported:** `.scratch/blood/review.sh` (a
  copy with every author's drafts: completeness, the subject tests with
  the marks placed, word counts, accent, topic and image clashes), a
  contact sheet of the plates and charts, the report's unsure claims, and
  the readings that carry the most risk read in full (`tube-typing`,
  `segregated-blood`), then `.scratch/blood/commit.sh`: names added, marks
  placed, staged with `stage_segment.py`, the exported index tested before
  every commit. Twenty content commits; none failed its index check.
  Parts whose trail anchor had not landed waited for it (groups1, war1,
  war2, clot1, clot2); `.scratch/blood/borrow.py` added names a part's
  marks borrowed, without `home` when the owner's frame was not committed,
  and the owner's draft was applied with `add --update` when it was.
- **Fixed at review:** the Perutz plate's colliding labels; one image used
  in two frames (`lis` and `whole-blood-returns`, kept in the second); six
  headlines shortened so the counter clears the metadata at 1400×900
  (korg 3469's measure); twelve names given their `home` once the owner's
  frame landed.
- **What it came to:** 62 frames and about 56,700 words of narrative (206
  pages at 275 words a page); 67 images, each looked at before use and
  none repeated in the repository; 12 charts and 63 tables; 600
  citations; eleven frames dated with `asOf`; every accent unique; 312 new
  names (the registry has 2,822).
- **The brief was wrong in nearly every paragraph**, each caught by an
  author reading the source: Blundell's 1818 patient (a man with stomach
  cancer, not a postpartum case), the 1668 Paris "ban" (a condition),
  Malassez's chamber (Thoma's, 1881), a crossmatch of 1950 with an
  antiglobulin phase (it had none until later), Hünefeld's crystals (pig
  and human blood, not earthworm), Duffy on chromosome 1 (1968, not 1951),
  the 1944 airlift's solution (Alsever's, not ACD), Quick's plasma
  (oxalated), the 1968 sibling marrow graft (Good's; Thomas's was 1969),
  the Coombs test's spin (none in 1945). The leads-not-sources rule held
  for a fourth run. Thirteen name ids in it were also wrong or had no
  article, which the author-subject skill now says to check.
- **Accuracy where this reader will look first.** The bench and blood-bank
  procedures rest on the manuals that taught them: TM 8-227 (1951), the
  Air Force laboratory course (1978), the Army's MD08xx subcourses, the
  Fort Knox cryoprecipitate monograph (USAMRL 964, 1972) and the papers
  themselves (Coombs, Mourant and Race 1945 read from its scan). The
  military trail rests on Kendrick's and Neel's official histories, the
  2011 Joint Blood Program Handbook and the Joint Trauma System's
  guidelines. Where the Army's own sources disagree (bags in Korea, the
  ASBP's founding in 1952 or 1962), the readings give both.

### What the tools and skills assumed

Every author reported where the skills, the brief or a tool was wrong,
silent or in the way (raw notes: `.scratch/blood/findings.md`). Sprint
027's repairs held: no author was stopped by another's plate module,
`mark --check` exited 0 for everyone, and the citation forms for
translations, letters, abstracts and second-hand sources were used
without trouble. What recurred or was new:

- **Sites refusing a script** grew worse for biomedicine: PMC and NCBI
  Bookshelf now answer with a reCAPTCHA, Europe PMC's renderer with
  Cloudflare. The authors found routes round nearly every refusal
  (Wayback copies of the renderer and of publishers' PDFs, PubMed's
  E-utilities, NLM's Profiles in Science OCR, the Internet Archive's
  journal runs). `reaching-sources.md` now carries them all.
- **`mark --check` buried an author's own warnings** under every other
  author's stale drafts (four authors). Repaired.
- **Two drafts directories holding one id** let the last win silently, and
  a draft lost its `home`. Repaired.
- **Commons metadata** still needed hand work (organisations split into
  names, the Google Art Project's template text, a date span written as a
  day). Repaired in the tool; what is left is on korg 3473.
- **The brief's own faults** (mine): name ids not looked up, two frames
  left to open from one event (`hiv-blood` and `hemophilia-hiv`), a dead
  history site named as the source for the Army's histories. The
  author-subject skill now says to look ids up and to settle frames that
  share an opening event.
- **Marks typed by hand** recurred in three first drafts, all caught by
  their authors; whether to change what the brief shows them is on korg 3473.
- **The 550–900 band** was tight for about half the authors and
  comfortable for the rest; no change proposed.

### Connections, and the links asked for

- **88 connections are stored on blood frames**: 68 between blood frames
  (about 65 added at review from the authors' reports by
  `.scratch/blood/conns.py`, which refuses one whose terms neither reading
  holds) and 20 into other subjects: 15 chemistry, 2 mathematics, 2
  physics, 1 computing. Two of the chemistry ones join the hand-written
  `humours` to `four-elements` and `jabir`.
- **The links the work item asked for:**
  - chemistry, the strongest as expected: `stained-film` → `mauveine`
    and `salvarsan`, `perutz-hemoglobin` → `crystallography` and
    `protein-structure`, `hales` → `fixed-air`, `nat` and
    `royal-hemophilia` → `pcr`, `autoanalyzer` → `enzymes` and
    `wohler-urea`, `blood-bag` → `polymers`, `galen` → `paracelsus`,
    `whole-blood-wwii` → `penicillin`;
  - physics: `hemoglobin` → `spectra` (the spectroscope), and
    `hemoglobin` → `energy`, found at review: Mayer's conservation of
    energy began with the colour of the blood he let in the tropics;
  - computing: `lis` → `minicomputer` (MUMPS at Massachusetts General);
  - mathematics: `louis-numerical` → `large-numbers` (Gavarret's
    Poisson bounds), `forensic-typing` → `bayes` (Essen-Möller's
    probability of paternity).
- **Left unmade, because no reading on either side states the link:**
  western-civ (it has no medical frame, and no reading names Galen,
  Harvey or the humours), making (no frame on instrument making touches a
  blood apparatus), physics' centrifuge and Coulter principle (physics has
  no frame on either), and computing's IBM (the apheresis reading names
  IBM's engineer, which is a shared name, not a connection).
- **The nursing subject (korg 3470)** is not written, so its links are
  pending: about thirty, from bedside transfusion and the identity check
  to wartime nursing and home infusion, are listed in a comment on 3470
  for that sprint to make from its side.
- **Density** (`names.py density`), after:

  | Subject     | Frames | Marks per frame | Connections per frame |
  | ----------- | -----: | --------------: | --------------------: |
  | ai          |     66 |           11.24 |                  1.15 |
  | blood       |     62 |            7.10 |                  1.40 |
  | chemistry   |     66 |            7.73 |                  2.17 |
  | computing   |     70 |           10.33 |                  1.36 |
  | feynman     |     62 |            8.65 |                  1.65 |
  | making      |     68 |            7.21 |                  1.22 |
  | mathematics |     65 |            7.71 |                  2.28 |
  | physics     |     68 |            7.37 |                  3.31 |
  | western-civ |     24 |            7.04 |                  3.88 |

  The one blood frame with no mark is the dedication, by design.

- **Western-civ's reach** (`names.py reach`), before (recorded at the
  start) and after: unchanged into every subject that existed before
  (ai 6, computing 12, feynman 14, making 18 frames in two steps); into
  blood, 0 in one step, 5 in two and 13 in three. In two steps blood
  itself reaches 30 chemistry, 8 mathematics, 6 physics, 6 western-civ, 5
  making, 3 computing and 1 feynman frame: it is a chemistry-side
  subject, as its links say.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint,
  1,130 vitest tests (every subject loaded and validated, every SVG
  sanitised, every connection's frame and every mark's name found), `just
tools-test`, and every mark spec with `--check --placed`.
- **Every content commit was validated on its own**, the index exported
  and the subject tests run on it.
- **Negative tests, each seen failing:** the four tool repairs' tests
  against the old code (`names.py`'s scoped warnings, `subject_plan.py`'s
  duplicate-draft warning, `wiki_cite.py`'s per-language file, and
  `commons_media.py`'s organisations, titles and spans); the draft check
  caught a Wikidata ID typed from memory (Q645187 for pulmonary
  circulation, which `lookup` gives as Q494603); the review's image check
  caught one image in two frames; the overlap measure found six scenes and
  then none.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on the
  dev server, `.scratch/blood/walk.mjs`):
  - `/blood`: the start screen titled "In the Blood" with "what we
    believed, what we learned, how we use it" under it, and the subject
    in the start list with its subtitle; Enter to begin;
  - → through all 40 main-spine frames in plan order, with the right
    accent and HUD label at each; T into each of the four trails at its
    anchor, → through every trail frame, Esc back to the anchor: 62 stops,
    no mismatch;
  - Home and End reach FOUR. and the dedication's USA.; a deep link to a
    trail frame (`/blood/bombay`); no broken images, console errors or
    failed requests, and no horizontal overflow at 390px.
- **The counter overlap** (korg 3469), measured as before
  (`.scratch/blood/overlap.mjs`): six blood frames overlapped at
  1400×900 by 7 px; with their headlines shortened, none does.

## Repaired in passing

- **`skills/grow/reaching-sources.md`**: PMC, Europe PMC's renderer and
  NCBI Bookshelf refusing a script, and every route the authors found
  round them; government and military sources (manuals and DTIC, the Army
  histories' new home, Profiles in Science, govinfo, the eCFR, FDA
  inserts, the Joint Trauma System); the Internet Archive's journal runs,
  page lookup, lending-only books and wrong metadata; Wayback rate limits
  and truncated captures; `curl -m`; and sprint 028's refusals.
- **`names.py mark --check`** names only the stale drafts the specs being
  checked mark, and counts the rest.
- **`subject_plan.py --complete`** warns when two drafts directories hold
  one id differently.
- **`wiki_cite.py --lang`** writes `<Title>.<lang>.txt`, so another
  language's text no longer overwrites the English.
- **`commons_media.py`** writes an organisation as a `name`, drops the
  Google Art Project's link and template text, and writes a date span as
  circa its first year, with a warning.
- **The author-subject skill**: look up every name id a brief gives; name
  the frame that tells an event two frames open from; apply an owner's
  draft when a borrower's reached the registry first. **The grow skill**:
  "in our translation", the practice of twelve readings in four subjects.
- **The dev server would not start**: its file watcher reached the
  system's limit on `.scratch`, where the authors' checking copies of
  every subject (over half a million files) sit. `vite.config.ts` now
  ignores `.scratch`, which nothing serves.
- **Eight shared names widened** from one subject's angle (Haldane,
  Göttingen, Paris, Poisson, Toronto, Stanford, the Office of Naval
  Research, Cambridge); `blood-tx2`'s mark spec formatted.

## Follow-ups

- **korg 3473**: what the authors reported that needs a decision: four
  citation forms (first paragraph only, a record with no URL, a diary, a
  mirror-only source; and JSTOR's DOIs), the draft-checking path,
  contact sheets for many plates, `commons_media` and `lookup` gaps, typed
  marks, and naming owners under rolling commits.
- **korg 3470** carries the nursing subject's pending links.
- The dedication's accent word, "USA.", no longer shows on the scene: the
  name now appears in place of the headline (korg 3475).
