#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow>=10"]
# ///
"""Images from Wikimedia Commons for a reading, with their `media` citation.

    python3 create-tools/commons-media/commons_media.py search "Mark I perceptron"
    python3 create-tools/commons-media/commons_media.py fetch "File:Name.jpg" FRAME_DIR [--as NAME] [--width 960] [--page N]
    uv run create-tools/commons-media/commons_media.py fetch "File:Name.png" FRAME_DIR --jpeg
    uv run create-tools/commons-media/commons_media.py jpeg page.png FRAME_DIR/page.jpg
    create-tools/commons-media/commons_media.py crop scan.png FRAME_DIR/page.jpg --box 120,80,1480,2100 [--width 960]

`search` lists matching file pages with their licence, so you can pick one
you may use. `fetch` downloads a scaled copy into the frame's directory and
prints the kloom `media` citation for it: title, file page, author, date,
licence and file name, taken from the file page's own metadata, and says on
stderr the exact licence tags the page carries (PD-Art, PD-old-100, …).
`--page N` takes one page of a PDF or DjVu as a JPEG. `--jpeg`, and the
`jpeg` command for a page you cropped yourself, convert to JPEG, a PNG's
transparency composited onto white first. `crop` cuts a box (left, top,
right, bottom, in the image's pixels) out of a page image from outside
Commons, a scan from the Internet Archive or a library, scales it to
`--width` and writes a JPEG (sprint 029). Read the file page anyway: Commons
metadata is what uploaders typed, and the page is where a licence is really
stated.

Two licences need a word more (sprint 029). Flickr's "No restrictions" (the
Internet Archive's book scans, the Smithsonian's photographs) is taken as
public domain with a warning, and the citation's `note` is left empty, which
the gate refuses until it states the public-domain basis ("Published in the
US in 1904"). A `PD-self` file with no author credits its uploader, "Name
(uploader)": the uploader is who released it.

Standard library only, except the JPEG conversion: Pillow, declared in the
metadata above. The script runs itself under `uv run --script` (its
shebang), and a command that converts to JPEG, run with a plain `python3`
that lacks Pillow, runs itself again under `uv` (korg 3404, sprint 029).
"""
import argparse, datetime, html, io, json, os, re, sys, urllib.parse, urllib.request

API = 'https://commons.wikimedia.org/w/api.php'
AGENT = 'kloom-create-tools/1.0 (https://github.com/kenhia/kloom)'
# Licences a reading may carry without asking anyone (docs/design.md §Citations).
# What the reading pane serves (engine/validate.ts MEDIA_FILE).
MIME = {'image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml'}
# A scanned book on Commons, whose pages Commons renders as JPEGs (`--page`).
PAGED = {'application/pdf', 'image/vnd.djvu'}
# Commons serves thumbnails only at these widths, rounding a request up to the next one.
STEPS = [120, 250, 330, 500, 960, 1280, 1920]
# A reading's image larger than this is worth a smaller --width (sprint 006 kept them under it).
LARGE = 350 * 1024
FREE = re.compile(r'^(public domain|pd|cc0|cc by(-sa)? [0-9.]+|cc-by(-sa)?-[0-9.]+)', re.I)
# Flickr's "no known copyright restrictions", Commons' short name for it: public domain only on a stated basis.
NO_RESTRICTIONS = re.compile(r'^no (known copyright )?restrictions$', re.I)


def get(params):
    query = urllib.parse.urlencode({**params, 'format': 'json'})
    req = urllib.request.Request(f'{API}?{query}', headers={'User-Agent': AGENT})
    return json.load(urllib.request.urlopen(req, timeout=30))


