"""Wikipedia citations pinned to a revision, for a frame's `citations`.

    python3 create-tools/wiki-cite/wiki_cite.py [--accessed YYYY-MM-DD] [--text DIR] [--lang xx] [--expect WORD] Title[=word] ...

Prints a JSON list, one kloom `wikipedia` citation per title, each pointing
at the article's current revision (`oldid=`) and dated by it. Redirects are
followed. A missing article, or a title that lands on a disambiguation page,
is named on stderr and left out, and the run exits 1 after the citations
that were found are printed. `--text DIR` also writes each cited revision's
readable text to DIR/<Title>.txt (DIR/<Title>.<lang>.txt for --lang), so what you read is the revision you cite;
a formula is written once, as its TeX. `--lang` cites another language's
Wikipedia, with the citation's `language`. `--expect WORD` checks that each
article is the one meant, as `names.py lookup --expect` does and with the
same code: its short description or first line must say WORD, or a warning
on stderr names the article it landed on, and the run exits 1 after
printing (sprint 033: "Army Medical School" quietly cited the US school, a
namesake). A title may carry its own word, `"Army Medical School=London"`.
Standard library only.
"""
import argparse, datetime, html.parser, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

# The article check, shared with names.py lookup so the two never drift (sprint 033).
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib'))
from article_check import article_mismatch, expectations, untex  # noqa: E402

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


def api(lang):
    return f'https://{lang}.wikipedia.org/w/api.php'


def revisions(titles, lang='en', about=None):
    """{requested title: (canonical title, revid, date)} in batches of 20 (the most intro extracts the
    API gives in one request); a title that is missing or a disambiguation page is named on stderr
    and left out. `about`, a dict, is filled with {canonical title: (short description, first line)},
    for --expect."""
    out = {}
    for i in range(0, len(titles), 20):
        batch = titles[i:i + 20]
        query = urllib.parse.urlencode({
            'action': 'query', 'prop': 'revisions|pageprops|extracts', 'rvprop': 'ids|timestamp',
            'ppprop': 'disambiguation|wikibase-shortdesc', 'exintro': 1, 'explaintext': 1, 'exsentences': 1,
            'exlimit': 'max', 'redirects': 1, 'format': 'json', 'titles': '|'.join(batch),
        })
        data = get(f'{api(lang)}?{query}')['query']
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
            if 'disambiguation' in page.get('pageprops', {}):
                # A list of meanings is not a source (sprint 024 cited "Gerhard Frey"'s by accident).
                print(f'wiki_cite: "{name}" is a disambiguation page: cite the article meant', file=sys.stderr)
                continue
            if name != t and name.lower() != t.lower().replace('_', ' '):
                print(f'wiki_cite: "{t}" is cited as "{name}"', file=sys.stderr)
            rev = page['revisions'][0]
            out[t] = (name, rev['revid'], rev['timestamp'][:10])
            if about is not None:
                about[name] = (page.get('pageprops', {}).get('wikibase-shortdesc', ''),
                               untex(' '.join(page.get('extract', '').split())))
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
        if tag == 'math':
            # A formula once, as its TeX: its MathML would come out a token to a line (sprint 024).
            tex = (dict(attrs).get('alttext') or '').strip()
            tex = re.sub(r'^\{\\displaystyle\s*(.*)\}$', r'\1', tex, flags=re.S).strip()
            if not self.skipping and tex:
                self.out.append(f' ${tex}$ ')
            self.stack.append((tag, True))
            self.skipping += 1
            return
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


def readable(html_text):
    p = _Text()
    p.feed(html_text)
    return p.text()


def revision_text(revid, lang='en'):
    """The readable text of one revision, from the API's parse of exactly that revision."""
    query = urllib.parse.urlencode({'action': 'parse', 'oldid': revid, 'prop': 'text', 'format': 'json',
                                    'disableeditsection': 1, 'disabletoc': 1})
    return readable(get(f'{api(lang)}?{query}')['parse']['text']['*'])


def citation(title, revid, date, accessed, lang='en'):
    return {
        'kind': 'wikipedia',
        'title': title,
        'url': f'https://{lang}.wikipedia.org/w/index.php?title={quote(title)}&oldid={revid}',
        # Another language's Wikipedia says which (docs/design.md §Citations, sprint 027).
        **({'language': lang} if lang != 'en' else {}),
        'accessed': accessed,
        'authors': [{'name': 'Wikipedia contributors'}],
        'container': 'Wikipedia, The Free Encyclopedia',
        'publisher': 'Wikimedia Foundation',
        'published': date,
    }


def text_name(title, lang='en'):
    """The --text file for a title: another language's text carries its code, so German
    "Luis Agote" does not overwrite the English one (sprint 028)."""
    return title.replace('/', '_') + ('' if lang == 'en' else f'.{lang}') + '.txt'


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('titles', nargs='+')
    # UTC, as the revision dates are: a local date put `published` a day after `accessed` in the
    # evening west of Greenwich (sprint 049).
    ap.add_argument('--accessed', default=datetime.datetime.now(datetime.timezone.utc).date().isoformat())
    ap.add_argument('--text', metavar='DIR', help="also write each revision's readable text to DIR/<Title>.txt")
    ap.add_argument('--lang', default='en', help="the Wikipedia's language code (default en): de cites de.wikipedia.org")
    ap.add_argument('--expect', metavar='WORD',
                    help='warn, and exit 1, for an article whose description and first line lack this word '
                         '(a title may carry its own: "Title=word")')
    a = ap.parse_args()
    if not re.fullmatch(r'[a-z][a-z-]*', a.lang):
        ap.error('--lang is a Wikipedia language code, like de')
    asked = expectations(a.titles, a.expect)
    a.titles = [t for t, _ in asked]
    about = {}
    revs = revisions(a.titles, a.lang, about)
    seen, found = set(), []  # titles that redirect to one article give one citation
    for t in a.titles:
        if t in revs and revs[t][0] not in seen:
            seen.add(revs[t][0])
            found.append(t)
    if a.text:
        os.makedirs(a.text, exist_ok=True)
        for t in found:
            name, revid, _ = revs[t]
            path = os.path.join(a.text, text_name(name, a.lang))
            with open(path, 'w') as fh:
                fh.write(f'{name} (revision {revid})\n\n' + revision_text(revid, a.lang))
            print(f'wiki_cite: wrote {path}', file=sys.stderr)
    print(json.dumps([citation(*revs[t], a.accessed, a.lang) for t in found], indent='\t', ensure_ascii=False))
    doubtful = mismatches(asked, revs, about)
    for why in doubtful:
        print(f'wiki_cite: warning: {why}', file=sys.stderr)
    if len(revs) < len(a.titles) or doubtful:
        sys.exit(1)  # the others are printed; a missing article, a disambiguation page or a namesake is still an error


def mismatches(asked, revs, about):
    """The --expect warnings: each asked title whose article does not say its keyword, naming the
    article it landed on."""
    out = []
    for t, keyword in asked:
        if t in revs:
            name = revs[t][0]
            description, first_line = about.get(name, ('', ''))
            why = article_mismatch(name, description, first_line, keyword)
            if why:
                out.append(why if name == t else f'"{t}" landed on {why}')
    return out


if __name__ == '__main__':
    main()
