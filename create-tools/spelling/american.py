#!/usr/bin/env python3
"""American spelling for kloom's own words (korg 3521, sprint 044).

kloom writes in American English; what it quotes keeps its own spelling. This
finds British spellings in kloom's prose and changes them, and leaves alone
what is not kloom's to respell:

- quotations: block quotes, and "double-quoted" or “curly-quoted” spans;
- titles of works: italics with a capital in them (`_Notes on Nursing_`); an
  italic in lower case is a term kloom introduces, and is kloom's words;
- proper names: a capitalized word that does not start a sentence (`Royal
  College of Nursing`, a mark's `[Metre Convention](kloom:e/...)`), and the
  phrases in KEEP (`Ministry of Defence` where it starts a sentence or is all
  caps on a scene). A name's mark on a common noun (`[haemophilia](...)`) is
  kloom's words: its mark spec in `create-tools/names/examples` changes with
  it (`american.py apply` does both);
- citation fields, code, link targets, URLs and HTML.

It knows a word only from WORDS: a spelling it has not been told about is
never changed. `suspects` lists the words that look British and WORDS does not
hold, so the list can grow by review rather than by guessing.

    american.py report  [paths...]      every hit, what would change and what is skipped, and why
    american.py apply   [paths...]      make the changes `report` marks `change`
    american.py check   [paths...]      exit 1 if anything would change (a gate)
    american.py suspects [paths...]     words that look British and are not in WORDS

A path is a file or a directory, walked for the files below; the default is
`subjects` and `names`. What is read in each:

- `reading.md`, any `.md`: the prose, as above;
- `frame.json`: topic, the scene's words, position labels, connections' why,
  edits' summaries; never citations;
- `spine.json`, a trail: section and trail titles;
- `subject.json`: title and subtitle;
- a name file: its description, never its name or aliases;
- `.svg`: the words of each `<text>`;
- `.svelte`: the markup's words and its aria-label, title, alt and
  placeholder attributes, not the script or style.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# The words. Each family is written once and its forms generated, so that
# `organise` brings `organised`, `organising`, `organisation`, `reorganise`...


def _forms(pairs, suffixes):
    out = {}
    for gb, us in pairs:
        for s in suffixes:
            out[gb + s] = us + s
    return out


WORDS = {}

# -ise → -ize, -isation → -ization. A stem is what comes before `ise`.
_IZE = '''
agon apolog atom author bowdler canal capital caramel carbon carbur categor central character
civil colon commercial computer critic crystall decentral demobil democrat
digit dramat econom emphas energ epitom equal evangel familiar fantas fertil
final formal fossil fratern galvan general global harmon homogen hospital
human hypothes ideal immobil immun individual industrial institutional ion
ital jeopard legal legitim liberal local magnet marginal material maxim mechan memor factor
mesmer metabol militar miniatur minim mobil modern monopol moral motor
national natural neutral normal optim organ ostrac oxid pallet pasteur patron penal plastic quant rugged sanit sensit token transistor
personal philosoph plagiar polar popular pressur prior privat public
radical random rational real recogn regular revolution romantic satir
scandal secular sensational serial social special stabil standard steril
stigmat subsid summar symbol sympath synchron synthes systemat tantal
terror theor tranquil trivial unional urban util vandal vapor vers
vocal vulcan western woman
'''.split()
_IZE_SUFFIXES = ['ise', 'ised', 'ises', 'ising', 'isation', 'isations', 'iser', 'isers', 'isable']
for stem in _IZE:
    for prefix in ['', 're', 'un', 'de', 'non', 'over', 'mis']:
        for s in _IZE_SUFFIXES:
            WORDS[prefix + stem + s] = prefix + stem + s.replace('is', 'iz', 1)

# -yse → -yze (`analyses` is left: it is the plural of analysis too).
for stem in ['anal', 'paral', 'catal', 'hydrol', 'electrol', 'dial', 'psychoanal']:
    for s in ['yse', 'ysed', 'ysing', 'yser', 'ysers']:
        WORDS[stem + s] = stem + s.replace('ys', 'yz', 1)
WORDS['catalyses'] = 'catalyzes'
WORDS['paralyses'] = 'paralyzes'
WORDS['hydrolyses'] = 'hydrolyzes'

# -our → -or. Not hour, four, your, flour, tour, contour, glamour, troubadour...
_OUR = '''
arbour ardour armour behaviour candour clamour colour demeanour endeavour
favour fervour flavour harbour honour humour labour neighbour odour parlour
rancour rigour rumour saviour savour splendour succour tumour valour vapour
vigour
'''.split()
WORDS.update(_forms([(w, w[:-2] + 'r') for w in _OUR],
                    ['', 's', 'ed', 'ing', 'ings', 'ful', 'fully', 'less', 'able', 'ably', 'er', 'ers',
                     'ist', 'ists', 'ite', 'ites', 'hood', 'hoods', 'ly', 'y', 'ation', 'al', 'ally', 'ism']))
for gb in ['colourise', 'colourised', 'colourisation', 'colourant', 'colourants', 'discolour', 'discoloured',
           'discolouration', 'unfavourable', 'unfavourably', 'dishonour', 'dishonoured', 'dishonourable',
           'misbehaviour', 'multicoloured', 'watercolour', 'watercolours', 'labour-saving', 'uncoloured',
           'unflavoured', 'unarmoured']:
    WORDS[gb] = gb.replace('our', 'or').replace('isation', 'ization').replace('ise', 'ize')

# -re → -er.
_RE = '''
calibre centre fibre goitre litre lustre manoeuvre meagre metre mitre nitre
ochre sabre saltpetre sceptre sepulchre sombre spectre theatre
'''.split()
for w in _RE:
    us = w[:-2] + 'er'
    if w == 'manoeuvre':
        us = 'maneuver'
    WORDS[w] = us
    WORDS[w + 's'] = us + 's'
    WORDS[w[:-1] + 'ed'] = us + 'ed'
    WORDS[w[:-1] + 'ing'] = us + 'ing'
for prefix in ['kilo', 'centi', 'milli', 'micro', 'nano', 'pico', 'femto', 'deci']:
    WORDS[prefix + 'metre'] = prefix + 'meter'
    WORDS[prefix + 'metres'] = prefix + 'meters'
    WORDS[prefix + 'litre'] = prefix + 'liter'
    WORDS[prefix + 'litres'] = prefix + 'liters'
for gb in ['epicentre', 'epicentres', 'amphitheatre', 'amphitheatres', 'centrepiece', 'centrepieces',
           'fibreglass', 'fibre-optic', 'manoeuvred', 'manoeuvring',
           'manoeuvrable', 'manoeuvrability', 'theatregoers']:
    WORDS[gb] = (gb.replace('manoeuvr', 'maneuver').replace('centre', 'center').replace('centred', 'centered')
                 .replace('theatre', 'theater').replace('fibre', 'fiber'))
WORDS['manoeuvred'] = 'maneuvered'
WORDS['manoeuvring'] = 'maneuvering'

# -ence → -ense.
for gb, us in [('defence', 'defense'), ('offence', 'offense'), ('pretence', 'pretense'), ('licence', 'license')]:
    WORDS.update({gb: us, gb + 's': us + 's', gb + 'less': us + 'less'})

# A doubled l (unstressed last syllable), and a single one where American doubles it.
for gb in '''
bevel cancel channel counsel dial duel enamel equal fuel funnel jewel label level marshal
marvel model panel pedal pencil quarrel revel rival shovel signal snorkel
swivel total travel tunnel unravel
'''.split():
    for prefix in ['', 'mis', 'un', 're']:
        WORDS.update({prefix + gb + 'l' + s: prefix + gb + s for s in ['ed', 'ing', 'er', 'ers']})
WORDS.update({
    'marvellous': 'marvelous', 'marvellously': 'marvelously', 'counsellor': 'counselor', 'counsellors': 'counselors',
    'jeweller': 'jeweler', 'jewellers': 'jewelers', 'jewellery': 'jewelry', 'woollen': 'woolen', 'woollens': 'woolens',
    'cancellation': 'cancellation',
    'fulfil': 'fulfill', 'fulfils': 'fulfills', 'fulfilment': 'fulfillment', 'enrol': 'enroll', 'enrols': 'enrolls',
    'enrolment': 'enrollment', 'enrolments': 'enrollments', 'instil': 'instill', 'instils': 'instills',
    'distil': 'distill', 'distils': 'distills', 'instalment': 'installment', 'instalments': 'installments',
    'skilful': 'skillful', 'skilfully': 'skillfully', 'wilful': 'willful', 'wilfully': 'willfully',
})
del WORDS['cancellation']  # the same in both

# Greek and Latin ae and oe, mostly medical and scientific.
for gb, us in [
    ('haemoglobin', 'hemoglobin'), ('haematology', 'hematology'), ('haematologist', 'hematologist'),
    ('haematologists', 'hematologists'), ('haematological', 'hematological'), ('haemorrhage', 'hemorrhage'),
    ('haemorrhages', 'hemorrhages'), ('haemorrhaged', 'hemorrhaged'), ('haemorrhaging', 'hemorrhaging'),
    ('haemorrhagic', 'hemorrhagic'), ('haemophilia', 'hemophilia'), ('haemophiliac', 'hemophiliac'),
    ('haemophiliacs', 'hemophiliacs'), ('haemolysis', 'hemolysis'), ('haemolytic', 'hemolytic'),
    ('haematocrit', 'hematocrit'), ('haemostasis', 'hemostasis'), ('haemostatic', 'hemostatic'),
    ('haematoma', 'hematoma'), ('haemodialysis', 'hemodialysis'), ('haemorrhoids', 'hemorrhoids'),
    ('haemoglobins', 'hemoglobins'), ('haem', 'heme'), ('haemocytometer', 'hemocytometer'),
    ('haematopoiesis', 'hematopoiesis'), ('haematopoietic', 'hematopoietic'), ('haemagglutination', 'hemagglutination'),
    ('anaemia', 'anemia'), ('anaemic', 'anemic'), ('leukaemia', 'leukemia'), ('leukaemias', 'leukemias'),
    ('septicaemia', 'septicemia'), ('toxaemia', 'toxemia'), ('bacteraemia', 'bacteremia'), ('uraemia', 'uremia'),
    ('ischaemia', 'ischemia'), ('ischaemic', 'ischemic'), ('hypoglycaemia', 'hypoglycemia'),
    ('hyperglycaemia', 'hyperglycemia'), ('viraemia', 'viremia'),
    ('anaesthesia', 'anesthesia'), ('anaesthetic', 'anesthetic'), ('anaesthetics', 'anesthetics'),
    ('anaesthetist', 'anesthetist'), ('anaesthetists', 'anesthetists'), ('anaesthetise', 'anesthetize'),
    ('anaesthetised', 'anesthetized'), ('anaesthetising', 'anesthetizing'), ('anaesthetic-free', 'anesthetic-free'),
    ('paediatric', 'pediatric'), ('paediatrics', 'pediatrics'), ('paediatrician', 'pediatrician'),
    ('paediatricians', 'pediatricians'), ('orthopaedic', 'orthopedic'), ('orthopaedics', 'orthopedics'),
    ('encyclopaedia', 'encyclopedia'), ('encyclopaedias', 'encyclopedias'), ('encyclopaedic', 'encyclopedic'),
    ('gynaecology', 'gynecology'), ('gynaecological', 'gynecological'), ('gynaecologist', 'gynecologist'),
    ('oedema', 'edema'), ('oestrogen', 'estrogen'), ('oestrogens', 'estrogens'), ('oesophagus', 'esophagus'),
    ('oesophageal', 'esophageal'), ('aetiology', 'etiology'), ('foetus', 'fetus'), ('foetuses', 'fetuses'),
    ('foetal', 'fetal'), ('faeces', 'feces'), ('faecal', 'fecal'), ('diarrhoea', 'diarrhea'),
    ('gonorrhoea', 'gonorrhea'), ('caesarean', 'cesarean'), ('caesium', 'cesium'),
    ('palaeolithic', 'paleolithic'), ('palaeontology', 'paleontology'), ('palaeontologist', 'paleontologist'),
    ('palaeontologists', 'paleontologists'), ('palaeography', 'paleography'), ('mediaeval', 'medieval'),
    ('titre', 'titer'), ('titres', 'titers'), ('titred', 'titered'),
    ('aeroplane', 'airplane'), ('aeroplanes', 'airplanes'), ('manoeuvre', 'maneuver'), ('manoeuvres', 'maneuvers'),
]:
    WORDS[gb] = us

# The rest, one by one.
for gb, us in [
    ('grey', 'gray'), ('greys', 'grays'), ('greyish', 'grayish'), ('greyer', 'grayer'), ('greying', 'graying'),
    ('greyscale', 'grayscale'), ('grey-green', 'gray-green'),
    ('programme', 'program'), ('programmes', 'programs'),
    ('catalogue', 'catalog'), ('catalogues', 'catalogs'), ('catalogued', 'cataloged'), ('cataloguing', 'cataloging'),
    ('analogue', 'analog'), ('analogues', 'analogs'),
    ('ageing', 'aging'), ('judgement', 'judgment'), ('judgements', 'judgments'),
    ('acknowledgement', 'acknowledgment'), ('acknowledgements', 'acknowledgments'),
    ('artefact', 'artifact'), ('artefacts', 'artifacts'),
    ('sceptic', 'skeptic'), ('sceptics', 'skeptics'), ('sceptical', 'skeptical'), ('scepticism', 'skepticism'),
    ('aluminium', 'aluminum'), ('sulphur', 'sulfur'), ('sulphuric', 'sulfuric'), ('sulphurous', 'sulfurous'),
    ('sulphate', 'sulfate'), ('sulphates', 'sulfates'), ('sulphide', 'sulfide'), ('sulphides', 'sulfides'),
    ('sulphite', 'sulfite'), ('sulphonamide', 'sulfonamide'), ('sulphonamides', 'sulfonamides'),
    ('sulpha', 'sulfa'), ('sulphanilamide', 'sulfanilamide'),
    ('mould', 'mold'), ('moulds', 'molds'), ('moulded', 'molded'), ('moulding', 'molding'), ('mouldings', 'moldings'),
    ('mouldy', 'moldy'), ('moult', 'molt'), ('smoulder', 'smolder'), ('smouldering', 'smoldering'),
    ('plough', 'plow'), ('ploughs', 'plows'), ('ploughed', 'plowed'), ('ploughing', 'plowing'),
    ('ploughshare', 'plowshare'), ('ploughshares', 'plowshares'),
    # Not `draughts`: the game, which American calls checkers, as often as drafts of air.
    ('draught', 'draft'), ('draughtsman', 'draftsman'), ('draughtsmen', 'draftsmen'),
    ('draughtsmanship', 'draftsmanship'),
    ('tyre', 'tire'), ('tyres', 'tires'), ('cheque', 'check'), ('cheques', 'checks'), ('kerb', 'curb'),
    ('pyjamas', 'pajamas'), ('storey', 'story'), ('storeys', 'stories'),
    ('practise', 'practice'), ('practised', 'practiced'), ('practises', 'practices'), ('practising', 'practicing'),
    ('learnt', 'learned'), ('cosy', 'cozy'), ('speciality', 'specialty'), ('specialities', 'specialties'),
    ('moustache', 'mustache'), ('moustaches', 'mustaches'), ('mollusc', 'mollusk'), ('molluscs', 'mollusks'),
    ('gaol', 'jail'), ('gaols', 'jails'), ('annexe', 'annex'), ('yoghurt', 'yogurt'), ('chilli', 'chili'),
    ('whisky', 'whisky'), ('omelette', 'omelet'), ('jewellery', 'jewelry'),
]:
    if gb != us:
        WORDS[gb] = us

# Respelled even when capitalized in mid-sentence: a period or a style, not a name.
FORCE = {'palaeolithic', 'mediaeval'}

# Proper names that hold a British spelling and are not always capitalized where
# they stand (all caps on a scene, or starting a sentence). Case-insensitive.
KEEP = [
    r'ministry of defen[cs]e', r'labour party', r'royal college of \w+', r'theatre royal',
    r'national theatre', r'centre for \w+', r'legion of honour', r'order of \w+', r'department of defence',
    r'defence force', r'defence forces', r'army medical', r'harbour (?:board|bridge)', r'pearl harbour',
    r'globe theatre', r'sceptical chymist', r'encyclopaedia \w+', r'third defence', r'tyre',
]
_KEEP = re.compile(r'(?<![A-Za-z])(?:' + '|'.join(KEEP) + r')(?![A-Za-z])', re.I)

# Words kept however they are written: a coinage quoted as its coiner spelled it.
COINED = ['haematokrit']  # Hedin's instrument, 1891
_COINED = re.compile(r'(?<![A-Za-z])(?:' + '|'.join(COINED) + r')(?![A-Za-z])', re.I)

# ---------------------------------------------------------------------------
# Spans that are not kloom's words.

_FENCE = re.compile(r'^```.*?^```[^\n]*$', re.M | re.S)
_BLOCKQUOTE = re.compile(r'^[ \t]*>.*$', re.M)
_CODE = re.compile(r'`[^`\n]*`')
_LINK = re.compile(r'!?\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]*)(?:\s+"[^"]*")?\)')
_URL = re.compile(r'https?://\S+')
_HTML = re.compile(r'<[^>\n]+>')
_ITALIC = re.compile(r'(?<![\w*_])(_|\*)(?![\s_*])((?:(?!\n\s*\n).)+?)(?<![\s_*])\1(?![\w*_])', re.S)
_QUOTE = re.compile(r'"(?:(?!\n\s*\n)[^"])*"|“[^”]*”', re.S)
_WORD = re.compile(r"[A-Za-z]+(?:-[A-Za-z]+)*")


def protected(text):
    """Spans of `text` that are quoted, a title, a name's mark, code or markup: (start, end, why)."""
    spans = []
    for m in _FENCE.finditer(text):
        spans.append((m.start(), m.end(), 'code'))
    for m in _BLOCKQUOTE.finditer(text):
        spans.append((m.start(), m.end(), 'quotation'))
    for m in _CODE.finditer(text):
        spans.append((m.start(), m.end(), 'code'))
    for m in _LINK.finditer(text):
        spans.append((m.start(2), m.end(), 'link'))
    for m in _URL.finditer(text):
        spans.append((m.start(), m.end(), 'link'))
    for m in _HTML.finditer(text):
        spans.append((m.start(), m.end(), 'markup'))
    for m in _QUOTE.finditer(text):
        spans.append((m.start(), m.end(), 'quotation'))
    for m in _ITALIC.finditer(text):
        # A title is capitalized; an italic in lower case is a term kloom introduces (_tokeniser_).
        if any(c.isupper() for c in m.group(2)):
            spans.append((m.start(), m.end(), 'title'))
    for m in _KEEP.finditer(text):
        if m.group()[0].isupper():
            spans.append((m.start(), m.end(), 'name'))
    for m in _COINED.finditer(text):
        spans.append((m.start(), m.end(), 'quotation'))
    return spans


