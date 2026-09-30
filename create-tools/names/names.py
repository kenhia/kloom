#!/usr/bin/env python3
"""Name the people, places and things a subject mentions (docs/design.md §Connections).

Five commands:

  lookup   Wikipedia titles -> the name files' skeletons: the Wikidata item each
           article is about, and Wikidata's own one-line description, to start
           from (rewrite it in the house style). A title that redirects says so
           (`redirected`): the article it lands on may be about something wider
           (Project MAC lands on CSAIL), so look the item up on Wikidata instead.
           A title that lands on a disambiguation page says `ambiguous`, and
           gives no item: choose the article that is meant and look that up.
  add      Write name files into the registry, from JSON files or directories
           of them. A new name is written; one already there is left alone
           unless --update is given; a name whose Wikidata item another file
           already holds is refused, naming that file. Nothing is written if
           anything is refused.
  mark     Mark each name's first mention in a frame's reading, from a spec:
           {"<subject>/<frame>": [["words as the reading writes them", "<name id>"], ...]}.
           The first occurrence in prose is marked: never inside a heading, a
           table row, an image's alt text or another link. Words may wrap across
           lines. A name already marked in the frame is left alone.

  density  Names and connections per frame, by subject: what the map's
           defaults are set from.

  names.py lookup "Johannes Gutenberg" "Printing press"
  names.py add drafts/ [--names names] [--update] [--check]
  names.py mark examples/western-civ.json [--root subjects] [--check]
  names.py density [--root subjects]

`mark --check` changes nothing, and exits 1 if any mark would be missing or cannot be
placed, so a spec can be kept as the record of what was marked and checked again.
`add --check` changes nothing, and exits 1 if anything would be refused.
Standard library only.
"""

import argparse
import json
import re
import sys
import time
import unicodedata
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


# Letters NFKD does not take apart into a base letter and an accent.
LETTERS = str.maketrans({'Ø': 'O', 'ø': 'o', 'Æ': 'AE', 'æ': 'ae', 'Œ': 'OE', 'œ': 'oe', 'ß': 'ss',
                         'Ł': 'L', 'ł': 'l', 'Đ': 'D', 'đ': 'd', 'Þ': 'Th', 'þ': 'th', 'ð': 'd'})


def slug(title):
    """An id from a title: accents and apostrophes dropped (Gödel -> godel, Moore's -> moores), & as and,
    and an en or em dash a break between words (Hellmann–Feynman -> hellmann-feynman, sprint 021)."""
    plain = unicodedata.normalize('NFKD', title.translate(LETTERS).replace('–', ' ').replace('—', ' ')).encode('ascii', 'ignore').decode()
    plain = re.sub(r"['’]", '', plain).replace('&', ' and ')
    return re.sub(r'[^a-z0-9]+', '-', plain.lower()).strip('-')


