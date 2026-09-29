#!/usr/bin/env python3
"""Name the people, places and things a subject mentions (docs/design.md §Connections).

Two commands:

  lookup   Wikipedia titles -> the name files' skeletons: the Wikidata item each
           article is about, and Wikidata's own one-line description, to start
           from (rewrite it in the house style). A title that redirects says so
           (`redirected`): the article it lands on may be about something wider
           (Project MAC lands on CSAIL), so look the item up on Wikidata instead.
  mark     Mark each name's first mention in a frame's reading, from a spec:
           {"<subject>/<frame>": [["words as the reading writes them", "<name id>"], ...]}.
           The first occurrence in prose is marked: never inside a heading, a
           table row, an image's alt text or another link. Words may wrap across
           lines. A name already marked in the frame is left alone.

  names.py lookup "Johannes Gutenberg" "Printing press"
  names.py mark examples/western-civ.json [--root subjects] [--check]

`mark --check` changes nothing, and exits 1 if any mark would be missing or cannot be
placed, so a spec can be kept as the record of what was marked and checked again.
Standard library only.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = 'https://en.wikipedia.org/w/api.php'
# A project URL, never a person: the Wikimedia APIs ask for a contact, and this is it.
AGENT = 'kloom-create-tools/1.0 (https://github.com/kenhia/kloom)'


def get(url, tries=5):
    """JSON from the API, waiting out a rate limit (429, honouring Retry-After) a few times."""
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': AGENT})
            return json.load(urllib.request.urlopen(req, timeout=30))
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == tries - 1:
                raise
            time.sleep(float(e.headers.get('Retry-After') or 2 ** attempt))


def slug(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')


def lookup(titles):
    """{requested title: {id, wikidata, name, description}}, following redirects, 50 at a time."""
    out = {}
    for i in range(0, len(titles), 50):
        batch = titles[i:i + 50]
        query = urllib.parse.urlencode({
            'action': 'query', 'prop': 'pageprops', 'ppprop': 'wikibase_item|wikibase-shortdesc',
            'redirects': 1, 'format': 'json', 'titles': '|'.join(batch),
        })
        data = get(f'{API}?{query}')['query']
        renamed = {}
        for step in data.get('normalized', []) + data.get('redirects', []):
            renamed[step['to']] = renamed.get(step['from'], step['from'])
        for page in data.get('pages', {}).values():
            asked = renamed.get(page['title'], page['title'])
            props = page.get('pageprops', {})
            out[asked] = {
                **({'redirected': page['title']} if asked != page['title'] else {}),
                'id': slug(page['title']),
                'wikidata': props.get('wikibase_item'),
                'name': page['title'],
                'description': props.get('wikibase-shortdesc', ''),
            }
    return out


# What a mark may not sit inside: a link or image (alt text wraps lines), a
# heading, a table row.
SHUT = re.compile(r'!?\[[^\]]*\]\([^)]*\)|^#.*$|^\|.*$', re.M)


def mark(reading, words, name):
    """The reading with the first prose mention of `words` marked, or None if there is none."""
    if f'](kloom:e/{name})' in reading:
        return reading
    shut = [m.span() for m in SHUT.finditer(reading)]
    pattern = r'(?<![\w-])' + r'\s+'.join(map(re.escape, words.split())) + r'(?![\w-])'
    for m in re.finditer(pattern, reading):
        if any(a < m.end() and m.start() < b for a, b in shut):
            continue
        return f'{reading[:m.start()]}[{m.group(0)}](kloom:e/{name}){reading[m.end():]}'
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='command', required=True)
    lk = sub.add_parser('lookup', help='Wikipedia titles to name-file skeletons')
    lk.add_argument('titles', nargs='+')
    mk = sub.add_parser('mark', help="mark names' first mentions from a spec")
    mk.add_argument('spec')
    mk.add_argument('--root', default='subjects', help='the subjects directory')
    mk.add_argument('--check', action='store_true', help='change nothing; exit 1 if a mark is missing')
    args = p.parse_args()

    if args.command == 'lookup':
        found = lookup(args.titles)
        for t in args.titles:
            print(json.dumps(found.get(t, {'missing': t}), ensure_ascii=False))
        return 0

    spec = json.loads(Path(args.spec).read_text())
    failed = 0
    for ref, pairs in spec.items():
        path = Path(args.root) / ref.split('/')[0] / 'frames' / ref.split('/')[1] / 'reading.md'
        reading = before = path.read_text()
        for words, name in pairs:
            done = mark(reading, words, name)
            if done is None:
                print(f'{ref}: no prose mention of "{words}" to mark as {name}', file=sys.stderr)
                failed += 1
            else:
                reading = done
        if reading != before:
            if args.check:
                print(f'{ref}: not marked yet', file=sys.stderr)
                failed += 1
            else:
                path.write_text(reading)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