def _sentence_start(text, i):
    """Does the word at `i` start a sentence, a heading, a list item, a table cell or the text?

    A reading wraps its lines, so a line break inside a paragraph starts nothing.
    """
    j = i - 1
    while j >= 0 and text[j] in ' \t*_[(#"“‘>-—–':
        j -= 1
    if j >= 0 and text[j] == '\n':
        k = j - 1
        while k >= 0 and text[k] in ' \t':
            k -= 1
        return k < 0 or text[k] in '.!?:|\n'
    return j < 0 or text[j] in '.!?:|'


def _case(word, us):
    if word.isupper() and len(word) > 1:
        return us.upper()
    if word[0].isupper():
        return us[0].upper() + us[1:]
    return us


_AE = re.compile(r'haem|aemi(?=as?$|c$)')


def _lookup(word):
    """The American spelling of `word`, or None; a hyphenated word part by part."""
    lower = word.lower()
    if lower in WORDS:
        return _case(word, WORDS[lower])
    # The blood words come in more compounds than a list holds: thalassaemia, immunohaematology.
    us = _AE.sub(lambda m: m.group().replace('ae', 'e'), lower)
    if us != lower and '-' not in lower:
        return _case(word, us)
    if '-' in word:
        parts = word.split('-')
        out = [_lookup(p) or p for p in parts]
        if out != parts:
            return '-'.join(out)
    return None


