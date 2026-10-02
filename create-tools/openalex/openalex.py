"""OpenAlex, with the homelab's API key, for an author with a shell.

    python3 create-tools/openalex/openalex.py work <doi | W-id | URL> [--json]
    python3 create-tools/openalex/openalex.py search "<query>" [--per-page N] [--json]
    python3 create-tools/openalex/openalex.py raw <path?query>

`work` prints one paper: title, year, venue, DOI, authors, whether it is
open access and where (`oa_url` and every location), and its abstract,
rebuilt from OpenAlex's inverted index. `search` lists matching works with
the same open-access facts. `raw` prints the JSON of any API path (e.g.
`raw "works?filter=doi:10.1038/171737a0"`). `--json` prints the record
instead of the summary.

The key is OPENALEX_API_KEY, from the environment or else from the host's
/etc/khomelab/secrets.env, the one copy the homelab keeps (k-homelab
`openalex-api-key`; krot registry/openalex.toml). It is added to each
request and **never printed**: not in output, not in an error, not in a
URL echoed back. Without a key the tool still runs, on OpenAlex's shared
anonymous budget, and says so on stderr. Standard library only.
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

API = 'https://api.openalex.org/'
AGENT = 'kloom-create-tools/1.0 (https://github.com/kenhia/kloom)'
SECRETS = '/etc/khomelab/secrets.env'
KEY = 'OPENALEX_API_KEY'


def read_env_file(path, key=KEY):
    """The value of `key` in a KEY='value' env file, one matching pair of quotes stripped; None if absent."""
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if line.startswith(key + '='):
                    v = line[len(key) + 1:]
                    if len(v) > 1 and v[0] in '\'"' and v[-1] == v[0]:
                        v = v[1:-1]
                    return v or None
    except OSError:
        return None
    return None


def api_key(environ=os.environ, path=SECRETS):
    return environ.get(KEY) or read_env_file(path)


def redact(text, key):
    """`text` with the key, raw or URL-encoded, replaced."""
    if not key:
        return text
    for form in {key, urllib.parse.quote(key, safe='')}:
        text = text.replace(form, '<key>')
    return text


def url_for(path, key=None):
    """The API URL for `path`, with api_key added when there is one."""
    url = API + path.lstrip('/')
    if key:
        url += ('&' if '?' in url else '?') + 'api_key=' + urllib.parse.quote(key, safe='')
    return url


def work_path(ref):
    """An API path for a DOI (bare, doi:, or doi.org URL), an OpenAlex W-id, or an openalex.org URL."""
    ref = ref.strip()
    m = re.match(r'^(?:https?://)?(?:dx\.)?doi\.org/(.+)$', ref, re.I) or re.match(r'^doi:(.+)$', ref, re.I)
    if m:
        return 'works/doi:' + m.group(1)
    if re.match(r'^10\.\d{4,9}/\S+$', ref):
        return 'works/doi:' + ref
    m = re.match(r'^(?:https?://)?(?:api\.)?openalex\.org/(?:works/)?(W\d+)$', ref, re.I)
    if m:
        return 'works/' + m.group(1).upper()
    if re.match(r'^W\d+$', ref, re.I):
        return 'works/' + ref.upper()
    raise ValueError(f'not a DOI or an OpenAlex work id: {ref}')


def abstract(inverted):
    """The abstract text from OpenAlex's abstract_inverted_index, or None."""
    if not inverted:
        return None
    words = {}
    for word, positions in inverted.items():
        for p in positions:
            words[p] = word
    return ' '.join(words[p] for p in sorted(words))


def get(path, key, tries=5):
    """JSON for an API path, waiting out a rate limit a few times. Errors never carry the key."""
    url = url_for(path, key)
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': AGENT})
            return json.load(urllib.request.urlopen(req, timeout=30))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < tries - 1:
                time.sleep(min(int(e.headers.get('Retry-After') or 2 ** attempt), 60))
                continue
            body = e.read().decode('utf-8', 'replace')[:300]
            raise SystemExit(redact(f'openalex: HTTP {e.code} for {url_for(path)}: {body}', key))
        except urllib.error.URLError as e:
            raise SystemExit(redact(f'openalex: {e.reason} for {url_for(path)}', key))


def summary(w):
    oa = w.get('open_access') or {}
    src = ((w.get('primary_location') or {}).get('source') or {})
    lines = [
        w.get('display_name') or '(untitled)',
        f"  {w.get('publication_year')} · {src.get('display_name') or 'no venue'} · {w.get('type')}",
        f"  doi: {w.get('doi') or '-'}   openalex: {w.get('id')}",
        '  authors: ' + (', '.join(a['author']['display_name'] for a in w.get('authorships', [])[:8]) or '-'),
        f"  open access: {oa.get('oa_status') or 'unknown'}" + (f" — {oa['oa_url']}" if oa.get('oa_url') else ''),
    ]
    for loc in w.get('locations') or []:
        if loc.get('is_oa') and loc.get('landing_page_url'):
            lines.append(f"    open copy: {loc.get('pdf_url') or loc['landing_page_url']} ({loc.get('version') or 'version unknown'})")
    text = abstract(w.get('abstract_inverted_index'))
    if text:
        lines.append('  abstract: ' + text)
    return '\n'.join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    w = sub.add_parser('work'); w.add_argument('ref'); w.add_argument('--json', action='store_true')
    s = sub.add_parser('search'); s.add_argument('query'); s.add_argument('--per-page', type=int, default=10)
    s.add_argument('--json', action='store_true')
    r = sub.add_parser('raw'); r.add_argument('path')
    a = p.parse_args(argv)

    key = api_key()
    if not key:
        print(f'openalex: no {KEY} (environment or {SECRETS}); using the shared anonymous budget', file=sys.stderr)

    if a.cmd == 'raw':
        print(redact(json.dumps(get(a.path, key), indent=1, ensure_ascii=False), key))
        return 0
    if a.cmd == 'work':
        try:
            path = work_path(a.ref)
        except ValueError as e:
            print(f'openalex: {e}', file=sys.stderr)
            return 2
        rec = get(path, key)
        print(redact(json.dumps(rec, indent=1, ensure_ascii=False) if a.json else summary(rec), key))
        return 0
    q = urllib.parse.urlencode({'search': a.query, 'per-page': a.per_page})
    res = get('works?' + q, key)
    if a.json:
        print(redact(json.dumps(res, indent=1, ensure_ascii=False), key))
    else:
        print(redact('\n\n'.join(summary(x) for x in res.get('results', [])) or 'no results', key))
    return 0


if __name__ == '__main__':
    sys.exit(main())
