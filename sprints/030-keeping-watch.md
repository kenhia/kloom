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