def hits(text):
    """Every British spelling in `text`: (start, end, word, american, why), why None when it changes."""
    spans = protected(text)
    out = []
    for m in _WORD.finditer(text):
        word = m.group()
        us = _lookup(word)
        if us is None:
            continue
        a, b = m.span()
        why = next((w for s, e, w in spans if s <= a and b <= e), None)
        # Only the parts that change say whether it is a name: `Sun-centred` is not one.
        changing = [p for p, q in zip(word.split('-'), us.split('-')) if p.lower() != q.lower()] or [word]
        capital = any(p[0].isupper() and not p.isupper() for p in changing)
        if why is None and capital and word.lower() not in FORCE:
            if not _sentence_start(text, a):
                why = 'name'
            else:
                nxt = re.match(r'[ \t]+([A-Za-z])', text[b:])
                if nxt and nxt.group(1).isupper():
                    why = 'name'
        out.append((a, b, word, us, why))
    return out


def respell(text):
    """`text` with every hit that is kloom's own words in American spelling."""
    for a, b, _word, us, why in reversed(hits(text)):
        if why is None:
            text = text[:a] + us + text[b:]
    return text


# ---------------------------------------------------------------------------
# Where the words are, file by file. A JSON file is changed in place, string by
# string, so its formatting is left exactly as it was.

