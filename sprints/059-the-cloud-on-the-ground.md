# 059 — The Cloud on the Ground

## Goal

korg proposal 4898, covering korg 4897: the fourteenth subject,
`subjects/datacenters`, _The Cloud on the Ground_, "data centers: good,
evil, or something in between?". A friend asked Ken about the data center
controversy; most of what is on the web and social media is slanted one
way or the other, and Ken asked for a subject that gives both sides without
a bias and lets the reader decide. He asked in particular for the water
question to be settled from research: his understanding was that water is a
major issue only where data centers cool by evaporation in dry climates,
and that server liquid cooling is a closed loop, filled once. Started by
hand on kai from `main` at `5f89f8e8`.

## Decisions

- **The premise held** (checked at start): no data center subject existed,
  kloom is not in the cross-project plan index, and no grow branch was
  pending (`just grow-pending`, exit 0).
- **The title.** Ken's first thought was _Datacenters: Good or Evil?_,
  "…or something in between?", and he left it open. The subject is _The
  Cloud on the Ground_, subtitled "data centers: good, evil, or something in
  between?" (50 characters): a main title that names the physical thing
  without a verdict, and Ken's question kept whole in the subtitle. The id
  is `datacenters`, served at `/datacenters`.
- **Balance is the acceptance criterion.** Every contested frame steelmans
  both sides in their advocates' own terms, labels every number _measured_,
  _projected_ or _claimed_ (and its year), names who paid for an interested
  study, keeps loaded words inside quotations, says plainly when a
  measurement settles a claim from either side, and ends on what is not
  known. Each author reads their draft twice, as an opponent and as an
  advocate, and reports what each reading flagged. The hand frame
  `the-fight` sets out the scheme for the reader.
- **The before, recorded first** (`.scratch/059/density-before.txt`,
  `reach-before.txt`): a new subject has no reach before it; the others'
  densities are kept for the after.

### Shape

The plan is `create-tools/subject-plan/datacenters.json` (written by
`.scratch/059/mkplan.py`): 55 frames, 41 on the main spine and 14 in three
trails. The main spine opens with a hand-written section that frames the
argument, runs one dated section of history, then turns to the argument by
topic. Ken asked for no count; 55 matches the topic's depth, a little under
the 62 to 72 of the history subjects.

| Section             | Palette     | Frames | Label kind |
| ------------------- | ----------- | -----: | ---------- |
| The argument        | `hall`      |      2 | category   |
| Rooms for computers | `punchcard` |      8 | date       |
| Why we build them   | `ledger`    |      5 | category   |
| Power and the grid  | `current`   |      6 | category   |
| Water               | `tower`     |      5 | category   |
| The neighbors       | `parcel`    |      4 | category   |
| Who decides         | `chamber`   |      6 | category   |
| What comes next     | `horizon`   |      5 | category   |

| Trail           | Anchor             | Palette   | Frames |
| --------------- | ------------------ | --------- | -----: |
| Water, measured | `where-water-goes` | `tower`   |      5 |
| One county      | `zoning`           | `chamber` |      5 |
| Elsewhere       | `moratoriums`      | `chamber` |      4 |

### Theme

Four dark/light pairs, one palette per section (`.scratch/059/palettes.py`).
**No accent is green or red**, so no section is colored as good or bad.

| Palette   | Scheme | For                                | Ink  | Muted | Accent | Line |
| --------- | ------ | ---------------------------------- | ---- | ----- | ------ | ---- |
| hall      | dark   | the argument                       | 16.0 | 7.7   | 9.6    | 12.0 |
| punchcard | light  | rooms for computers                | 14.9 | 6.1   | 6.0    | 12.7 |
| ledger    | light  | why we build them                  | 15.0 | 6.5   | 6.2    | 13.0 |
| current   | dark   | power and the grid                 | 15.7 | 8.1   | 10.2   | 11.8 |
| tower     | dark   | water; Water, measured             | 15.9 | 8.0   | 10.0   | 12.0 |
| parcel    | light  | the neighbors                      | 14.9 | 6.6   | 5.8    | 13.2 |
| chamber   | dark   | who decides; One county; Elsewhere | 15.4 | 7.7   | 8.9    | 11.4 |
| horizon   | light  | what comes next                    | 15.3 | 6.4   | 5.9    | 13.3 |

The lowest contrast is 5.8:1, `parcel`'s accent.

### The hand frames

_The argument_, written by hand as the bar (commit `c781fddf`):

