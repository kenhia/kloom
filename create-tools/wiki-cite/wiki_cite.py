"""Wikipedia citations pinned to a revision, for a frame's `citations`.

    python3 create-tools/wiki-cite/wiki_cite.py [--accessed YYYY-MM-DD] [--text DIR] Title ...

Prints a JSON list, one kloom `wikipedia` citation per title, each pointing
at the article's current revision (`oldid=`) and dated by it. Redirects are
followed. A missing article is named on stderr and exits 1, after the
citations that were found are printed. `--text DIR` also writes each cited
revision's readable text to DIR/<Title>.txt, so what you read is the
revision you cite. Standard library only.
"""
import argparse, datetime, html.parser, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

API = 'https://en.wikipedia.org/w/api.php'
AGENT = 'kloom-create-tools/1.0 (https://github.com/kenhia/kloom)'


def quote(title):
    return urllib.parse.quote(title.replace(' ', '_'), safe="_(),'")


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


def revisions(titles):
    """{requested title: (canonical title, revid, date)} in batches of 50."""
    out = {}
    for i in range(0, len(titles), 50):
        batch = titles[i:i + 50]
        query = urllib.parse.urlencode({
            'action': 'query', 'prop': 'revisions', 'rvprop': 'ids|timestamp',
            'redirects': 1, 'format': 'json', 'titles': '|'.join(batch),
        })
        data = get(f'{API}?{query}')['query']
        renamed = {}
        for step in data.get('normalized', []) + data.get('redirects', []):
            renamed[step['from']] = step['to']
        pages = {p['title']: p for p in data['pages'].values()}
        for t in batch:
            name = t
            while name in renamed:
                name = renamed[name]
            page = pages.get(name)
            if not page or 'missing' in page:
                print(f'wiki_cite: no article "{t}"', file=sys.stderr)
                continue
            rev = page['revisions'][0]
            out[t] = (name, rev['revid'], rev['timestamp'][:10])
    return out


class _Text(html.parser.HTMLParser):
    """The readable text of a parsed article: headings, paragraphs, lists and table cells, without
    footnote markers, edit links, styles or the reference list's own markup."""
    SKIP = {'style', 'script'}
    SKIP_CLASS = ('reference', 'mw-editsection', 'mw-cite-backlink', 'navbox', 'noprint')
    BLOCK = {'p', 'li', 'tr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'dd', 'dt', 'blockquote', 'caption', 'div', 'table'}
    VOID = {'br', 'img', 'hr', 'meta', 'link', 'input', 'wbr', 'col', 'area', 'source'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.stack, self.skipping = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            if tag == 'br':
                self.out.append('\n')
            return
        cls = dict(attrs).get('class') or ''
        skip = tag in self.SKIP or any(c in cls.split() for c in self.SKIP_CLASS)
        self.stack.append((tag, skip))
        self.skipping += skip
        if not self.skipping:
            if tag in self.BLOCK:
                self.out.append('\n')
            if tag in ('h2', 'h3', 'h4'):
                self.out.append('#' * int(tag[1]) + ' ')
            if tag in ('td', 'th'):
                self.out.append(' | ')

    def handle_endtag(self, tag):
        while self.stack:
            t, skip = self.stack.pop()
            self.skipping -= skip
            if t == tag:
                break
        if not self.skipping and tag in self.BLOCK:
            self.out.append('\n')

    def handle_data(self, data):
        if not self.skipping:
            self.out.append(data)

    def text(self):
        t = re.sub(r'[ \t]+', ' ', ''.join(self.out))
        return re.sub(r'\n\s*\n+', '\n\n', t).strip() + '\n'


def revision_text(revid):
    """The readable text of one revision, from the API's parse of exactly that revision."""
    query = urllib.parse.urlencode({'action': 'parse', 'oldid': revid, 'prop': 'text', 'format': 'json',
                                    'disableeditsection': 1, 'disabletoc': 1})
    p = _Text()
    p.feed(get(f'{API}?{query}')['parse']['text']['*'])
    return p.text()


def citation(title, revid, date, accessed):
    return {
        'kind': 'wikipedia',
        'title': title,
        'url': f'https://en.wikipedia.org/w/index.php?title={quote(title)}&oldid={revid}',
        'accessed': accessed,
        'authors': [{'name': 'Wikipedia contributors'}],
        'container': 'Wikipedia, The Free Encyclopedia',
        'publisher': 'Wikimedia Foundation',
        'published': date,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('titles', nargs='+')
    ap.add_argument('--accessed', default=datetime.date.today().isoformat())
    ap.add_argument('--text', metavar='DIR', help="also write each revision's readable text to DIR/<Title>.txt")
    a = ap.parse_args()
    revs = revisions(a.titles)
    seen, found = set(), []  # titles that redirect to one article give one citation
    for t in a.titles:
        if t in revs and revs[t][0] not in seen:
            seen.add(revs[t][0])
            found.append(t)
    if a.text:
        os.makedirs(a.text, exist_ok=True)
        for t in found:
            name, revid, _ = revs[t]
            path = os.path.join(a.text, name.replace('/', '_') + '.txt')
            with open(path, 'w') as fh:
                fh.write(f'{name} (revision {revid})\n\n' + revision_text(revid))
            print(f'wiki_cite: wrote {path}', file=sys.stderr)
    print(json.dumps([citation(*revs[t], a.accessed) for t in found], indent='\t', ensure_ascii=False))
    if len(revs) < len(a.titles):
        sys.exit(1)  # the others are printed; a missing article is still an error


if __name__ == '__main__':
    main()
