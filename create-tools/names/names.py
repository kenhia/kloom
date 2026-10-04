#!/usr/bin/env python3
"""Name the people, places and things a subject mentions (docs/design.md §Connections).

Seven commands:

  lookup   Wikipedia titles -> the name files' skeletons: the Wikidata item each
           article is about, Wikidata's own one-line description, to start
           from (rewrite it in the house style), and the article's first line.
           Read both: a real article on a namesake passes otherwise, and
           `--expect WORD` warns when neither says WORD (the article only; a title
           may carry its own, `"Title=word"`). A title that redirects says so
           (`redirected`): the article it lands on may be about something wider
           (Project MAC lands on CSAIL), so look the item up on Wikidata instead.
           A title that lands on a disambiguation page, or a set-index page (a list
           of compounds or ships of one name, sprint 029), says `ambiguous`, and
           gives no item: choose the article that is meant and look that up.
           Each item's Wikidata class (`instance_of`) and description are given
           too, and `--expect-item WORD` checks them as well, opt-in: an article on
           a blood group whose item is the gene product ("ACKR1 protein") is warned
           of. (Sprint 029 checked the item under `--expect`; it warned on right
           items for six of sprint 030's authors, so sprint 033 split it out.)
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

  drafts   The name drafts a subject's authors have written so far, one per line: id,
           Wikidata item, home and the part that drafted it (the drafts directory
           `.scratch/names/<subject>-<part>/`). It flags, and exits 1 on, a name drafted
           by two parts (the same id, or the same item under two ids) and a name drafted
           by a part the plan's `owners` does not give it to (sprint 033: sprint 030's
           authors found owners by grepping, and two names were drafted twice).

  density  Names and connections per frame, by subject: what the map's
           defaults are set from.
  reach    For every other subject, its frames within one and within --steps
           connections of a subject's frames.
  strip    Frames' readings with every name mark taken out, the words left:
           what an author is shown as the quality bar, so no author copies a
           mark by hand (sprint 029). Marks are `mark`'s job, from a spec.

  names.py lookup "Johannes Gutenberg" "Printing press=printing" [--expect WORD] [--expect-item WORD]
  names.py add drafts/ [--names names] [--update] [--check]
  names.py mark examples/western-civ.json [...] [--root subjects] [--check [--placed]]
  names.py drafts nursing [--plan create-tools/subject-plan/nursing.json] [--dir .scratch/names]
  names.py density [--root subjects]
  names.py reach western-civ [--steps 2] [--root subjects]
  names.py strip blood/abo blood/harvey [--root subjects] [--out DIR]

`mark --check` changes nothing: it says where each mark not yet placed would land (the
sentence, and a warning when that is before the reading's bold mention), and exits 1 only
on a problem: a mention it cannot find, a name no file or draft holds, or a mark no spec
lists (one typed by hand). "Would place" is success, and exits 0. `--placed` makes a mark
not yet placed a problem too: `just check` runs every spec that way, so a spec is the
record of what was marked and a hand-typed mark fails the gate (sprint 027).
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

# The article check, shared with wiki_cite.py so the two never drift (sprint 033).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'lib'))
from article_check import article_mismatch, expectations, item_mismatch, untex  # noqa: E402

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


# Greek letters, spelled: "Leibniz formula for π" is leibniz-formula-for-pi, not -for (sprint 024).
GREEK = dict(zip('αβγδεζηθικλμνξοπρστυφχψω',
                 'alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho '
                 'sigma tau upsilon phi chi psi omega'.split()))
GREEK.update({k.upper(): v for k, v in GREEK.items()}, ς='sigma')
# A title that is a bare number names the number: Wikipedia's "0" is zero, not the id 0 (sprint 024).
NUMBERS = 'zero one two three four five six seven eight nine ten eleven twelve'.split()


def slug(title):
    """An id from a title: accents and apostrophes dropped (Gödel -> godel, Moore's -> moores), & as and,
    an en or em dash a break between words (Hellmann–Feynman -> hellmann-feynman, sprint 021), a Greek
    letter spelled (π -> pi), and a bare number in words (0 -> zero, 1729 -> number-1729)."""
    if re.fullmatch(r'\d+', title.strip()):
        n = int(title)
        return NUMBERS[n] if n < len(NUMBERS) else f'number-{n}'
    title = ''.join(f' {GREEK[c]} ' if c in GREEK else c for c in title)
    plain = unicodedata.normalize('NFKD', title.translate(LETTERS).replace('–', ' ').replace('—', ' ')).encode('ascii', 'ignore').decode()
    plain = re.sub(r"['’]", '', plain).replace('&', ' and ')
    return re.sub(r'[^a-z0-9]+', '-', plain.lower()).strip('-')


def lookup(titles):
    """{requested title: {id, wikidata, name, description, first_line, item_description, instance_of}},
    following redirects, 20 at a time (the most intro extracts the API gives in one request)."""
    out = {}
    for i in range(0, len(titles), 20):
        batch = titles[i:i + 20]
        query = urllib.parse.urlencode({
            'action': 'query', 'prop': 'pageprops|extracts|categories',
            'ppprop': 'wikibase_item|wikibase-shortdesc|disambiguation',
            'exintro': 1, 'explaintext': 1, 'exsentences': 1, 'exlimit': 'max',
            'clcategories': SET_INDEX, 'cllimit': 'max',
            'redirects': 1, 'format': 'json', 'titles': '|'.join(batch),
        })
        out.update(rows(batch, get(f'{API}?{query}')['query']))
    classes = item_classes([r['wikidata'] for r in out.values() if r.get('wikidata')])
    for row in out.values():
        row.update(classes.get(row.get('wikidata'), {}))
    return out


# Every set-index article is in this hidden category; it carries no disambiguation flag.
SET_INDEX = 'Category:All set index articles'


def rows(batch, data):
    """The rows for one batch of asked titles, from the API's `query` answer."""
    out = {}
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
        if 'disambiguation' in props or any(c.get('title') == SET_INDEX for c in page.get('categories', [])):
            # A disambiguation or set-index page is a list of meanings, not one of them.
            out[asked] = {'ambiguous': asked, 'page': page['title']}
            continue
        out[asked] = {
            **({'redirected': page['title']} if moved else {}),
            'id': slug(page['title']),
            'wikidata': props.get('wikibase_item'),
            'name': page['title'],
            'description': props.get('wikibase-shortdesc', ''),
            # The article's own first sentence: a namesake shows here (sprint 026's four).
            'first_line': untex(' '.join(page.get('extract', '').split())),
        }
    return out


WIKIDATA = 'https://www.wikidata.org/w/api.php'


def item_classes(qids):
    """{qid: {item_description, instance_of: [labels]}}: what Wikidata says each item is, which may not be
    what the article is about ("Duffy antigen system" is the ACKR1 protein's item, sprint 029)."""
    def entities(ids, props):
        found = {}
        for i in range(0, len(ids), 50):
            query = urllib.parse.urlencode({'action': 'wbgetentities', 'ids': '|'.join(ids[i:i + 50]),
                                            'props': props, 'languages': 'en', 'format': 'json'})
            found.update(get(f'{WIKIDATA}?{query}').get('entities', {}))
        return found
    qids = sorted(set(qids))
    if not qids:
        return {}
    items = entities(qids, 'descriptions|claims')
    kinds = {q: [c['mainsnak'].get('datavalue', {}).get('value', {}).get('id')
                 for c in e.get('claims', {}).get('P31', [])] for q, e in items.items()}
    wanted = sorted({k for ks in kinds.values() for k in ks if k})
    labels = {q: e.get('labels', {}).get('en', {}).get('value', q) for q, e in entities(wanted, 'labels').items()}
    return {q: {'item_description': items[q].get('descriptions', {}).get('en', {}).get('value', ''),
                'instance_of': [labels.get(k, k) for k in kinds[q] if k]} for q in items}


def unexpected(found, expect, expect_item=None):
    """Why a looked-up article may not be the thing meant: `expect` is in neither its description
    nor its first line (a namesake: "Hideo Kodama" --expect printing is a politician), or, with
    `expect_item`, in neither its Wikidata item's description nor its class (a gene product for a
    blood group, sprint 029). None when all is well, or the title was not found."""
    if 'id' not in found:
        return None
    why = article_mismatch(found['name'], found.get('description'), found.get('first_line'), expect)
    if why or not expect_item or 'instance_of' not in found:
        return why
    return item_mismatch(found['name'], found.get('wikidata'), found.get('item_description'),
                         found['instance_of'], expect_item)


# What a mark may not sit inside: a link or image (alt text wraps lines), a
# heading, a table row.
SHUT = re.compile(r'!?\[[^\]]*\]\([^)]*\)|^#.*$|^\|.*$', re.M)


def place(reading, words, name):
    """Where the first prose mention of `words` is, as (start, end); 'marked' if the name is
    already marked in the frame, or None if there is no mention to mark. Matched whole: "electron"
    is not found inside "electrons", and case counts ("antimony" is not "Antimony")."""
    if f'](kloom:e/{name})' in reading:
        return 'marked'
    shut = [m.span() for m in SHUT.finditer(reading)]
    pattern = r'(?<![\w-])' + r'\s+'.join(map(re.escape, words.split())) + r'(?![\w-])'
    for m in re.finditer(pattern, reading):
        if not any(a < m.end() and m.start() < b for a, b in shut):
            return m.span()
    return None


def mark(reading, words, name):
    """The reading with the first prose mention of `words` marked, or None if there is none."""
    at = place(reading, words, name)
    if at is None or at == 'marked':
        return None if at is None else reading
    a, b = at
    return f'{reading[:a]}[{reading[a:b]}](kloom:e/{name}){reading[b:]}'


BOLD = re.compile(r'\*\*(?=\S)((?:(?!\n\n).)+?)(?<=\S)\*\*', re.S)


def sentence(reading, a, b):
    """The sentence holding reading[a:b], on one line, with those words in brackets."""
    start = max(reading.rfind('\n\n', 0, a), max((reading.rfind(p, 0, a) for p in ('. ', '? ', '! ')), default=-1))
    start = 0 if start < 0 else start + 2
    ends = [i for i in (reading.find(p, b) for p in ('. ', '? ', '! ', '.\n', '\n\n')) if i >= 0]
    end = min(ends) + 1 if ends else len(reading)
    text = f'{reading[start:a]}[{reading[a:b]}]{reading[b:end]}'
    return re.sub(r'\s+', ' ', text).strip()


def bold_elsewhere(reading, words, a, b):
    """The bold mention of `words` when the mark at a..b is not on it, else None.

    A bold mention is a bold run that is the words themselves, in any case or as a plural
    ("**Antimony**", "**electrons**" for "electron"), and holds no mark of its own. It is the
    mention the author meant; a mark that lands elsewhere is on a passing mention, a quotation
    or a different case (sprints 024 and 025: eleven authors)."""
    want = ' '.join(words.split()).lower().strip('_*.,;:')   # a spec's italic words, as the bold run is read
    for m in BOLD.finditer(reading):
        text = ' '.join(m.group(1).split()).lower().strip('_*.,;:')
        if 'kloom:e/' in text or text not in (want, want + 's', want + 'es'):
            continue
        return None if m.start() <= a and b <= m.end() else m.group(0)
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


def draft_files(paths):
    """Every name file under the given files and directories, in order. (Named apart from `drafts`, the
    subcommand, which shadowed it from sprint 033 until sprint 049 and broke `add`.)"""
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
    refused, writes, kept = [], [], []
    for f in draft_files(paths):
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
            kept.append(name['id'])
            continue
        if name['wikidata']:
            held[name['wikidata']] = name['id']
        writes.append((target, name))
    if refused or check:
        if check and not refused:
            print(f'add --check: {len(writes)} to write, nothing refused')
            if kept:
                # Another author's draft may have reached the registry meanwhile (sprint 026).
                print(f"add --check: {len(kept)} already in the registry, left alone: {', '.join(kept)}")
        return refused
    names_dir.mkdir(parents=True, exist_ok=True)
    for target, name in writes:
        # Tabs, like Prettier writes the repo's JSON.
        target.write_text(json.dumps(name, indent='\t', ensure_ascii=False) + '\n')
        print(f'wrote {target}')
    return []


MARK = re.compile(r'\]\(kloom:e/([a-z0-9][a-z0-9-]*)\)')
# A whole mark, its words kept: words may wrap lines, and hold no bracket.
WHOLE_MARK = re.compile(r'\[([^\]]+)\]\(kloom:e/[a-z0-9][a-z0-9-]*\)')


def strip(reading):
    """A reading with its name marks taken out and their words left (`**[Harvey](kloom:e/x)**` -> `**Harvey**`)."""
    return WHOLE_MARK.sub(r'\1', reading)


def strip_frames(root, refs, out=None):
    """Each `<subject>/<frame>`'s reading stripped of marks: written to `out/<subject>-<frame>.md`, or
    returned as one text with a heading per frame. Returns (text or None, problems)."""
    texts, problems = [], []
    for ref in refs:
        subject, _, frame = ref.partition('/')
        path = Path(root) / subject / 'frames' / frame / 'reading.md'
        if not frame or not path.is_file():
            problems.append(f'{ref}: no reading at {path}')
            continue
        plain = strip(path.read_text())
        if out:
            Path(out).mkdir(parents=True, exist_ok=True)
            (Path(out) / f'{subject}-{frame}.md').write_text(plain)
        else:
            texts.append(f'<!-- {ref} -->\n\n{plain.rstrip()}\n')
    return (None if out else '\n'.join(texts)), problems


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
    lk.add_argument('--expect', metavar='WORD',
                    help='warn, and exit 1, for an article whose description and first line lack this word '
                         '(a title may carry its own: "Title=word")')
    lk.add_argument('--expect-item', metavar='WORD',
                    help="also warn, and exit 1, when the article's Wikidata item's description and class lack "
                         'this word: an item that is something else (a gene product for a blood group)')
    ad = sub.add_parser('add', help='write name files into the registry')
    ad.add_argument('drafts', nargs='+', help='name files, or directories of them')
    ad.add_argument('--names', default='names', help='the registry directory')
    ad.add_argument('--update', action='store_true', help='rewrite names already there')
    ad.add_argument('--check', action='store_true', help='change nothing; exit 1 if any is refused')
    dr = sub.add_parser('drafts', help="a subject's name drafts: who drafted what, and what was drafted twice")
    dr.add_argument('subject')
    dr.add_argument('--plan', help="the subject's plan, for its owners (default: create-tools/subject-plan/<subject>.json)")
    dr.add_argument('--dir', default='.scratch/names', help='where the drafts directories are')
    dr.add_argument('--names', default='names', help='the registry directory')
    dr.add_argument('--json', action='store_true', help='one JSON line per draft')
    dn = sub.add_parser('density', help='names and connections per frame, by subject')
    dn.add_argument('--root', default='subjects', help='the subjects directory')
    dn.add_argument('--json', action='store_true', help='one JSON line per subject')
    rc = sub.add_parser('reach', help="other subjects' frames within N connections of a subject")
    rc.add_argument('subject')
    rc.add_argument('--steps', type=int, default=2)
    rc.add_argument('--root', default='subjects', help='the subjects directory')
    rc.add_argument('--json', action='store_true', help='one JSON line per subject')
    st = sub.add_parser('strip', help="frames' readings without their name marks, for an author's brief")
    st.add_argument('frames', nargs='+', metavar='SUBJECT/FRAME')
    st.add_argument('--root', default='subjects', help='the subjects directory')
    st.add_argument('--out', metavar='DIR', help='write DIR/<subject>-<frame>.md for each, rather than print them')
    mk = sub.add_parser('mark', help="mark names' first mentions from a spec")
    mk.add_argument('spec', nargs='+', help='one or more specs')
    mk.add_argument('--root', default='subjects', help='the subjects directory')
    mk.add_argument('--check', action='store_true',
                    help='change nothing: say where each mark would land; exit 1 only if one cannot be placed, '
                         'names an unknown name, or a mark is in no spec')
    mk.add_argument('--placed', action='store_true',
                    help='with --check: exit 1 too if a mark is not placed yet (the gate, over committed readings)')
    mk.add_argument('--names', default='names', help='the registry directory')
    mk.add_argument('--drafts', action='append', default=[],
                    help='a directory of name drafts not yet added, whose ids count as known (repeatable)')
    args = p.parse_args()

    if args.command == 'lookup':
        asked = expectations(args.titles, args.expect)
        found = lookup([t for t, _ in asked])
        doubtful = 0
        for t, keyword in asked:
            row = found.get(t, {'missing': t})
            print(json.dumps(row, ensure_ascii=False))
            why = unexpected(row, keyword, args.expect_item)
            if why:
                print(f'warning: {why}', file=sys.stderr)
                doubtful += 1
        return 1 if doubtful else 0

    if args.command == 'drafts':
        plan_path = Path(args.plan or Path(__file__).resolve().parent.parent / 'subject-plan' / f'{args.subject}.json')
        plan = json.loads(plan_path.read_text()) if plan_path.exists() else None
        registry = {f.stem: f for f in Path(args.names).glob('*.json')} if Path(args.names).is_dir() else {}
        rows, problems, notes = drafts(args.subject, args.dir, plan, registry)
        for r in rows:
            print(json.dumps(r) if args.json else f"{r['id']} | {r['wikidata']} | {r['home'] or '-'} | {r['part']}")
        if plan is None:
            print(f'note: no plan at {plan_path}, so no owners to check', file=sys.stderr)
        elif not plan.get('owners'):
            print(f'note: {plan_path} gives no owners', file=sys.stderr)
        # Once a part is committed its drafts are all added; name a few, count the rest.
        for line in notes[:3]:
            print(f'note: {line}', file=sys.stderr)
        if len(notes) > 3:
            print(f'note: {len(notes) - 3} more drafts are already in the registry', file=sys.stderr)
        for line in problems:
            print(line, file=sys.stderr)
        return 1 if problems else 0

    if args.command == 'strip':
        text, problems = strip_frames(args.root, args.frames, args.out)
        if text:
            print(text, end='')
        for line in problems:
            print(line, file=sys.stderr)
        return 1 if problems else 0

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

    return mark_spec(args)


def drafts(subject, drafts_dir, plan=None, registry=None):
    """(rows, problems, notes) for a subject's name drafts: a row per draft (id, wikidata, home, part),
    a problem for a name two parts drafted or a part that does not own it, and a note for a draft the
    registry already holds (it has been added; the draft can go)."""
    owners = (plan or {}).get('owners', {})
    rows, problems, notes = [], [], []
    prefix = f'{subject}-'
    for d in sorted(Path(drafts_dir).glob(f'{prefix}*')):
        if not d.is_dir():
            continue
        part = d.name[len(prefix):]
        for f in sorted(d.glob('*.json')):
            body = json.loads(f.read_text())
            rows.append({'id': f.stem, 'wikidata': body.get('wikidata', ''), 'home': body.get('home', ''), 'part': part})
    by_id, by_item = {}, {}
    for r in rows:
        by_id.setdefault(r['id'], []).append(r['part'])
        if r['wikidata']:
            by_item.setdefault(r['wikidata'], set()).add(r['id'])
    for name, parts in sorted(by_id.items()):
        if len(parts) > 1:
            problems.append(f'{name} is drafted by {len(parts)} parts: {", ".join(parts)}')
        owner = owners.get(name)
        for part in parts:
            if owner and part != owner:
                problems.append(f'{name} is drafted by {part}, but the plan gives it to {owner}: borrow '
                                f"{owner}'s draft, or change the plan's owners if {part} is to commit first")
    for item, ids in sorted(by_item.items()):
        if len(ids) > 1:
            problems.append(f'{item} is drafted under {len(ids)} ids: {", ".join(sorted(ids))}')
    for stem, held, line in stale_drafts(registry or {}, {r['id']: Path(drafts_dir) / f"{prefix}{r['part']}" / f"{r['id']}.json"
                                                          for r in rows}):
        notes.append(line)
    return rows, problems, notes


def mark_spec(args):
    """`mark`: place each spec's marks, or with --check say what would be placed. 0, or 1 on a problem."""
    failed = 0
    # A mark on a name no file holds fails the gate; say so here, not at vitest (sprint 021).
    registry = {f.stem: f for f in Path(args.names).glob('*.json')} if Path(args.names).is_dir() else {}
    drafted = {f.stem: f for d in args.drafts if Path(d).is_dir() for f in Path(d).glob('*.json')}
    known = set(registry) | set(drafted)
    # Name the stale drafts these specs mark; count the rest. Passing other authors' drafts
    # printed dozens of their names, which buried this author's own (sprint 028, four authors).
    marked = {pair[1] for p in args.spec for pairs in json.loads(Path(p).read_text()).values() for pair in pairs}
    others = 0
    for stem, held, line in stale_drafts(registry, drafted):
        if stem in marked or held in marked:
            print(f'warning: {line}', file=sys.stderr)
        else:
            others += 1
    if others:
        print(f'note: {others} other drafts passed with --drafts are already in the registry; '
              'they are not marked by these specs', file=sys.stderr)
    for spec_path in args.spec:
        failed += mark_one(args, Path(spec_path), known)
    return 1 if failed else 0


def mark_one(args, spec_path, known):
    """One spec's marks; returns how many problems it found."""
    failed = 0
    for ref, pairs in json.loads(spec_path.read_text()).items():
        unknown = [name for _, name in pairs if name not in known]
        for name in unknown:
            print(f'{ref}: {name} is not in the registry or a draft', file=sys.stderr)
            failed += 1
        path = Path(args.root) / ref.split('/')[0] / 'frames' / ref.split('/')[1] / 'reading.md'
        if not path.exists():
            # A checking copy built with --only leaves other authors' frames out (sprint 049, where
            # this crashed); the gate's --placed still refuses a spec for a frame that is not there.
            print(f'{ref}: not in {args.root}, skipped', file=sys.stderr)
            failed += 1 if args.placed else 0
            continue
        reading = before = path.read_text()
        landed = []
        for words, name in pairs:
            at = place(reading, words, name)
            if at is None:
                print(f'{ref}: no prose mention of "{words}" to mark as {name}', file=sys.stderr)
                failed += 1
            elif at != 'marked':
                a, b = at
                landed.append((name, words, sentence(reading, a, b), bold_elsewhere(reading, words, a, b)))
                reading = mark(reading, words, name)
        if args.check:
            # The specs are the record of what was marked: a mark placed by hand is in none of them
            # (sprint 021). A frame's marks may be split across specs (shared.json), so read them all.
            listed = {name for sp in spec_path.parent.glob('*.json')
                      for name_ref, ps in json.loads(sp.read_text()).items() if name_ref == ref
                      for _, name in ps}
            for name in sorted(set(MARK.findall(reading)) - listed):
                print(f'{ref}: marks {name}, which the spec does not list (a mark typed by hand?)', file=sys.stderr)
                failed += 1
        if reading != before:
            # Say what would land, and where, so a clean check is seen to place every mark on the
            # words meant (sprints 024, 025).
            if args.check and args.placed:
                print(f'{ref}: {len(landed)} marks not placed yet', file=sys.stderr)
                failed += 1
            elif args.check:
                print(f'{ref}: {len(landed)} marks would place')
            elif unknown:
                # Placing a mark on no name writes a frame the gate refuses (sprint 030), so a frame
                # with one is left as it was, and every mark waits for the name to be added.
                print(f'{ref}: not marked, until {", ".join(unknown)} is added', file=sys.stderr)
            else:
                path.write_text(reading)
                print(f'{ref}: marked {len(landed)}')
            for name, words, where, bold in landed:
                print(f'  {name}: {where}')
                if bold:
                    print(f'{ref}: warning: {name} lands on "{words}" before the bold {bold}; '
                          'reword the reading, or make the spec\'s words the bold ones', file=sys.stderr)
    return failed


def stale_drafts(registry, drafted):
    """A draft whose id, or Wikidata item, the registry already holds: another author's name
    reached it meanwhile (sprint 025), so the draft is a duplicate to drop or to merge.
    Yields (draft id, the registry id it collides with, the warning)."""
    held = {}
    for stem, f in registry.items():
        item = json.loads(f.read_text()).get('wikidata')
        if item:
            held[item] = stem
    out = []
    for stem, f in sorted(drafted.items()):
        if stem in registry:
            out.append((stem, stem, f'draft {f} is already in the registry as names/{stem}.json'))
            continue
        item = json.loads(f.read_text()).get('wikidata')
        if item and item in held:
            out.append((stem, held[item], f'draft {f}: {item} is already names/{held[item]}.json; mark that id instead'))
    return out


if __name__ == '__main__':
    sys.exit(main())