_JSON_STRING = re.compile(r'"(?:[^"\\]|\\.)*"')


def _json_strings(raw):
    """(path, start, end) for every string value in `raw`; path is a tuple of keys and '*' for an index."""
    out = []
    pos = 0

    def ws():
        nonlocal pos
        while pos < len(raw) and raw[pos] in ' \t\r\n':
            pos += 1

    def value(path):
        nonlocal pos
        ws()
        c = raw[pos]
        if c == '{':
            pos += 1
            ws()
            if raw[pos] == '}':
                pos += 1
                return
            while True:
                ws()
                m = _JSON_STRING.match(raw, pos)
                key = json.loads(m.group())
                pos = m.end()
                ws()
                pos += 1  # :
                value(path + (key,))
                ws()
                c = raw[pos]
                pos += 1
                if c == '}':
                    return
        elif c == '[':
            pos += 1
            ws()
            if raw[pos] == ']':
                pos += 1
                return
            while True:
                value(path + ('*',))
                ws()
                c = raw[pos]
                pos += 1
                if c == ']':
                    return
        elif c == '"':
            m = _JSON_STRING.match(raw, pos)
            out.append((path, m.start(), m.end()))
            pos = m.end()
        else:
            m = re.compile(r'[^,\]}\s]+').match(raw, pos)
            pos = m.end()

    value(())
    return out


