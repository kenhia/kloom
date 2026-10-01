# names

Names the people, places and things a subject mentions, for the shared name
registry (`names/`, docs/design.md §Connections). Six commands.

```sh
python3 create-tools/names/names.py lookup "Johannes Gutenberg" "Printing press"
python3 create-tools/names/names.py add drafts/ [--update] [--check]
python3 create-tools/names/names.py mark create-tools/names/examples/western-civ.json
python3 create-tools/names/names.py mark create-tools/names/examples/western-civ.json --check
python3 create-tools/names/names.py density
python3 create-tools/names/names.py reach western-civ
python3 create-tools/names/names.py strip blood/abo blood/harvey --out .scratch/hand
```

- **`lookup`** prints one JSON line per Wikipedia title: a slugged `id`,
  the `wikidata` item the article is about, its `name`, Wikidata's short
  description to start the name file's `description` from (rewrite it:
  one plain sentence on what it is and why it matters here), and the
  article's `first_line`. **Read both before you use the item**: a real
  article on a namesake passes every other check ("Hideo Kodama" is a
  politician, "Robin Forrest" a priest; sprint 026 met four), and
  `--expect WORD` warns, and exits 1, for each article whose description
  and first line lack WORD (`--expect printing`). A title that redirects
  says so in `redirected`, because the article it lands on may be a wider
  thing: "Project MAC" lands on CSAIL. Look such an item up on Wikidata
  itself (`wbsearchentities`), and check units and namesakes there too:
  "Horsepower" is not the metric horsepower. A title that lands on a
  disambiguation page, or a set-index page ("Sodium citrate", a list of
  compounds of one name, sprint 029), prints `ambiguous` and no item,
  rather than the page's own: choose the article meant and look that up.
  Each row also gives what Wikidata says the item is, `instance_of` (its
  classes) and `item_description`, and `--expect` checks those too: an
  article can be right while its item is something else ("Duffy antigen
  system" is a blood group's article whose item, Q205042, is the ACKR1
  protein; sprint 028 met it). Such an item may be the only one Wikidata
  has, as there; then keep it, and say so in the report. A
  title with no article prints `missing`. Ids spell a Greek letter ("π" is
  `pi`) and a bare number in words (Wikipedia's "0" is `zero`), since
  sprint 027.
- **`add`** writes name files (files, or directories of them) into the
  registry. A new name is written, tab-indented as Prettier leaves the
  repo's JSON. A name already there is left alone unless `--update`. A
  draft whose Wikidata item another file already holds is refused, naming
  that file: use its id instead. A malformed draft is refused too. If
  anything is refused nothing is written, and `--check` only reports: the refusals, or one line saying how many it would write (sprint 025, whose authors could not tell a pass from a no-op), and a second naming any draft it leaves alone because the registry already holds that id (sprint 026, where other authors' names landed mid-run).
- **`mark`** reads a spec, `{"<subject>/<frame>": [["words", "<name id>"],
...]}`, and marks each name's first mention in the frame's reading as
  `[words](kloom:e/<id>)`. The words are matched as the reading writes
  them, and may wrap across lines. A mention in a heading, a table row, an
  image's alt text or another link is skipped: the mark goes on the first
  one in prose, or the command names the pair it could not place and
  exits 1. A name already marked in the frame is left alone, so a spec can
  be run again. Write the words with any emphasis the reading gives them:
  a title in italics is `"_The Method_"`, and the mark keeps the
  underscores inside it, as `[_The Method_](kloom:e/…)`.
- **`mark`** says what it placed, per frame (`marked 8`), and the sentence
  each mark landed in, with the marked words in brackets. **`mark
--check`** changes nothing and says the same of every mark not placed
  yet ("8 marks would place", then each sentence): read them, because a
  mark lands on the first mention in prose, which may not be the one you
  meant. It warns when a mark would land before the reading's bold
  mention of the same words (a passing mention, a quotation, "Antimony"
  for "antimony", "electron" when the bold one is "**electrons**"):
  reword the reading, or make the spec's words the bold ones. Matching is
  whole words and exact case. `--root DIR` marks a copy of the subjects
  instead of the live ones, such as the one `subject_plan.py --complete`
  writes; wrapped words are written in the spec with a single space.
- **`mark --check` exits 0 when every mark is placed or would place**, and
  1 only on a problem: a mention it cannot find, a name no file or draft
  holds, or a mark in a frame the spec names that no spec in its
  directory lists (one typed by hand). Before sprint 027 "would place"
  exited 1 too, and fifteen of sprint 026's authors could not tell success
  from failure. **`--placed`** makes a mark not placed yet a problem as
  well: `just check` runs `mark examples/*.json --check --placed`, so the
  specs are the record of every mark and a hand-typed one fails the gate.
  `mark` takes several specs at once.
- **Every name a spec marks must be known**: a file in the registry
  (`--names`, by default `names/`) or in a directory of drafts not yet
  added (`--drafts DIR`, repeatable). Otherwise `mark` names it and exits
  1, rather than placing a mark the gate would refuse (sprint 021). An
  author checks with `--check --drafts .scratch/names/<subject>-<segment>`.
  A draft whose id or Wikidata item the registry already holds is named
  in a warning: another author's name reached the registry meanwhile, so
  drop the draft or mark the registry's id (sprint 025). Only drafts the
  specs being checked mark are named; other authors' stale drafts passed
  with `--drafts` are counted in one line, since naming them all buried an
  author's own warnings (sprint 028).
- **`density`** prints, per subject: frames, marks, distinct names, marks
  per frame, frames with no mark, connections stored on its frames and
  touching them (either end), and connections per frame. `--json` for one
  line per subject. The map's defaults are set from these (korg 3441).
- **`reach <subject>`** counts, for every other subject, its frames within
  one and within `--steps` (default two) connections of any frame of the
  subject. The graph is undirected, since a connection shows on both ends,
  and a path may run through any subject. Sprint 021 measured the Physics
  bridge with it: western-civ's reach into ai, computing and feynman,
  before and after. `--json` for one line per subject.
- **`strip`** prints frames' readings, `<subject>/<frame>` each, with
  every name mark taken out and its words left (`**[Harvey](kloom:e/…)**`
  becomes `**Harvey**`), or writes them to `--out DIR` as
  `<subject>-<frame>.md`. An author is given the hand-written frames this
  way, as the quality bar, so there is no mark to copy: three of sprint
  028's eighteen authors typed marks by hand after reading the marked
  frames, despite the brief's warning (sprint 029). `just check`'s `mark
--check --placed` stays the backstop.
- Standard library only. `lookup` queries en.wikipedia.org's API and
  Wikidata's with a project User-Agent, never a person's name. `test_names.py` is its test
  (`just check` runs it; it needs no network).

A name file (engine/names.ts has the rules):

```json
{
	"id": "johannes-gutenberg",
	"wikidata": "Q8958",
	"name": "Johannes Gutenberg",
	"aliases": ["Gutenberg"],
	"kind": "person",
	"description": "German goldsmith who brought movable-type printing to Europe around 1440.",
	"home": "western-civ/printing-press"
}
```

`examples/` holds the specs, the record of what was marked:
`western-civ.json` and `shared.json` (the things in two subjects: the IBM
701 and 704, Project MAC, the VAX, Bletchley Park, Hoff, Mead) from sprint
017, and `ai.json`, `computing.json` and `feynman.json` from sprint 018, and
`physics-<segment>.json` from sprint 021, one per author.
