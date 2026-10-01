"""Images from Wikimedia Commons for a reading, with their `media` citation.

    python3 create-tools/commons-media/commons_media.py search "Mark I perceptron"
    python3 create-tools/commons-media/commons_media.py fetch "File:Name.jpg" FRAME_DIR [--as NAME] [--width 960]

`search` lists matching file pages with their licence, so you can pick one
you may use. `fetch` downloads a scaled copy into the frame's directory and
prints the kloom `media` citation for it: title, file page, author, date,
licence and file name, taken from the file page's own metadata. Read the
file page anyway: Commons metadata is what uploaders typed, and the page is
where a licence is really stated. Standard library only.
"""
import argparse, datetime, html, json, os, re, sys, urllib.parse, urllib.request

API = 'https://commons.wikimedia.org/w/api.php'
AGENT = 'kloom-create-tools/1.0 (https://github.com/kenhia/kloom)'
# Licences a reading may carry without asking anyone (docs/design.md §Citations).
# What the reading pane serves (engine/validate.ts MEDIA_FILE).
MIME = {'image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml'}
# Commons serves thumbnails only at these widths, rounding a request up to the next one.
STEPS = [120, 250, 330, 500, 960, 1280, 1920]
# A reading's image larger than this is worth a smaller --width (sprint 006 kept them under it).
LARGE = 350 * 1024
FREE = re.compile(r'^(public domain|pd|cc0|cc by(-sa)? [0-9.]+|cc-by(-sa)?-[0-9.]+)', re.I)


def get(params):
    query = urllib.parse.urlencode({**params, 'format': 'json'})
    req = urllib.request.Request(f'{API}?{query}', headers={'User-Agent': AGENT})
    return json.load(urllib.request.urlopen(req, timeout=30))


def plain(value):
    """Commons metadata is HTML; keep its text."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', str(value or '')))).strip()


def info(titles, width=800):
    data = get({'action': 'query', 'titles': '|'.join(titles), 'prop': 'imageinfo',
                'iiprop': 'url|extmetadata|size|mime', 'iiurlwidth': width})
    for page in data['query']['pages'].values():
        if 'missing' in page or 'imageinfo' not in page:
            yield page['title'], None
            continue
        ii = page['imageinfo'][0]
        meta = {k: plain(v.get('value')) for k, v in ii.get('extmetadata', {}).items()}
        yield page['title'], {**ii, 'meta': meta}


def search(text, limit=12):
    data = get({'action': 'query', 'list': 'search', 'srsearch': text, 'srnamespace': 6,
                'srlimit': limit})
    titles = [r['title'] for r in data['query']['search']]
    for title, i in info(titles) if titles else []:
        if not i or i['mime'] not in MIME:
            continue
        lic = i['meta'].get('LicenseShortName', '?')
        mark = 'ok ' if FREE.match(lic) else '?? '
        print(f'{mark}{title}  [{lic}]  {i["width"]}x{i["height"]}  {i["meta"].get("Artist", "")[:60]}')


def year(meta):
    # Wikidata writes an unknown month or day as 00 ("1913-00-00"), which is not a date: keep the year.
    # A date BC has no form in `published` (four digits, AD): leave it out rather than turn
    # "c. 1504 BC" into AD 1504 (sprint 026).
    if re.search(r'\bB\.?\s?C\.?(E\.?)?(?![a-z])', meta.get('DateTimeOriginal', ''), re.I):
        return None
    m = re.search(r'\b(1[0-9]{3}|20[0-9]{2})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?\b', meta.get('DateTimeOriginal', ''))
    return m.group(0) if m else None


def step(width):
    """The widest thumbnail Commons will actually serve that is no wider than `width`."""
    return max([w for w in STEPS if w <= width] or [STEPS[0]])


def fetch(title, frame_dir, name=None, width=960, accessed=None):
    title = title if title.startswith('File:') else f'File:{title}'
    width = step(width)
    (_, i), = info([title], width)
    if not i:
        sys.exit(f'commons_media: no file "{title}"')
    if i['mime'] not in MIME:
        sys.exit(f'commons_media: "{title}" is {i["mime"]}; pick an image')
    meta = i['meta']
    lic = meta.get('LicenseShortName', '')
    if not FREE.match(lic):
        sys.exit(f'commons_media: "{title}" is licensed "{lic}"; pick a public-domain, CC0 or CC BY(-SA) file')
    # An SVG from elsewhere is served, not inlined, but take Commons' PNG of it anyway: smaller surprises.
    src = i.get('thumburl') if i['width'] > width or i['mime'] == 'image/svg+xml' else i['url']
    ext = os.path.splitext(urllib.parse.urlparse(src).path)[1].lower().replace('.jpeg', '.jpg')
    name = name or re.sub(r'[^a-z0-9]+', '-', os.path.splitext(title[5:])[0].lower()).strip('-')[:48]
    file = f'{name}{ext}'
    req = urllib.request.Request(src, headers={'User-Agent': AGENT})
    body = urllib.request.urlopen(req, timeout=60).read()
    os.makedirs(frame_dir, exist_ok=True)
    with open(os.path.join(frame_dir, file), 'wb') as fh:
        fh.write(body)
    artist = meta.get('Artist') or ''
    # Commons' {{Unknown|author}} template renders its text twice ("Unknown authorUnknown author").
    doubled = re.fullmatch(r'(.+?)\1', artist)
    artist = doubled.group(1) if doubled else artist
    citation = {
        'kind': 'media',
        'title': meta.get('ObjectName') or os.path.splitext(title[5:])[0],
        'url': i['descriptionurl'],
        'accessed': accessed or datetime.date.today().isoformat(),
        'container': 'Via Wikimedia Commons',
        'licence': 'Public domain' if re.match(r'^(public domain|pd)', lic, re.I) else lic,
        'file': file,
    }
    # "Unknown author", "AnonymousUnknown author" (two templates run together, sprint 026), 不明 …
    if artist and not re.search(r'unknown|anonymous|不明', artist, re.I):
        citation['authors'] = [{'name': artist}]
    if year(meta):
        citation['published'] = year(meta)
    print(json.dumps(citation, ensure_ascii=False, indent='\t'))
    print(f'commons_media: wrote {file} ({len(body) // 1024} KB); credit line: {meta.get("Credit", "")[:120]}',
          file=sys.stderr)
    if len(body) > LARGE:
        print(f'commons_media: {file} is over {LARGE // 1024} KB; try a smaller --width '
              f'(Commons serves {", ".join(map(str, STEPS))})', file=sys.stderr)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('search')
    s.add_argument('text')
    f = sub.add_parser('fetch')
    f.add_argument('title')
    f.add_argument('frame_dir')
    f.add_argument('--as', dest='name')
    f.add_argument('--width', type=int, default=960)
    f.add_argument('--accessed')
    a = ap.parse_args()
    if a.cmd == 'search':
        search(a.text)
    else:
        fetch(a.title, a.frame_dir, a.name, a.width, a.accessed)