- `the-fight` (2026, EARTH., `asOf`): Gallup's first poll on local AI data
  centers (March 2026: 71% opposed, against 53% for a nuclear plant), its
  open answers as a table of each side's reasons, Heatmap Pro's October
  2026 poll (tax revenue the top reason for, bills the top reason against),
  the strongest case on each side, the partisan split, Data Center Watch's
  counts with its funder (10a Labs) and Exponent's caution, NIMBY as itself
  an argument, and how to read the subject's numbers.
- `inside-a-data-center` (Anatomy, BUILDING.): the four systems, the power
  and cooling chains (the indoor loop closed; heat rejection where water is
  consumed), PUE and WUE with Uptime's self-reported averages 2007–2025 as
  a chart from 1.0, Google's own 1.09, LBNL's modeled national average,
  rack power (69% under 10 kW; a GB200 NVL72 rack about 132 kW), and the
  national 176 TWh with the 2028 range.

What the hand frames found:

- **An industry count with a stake**: the PwC study for the Data Center
  Coalition counts 5.5 million jobs, under an expanded, function-based
  definition that reaches beyond NAICS 518210 (its Appendix B). Folded into
  `data-center-jobs`' brief.
- **An opposition count with a stake**: Data Center Watch is funded by 10a
  Labs, which works for AI companies; Exponent's engineers found its first
  report listed relocated projects as "blocked".
- **Polls moved fast**: Heatmap's 44% support in 2025 became over 70%
  opposition by 2026, so every opinion figure carries its month.
- **A tool crashed**: `commons_media search` died on a KeyError when a PDF
  in the results made Commons refuse the info query; repaired (below).
- **Commons holds AI-generated pictures of data centers**; the brief rules
  them out.

## Authoring at scale

Twenty-three authors, one per part of two or three frames, each a subagent
given the shared brief (`.scratch/059/brief.md`) and a paragraph of its own
(`.scratch/059/parts/`, written by `.scratch/059/mkparts.py` from the plan
and `.scratch/059/paras1.py`, `paras2.py`). Every name id the paragraphs
give was looked up before they went out (`.scratch/059/idcheck.jsonl`):
107 ids, of which the lookups changed eleven (xAI's Colossus is
`colossus-data-center`; NREL's article is now `national-laboratory-of-the-rockies`;
Ireland is `republic-of-ireland`; PFAS was already `pfas`; Liebert is a
disambiguation page; seven had no article and went to plain prose). The
plan's `owners` names 18 shared names. Twenty started at once, the
session's limit; the last three as the first finished.

- **Committed as each part could be**, in dependency order rather than the
  planned one: a part waited for its trail's anchor and for names it
  borrowed from parts still at work, and the first committer of a pair
  brought the other's draft in without `home` (`.scratch/059/commit.sh`'s
  `BORROW`). Twenty-five content commits, each validated on its exported
  index before it was made; none failed. The authors took 14 to 25 minutes
  each.
- **What it came to**: 55 frames, 45,568 words of prose (644 to 900 a frame;
  several contested frames sit at the 900 ceiling); 26 images, each looked at
  and none repeated in the repository, and none generated by AI; 18 charts;
  735 citations; 34 frames with `asOf`, since most of the subject describes a
  present that is still moving. Every accent is unique. The registry grew
  from 5,527 names to 5,770.
- **The paragraphs were wrong somewhere in nearly every part**, and the
  authors caught each by reading the source, the leads-not-sources rule
  holding for a tenth run. The largest: the Digital Gateway's rezoning was
  1,760 acres, not about 2,100, and the court that voided it ruled in August
  2025 on how the hearing was advertised; EO 14141 was revoked by EO 14318;
  Microsoft's 2026 pledge forgoes property tax _rate_ cuts, not tax breaks;
  no state has repealed a data center sales tax exemption outright; Chile's
  court ruling on Google was 2024, not 2020; Texas SB 6's disconnection rule
  is for customers connected after 2025, its 75 MW threshold for curtailment;
  the "Netflix hour = 4 miles of driving" figure was half an hour, and the
  driving comparison was the press's; Meta, not a Heatmap story, said it was
  re-evaluating its 2030 goal; Singapore's pause was never announced; and
  the USGS's thermoelectric share is 41% of all withdrawals, 34% of fresh.