def lookup(titles):
    """{requested title: {id, wikidata, name, description}}, following redirects, 50 at a time."""
    out = {}
    for i in range(0, len(titles), 50):
        batch = titles[i:i + 50]
        query = urllib.parse.urlencode({
            'action': 'query', 'prop': 'pageprops', 'ppprop': 'wikibase_item|wikibase-shortdesc|disambiguation',
            'redirects': 1, 'format': 'json', 'titles': '|'.join(batch),
        })
        data = get(f'{API}?{query}')['query']
        # Follow each asked title to its page: several may land on one.
        step = {x['from']: x['to'] for x in data.get('normalized', []) + data.get('redirects', [])}
        redirect = {x['from'] for x in data.get('redirects', [])}
        pages = {page['title']: page for page in data.get('pages', {}).values()}
        for asked in batch:
            title, seen = asked, set()
            while title in step and title not in seen:
                seen.add(title)
                title = step[title]
            moved = bool(seen & redirect)
            page = pages.get(title, {'missing': ''})
            props = page.get('pageprops', {})
            if 'missing' in page or 'invalid' in page:
                out[asked] = {'missing': asked}
                continue
            if 'disambiguation' in props:
                # A disambiguation page is a list of meanings, not one of them.
                out[asked] = {'ambiguous': asked, 'page': page['title']}
                continue
            out[asked] = {
                **({'redirected': page['title']} if moved else {}),
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


NAME_ID = re.compile(r'^[a-z0-9][a-z0-9-]*$')
KINDS = ('person', 'place', 'org', 'artifact', 'idea', 'event')


def name_problems(name):
    """What is wrong with one name file's content, as engine/names.ts sees it (its form only)."""
    if not isinstance(name, dict):
        return ['not an object']
    problems = []
    if not isinstance(name.get('id'), str) or not NAME_ID.match(name['id']):
        problems.append('id must be lower case, digits and -')
    w = name.get('wikidata', 'absent')
    if not (w is None or (isinstance(w, str) and re.fullmatch(r'Q\d+', w))):
        problems.append('wikidata must be a Wikidata item id (Q...) or null')
    for field in ('name', 'description'):
        if not isinstance(name.get(field), str) or not name[field].strip():
            problems.append(f'{field} is required')
    if name.get('kind') not in KINDS:
        problems.append(f'kind must be one of {", ".join(KINDS)}')
    return problems


def drafts(paths):
    """Every name file under the given files and directories, in order."""
    for p in map(Path, paths):
        yield from sorted(p.glob('*.json')) if p.is_dir() else [p]


def add(paths, names_dir, update=False, check=False):
    """Write drafts into the registry; returns the lines refused (empty means all written)."""
    names_dir = Path(names_dir)
    held = {}  # wikidata item -> the id holding it
    for f in sorted(names_dir.glob('*.json')):
        item = json.loads(f.read_text()).get('wikidata')
        if item:
            held[item] = f.stem
    refused, writes = [], []
    for f in drafts(paths):
        name = json.loads(f.read_text())
        problems = name_problems(name)
        if problems:
            refused += [f'{f}: {p}' for p in problems]
            continue
        target = names_dir / f"{name['id']}.json"
        other = name['wikidata'] and held.get(name['wikidata'])
        if other and other != name['id']:
            refused.append(f"{f}: {name['wikidata']} is already names/{other}.json")
            continue
        if target.exists() and not update:
            continue
        if name['wikidata']:
            held[name['wikidata']] = name['id']
        writes.append((target, name))
    if refused or check:
        return refused
    names_dir.mkdir(parents=True, exist_ok=True)
    for target, name in writes:
        # Tabs, like Prettier writes the repo's JSON.
        target.write_text(json.dumps(name, indent='\t', ensure_ascii=False) + '\n')
        print(f'wrote {target}')
    return []


MARK = re.compile(r'\]\(kloom:e/([a-z0-9][a-z0-9-]*)\)')


def density(root):
    """Per subject: frames, marks, distinct names, connections stored and touching, per frame."""
    root = Path(root)
    frames = {}  # subject -> frame ids
    stored = {}  # subject -> connections stored on its frames
    touching = {}  # subject -> connections with an end on its frames
    for s in sorted(p for p in root.iterdir() if (p / 'subject.json').exists()):
        frames[s.name] = [f.name for f in sorted((s / 'frames').iterdir()) if (f / 'frame.json').exists()]
    for subject, ids in frames.items():
        for fid in ids:
            for c in json.loads((root / subject / 'frames' / fid / 'frame.json').read_text()).get('connections', []):
                stored[subject] = stored.get(subject, 0) + 1
                ends = {subject, c['to'].split('/')[0]}
                for end in ends:
                    touching[end] = touching.get(end, 0) + 1
    rows = []
    for subject, ids in frames.items():
        marks, distinct, bare = 0, set(), 0
        for fid in ids:
            found = set(MARK.findall((root / subject / 'frames' / fid / 'reading.md').read_text()))
            marks += len(found)
            distinct |= found
            bare += not found
        n = len(ids) or 1
        rows.append({
            'subject': subject, 'frames': len(ids), 'marks': marks, 'names': len(distinct),
            'marks_per_frame': round(marks / n, 2), 'frames_unmarked': bare,
            'connections_stored': stored.get(subject, 0),
            'connections_touching': touching.get(subject, 0),
            'connections_per_frame': round(touching.get(subject, 0) / n, 2),
        })
    return rows


def reach(root, source, steps=2):
    """Frames of each other subject within `steps` connections of any frame of `source`.

    Connections are shown on both ends, so the graph is undirected, and a path
    may pass through any subject (a bridge subject's frames count as steps)."""
    root = Path(root)
    adj, frames = {}, {}
    for s in sorted(p for p in root.iterdir() if (p / 'subject.json').exists()):
        for f in sorted((s / 'frames').iterdir()):
            if not (f / 'frame.json').exists():
                continue
            here = f'{s.name}/{f.name}'
            frames.setdefault(s.name, set()).add(here)
            adj.setdefault(here, set())
            for c in json.loads((f / 'frame.json').read_text()).get('connections', []):
                adj[here].add(c['to'])
                adj.setdefault(c['to'], set()).add(here)
    seen = set(frames.get(source, ()))
    edge, rows = set(seen), []
    within = {}
    for step in range(1, steps + 1):
        edge = {n for e in edge for n in adj.get(e, ())} - seen
        seen |= edge
        within[step] = set(seen)
    for subject in sorted(frames):
        if subject == source:
            continue
        row = {'from': source, 'to': subject, 'frames': len(frames[subject])}
        for step in range(1, steps + 1):
            row[f'within_{step}'] = len(within[step] & frames[subject])
        rows.append(row)
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='command', required=True)
    lk = sub.add_parser('lookup', help='Wikipedia titles to name-file skeletons')
    lk.add_argument('titles', nargs='+')
    ad = sub.add_parser('add', help='write name files into the registry')
    ad.add_argument('drafts', nargs='+', help='name files, or directories of them')
    ad.add_argument('--names', default='names', help='the registry directory')
    ad.add_argument('--update', action='store_true', help='rewrite names already there')
    ad.add_argument('--check', action='store_true', help='change nothing; exit 1 if any is refused')
    dn = sub.add_parser('density', help='names and connections per frame, by subject')
    dn.add_argument('--root', default='subjects', help='the subjects directory')
    dn.add_argument('--json', action='store_true', help='one JSON line per subject')
    rc = sub.add_parser('reach', help="other subjects' frames within N connections of a subject")
    rc.add_argument('subject')
    rc.add_argument('--steps', type=int, default=2)
    rc.add_argument('--root', default='subjects', help='the subjects directory')
    rc.add_argument('--json', action='store_true', help='one JSON line per subject')
    mk = sub.add_parser('mark', help="mark names' first mentions from a spec")
    mk.add_argument('spec')
    mk.add_argument('--root', default='subjects', help='the subjects directory')
    mk.add_argument('--check', action='store_true', help='change nothing; exit 1 if a mark is missing')
    mk.add_argument('--names', default='names', help='the registry directory')
    mk.add_argument('--drafts', action='append', default=[],
                    help='a directory of name drafts not yet added, whose ids count as known (repeatable)')
    args = p.parse_args()

    if args.command == 'lookup':
        found = lookup(args.titles)
        for t in args.titles:
            print(json.dumps(found.get(t, {'missing': t}), ensure_ascii=False))
        return 0

    if args.command == 'add':
        refused = add(args.drafts, args.names, args.update, args.check)
        for line in refused:
            print(line, file=sys.stderr)
        return 1 if refused else 0

    if args.command in ('density', 'reach'):
        rows = density(args.root) if args.command == 'density' else reach(args.root, args.subject, args.steps)
        if args.json:
            for r in rows:
                print(json.dumps(r))
        else:
            cols = list(rows[0]) if rows else []
            print(' | '.join(cols))
            for r in rows:
                print(' | '.join(str(r[c]) for c in cols))
        return 0

    spec = json.loads(Path(args.spec).read_text())
    failed = 0
    # A mark on a name no file holds fails the gate; say so here, not at vitest (sprint 021).
    known = {f.stem for d in [args.names, *args.drafts] if Path(d).is_dir() for f in Path(d).glob('*.json')}
    for ref, pairs in spec.items():
        for words, name in pairs:
            if name not in known:
                print(f'{ref}: {name} is not in the registry or a draft', file=sys.stderr)
                failed += 1
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
