# spelling

`american.py` keeps kloom's own words in American English (korg 3521,
sprint 044; docs/design.md §Spelling). What kloom quotes keeps its own
spelling, and the tool leaves it alone:

- quotations: block quotes, and "double-quoted" spans;
- titles of works: an italic with a capital in it (`_Notes on Nursing_`);
  an italic in lower case is a term kloom introduces, and is respelled;
- proper names: a capitalized word that does not start a sentence, a table
  cell or a heading (`Royal College of Nursing`, `Metre Convention`), and
  the phrases in `KEEP` (`Ministry of Defence` starting a sentence, or in
  capitals on a scene);
- citation fields, code, link targets, URLs and HTML.

It knows a word only from `WORDS`, a list built from families (`organise`
brings `organised`, `reorganisation`...). A spelling it has not been told
about is never changed; `suspects` lists the words that look British and
the list lacks, so it grows by review.

```sh
python3 create-tools/spelling/american.py report [paths]      # what would change; --skipped for what is kept, and why
python3 create-tools/spelling/american.py apply [paths]       # change it; respells mark specs with their marks
python3 create-tools/spelling/american.py check [paths]       # exit 1 if anything would change (just check)
python3 create-tools/spelling/american.py suspects [paths]    # British-looking words not in WORDS
```

Paths default to `subjects` and `names`; `just check` passes
`subjects names src engine`. What it reads in each file:

| File                | What is kloom's words                                                                            |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| `*.md`              | the prose, masked as above                                                                       |
| `frame.json`        | topic, position label, the scene's words, connections' `why`, edits' summaries; never citations  |
| `spine.json`, trail | section and trail titles                                                                         |
| `subject.json`      | title and subtitle                                                                               |
| a name file         | its description; never its name or aliases (a name's spelling is decided by hand, §Spelling)     |
| `*.svg`             | the words of each `<text>`                                                                       |
| `*.svelte`          | markup text, `aria-label`, `title`, `alt` and `placeholder`, and the script's prose strings      |
| `*.ts`              | prose strings: with a space in them, or a capitalized label; not comments, imports or `.test.ts` |

A JSON file is changed string by string, so its formatting stays as it
was. A Markdown table is not realigned: run Prettier on what `apply`
changed (`npx prettier --write <files>`) before `just check`. A name's mark on a common noun (`[haemophilia](kloom:e/haemophilia)`)
is respelled, and `apply` respells its entry in
`create-tools/names/examples` to match, so `mark --check --placed` still
finds it.

**A false hit** (a proper name at the start of a sentence, or a coinage
quoted as written) goes in `KEEP` or `COINED`, with a test.

Tests: `test_american.py` (standard library, no network), run by
`just tools-test`.
