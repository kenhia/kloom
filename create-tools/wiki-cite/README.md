# wiki-cite

Prints kloom `wikipedia` citations for a frame's `citations` list, each
pinned to the article's current revision. Validation rejects a Wikipedia URL
without `oldid=`, because articles change.

```sh
python3 create-tools/wiki-cite/wiki_cite.py "Printing press" "Johannes Gutenberg"
python3 create-tools/wiki-cite/wiki_cite.py --accessed 2026-09-26 "Pantheon, Rome"
python3 create-tools/wiki-cite/wiki_cite.py --text .scratch/wiki "ENIAC"   # and save its text to read
```

- Output: a JSON list, one citation per title, in the order given. The
  `published` date is the revision's date, rendered "Last modified". The
  `accessed` date defaults to today.
- Redirects and title normalisation are followed, titles that land on one
  article give one citation, and the canonical title is
  used. A title cited as another article is named on stderr ("Leaded
  gasoline" is cited as "Gasoline"), since the article it lands on may be
  a wider thing, and `--text` saves the text under that article's name
  (sprint 025). A missing article, or a title that lands on a
  disambiguation page ("Gerhard Frey"), is named on stderr and left out,
  and the run carries on and exits 1 after the citations that were found
  are printed (sprint 027).
- `--lang de` cites another language's Wikipedia (`de.wikipedia.org`),
  and the citation carries `"language": "de"`, which validation requires
  of a non-English Wikipedia (sprint 027). Its `container` stays
  "Wikipedia, The Free Encyclopedia".
- Standard library only; it queries the MediaWiki API at
  `<lang>.wikipedia.org`. `test_wiki_cite.py` is its test (`just check`
  runs it; no network).

- `--text DIR` also writes each cited revision's readable text to
  `DIR/<Title>.txt` (headings, paragraphs, lists and table cells, without
  footnote markers), from the API's parse of exactly that revision (sprint
  015). A formula is written once, as its TeX between `$…$`, where its
  MathML used to come out a token to a line (sprint 027). With `--lang`
  the file is `DIR/<Title>.<lang>.txt`, so one person's German and English
  articles do not overwrite each other (sprint 028). Keep it out of
  the repo: `.scratch/` is ignored.

Read the revision you cite. The citation says you took the facts from that
text, so check the frame's claims against it (sprint 002 did, and the check
changed several).
