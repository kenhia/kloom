"""Sprint 008 (korg 3405): migrate every subject's frames to the new citation form.

    python3 sprints/008-migrate.py [SUBJECTS_DIR] && npx prettier --write SUBJECTS_DIR

Kept with the sprint record, not in the app: it runs once, over the content
as it stood at the start of sprint 008, and is not a tool anyone reruns.

1. Sources become key citations. Each hand-kept source is matched to the
   frame's citation for the same page (a Wikipedia article by title, any
   other page by URL), which gets `"key": true`, and `sources` is dropped.
   Key citations move to the front, in the old Sources order, because the
   Sources list is now derived in citation order. Three sources matched no
   citation; KEY_BY_TITLE and ADD name them.
2. A doi.org URL becomes a structured `doi`.
3. Papers in proceedings and symposium volumes become `chapter`; technical
   reports and system cards become `report` (RECLASSIFY).
4. The two approximate dates that were written into `container` become
   `circa` (CIRCA).
5. A source note that said more than where and when (a page, a judgement)
   becomes the citation's `note` (NOTES).

A frame with no `sources` is already in the new form and is left alone, so
the script can run again over a tree that is partly migrated: the service's
content clone, whose grow branch carries frames grown before sprint 008
(see the sprint record, Deploy). A source that matches no citation stops it.
"""
import glob, json, re, sys
from urllib.parse import parse_qs, unquote, urlparse


def page(url):
    """Which page a URL names: a Wikipedia article by title, anything else by URL."""
    if not url:
        return None
    p = urlparse(url)
    if 'wikipedia.org' in p.netloc:
        title = parse_qs(p.query).get('title', [None])[0] or unquote(p.path.split('/wiki/')[-1])
        return 'wikipedia:' + title.replace(' ', '_')
    return url.rstrip('/').replace('http://', 'https://')


# A source whose citation sits at another URL (the published version of a preprint).
KEY_BY_TITLE = {('token-embeddings', 'Jianlin Su et al., RoFormer'): 'RoFormer:'}

# Sources no citation covered: the citation they needed.
ADD = {
    ('perceptron', 'John C. Hay, Albert E. Murray, Mark I Perceptron'): {
        'kind': 'report',
        'title': 'Mark I Perceptron Operators’ Manual (Project PARA)',
        'url': 'https://apps.dtic.mil/sti/tr/pdf/AD0236965.pdf',
        'accessed': '2026-09-27',
        'authors': [{'family': 'Hay', 'given': 'John C.'}, {'family': 'Murray', 'given': 'Albert E.'}],
        'place': 'Buffalo, NY',
        'publisher': 'Cornell Aeronautical Laboratory',
        'published': '1960-02-15',
    },
    ('metre-survey', 'Ken Alder, The Measure of All Things'): {
        'kind': 'book',
        'title': 'The Measure of All Things: The Seven-Year Odyssey and Hidden Error That Transformed the World',
        'url': 'https://openlibrary.org/works/OL3279069W',
        'accessed': '2026-09-28',
        'authors': [{'family': 'Alder', 'given': 'Ken'}],
        'place': 'New York',
        'publisher': 'Free Press',
        'published': '2002',
    },
}

# A source note carrying more than the citation's own where and when: a page,
# an edition, who wrote it, where it was read. Frame `*` is every frame.
NOTES = {
    ('hebbian-learning', 'The Organization of Behavior'): 'The postulate is on p. 62',
    ('metre-survey', 'The Measure of All Things'): 'The standard history of the Delambre–Méchain survey',
    ('*', "Arthur Samuel's Legacy"): 'Quoting Schaeffer, One Jump Ahead: Challenging Human Supremacy at Checkers (Springer, 1997)',
    ('eliza', 'ELIZA'): 'Read in the scan at web.stanford.edu/class/cs124 and the transcription at csee.umbc.edu',
    ('mechanical-turk', "Maelzel's Chess-Player"): 'Text from the Edgar Allan Poe Society of Baltimore',
    ('perceptron', 'New Navy Device'): 'P. 25 (UPI); via AITopics',
    ('perceptrons-book', 'Perceptrons'): 'Expanded edition 1988',
    ('leibniz', 'Leviathan'): 'Part I, chapter 5; read at Project Gutenberg',
    ('diffusion', 'Getty Images v Stability AI'): 'Judgment of Mrs Justice Joanna Smith, High Court of England and Wales',
    ('*', 'They Used Physics to Find Patterns'): 'Text by Anna Davour',
    ('tokens', 'tiktoken'): 'The GPT-2 tokeniser, used to compute the token ids shown',
    ('ninety-five-theses', 'Printing, Propaganda'): 'The counts of printings and the 1,000-copy assumption',
    ('ninety-five-theses', 'Brand Luther'): 'Lotter, Cranach and the Wittenberg title page',
}