FRAME_FIELDS = [
    ('topic',), ('position', 'label'), ('scene', 'headline'), ('scene', 'accent'), ('scene', 'metadata', '*'),
    ('scene', 'counter', 'label'), ('scene', 'counter', 'value'), ('scene', 'dedication', 'kicker'),
    ('scene', 'dedication', 'note'), ('connections', '*', 'why'), ('edits', '*', 'summary'),
]
SPINE_FIELDS = [('segments', '*', 'title')]
TRAIL_FIELDS = [('title',), ('spine', 'segments', '*', 'title')]
SUBJECT_FIELDS = [('title',), ('subtitle',)]
NAME_FIELDS = [('description',)]


def json_fields(path):
    """The fields of a JSON file that are kloom's words, by what the file is; None for a file not read."""
    p = Path(path)
    if p.name == 'frame.json':
        return FRAME_FIELDS
    if p.name == 'spine.json':
        return SPINE_FIELDS
    if p.name == 'subject.json':
        return SUBJECT_FIELDS
    if p.parent.name == 'trails':
        return TRAIL_FIELDS
    if p.parent.name == 'names':
        return NAME_FIELDS
    return None


_SVG_TEXT = re.compile(r'(<text\b[^>]*>)([^<]*)(</text>)')
_TS_STRING = re.compile(r"//[^\n]*|/\*.*?\*/|'(?:[^'\\\n]|\\.)*'|\"(?:[^\"\\\n]|\\.)*\"|`(?:[^`\\]|\\.)*`", re.S)
_TS_IMPORT = re.compile(r'\s*(?:import|export\s+\*|export\s+\{[^}]*\}\s+from)\b')
_SVELTE_SKIP =re.compile(r'<(script|style)\b.*?</\1>', re.S)
_SVELTE_ATTR = re.compile(r'\b(aria-label|title|alt|placeholder)="([^"{]*)"')


