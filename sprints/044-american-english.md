# 044 — American English throughout, as house style

## Goal

korg proposal 3528, covering 3521, run directly with `/start-sprint` after
3527 shipped. kloom's own words become American English: the UI labels and
copy ("Scene colours" becomes "Scene colors"), every subject's readings,
scenes, captions and name descriptions, and the rule in CLAUDE.md and the
skills, so new content is written that way. What kloom quotes keeps its
own spelling: quotations, block quotes, titles of works, proper names and
citation fields.

Ken's hard rule: **this is not a revision.** No frame gains an `edits`
entry, nothing new appears in the Changelog or as "new to you", and the
commit and PR are titled "style: American English, no content change".

## Premise, checked at start

- **3521 holds.** The settings still said "Scene colours" and "Reading
  colours", the User's Guide named them so, and the readings were mixed
  (fibres, nanometres and recognised in one DNA reading).
- **3527 shipped** (it was this sprint's dependency), so the sweep also
  covers the text it added (edit summaries, the Changelog's copy).
- **Nothing pending.** `just grow-pending` listed nothing, and kloom is not
  in the cross-project plan index.

## Decisions

- **A word list, never a rule.** `create-tools/spelling/american.py`
  changes a word only if `WORDS` holds it (about 10,600 forms, built from
  families: `organise` brings `reorganisation`). A pattern like "-ise → -ize"
  would have rewritten advise, surprise and exercise. Instead, a `suspects`
  command lists words that look British but aren't in the list, and the
  list grew by review. The one rule-based change is `haem` and `-aemia`,
  because the blood subject coins more compounds than a list holds
  (thalassaemia, immunohaematology).
- **What is not kloom's is masked, and the mask leans toward keeping.**
  - Block quotes and double-quoted spans are kept. That includes scare
    quotes ("live centre"), which can't be told from quotations by machine.
  - An italic with a capital in it is a title. An italic in lower case is a
    term kloom introduces (_tokeniser_, _flavours_), so it is respelled.
  - A capitalized word that does not start a sentence, a heading or a table
    cell is a name. Line breaks inside a paragraph don't start sentences.
  - KEEP lists names that turn up at a sentence start or in capitals on a
    scene: Ministry of Defence, Tyre, THE SCEPTICAL CHYMIST, ENCYCLOPAEDIA
    BRITANNICA.
  - COINED holds a word quoted as its coiner spelled it (Hedin's
    _haematokrit_).
  - Code, link targets, URLs and HTML are never touched. Neither are
    citations, a name's `name` or its aliases, or palette names.
- **A name mark on a common noun is respelled** (`[hemophilia](kloom:e/haemophilia)`),
  and `apply` respells its mark spec in `create-tools/names/examples` so
  `mark --check --placed` still finds it (32 specs). Ids never change.
- **Registry names by hand.** Nine names that are common nouns took the
  American form, with the British one moved into their aliases (each
  already had the American form as an alias): Aluminum, Cesium, Carbon
  fiber, Differential analyzer, Hemophilia, Hemophilia B, Injection
  molding, Meter, Postpartum hemorrhage. Proper names kept their spelling:
  Globe Theatre, Metre Convention, the Organisation for the Prohibition of
  Chemical Weapons, Tyre, the Boxgrove Palaeolithic site, _The Sceptical
  Chymist_.
- **`draughts` is not in the list.** It is the game (checkers) as often as
  drafts of air. The two name descriptions keep the game's name, and
  Ampère's "drafts" of air was respelled by hand.
- **Setting keys stay.** Only the labels changed. `kloom.scene` and
  `kloom.reading` are untouched, and settings live only in the browser, so
  readers' saved choices carry over on Ken's instance and the public site
  with no migration.
- **The `licence` field keeps its name.** The validator's two messages
  that name it now show it as code ("needs a `licence`"), so the gate skips
  it and an author still learns the field's name.
- **The gate covers content as well as UI.** `just check` runs `american.py
check subjects names src engine` (about a second). A grown frame written
  British is then caught at review; review-grown repairs it with `apply`,
  as wording with no `edits` entry.
- **Not swept:** docs (3521 calls them optional), code comments and
  identifiers (`coloursOf`, `colours-check`, the design doc's §Colours
  heading that code comments cite), and past sprint records. New writing
  follows the rule.

## What shipped

- `create-tools/spelling/`: `american.py` (`report`, `apply`, `check`,
  `suspects`), its README, and 18 tests (`test_american.py`) covering
  quotations, titles, names, marks, links, code, the JSON, SVG, Svelte and
  TS readers, and mark-spec respelling.
- Content: 2,669 words in 950 files across all ten subjects and the name
  registry (readings, scene words and SVG labels, topics, connections, name
  descriptions), 32 mark specs, 9 registry names, and Prettier's
  realignment of 54 readings' tables.
- UI:
  - Scene colors and Reading colors.
  - The map's "Center" buttons and its label "neighbors … Space centers".
  - The name card's "Organization" and the catalog-record citation note.
  - "minimize the window" among the reserved keys.
  - The User's Guide's wording.
  - Tests and `colours-check` follow the new labels.
- The rule:
  - CLAUDE.md (a rule, and this sprint's line).
  - docs/design.md §Spelling, with the labels updated where it names them.
  - `skills/grow` §The reading (the rule) and §Edits and corrections
    (respelling is never an edit).
  - `skills/review-grown` (`apply` is a wording repair), and
    `skills/review-notes` and `skills/author-subject` (not an edit).

## Verified

- `just check` green, with the spelling gate.
- The gate fails on a plant: "Scene colours" in `engine/settings.ts` and
  "The centre held." in a reading both made `check` exit 1, and it passed
  again once they were removed.
- Reproducible: on a clean HEAD worktree, `apply` produced exactly this
  branch's content, apart from the hand edits named above.
- No frame changed `edits`, `added` or `citations` (all 616 compared with
  HEAD).
- **The Changelog shows nothing new.** In a scratch clone, this diff was
  committed onto `main` as one squash-style commit. `gitAddedDates` gave
  byte-identical output before and after (27,552 bytes, all ten subjects),
  so neither the Changelog nor the "new to you" marks can move.
- `just scene-fit western-civ`: 0 misfits. The one scene line that grew was
  florence-dome's "WITHOUT CENTERING"; no SVG label grew.
- `just colours-check` 92/92 and `just keys-check` 70/70, after the label
  changes.
- Samples from two subjects (Keeping Watch and physics) were read before
  applying. So was every capitalized or all-caps hit, and the whole list of
  distinct respellings.

## Repaired in passing

- None outside the covered item.

## Follow-ups

- None filed. Publishing to the reader site waits on Ken, as 3527's did.

## Deployed

2026-10-03, `just deploy` (`.sprint-deploy`) to the service on kai from
merged `main` (`b6eb959`, PR #51). The content clone is on `b6eb959` too.
Every deploy check passed (both doors, write gating, reader data, the
library, compression). Checked live on :4891:

- the settings label reads "Scene colors";
- `western-civ/dna`'s reading serves fibers, nanometers and recognized;
- `/api/changelog` is as 043 recorded: 29 additions, the newest still
  `royal-society` (2026-10-02T22:49Z), and 4 edits. Nothing new.

The public reader site was not published; that waits on Ken.
