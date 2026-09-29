# names

Names the people, places and things a subject mentions, for the shared name
registry (`names/`, docs/design.md §Connections). Four commands.

```sh
python3 create-tools/names/names.py lookup "Johannes Gutenberg" "Printing press"
python3 create-tools/names/names.py add drafts/ [--update] [--check]
python3 create-tools/names/names.py mark create-tools/names/examples/western-civ.json
python3 create-tools/names/names.py mark create-tools/names/examples/western-civ.json --check
python3 create-tools/names/names.py density
```

- **`lookup`** prints one JSON line per Wikipedia title: a slugged `id`,
  the `wikidata` item the article is about, its `name`, and Wikidata's
  short description to start the name file's `description` from (rewrite
  it: one plain sentence on what it is and why it matters here). A title
  that redirects says so in `redirected`, because the article it lands on
  may be a wider thing: "Project MAC" lands on CSAIL. Look such an item up
  on Wikidata itself (`wbsearchentities`), and check units and namesakes
  there too: "Horsepower" is not the metric horsepower. A title that lands
  on a disambiguation page prints `ambiguous` and no item, rather than the
  disambiguation page's own: choose the article meant and look that up. A
  title with no article prints `missing`.
- **`add`** writes name files (files, or directories of them) into the
  registry. A new name is written, tab-indented as Prettier leaves the
  repo's JSON. A name already there is left alone unless `--update`. A
  draft whose Wikidata item another file already holds is refused, naming
  that file: use its id instead. A malformed draft is refused too. If
  anything is refused nothing is written, and `--check` only reports.
- **`mark`** reads a spec, `{"<subject>/<frame>": [["words", "<name id>"],
...]}`, and marks each name's first mention in the frame's reading as
  `[words](kloom:e/<id>)`. The words are matched as the reading writes
  them, and may wrap across lines. A mention in a heading, a table row, an
  image's alt text or another link is skipped: the mark goes on the first
  one in prose, or the command names the pair it could not place and exits
  1. A name already marked in the frame is left alone, so a spec can be
     run again.
- **`mark --check`** changes nothing and exits 1 if any mark is missing:
  keep the spec as the record of what was marked, and check it after an
  edit.
- **`density`** prints, per subject: frames, marks, distinct names, marks
  per frame, frames with no mark, connections stored on its frames and
  touching them (either end), and connections per frame. `--json` for one
  line per subject. The map's defaults are set from these (korg 3441).
- Standard library only. `lookup` queries en.wikipedia.org's API with a
  project User-Agent, never a person's name.

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
017, and `ai.json`, `computing.json` and `feynman.json` from sprint 018.
