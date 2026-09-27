# wiki-cite

Prints kloom `wikipedia` citations for a frame's `citations` list, each
pinned to the article's current revision. Validation rejects a Wikipedia URL
without `oldid=`, because articles change.

```sh
python3 create-tools/wiki-cite/wiki_cite.py "Printing press" "Johannes Gutenberg"
python3 create-tools/wiki-cite/wiki_cite.py --accessed 2026-09-26 "Pantheon, Rome"
```

- Output: a JSON list, one citation per title, in the order given. The
  `published` date is the revision's date, rendered "Last modified". The
  `accessed` date defaults to today.
- Redirects and title normalisation are followed, and the canonical title is
  used. A missing article exits 1.
- Standard library only; it queries the MediaWiki API at en.wikipedia.org.

Read the revision you cite. The citation says you took the facts from that
text, so check the frame's claims against it (sprint 002 did, and the check
changed several).