- **Many leads had moved since they were written**, which is the risk of a
  live subject: LBNL's 2026 update (192 TWh in 2024), EPRI's 2026 range
  (9–17% by 2030), PJM's three capped auctions, Dominion's GS-5 class, the
  Senate's permitting bill (62–33, November 19, 2026), New York's and Texas's
  statewide pauses, Loudoun's November 2026 pause, Ireland's 2025 connection
  rule in the High Court, Germany's 2026 bill to ease its law, Singapore's
  Digital Infrastructure Bill, xAI's move to Southaven. Each frame gives the
  state as of November 2026.

## Balance

Balance was checked three times: by each author reading their draft as an
opponent and as an advocate; by four balance reviewers (`.scratch/059/
balance-brief.md`), each reading a third of the subject twice and allowed to
reword but not to change a fact; and by the lead reading the readings and
the reviewers' reports. The reviewers made wording edits in about thirty frames (a
claim attributed, a number given its kind, "acknowledged" made "said",
"drowned" made "flooded", the gas-plants headline "The grid's new plants
burn GAS." made "Much new firm power burns GAS.", efficiency-case's from a
general verdict to an eight-year finding), and judged every frame balanced or
balanced after edits, with these mild residual tilts, each for want of a
source rather than wording:

- `what-runs-there` gives supporters more room than critics (no named,
  sourced critic of the value of digital services was found);
- `bubble` gives the skeptics more room and the last word on circular
  deals (no supporter's reply to that point was sourced);
- `secrecy` and `federal-push` give the critics more room (the case for
  confidentiality and for federal speed is mostly made in one or two
  quotations).

Two figures differ by accounting rather than by error: the April 2026 tally
in `the-fight` ($725 billion, "up 77%", so about $410 billion for 2025) and
`bubble`'s table of what the four companies filed (about $360 billion for
2025, Microsoft's by fiscal year). Each frame says whose count it gives.

The lead fixed two: `bubble`'s 2026 total recomputed from its own table
(about $715 billion, not $700 billion), and `gigawatt-campus` given the
LBNL–Brattle reply that large loads spread fixed costs.

The authors added two labels the brief lacked, both now used throughout:
**estimated (modeled)**, for a model's estimate of the past (LBNL's national
totals, Masanet et al.), and **company-reported**, for a firm's own metered
or computed figures. A figure read off a source's chart is "our reading of
its figure".

### Names and connections

- **Names**: 243 new, every Wikidata id from `names.py lookup`. Homes set on
  registry names this subject is chiefly about: `cooling-tower`,
  `water-usage-effectiveness`, `diesel-generator`, `district-heating`. Names
  the authors reported as written from another subject's angle (`google`,
  "which built the TPU and the transformer"; `microsoft`, "maker of MS-DOS and
  Windows"; `meta-platforms`, "maker of the Llama models"; `amazon-company`;
  `llama-language-model`; `epoch-ai`; `deepseek`, which takes its own cost
  claim as given) are listed for widening below, not widened here.
- **Connections**: 122 stored, 94 within the subject (71 added at review from
  the authors' lists, each why checked against a reading) and 28 to other
  subjects: 8 to computing, 7 to ai, 6 to physics, 3 each to western-civ and
  chemistry, 1 to food. None to biology, blood, nursing, making, mathematics,
  music or feynman: the subject's arc does not cross them.
- **Density** (`.scratch/059/density-after.txt`): 546 marks on 312 names, 9.93
  a frame; 2.22 connections a frame.
- **Reach**, in one and two steps: the subject reaches 7 and 11 of computing's
  70 frames, 3 and 12 of physics's, 4 and 6 of ai's, 3 and 11 of
  chemistry's; western-civ reaches 3 and 15 of its 55.

### What the tools and skills assumed

- **The skills say nothing about balance.** Every author said so, as the
  brief expected. Folded into the grow skill as §A contested subject (the
  labels, funders, neutral words, the two readings, measured beats claimed)
  and into author-subject as a balance review step.
- **Web searches are a budget shared by every subagent in a session** (200 a
  turn), and it ran out partway through nearly every part. Authors fell back
  to fetching known URLs and the Wayback Machine. Folded into author-subject:
  the brief names primary URLs and warns of the budget.
- **Sources the authors found routes to**, folded into
  `reaching-sources.md`: SEC EDGAR (refuses a User-Agent without an email,
  which kloom's rules forbid: use companies' investor pages or reported
  filings), FERC (403; Wayback CDX finds statement pages), Virginia's SCC and
  legislature, Municode and DEQ (bot checks), county ArcGIS feature services
  and Census TIGERweb (open, measured), Epoch AI's data CSVs (CC BY),
  OSTI's purl links for NREL reports, USGS's publication service, the EU press
  corner's JSON, JLARC's report PDFs.
- **Left for a decision** (below): citations for things the schema does not
  yet hold.

## Verification

- `just check` is green (run after the last commit).
- **Every content commit was validated on its own**, the index exported and
  the subject tests run on it.
- `just scene-fit datacenters`: 0 misfits in 55 frames at 1280×800,
  1400×900 and 390×844.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on the dev
  server, `.scratch/059/walk.mjs`): the start screen titled "The Cloud on the
  Ground"; → through all 41 main-spine frames with the right accent and HUD
  label at each; T into each of the three trails at its anchor, → through
  every trail frame and Esc back: 55 stops, no mismatch; Home and End reach
  EARTH. and OPEN.; a deep link (`/datacenters/cooling-tower`); no broken
  images, console errors or failed requests, and no horizontal overflow at
  390px; the subject list shows "Cloud on the Ground" (a leading "The" is
  dropped in the list by design, sprint 047).

