# 014 — Third subject: Richard Feynman

## Goal

korg proposal 3426 (Ken, 2026-09-28), covering korg 3397: the third subject,
and the first built around a person. Richard Feynman's life runs on a dated
spine, with deep trails for the physics, Los Alamos, computation and
Challenger. It is authored with sprint 006's method, which is first written
down as a reusable skill, so that this subject tests the skill. The proposal
also asks for rich readings, and for candidate links to the AI subject and to
a future History of Computing.

## Decisions

- **Premises held.** There was no `subjects/feynman` and no
  `skills/author-subject`. All seven create-tools the proposal names
  existed. kloom is not in the cross-project plan index.

### The method, written down (step 0)

- **`skills/author-subject/SKILL.md`** is the procedure, in five steps:
  1. plan, including the theme, the voice and the contrast check;
  2. write the first segment by hand;
  3. brief the parallel authors;
  4. review, validate and commit each segment;
  5. write the record.

  It is short on purpose. `skills/grow/SKILL.md` stays the style guide for
  every frame, and the new skill only orders the work around it.

- **The brief.** The one shared by every author is kept, with the plan, in
  the sprint's working notes. Its substance is in this record, in the
  sections below. Each author also got a paragraph naming its frames, their
  palettes, its plate module, and what the neighbouring frames cover, so
  that no two authors wrote the same story.

### Shape

- **A life on dated segments, and the depth in trails.** The plan is
  `create-tools/subject-plan/feynman.json`. Its 34 main-spine frames run in
  seven `date` segments:
  1. Far Rockaway, 1918–35;
  2. MIT and Princeton;
  3. Los Alamos;
  4. Cornell;
  5. Caltech;
  6. The wider world, 1969–85;
  7. The last years.

  A closing `category` segment, Afterlife, holds the legend and the legacy.
  It is a category because those two frames describe the reception, not
  events in the life.

- **Five trails, 28 frames:**

  | Trail              | Anchor               | Frames | Label kind |
  | ------------------ | -------------------- | ------ | ---------- |
  | Sum over histories | `thesis`             | 6      | technology |
  | The diagrams       | `diagrams`           | 6      | technology |
  | The Hill           | `los-alamos`         | 5      | date       |
  | Computing          | `simulating-physics` | 5      | date       |
  | The commission     | `challenger`         | 6      | date       |

  The two physics trails are labelled by idea, not date. Their frames
  explain one idea after another, so a year would be the wrong label.

- **Candidates not made trails.** Teaching and the Lectures stay on the
  main spine (`lectures`, `character-of-law`, `qed-book`). They are
  episodes of his Caltech years, and every reader should pass them. Bongos,
  safecracking and Tuva are split between the frames they belong to:
  - safecracking goes to The Hill;
  - drumming goes to `brazil` and `tuva`;
  - Tuva is a main-spine frame.

  Ten frames of anecdote would have been memoir, retold at length.

- **The voice is "he".** western-civ and ai use a collective "we". A
  life needs the third person ("He fixed radios by THINKING."). A frame
  about a thing may make the thing its subject.

### Theme

Three pairs of palettes, each the other's counterpart. Every ink, muted,
accent and line colour was checked against its background:

| Palette    | Scheme | For                              | Ink  | Muted | Accent | Line |
| ---------- | ------ | -------------------------------- | ---- | ----- | ------ | ---- |
| lamplight  | dark   | the life                         | 14.5 | 7.5   | 8.4    | 11.0 |
| manila     | light  | the life                         | 13.0 | 5.4   | 5.5    | 10.7 |
| chalkboard | dark   | physics and teaching             | 12.8 | 7.1   | 10.4   | 11.1 |
| graphpaper | light  | physics and teaching             | 15.0 | 5.9   | 6.1    | 12.1 |
| blueprint  | dark   | Los Alamos, Challenger, machines | 12.7 | 7.0   | 6.2    | 9.7  |
| vellum     | light  | Los Alamos, Challenger, machines | 14.5 | 5.8   | 5.8    | 11.1 |

The lowest contrast is 5.4:1, against a floor of 4.5.

### Accuracy and rights

- **His stories are his telling.** Frames that rest on the two memoirs say
  so in the reading. Claims of fact rest on documented sources where they
  exist: papers, the Nobel lecture, the Rogers Commission report, Caltech's
  archives and letters.
- **The AIP oral history** (Charles Weiner, 1966–73) is the best source for
  his early life. aip.org refuses fetches, so it was read through the
  Wayback Machine. Its terms forbid quoting without AIP's permission, so it
  is paraphrased everywhere and never quoted. It is cited by its own URL.
  The first draft of `least-action` quoted it, and the quotation was
  rewritten as a paraphrase before commit.
- **The Feynman Lectures** site blocks both fetches and the Wayback Machine.
  The Lectures are cited as the book, with the chapter's page URL.
- **Books** are cited by their Open Library work page, because a citation
  needs a URL.
- **Quotations** from anything still in copyright are a sentence at most.

### The first segment, by hand

Far Rockaway has three frames:

- `far-rockaway` (1918): his father, the encyclopedia and the dinosaur at
  the window;
- `radio-boy` (c. 1930): the laboratory, the radios, and the π in a tuned
  circuit;
- `least-action` (c. 1934): Abram Bader, and a worked example of the action
  of a thrown ball.

**What writing them found:**

- **An unsupported claim.** The draft said his father had wanted to be a
  scientist. None of the sources read said so, and it was cut.
- **Images need no caption line.** The page builds the credit from the
  `media` citation, which the AI frames already relied on. Three
  hand-written caption lines duplicated it and were removed (their facts
  moved into the alt text). The brief now says so.
- **The sources disagree about Columbia.** The usual story is its quota on
  Jewish students. Feynman in 1966 remembered only failing its entrance
  exam. `least-action` gives both accounts.
- **Spelling.** Weiner's transcript spells the teacher "Bater". The
  Lectures spell him "Bader", which the frames follow.