# OpenAI's GPT papers: reports, however each frame first filed them.
OPENAI_REPORTS = ('Language Models Are Unsupervised Multitask Learners',
                  'Improving Language Understanding by Generative Pre-Training')

CHAPTER = re.compile(
    r'Advances in Neural Information Processing Systems|International Conference|'
    r'International Symposium|Conference on|Proceedings of (the )?(\d|NAACL|IEEE/CVF|20\d\d)|'
    r'Paper Symposium|CVPR'
)


def reclassify(c):
    """Proceedings papers to `chapter`; reports and system cards to `report`."""
    cont = c.get('container', '')
    if c['kind'] == 'article' and cont.startswith('arXiv:1512.03385; in 2016 IEEE'):
        # ResNet: cited as the preprint, with the CVPR paper squeezed into container.
        c.update(kind='chapter', published='2016', pages='770–78',
                 container='Proceedings of the 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)')
    elif c['kind'] == 'article' and cont.startswith('Artificial Intelligence: A Paper Symposium'):
        c.update(kind='chapter', container='Artificial Intelligence: A Paper Symposium',
                 place='London', publisher='Science Research Council')
    elif c['kind'] == 'article' and CHAPTER.search(cont):
        c['kind'] = 'chapter'
    elif c['kind'] == 'article' and re.match(r'OpenAI (technical )?report', cont):
        c.update(kind='report', publisher='OpenAI')
        rest = re.sub(r'^OpenAI (technical )?report;?\s*', '', cont)
        if rest:
            c['container'] = rest[0].upper() + rest[1:]
        else:
            del c['container']
    elif c['kind'] in ('web', 'article') and c['title'].lower() in (t.lower() for t in OPENAI_REPORTS):
        c.update(kind='report', publisher='OpenAI')
        if c.get('container') in ('OpenAI', 'OpenAI technical report'):
            del c['container']
    elif c['kind'] == 'article' and c['title'].endswith('Technical Report'):
        c['kind'] = 'report'
    elif c['kind'] == 'web' and (
        c['title'].endswith('System Card')
        or c['title'].startswith('Scientific Background to the Nobel Prize')
        or c['title'].startswith('International AI Safety Report')
        or c['title'].startswith('Frontier Risk Report')
    ):
        c['kind'] = 'report'
        if 'publisher' not in c and cont:
            c['publisher'] = cont
            del c['container']
        elif c['title'].startswith('Scientific Background'):
            c['place'] = 'Stockholm'
            del c['container']


CIRCA = {'Photograph, c. 1951, from': 'Photograph, from', 'Watercolour, c. 1840 (': 'Watercolour ('}


def migrate(path):
    frame_id = path.split('/')[-2]
    d = json.load(open(path))
    if 'sources' not in d:
        return False
    cites = d.get('citations', [])
    by_page = {}
    for c in cites:
        by_page.setdefault(page(c['url']), c)

    keys = []
    for s in d.pop('sources'):
        c = by_page.get(page(s.get('url')))
        for (fid, prefix), title in KEY_BY_TITLE.items():
            if fid == frame_id and s['title'].startswith(prefix):
                c = next(x for x in cites if x['title'].startswith(title))
        for (fid, prefix), new in ADD.items():
            if fid == frame_id and s['title'].startswith(prefix):
                c = dict(new)
                cites.append(c)
        if c is None:
            sys.exit(f'{path}: source "{s["title"]}" matches no citation')
        if c not in keys:
            keys.append(c)
    for c in keys:
        c['key'] = True
    d['citations'] = keys + [c for c in cites if c not in keys]

    for c in d['citations']:
        m = re.match(r'https?://(dx\.)?doi\.org/(.+)$', c.get('url', ''))
        if m:
            c['doi'] = unquote(m.group(2))
            del c['url']
        reclassify(c)
        for old, new in CIRCA.items():
            if old in c.get('container', ''):
                c['container'] = c['container'].replace(old, new)
                c['circa'] = True
        for (fid, prefix), note in NOTES.items():
            if fid in (frame_id, '*') and c['title'].startswith(prefix) and c.get('key'):
                c['note'] = note

    # The flag and the DOI read best beside what they qualify.
    first = ['kind', 'key', 'title', 'url', 'doi']
    d['citations'] = [{**{k: c[k] for k in first if k in c}, **c} for c in d['citations']]

    with open(path, 'w') as fh:
        json.dump(d, fh, ensure_ascii=False, indent='\t')
        fh.write('\n')
    return True


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else 'subjects'
    paths = sorted(glob.glob(f'{root}/*/frames/*/frame.json'))
    done = [p for p in paths if migrate(p)]
    print(f'migrated {len(done)} of {len(paths)} frames', file=sys.stderr)