def _script_regions(text, start, end):
    """The string literals of a script that read as prose, not a comment or an import.

    Prose has a space in it (`'Scene colours'`) or is a capitalized label (`'Organisation'`);
    a key, a path or an id (`'colour'`, `'./colour'`) has neither.
    """
    out = []
    for m in _TS_STRING.finditer(text, start, end):
        lit = m.group()
        if lit.startswith('/') or not (' ' in lit or lit[1:2].isupper()) or _TS_IMPORT.match(text, text.rfind('\n', 0, m.start()) + 1):
            continue
        # A template's ${...} is code.
        at, stop = m.start() + 1, m.end() - 1
        for e in re.finditer(r'\$\{[^}]*\}', text[at:stop]):
            out.append((at, m.start() + 1 + e.start(), 'plain'))
            at = m.start() + 1 + e.end()
        out.append((at, stop, 'plain'))
    return out


def regions(path, text):
    """(start, end, kind) of the parts of a file that are prose: 'prose' is masked, 'plain' is not."""
    p = Path(path)
    if p.suffix == '.md':
        return [(0, len(text), 'prose')]
    if p.suffix == '.json':
        fields = json_fields(p)
        if not fields:
            return []
        out = []
        for key, a, b in _json_strings(text):
            if any(len(f) == len(key) and all(x == y for x, y in zip(f, key)) for f in fields):
                out.append((a + 1, b - 1, 'prose'))
        return out
    if p.suffix == '.svg':
        return [(m.start(2), m.end(2), 'plain') for m in _SVG_TEXT.finditer(text)]
    if p.suffix == '.ts':
        return [] if p.name.endswith('.test.ts') else _script_regions(text, 0, len(text))
    if p.suffix == '.svelte':
        scripts = [m for m in _SVELTE_SKIP.finditer(text)]
        skip = [(m.start(), m.end()) for m in scripts]
        out = []
        for m in scripts:
            if m.group(1) == 'script':
                out += _script_regions(text, m.start(), m.end())
        for m in re.finditer(r'>([^<{}]+)(?=<|\{)', text):
            if not any(s <= m.start() < e for s, e in skip) and m.group(1).strip():
                out.append((m.start(1), m.end(1), 'plain'))
        for m in _SVELTE_ATTR.finditer(text):
            if not any(s <= m.start() < e for s, e in skip):
                out.append((m.start(2), m.end(2), 'plain'))
        return out
    return []