def plain(value):
    """Commons metadata is HTML; keep its text."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', str(value or '')))).strip()


def info(titles, width=800, page=None):
    params = {'action': 'query', 'titles': '|'.join(titles), 'prop': 'imageinfo|templates',
              'iiprop': 'url|extmetadata|size|mime', 'iiurlwidth': width, 'tlnamespace': 10, 'tllimit': 'max'}
    if page:
        params['iiurlparam'] = f'page{page}-{width}px'
    data = get(params)
    for p in data['query']['pages'].values():
        if 'missing' in p or 'imageinfo' not in p:
            yield p['title'], None
            continue
        ii = p['imageinfo'][0]
        meta = {k: plain(v.get('value')) for k, v in ii.get('extmetadata', {}).items()}
        yield p['title'], {**ii, 'meta': meta, 'tags': licence_tags(t['title'] for t in p.get('templates', []))}


# The templates that are a licence, not their machinery: "PD-old-100", not "PD-old-text" or "PD-Art/layout".
TAG = re.compile(r'^Template:((?:PD|Cc|CC|GFDL|FAL|Attribution|Copyrighted free use|Flickr-no known copyright)[-\w. ]*)$')
MACHINERY = re.compile(r'-(text|layout|category|warning|footer|core|expired-text)$|^Cc-pd-mark', re.I)


def licence_tags(templates):
    """The licence tags a file page carries, as Commons names them (sprint 025: "public domain" hid
    PD-Japan-oldphoto on a Frankfurt photograph, and PD-USGov-DOE on a contractor's lab)."""
    out = []
    for t in templates:
        m = TAG.match(t)
        if m and '/' not in t and not MACHINERY.search(m.group(1)) and m.group(1) not in out:
            out.append(m.group(1))
    return out


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


# "c. 1504 BC", "circa 1890", never the C. of "b.C.": a word of its own, before a number.
# Two dates joined by a slash, a dash, "to", or "between … and" (NARA's form, sprint 030): a span,
# which the fetch says it wrote as circa its start.
RANGE = re.compile(r'\b(1[0-9]{3}|20[0-9]{2})(?:-[0-9]{2}){0,2}\s*(?:/|–|—| to |(?<=\d) and (?=\d))\s*(?:1[0-9]{3}|20[0-9]{2})\b')
CIRCA = re.compile(r'(?<![\w.])(c\.|ca\.|circa|about|approx(\.|imately)?)\s*(?=\d)', re.I)


def year(meta):
    """`published` and whether it is approximate, from the file's date: (date, circa) or (None, False).

    Wikidata writes an unknown month or day as 00 ("1913-00-00"), which is not a date: keep the year.
    A date BC is written "1504 BC", the form `published` takes since sprint 027; sprint 026 found the
    tool turning "c. 1504 BC" into AD 1504."""
    when = meta.get('DateTimeOriginal', '')
    circa = bool(CIRCA.search(when))
    span = RANGE.search(when)
    if span:  # a range ("1941-01-01/1945-12-31") is not its first day (sprint 028): its first year, circa
        return span.group(1), True
    bc = re.search(r'\b([1-9][0-9]{0,5})\s*B\.?\s?C\.?(E\.?)?(?![a-z])', when, re.I)
    if bc:
        return f'{bc.group(1)} BC', circa
    m = re.search(r'\b(1[0-9]{3}|20[0-9]{2})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?\b', when)
    if m:
        return m.group(0), circa
    ad = re.search(r'\b(?:AD|A\.D\.)\s*([1-9][0-9]{0,2})\b|\b([1-9][0-9]{0,2})\s*(?:AD|A\.D\.|CE|C\.E\.)(?![a-z])', when)
    if ad:
        return ad.group(1) or ad.group(2), circa
    return None, False


# Boilerplate where an author should be: unknown authors in several templates and languages, and
# what a scanner or an uploader typed (sprint 024 met a scanner model as the author).
NO_AUTHOR = re.compile(r'unknown|anonymous|不明|unbekannt|inconnu|not provided|own work|scann(ed|er)|'
                       r'internet archive book images|'
                       r'\b(canon|epson|nikon|hp scanjet|fujitsu)\b|see (below|source)', re.I)


# Words that make an Artist field an organisation, not a person: sprint 028 met "Smithsonian
# Institution", "NASA Johnson Space Center" and "Colegio de Fonseca" split into family and given.
ORG = re.compile(r'&|\b(Inc|Ltd|Co|Company|Museum|Library|University|Society|Archives?|Institution|Institute|'
                 r'Cent(er|re)|Colegio|College|School|Academy|Agency|Laborator(y|ies)|Department|Office|Service|'
                 r'Navy|Army|Corps|Command|Administration|Bureau|Ministry|Council|Foundation|Hospital|'
                 r'Collection|Gallery|Studio)\b')


def clean_title(name):
    """The ObjectName without the Wikidata template text the Google Art Project's files carry after it
    ("The Royal Family, Osborne 1857title QS:P1476,en:…", sprint 028)."""
    return re.sub(r'\s*(?:title\s*)?QS:P\d+.*$', '', name or '').strip()


def authors(artist):
    """The citation's `authors` from Commons' Artist field: [] when it is boilerplate, a person
    ("Richard Marsden (1859-1938)") as family and given names, anything else as a name."""
    artist = re.sub(r'\s*Details on Google Art Project\s*$', '', artist)  # the Art Project's link text
    artist = re.sub(r'\s*\((?:[^()]*\d{3,4}[^()]*)\)\s*$', '', artist).strip()  # life dates
    if not artist or NO_AUTHOR.search(artist):
        return []
    words = artist.split()
    person = 2 <= len(words) <= 4 and all(re.fullmatch(r"[A-Z][\w'’.-]*\.?|(van|von|de|da|der|du|la)", w)
                                          for w in words) and not ORG.search(artist)
    if person:
        return [{'family': words[-1], 'given': ' '.join(words[:-1])}]
    return [{'name': artist}]


def licence_for(lic):
    """(the citation's licence, whether its note must state a public-domain basis), or None if not free."""
    if NO_RESTRICTIONS.match(lic.strip()):
        return 'Public domain', True
    if not FREE.match(lic):
        return None
    return ('Public domain' if re.match(r'^(public domain|pd)', lic, re.I) else lic), False


def uploader_credit(tags, who, uploader):
    """A `PD-self` file's author when the page gives none: its uploader, who released it."""
    if who or not uploader or not any(t.lower().startswith('pd-self') for t in tags):
        return who
    return [{'name': f'{uploader} (uploader)'}]


def first_uploader(title):
    """Who uploaded the file's first version (imageinfo lists newest first)."""
    data = get({'action': 'query', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'user', 'iilimit': 50})
    for p in data['query']['pages'].values():
        versions = p.get('imageinfo') or []
        return versions[-1].get('user') if versions else None


def to_jpeg(body, quality=85, box=None, width=None):
    """A JPEG of an image's bytes, any transparency composited onto white (sprint 026: a PNG with an
    alpha channel turned black when converted as it was)."""
    from PIL import Image  # Pillow: only this conversion needs it (main() runs the tool under uv for it)
    im = Image.open(io.BytesIO(body))
    if box:
        im = im.crop(box)
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        white = Image.new('RGB', im.size, 'white')
        white.paste(im, mask=im.getchannel('A'))
        im = white
    elif im.mode != 'RGB':
        im = im.convert('RGB')
    out = io.BytesIO()
    im.save(out, 'JPEG', quality=quality, optimize=True, progressive=True)
    return out.getvalue()


def step(width):
    """The widest thumbnail Commons will actually serve that is no wider than `width`."""
    return max([w for w in STEPS if w <= width] or [STEPS[0]])


def fetch(title, frame_dir, name=None, width=960, accessed=None, page=None, jpeg=False):
    title = title if title.startswith('File:') else f'File:{title}'
    width = step(width)
    (_, i), = info([title], width, page)
    if not i:
        sys.exit(f'commons_media: no file "{title}"')
    if i['mime'] in PAGED and not page:
        sys.exit(f'commons_media: "{title}" is {i["mime"]}; name a page with --page N')
    if i['mime'] not in MIME and i['mime'] not in PAGED:
        sys.exit(f'commons_media: "{title}" is {i["mime"]}; pick an image')
    meta = i['meta']
    lic = meta.get('LicenseShortName', '')
    free = licence_for(lic)
    if not free:
        sys.exit(f'commons_media: "{title}" is licensed "{lic}"; pick a public-domain, CC0 or CC BY(-SA) file')
    licence, needs_basis = free
    # An SVG from elsewhere is served, not inlined, but take Commons' PNG of it anyway: smaller surprises.
    # A PDF or DjVu page is only ever its rendering.
    paged = i['mime'] in PAGED
    src = i.get('thumburl') if paged or i['width'] > width or i['mime'] == 'image/svg+xml' else i['url']
    ext = os.path.splitext(urllib.parse.urlparse(src).path)[1].lower().replace('.jpeg', '.jpg')
    name = name or re.sub(r'[^a-z0-9]+', '-', os.path.splitext(title[5:])[0].lower()).strip('-')[:48]
    if paged and not name.endswith(f'-p{page}'):
        name = f'{name}-p{page}'
    req = urllib.request.Request(src, headers={'User-Agent': AGENT})
    body = urllib.request.urlopen(req, timeout=60).read()
    if jpeg and ext != '.jpg':
        body, ext = to_jpeg(body), '.jpg'
    file = f'{name}{ext}'
    os.makedirs(frame_dir, exist_ok=True)
    with open(os.path.join(frame_dir, file), 'wb') as fh:
        fh.write(body)
    artist = meta.get('Artist') or ''
    # Commons' {{Unknown|author}} template renders its text twice ("Unknown authorUnknown author").
    doubled = re.fullmatch(r'(.+?)\1', artist)
    artist = doubled.group(1) if doubled else artist
    # No `container`: "Via Wikimedia Commons" was boilerplate every author rewrote (13 in sprint 025).
    # Where the work is from (a museum, a book) is the container, and only the file page says it.
    citation = {
        'kind': 'media',
        'title': clean_title(meta.get('ObjectName')) or os.path.splitext(title[5:])[0],
        'url': i['descriptionurl'] + (f'?page={page}' if paged else ''),
        'accessed': accessed or datetime.date.today().isoformat(),
        'licence': licence,
        'file': file,
    }
    if needs_basis:  # left empty on purpose: the gate refuses an empty note until the basis is written
        citation['note'] = ''
    who = authors(artist)
    if not who and any(t.lower().startswith('pd-self') for t in i['tags']):
        who = uploader_credit(i['tags'], who, first_uploader(title))
    if who:
        citation['authors'] = who
    published, circa = year(meta)
    if RANGE.search(meta.get('DateTimeOriginal', '')):
        print(f"commons_media: the date is a span ({plain(meta.get('DateTimeOriginal'))}); written as circa its first "
              'year: check it', file=sys.stderr)
    if published:
        citation['published'] = published
        if circa:
            citation['circa'] = True
    print(json.dumps(citation, ensure_ascii=False, indent='\t'))
    say = lambda line: print(f'commons_media: {line}', file=sys.stderr)  # noqa: E731
    say(f'wrote {file} ({len(body) // 1024} KB)' + (f', page {page} of {i.get("pagecount", "?")}' if paged else ''))
    say(f'licence tags on the file page: {", ".join(i["tags"]) or "none found; read the page"}')
    if needs_basis:
        say(f'"{lic}" is Flickr\'s "no known copyright restrictions", not a licence: written as public domain, '
            'with an empty note the gate refuses. Write the basis in it (published in the US before 1931, a US '
            'government work, …), from the work itself, not the Flickr page')
    if who and who[0].get('name', '').endswith(' (uploader)'):
        say(f'author written as the uploader, {who[0]["name"]}: the file is PD-self and names no author')
    if not who:
        say(f'no author written: the page gives "{artist or "nothing"}"; add one by hand if it is known')
    elif who[0].get('name'):
        say(f'author written as a name, "{who[0]["name"]}": make it family and given if it is a person')
    say('no container written: add where the work is from (a museum, a book), from the file page')
    if meta.get('Credit'):
        say(f'credit line: {meta["Credit"][:120]}')
    if len(body) > LARGE:
        print(f'commons_media: {file} is over {LARGE // 1024} KB; try a smaller --width '
              f'(Commons serves {", ".join(map(str, STEPS))})', file=sys.stderr)


def jpeg(src, dest, quality=85, box=None, width=None):
    """Convert a file you cropped yourself (a scan's page) to a JPEG, transparency onto white; with `box`,
    crop it first, and with `width`, scale it down to that."""
    with open(src, 'rb') as fh:
        body = to_jpeg(fh.read(), quality, box, width)
    with open(dest, 'wb') as fh:
        fh.write(body)
    print(f'commons_media: wrote {dest} ({len(body) // 1024} KB)', file=sys.stderr)
    if len(body) > LARGE:
        print(f'commons_media: {dest} is over {LARGE // 1024} KB; scale it down or lower --quality', file=sys.stderr)


def box_arg(text):
    """`left,top,right,bottom` in pixels."""
    parts = [int(p) for p in text.split(',')]
    if len(parts) != 4 or parts[0] >= parts[2] or parts[1] >= parts[3]:
        raise argparse.ArgumentTypeError('a box is left,top,right,bottom in pixels, right of left and below top')
    return tuple(parts)


def needs_pillow(a):
    return a.cmd in ('jpeg', 'crop') or (a.cmd == 'fetch' and a.jpeg)


def under_uv(argv):
    """Run this script again under `uv run --script`, which installs Pillow from its metadata, when a
    command needs Pillow and this Python lacks it (sprint 029: `--jpeg` worked only under `uv run`)."""
    try:
        import PIL  # noqa: F401
        return
    except ImportError:
        pass
    if os.environ.get('COMMONS_MEDIA_UNDER_UV'):
        sys.exit('commons_media: Pillow is missing even under uv run; install uv, or Pillow')
    os.environ['COMMONS_MEDIA_UNDER_UV'] = '1'
    try:
        os.execvp('uv', ['uv', 'run', '--quiet', '--script', os.path.abspath(__file__), *argv])
    except FileNotFoundError:
        sys.exit('commons_media: converting to JPEG needs Pillow; install uv (or Pillow) and run again')


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
    f.add_argument('--page', type=int, help='a PDF or DjVu: the page to take, as a JPEG')
    f.add_argument('--jpeg', action='store_true', help='convert to JPEG, transparency onto white')
    j = sub.add_parser('jpeg', help='convert an image you cropped to JPEG, transparency onto white')
    j.add_argument('src')
    j.add_argument('dest')
    j.add_argument('--quality', type=int, default=85)
    c = sub.add_parser('crop', help='cut a box out of a page image from outside Commons, as a JPEG')
    c.add_argument('src')
    c.add_argument('dest')
    c.add_argument('--box', type=box_arg, required=True, metavar='LEFT,TOP,RIGHT,BOTTOM')
    c.add_argument('--width', type=int, default=960, help='scale down to at most this wide (default 960)')
    c.add_argument('--quality', type=int, default=85)
    a = ap.parse_args()
    if needs_pillow(a):
        under_uv(sys.argv[1:])
    if a.cmd == 'search':
        search(a.text)
    elif a.cmd == 'jpeg':
        jpeg(a.src, a.dest, a.quality)
    elif a.cmd == 'crop':
        jpeg(a.src, a.dest, a.quality, a.box, a.width)
    else:
        fetch(a.title, a.frame_dir, a.name, a.width, a.accessed, a.page, a.jpeg)
