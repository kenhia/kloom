# 033 — Tune author-subject, third pass: Keeping Watch's findings

## Goal

korg proposal 3485, covering korg 3478: fold the ten decided findings of
_Keeping Watch_ (sprint 030, the second author-subject run after sprint
029's tuning) into the citation schema, the tools and the skills. Ken
decided items 1–10 on 2026-10-02 (the decisions comment on 3478); item 11,
the OpenAlex key, was done before the sprint (kloom#37). As for 027 and
029, everything is fixed here, even if it runs long.

Order of work, as the proposal set it: the citation schema (6, 7, 8) and
every subject re-validated; the tools (1, 2, 3, 4, 5, 9); the skill text
(5's owners, 7's line, 10's limits).

## Decisions

- **Premises, checked at start.** Items 1–7, 9 and 10 held. Item 6's
  inventory drifted: "Andersen v. Stability AI" is cited only as an NYU
  journal piece _about_ the case (ai/diffusion), so it stays `web`. Two
  more fit the shape: blood's two CFR subparts (apheresis, cryoprecipitate)
  and the EU AI Act's regulation (ai/governance). That makes 22 migrated
  rather than "about 20". Item 8 also drifted: a `doi` on a media citation
  already validated (seven charts carried one). What was wrong was its
  rendering. The entry linked the chart _to_ doi.org, as if the chart were
  there, so the work was to render the DOI as the data's and to have
  `bar_chart` emit it. kloom is not in the cross-project plan index.
- **The legal form.** A shared `LegalCite` (`{volume?, name, page?}`) is a
  case's `reporter` (all three required) and a statute's `code`. A case
  may give its `neutral` citation instead ("[2025] EWHC 2863 (Ch)", with
  no parenthetical, since it carries its year), and a `court` for the
  parenthetical when the reporter does not imply it ("Tex."). A statute
  takes `publicLaw` ("80-36"), `chapter` and `section`. One placement rule
  covers both Statutes at Large and codes: a session law's chapter and
  section come before a volume that has a page ("ch. 192, § 19, 31 Stat.
  748, 753"), and a code or a state's session laws, which have no page,
  take them after ("42 C.F.R. § 482.23", "2023 Or. Laws ch. 507"). The year
  is dropped when the name or the volume already says it (Bluebook's
  rule), which is why "Army-Navy Nurses Act of 1947, Pub. L. No. 80-36, 61
  Stat. 41" has none, and kept otherwise, as in Ken's example ("… 61 Stat.
  41 (1947)"). A pinpoint is written after a comma in `page` ("748, 753")
  rather than as another field. Neither kind takes `authors`: the
  validator refuses them, because the old citations put the court or
  Congress there. `container` and `publisher` now say where it was read,
  after the cite.
- **Pages were checked, not carried over.** The old citations gave the
  page each author read (753, 146). The legal form wants the act's first
  page, so the Statutes at Large text on the Internet Archive was read:
  ch. 192 of 1901 opens at 31 Stat. 748 and ch. 166 of 1908 at 35 Stat. 127. Act VII of February 1644/5 is on 1 Hening 291 (OCR lost the numbers
  of pp. 290 and 292, so the page was counted from the running heads).
  Public law numbers were written with their Congress (77-654, 77-828,
  78-238, 84-294).
- **A media DOI is the data's.** `citationHref` gives a media citation its
  `url` (the image's or the file's page), never the DOI. The DOI is
  rendered "Data: https://doi.org/…" before the access date, and appended
  to the caption credit as "data doi:…". So western-civ's printing-press
  chart now credits "kloom contributors / MIT / data doi:10.1017/…", and
  validate.test.ts was updated to match. Three charts whose `url` was a
  publisher's DOI page (NEJM twice, Wiley once) moved to `doi`.
- **Shared code lives in `create-tools/lib/`.** `article_check.py` holds
  the article check, the item check, `Title=keyword` parsing and `untex`,
  and both `names.py` and `wiki_cite.py` import it. This is the first
  shared module, so the create-tools README now has a line on where shared
  code goes.
- **Owners need parts the plan knows.** Keeping Watch's drafts
  directories are `navy2`, `letin1` and so on: parts are not segments. So
  a plan's frame entry may carry `part`, beside its topic, sort and
  palette, and `--check` accepts an owner only if it is a part a frame
  names. With no frame parts, a segment or trail id is accepted.
- **Wellcome's own creator field.** For two of the three Keeping Watch
  Wellcome files, the Collection's catalogue record is the _book_ the
  image is a plate from, and the API redirects to it. Its contributor is
  the book's author (Sarah Tooley for Mrs Wardroper's portrait), not the
  plate's maker. So a `Books` record puts the book in the container,
  writes no author, and names the book's author on stderr. Only a record
  of the image itself gives the author.
- **NARA's agency is the creator's last unit**, with the whole hierarchy
  said on stderr, so an author can name a parent instead ("Bureau of
  Special Services" is OWI's). A creator who is a person (the FDR
  Library's donor) is not written as the author.

## What shipped

**Citation schema (items 6, 7, 8).** `engine/citation.ts` gains the
`case` and `statute` kinds, `LegalCite`, `legalForm` and `legalText`, the
Sources line for both, their validation, `read: "record"` ("Read in its
catalogue record only."), the data DOI on media in the entry and in the
caption credit, and a media `number` after its container. There are seven
new tests in `citation.test.ts`. The migration covered 22 citations in ten
frames across four subjects, written by `.scratch/033/migrate_legal.py`,
which checked every old title before changing anything:

- 10 Acts of Congress (nursing): `statute` with `publicLaw` and/or
  `chapter`, `code`;
- 2 eCFR sections (nursing magnet, where-nursing-is), 2 CFR subparts
  (blood), and the EU AI Act (ai): `statute` with `code` and `section`;
- Oregon Laws 2023 ch. 507, and Virginia's Act VII of 1644/5 (making);
- 5 cases: Frank v. South, Ales v. Ryan, Sparger v. Worley Hospital, and
  Getty v Stability AI twice (neutral citation).

All ten subjects validate. The migrated citations were checked in the
reading pane, in both the Sources and Citations lists, on nurse-anesthetist,
nurse-rank, surgical-count, ai/diffusion and wood-screws, plus a chart's
"Data:" link on leaded-petrol. Case names are italic, statutes roman, and
the cite and its link are as above.

**Tools.**

1. `subject_plan.py --complete DIR --stand-in ANCHOR` (repeatable) writes
   a placeholder for a trail anchor into the copy only. It takes the
   plan's topic, sort and palette, and adds a one-line reading and a
   one-line drawing (the subject suite requires an illustration), with no
   marks, media or connections. It refuses without `--complete`, and for a
   frame no trail hangs from. It was proved on nursing with
   `rose-diagram` deleted: the copy's 800 subject and SVG tests pass. The
   README's hand recipe is gone.
2. `names.py lookup --expect` checks the article only, and
   `--expect-item` is the opt-in item check.
3. `wiki_cite.py --expect`, with `Title=keyword` in a batch for both tools.
   A mismatch warns on stderr, naming the article it landed on, and the
   run exits 1 after printing. Live, "Army Medical School=London" warns.
4. `commons_media crop --rotate 90|180|270`, clockwise, applied before the
   box. It is tested on a sideways fixture whose black corner must land at
   the upright top right.
5. `names.py drafts <subject>` lists the drafts (id, item, home, part). It
   exits 1 on a name drafted by two parts, one item under two ids, or a
   draft by a part the plan's `owners` does not give it to. It counts the
   drafts already in the registry. Live on nursing: 319 drafts, no
   problems (030 had resolved its doubles).
6. `subject_plan.py --check` validates `owners`.
7. (Item 8) `bar_chart.py` prints the media citation when its spec has a
   `source`, and refuses a source with no link or a doi.org link.
8. (Item 9) `commons_media` reads the file page's wikitext. For NARA,
   the series becomes the container, the agency the author, and NAID plus
   the local identifier the `number`. For the US Navy, the photographer
   comes from "photo by …" with rank and rate removed, the container is
   the NHHC, and the Navy image ID is the `number`. For Wellcome, the
   container is the Collection, the creator comes from its catalogue, and
   the image number is kept. Seven real Keeping Watch files are fixtures
   in `create-tools/commons-media/fixtures/`. A Commons file from anywhere
   else gets the same citation as before (Seacole/Challen checked live).

**Skill text.** grow SKILL: the `--expect`/`--expect-item` split and
wiki-cite's `--expect`; `case` and `statute`, replacing 030's
`chapter`/`web` advice; one line on `read: "record"` against `citedIn`;
the chart DOI; and the stand-in. reaching-sources.md: IA snippets are
supporting evidence only (corroborate or check a quotation, never a
frame's only source, never `key`; `read: "excerpt"` with a snippets
`note`; quote only what a snippet shows). author-subject §1 and §3: `part`
and `owners` in the plan, `names.py drafts`, `--expect-item`, and
`--stand-in` for trail parts. design.md §Citations: a "Forms from
_Keeping Watch_" block.

**Item 10 applied to the content.** The one IA-snippet citation,
navy-pow's "I Was on Guam", was `key`. It no longer is, and its note says
it was read through the snippets. Whether the Guam details that rest on it
alone (the straw mats, the "fourth-rate hotel") are re-sourced or cut is a
content call on Ken's mother's subject, not a mechanical one, so it is
korg 3487.

## The gate

`just check` is green: svelte-check with no warnings, prettier and eslint,
1,254 vitest tests (every subject validated under the new kinds), and the
tools' tests (lib 5, names 27, wiki-cite 6, commons-media 21, subject-plan
22, bar-chart 6, and the rest unchanged). As a negative test, a statute
stripped of `publicLaw` and `code`, and a case given `authors`, were
planted in nursing. The subject suite failed on both, naming the frame,
the citation and the fault, and both files were restored.

## Repaired in passing

- `create-tools/subject-plan/test_subject_plan.py` called `unittest.main()`
  above its last class, so running the file directly skipped
  `CompleteWithDrafts` (`just tools-test` uses discover, which ran it). The
  call is now at the end.

## Follow-ups

- korg 3487: navy-pow's Guam details that rest only on IA snippets. They
  need re-sourcing or cutting, a content decision (item 10 applied
  retroactively).

## Deployed

2026-10-02, to kai, by `just deploy` (`.sprint-deploy`) from merged `main`
`98042bf` (PR #39). The recipe's probes all passed: both doors read, the
tailnet door refuses anonymous writes and reader reads, a frame's body
comes from the library, and pages go compressed. The library was rebuilt
(`3a6ac9`). The service shows this sprint's work: nurse-anesthetist serves
_Frank v. South_ with its name in italics, nurse-rank serves "Pub. L. No.
80-36, 61 Stat. 41", and leaded-petrol's chart carries "Data:" in its
entry and "data doi:10.1289/EHP7932" in its caption.