## Repaired in passing

- **`commons_media search`** asked Commons for every result's image info at
  once, and one PDF among the results (a gazette Commons could not size a
  thumbnail of) made the API refuse the whole query; the tool died on a
  `KeyError`. It now asks only for image files and says an API error
  plainly (`8bdd326d`, two tests seen failing first).
- **Two mark specs** reformatted by Prettier (`afc953e5`).

## Decisions for Ken

- **Publishing**: datacenters is not in `publish.json`, so the public reader
  site will not carry it until Ken adds it. It is the subject most likely to
  date: 34 frames carry `asOf` 2026-11-22.
- **Keeping a live subject current**: the frames on Memphis, the Digital
  Gateway, Loudoun's pause, federal policy, Ireland's court case and
  Germany's bill describe November 2026. Whether to schedule a review
  (korg schedule) or leave it to grow and reader notes is Ken's call.
- **Citation forms the schema lacks**, each worked around with `note`: a
  gazette cited by issue number with no page (the Bundesgesetzblatt since
  2023, the EU's L series, the Staatscourant); a slip court opinion with no
  reporter yet; an executive order (cited as `statute` with its Federal
  Register page); a county ordinance amendment; a state code section with no
  session-law chapter; a dataset (Epoch's CSVs); a report marked "Commission
  draft"; `number` on a `web` citation.
- **Map data in plates**: two plates embed public geometry in their modules
  (Census TIGER and Prince William's ArcGIS layers; OpenStreetMap, ODbL, with
  its credit in the plate and the frame). `coastlines.py` covers coasts only;
  whether rivers, roads and boundaries get a shared module like it is a
  design choice. Two abroad plates draw schematic coasts, labeled so, for
  want of `singapore-johor` and `netherlands` regions.
- **Names to widen** (listed above): the descriptions of Google, Microsoft,
  Meta, Amazon, Llama, Epoch AI and DeepSeek were written from the AI and
  computing subjects' angle and say nothing of their data center business.
- **Tool features the authors asked for**: a pageless `gazette`; `names.py
drafts` with an exit status for one part; `subject_plan --check --accents`
  failing only on one's own clashes; `contact_sheet` flagging a label a
  construction line crosses; `bar_chart`'s `display` keeping the unit;
  `mark --check` hinting at italics when a spec's words miss a title.
- **The 900-word ceiling** bound several contested frames, which give each
  side's case, its reply, the measurement and the open question; whether
  contested frames may run to 1,000 is a content-model decision.

## Deployed

On 2026-11-22 at 19:00 UTC, `just deploy` ran on kai from merged `main` at `cdccacec` (PR #70). The service is `tailscale serve` on :4890, and content is on the same commit. Its own checks passed: the tailnet and ssh doors, write gating, reader data and notes kept from an anonymous read, library frames, and compression.

Checked live:
- `/datacenters`, `/datacenters/where-water-goes` and `/datacenters/open-questions` all return 200, and the water frame renders its headline.
- `/api/stats` lists *The Cloud on the Ground* with its subtitle: 55 frames (14 on its 3 trails), 26 images, 18 charts, 735 citations and 122 connections. It counts 51,062 words, against the 45,568 above, because it counts table text and captions too.

The public reader site is unchanged: the subject is not in `publish.json`, which is a decision for Ken.