def file_hits(path, text):
    """Every hit in a file: (offset, word, american, why)."""
    out = []
    for a, b, _kind in regions(path, text):
        part = text[a:b]
        if Path(path).suffix == '.json':
            part = json.loads('"' + part + '"')
            for s, _e, word, us, why in hits(part):
                out.append((a, word, us, why))
        else:
            for s, _e, word, us, why in hits(part):
                out.append((a + s, word, us, why))
    return out


def respell_file(path, text):
    """The file's text with its hits changed; JSON strings re-encoded as they were written."""
    for a, b, _kind in sorted(regions(path, text), reverse=True):
        part = text[a:b]
        if Path(path).suffix == '.json':
            value = json.loads('"' + part + '"')
            new = respell(value)
            if new != value:
                text = text[:a] + json.dumps(new, ensure_ascii=False)[1:-1] + text[b:]
        else:
            text = text[:a] + respell(part) + text[b:]
    return text


SUFFIXES = {'.md', '.json', '.svg', '.svelte', '.ts'}


def walk(paths):
    for p in map(Path, paths):
        if p.is_dir():
            yield from sorted(f for f in p.rglob('*') if f.suffix in SUFFIXES and f.is_file())
        elif p.is_file():
            yield p


def respell_specs(examples, subjects):
    """Bring the mark specs in `examples` into line with the readings under `subjects`.

    A mark spec names a mark by its words. When `apply` respells a mark's words
    (`[haemophilia](kloom:e/haemophilia)`), the spec's `["haemophilia", ...]` no longer
    finds them; it is respelled the same way, and only where the reading now holds the
    respelled mark. Returns the specs changed.
    """
    changed = []
    for spec in sorted(Path(examples).glob('*.json')):
        raw = before = spec.read_text()
        for ref, pairs in json.loads(raw).items():
            subject, frame = ref.split('/')
            reading = Path(subjects) / subject / 'frames' / frame / 'reading.md'
            if not reading.is_file():
                continue
            text = reading.read_text()
            for words, name in pairs:
                us = _WORD.sub(lambda m: _lookup(m.group()) or m.group(), words)
                if us != words and f'[{us}](kloom:e/{name})' in text and f'[{words}](kloom:e/{name})' not in text:
                    old = json.dumps([words, name], ensure_ascii=False)
                    raw = raw.replace(old, json.dumps([us, name], ensure_ascii=False))
        if raw != before:
            spec.write_text(raw)
            changed.append(spec)
    return changed


# ---------------------------------------------------------------------------
# What looks British and WORDS does not hold.

_SUSPECT = re.compile(
    r'^(?:\w+is(?:e|ed|es|ing|ation|ations)|\w+our(?:s|ed|ing|ite|able|er|ful)?|\w+(?:t|b|g|ch)re[sd]?'
    r'|\w*(?:haem|anaem|aemi|aesth|paed|oedem|oestr|oesoph|aetio|foet|faec|rhoea|palaeo|gynaec)\w*'
    r'|\w+yse[sd]?|\w+ysing|\w+ogue[sd]?|\w+ell(?:ed|ing|er|ers))$', re.I)
