"""Wikipedia citations pinned to a revision, for a frame's `citations`.

    python3 create-tools/wiki-cite/wiki_cite.py [--accessed YYYY-MM-DD] Title ...

Prints a JSON list, one kloom `wikipedia` citation per title, each pointing
at the article's current revision (`oldid=`) and dated by it. Redirects are
followed; a missing article is an error. Standard library only.
"""
import argparse, datetime, json, sys, time, urllib.error, urllib.parse, urllib.request

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
                sys.exit(f'wiki_cite: no article "{t}"')
            rev = page['revisions'][0]
            out[t] = (name, rev['revid'], rev['timestamp'][:10])
    return out


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
    a = ap.parse_args()
    revs = revisions(a.titles)
    print(json.dumps([citation(*revs[t], a.accessed) for t in a.titles], indent='\t', ensure_ascii=False))


if __name__ == '__main__':
    main()