NOT_SUSPECT = set('''
rise rises rising risen wise otherwise likewise clockwise advise advised advises advising advisers
surprise surprised surprises surprising exercise exercised exercises exercising enterprise enterprises
compromise compromised compromises compromising supervise supervised supervising revise revised revising
televise televised comprise comprised comprises comprising despise despised disguise disguised devise
devised devising improvise improvised improvising merchandise premise premises promise promised promises
promising precise concise franchise expertise chastise excise incise paradise raise raised raises raising
praise praised praises praising noise noises poise poised cruise bruise treatise treatises tortoise
porpoise demise reprise apprise guise arise arises arising arisen uprise sunrise moonrise
anise valise imprecise circumcise circumcised mortise reprised appraise appraised appraising
hour hours four your yours our ours flour pour poured pouring tour tours toured touring detour detours
contour contours devour devoured sour soured scour scoured glamour troubadour troubadours paramour velour
amour downpour hourglass endeavour endeavours vigour favour labour
acre ogre genre timbre macabre massacre mediocre lucre cadre euchre oeuvre louvre spectre theatre
dialogue dialogues monologue monologues prologue prologues epilogue epilogues travelogue demagogue
synagogue synagogues rogue rogues vogue morgue league leagues fugue plague plagued colleague colleagues
tongue tongues intrigue fatigue vague brogue apologue
analyses hypotheses emphasis basis
compelled compelling expelled expelling propelled propelling repelled repelling dispelled excelled
excelling rebelled rebelling spelled spelling smelled smelling yelled yelling dwelled dwelling quelled
shelled shelling seller sellers speller teller tellers dweller dwellers propeller propellers bestseller
bestsellers storyteller storytellers fortune-teller cellar impeller
'''.split())


def suspects(paths):
    """{word: count} over words in kloom's prose that look British, are not in WORDS and are not known."""
    counts = {}
    for f in walk(paths):
        text = f.read_text()
        for a, b, _kind in regions(f, text):
            part = text[a:b]
            spans = protected(part)
            for m in _WORD.finditer(part):
                for w in m.group().split('-'):
                    lw = w.lower()
                    if lw in WORDS or lw in NOT_SUSPECT or not _SUSPECT.match(lw):
                        continue
                    if any(s <= m.start() and m.end() <= e for s, e, _ in spans):
                        continue
                    counts[lw] = counts.get(lw, 0) + 1
    return counts


# ---------------------------------------------------------------------------


def _line(text, offset):
    return text.count('\n', 0, offset) + 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('command', choices=['report', 'apply', 'check', 'suspects'])
    ap.add_argument('paths', nargs='*', default=['subjects', 'names'])
    ap.add_argument('--skipped', action='store_true', help='report: list the skipped hits too, with why')
    args = ap.parse_args(argv)

    if args.command == 'suspects':
        for word, n in sorted(suspects(args.paths).items(), key=lambda kv: (-kv[1], kv[0])):
            print(f'{n:5}  {word}')
        return 0

    changed = files = skipped = 0
    for f in walk(args.paths):
        text = f.read_text()
        found = file_hits(f, text)
        if not found:
            continue
        will = [h for h in found if h[3] is None]
        skipped += len(found) - len(will)
        changed += len(will)
        if will:
            files += 1
        if args.command in ('report', 'check'):
            for offset, word, us, why in found:
                if why is None:
                    print(f'{f}:{_line(text, offset)}: {word} → {us}')
                elif args.skipped:
                    print(f'{f}:{_line(text, offset)}: {word} kept ({why})')
        elif args.command == 'apply' and will:
            f.write_text(respell_file(f, text))
    if args.command == 'apply':
        here = Path(__file__).resolve().parent
        for spec in respell_specs(here.parent / 'names' / 'examples', here.parent.parent / 'subjects'):
            print(f'{spec}: marks respelled with their readings', file=sys.stderr)
    verb = {'apply': 'changed', 'report': 'would change', 'check': 'would change'}[args.command]
    print(f'{verb} {changed} words in {files} files; {skipped} kept as quoted, a title or a name',
          file=sys.stderr)
    return 1 if args.command == 'check' and changed else 0


if __name__ == '__main__':
    sys.exit(main())
