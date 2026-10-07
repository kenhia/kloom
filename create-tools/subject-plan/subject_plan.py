"""Write a subject's spine and trails from a plan, keeping only frames that exist.

    python3 create-tools/subject-plan/subject_plan.py PLAN.json SUBJECT_DIR [--check]

A plan is the whole intended shape of a subject before its frames are
written: `{"spine": {"segments": [...]}, "trails": [{"id", "title", "anchor",
"spine": {...}}]}`, in exactly the shape of `spine.json` and `trails/*.json`,
and optionally `"frames": {"<id>": {"topic", "sort", "palette"}}`, what the
brief settles for each frame (sprint 027), so they are checked before any
author starts rather than only in the copies of the brief, with a `part`
(the author's part, its drafts directory's suffix: `navy2`), and `"owners":
{"<name id>": "<part>"}`, the part that drafts each name two parts will
mark (sprint 033), which `names.py drafts` reads.
This writes `spine.json` and one `trails/<id>.json` per trail, holding only
the frames whose directories exist under `SUBJECT_DIR/frames/`: an empty
segment is left out, and so is a trail whose anchor or every frame is
missing. So a subject authored segment by segment (or by several authors at
once) validates at every step, and the plan says what is still to come.

`--check` writes nothing and lists the planned frames not yet written. It
checks the plan's frames too: sorts rise within each `date` segment, topics
fit the 40-character cap and are unique, palettes are in `subject.json`.
A segment carries its section's `palette` (sprint 038, korg 3495: a palette
per section, tracking its era or theme, in place of the old rule that dark
and light alternate frame by frame), which `spine.json` keeps; it warns
where a frame's palette differs from its section's with no `paletteWhy` on
its entry, where a segment whose frames name palettes names none itself,
and where a written frame differs from its plan. `--accents FILE` reads the
authors' accent claims (`ACCENT part frame` a line) beside the plan's own
`accent`s, and a clash is a problem (sprint 050). It exits 1 on a problem,
never on a warning.
`--complete DIR` writes the spine into a copy of the subject at
DIR/<subject> that holds only the frames with a `frame.json` that land on a
spine (a trail frame whose anchor is not written yet is left out, and named),
and counts that copy, not the live tree (sprint 050), so one author
can validate their frames while others are mid-write. Beside it go the other
subjects, which connections may name, and the name registry at DIR/.names,
with any `--drafts` directories of names not yet added merged in (sprint
021; since sprint 017 a copy without them failed on every mark):
`KLOOM_TEST_SUBJECTS=DIR KLOOM_TEST_NAMES=DIR/.names npx vitest --run engine/subjects.test.ts engine/svg.test.ts`.
`--with-drafts` puts each frame's `frame.json.draft` into the copy as its
`frame.json`, so a frame not yet live is checked without copying it by hand
(sprint 029; three of sprint 028's authors wrote wrappers to do it).
`--stand-in ANCHOR` (repeatable) writes, into the copy only, a placeholder
for a trail's anchor not yet written: its id, the plan's topic, sort and
palette, a one-line reading and a one-line drawing, and no marks, media or connections, so the
trail's frames land on a spine (sprint 033; authors in sprints 025 to 030
built one by hand).
Standard library only.
"""
import argparse, datetime, json, os, re, shutil, subprocess, sys

# engine/validate.ts's TOPIC_MAX: a map label, a list line.
TOPIC_MAX = 40


def spines(plan):
    """(where, segment) for every segment of the main spine and the trails, in order."""
    for seg in plan['spine']['segments']:
        yield 'spine', seg
    for t in plan.get('trails', []):
        for seg in t['spine']['segments']:
            yield f'trail {t["id"]}', seg


def plan_problems(plan, palettes, written=None):
    """(problems, warnings) in a plan's per-frame fields; `written` is {frame: frame.json} for drift."""
    problems, warnings = [], []
    entries = plan.get('frames', {})
    planned = {f for _, seg in spines(plan) for f in seg['frames']}
    for f in sorted(set(entries) - planned):
        problems.append(f'frames.{f}: not on the spine or a trail')
    topics = {}
    for where, seg in spines(plan):
        at = f'{where} segment {seg["id"]}'
        previous = None
        # The section's palette (korg 3495): the segment's own, or else its first frame's.
        section = seg.get('palette')
        if section is not None and section not in palettes:
            problems.append(f'{at}: unknown palette "{section}" (subject.json has {", ".join(sorted(palettes))})')
        named = [entries.get(f, {}).get('palette') for f in seg['frames']]
        if section is None and any(named):
            warnings.append(f'{at}: give the segment its section\'s "palette"; its frames name theirs')
            section = next(n for n in named if n)
        for f in seg['frames']:
            e = entries.get(f, {})
            sort, topic, palette = e.get('sort'), e.get('topic'), e.get('palette')
            if seg['labelKind'] == 'date' and sort is not None:
                if not isinstance(sort, (int, float)) or isinstance(sort, bool):
                    problems.append(f'{at}: {f} sort must be a number (a year; negative for BC)')
                elif previous is not None and sort < previous[1]:
                    problems.append(f'{at}: {f} ({sort}) comes after {previous[0]} ({previous[1]})')
                else:
                    previous = (f, sort)
            elif seg['labelKind'] != 'date' and sort is not None:
                problems.append(f'{at}: {f} has a sort, but only a date segment sorts')
            if topic is not None:
                if not isinstance(topic, str) or not topic.strip():
                    problems.append(f'frames.{f}: topic must be text')
                else:
                    if len(topic.strip()) > TOPIC_MAX:
                        problems.append(f'frames.{f}: topic is {len(topic.strip())} characters; at most {TOPIC_MAX}')
                    if topic.rstrip().endswith(('.', '!')):
                        problems.append(f'frames.{f}: topic is a title: no closing "." or "!"')
                    other = topics.setdefault(topic.strip().lower(), f)
                    if other != f:
                        problems.append(f'frames.{f}: topic "{topic.strip()}" is already {other}\'s')
            if palette is not None:
                if palette not in palettes:
                    problems.append(f'frames.{f}: unknown palette "{palette}" (subject.json has {", ".join(sorted(palettes))})')
                elif palette != section and not e.get('paletteWhy'):
                    warnings.append(f'{at}: {f} wears "{palette}", not its section\'s "{section}"; '
                                    f'match it, or say why in frames.{f}.paletteWhy')
            # The plan is what the brief quotes; a frame that differs from it is worth a look.
            have = (written or {}).get(f)
            if have:
                for field, planned_value, value in (
                        ('topic', topic, have.get('topic')),
                        ('sort', sort, (have.get('position') or {}).get('sort')),
                        ('palette', palette, (have.get('scene') or {}).get('palette'))):
                    if planned_value is not None and value != planned_value:
                        warnings.append(f'frames.{f}: the plan\'s {field} is {planned_value!r}, the frame\'s {value!r}')
    return problems, warnings


def accent_word(accent):
    """An accent as engine/validate.ts compares them: capitals, no closing stop."""
    return re.sub(r'[.!?]+$', '', str(accent).strip().upper())


def parse_claims(text, where):
    """An accents file's claims, `ACCENT part frame` a line, `#` a comment: ([(word, part, frame, line)], problems)."""
    claims, problems = [], []
    for n, line in enumerate(text.splitlines(), 1):
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        bits = line.split()
        if len(bits) != 3:
            problems.append(f'{where}:{n}: write "ACCENT part frame"')
            continue
        claims.append((accent_word(bits[0]), bits[1], bits[2], f'{where}:{n}'))
    return claims, problems


def accent_problems(plan, written, claims):
    """(problems, warnings) for accents (korg 3554): the plan's `accent`s unique and worn by no other
    written frame, and each claim in an accents file clashing with neither, nor with an earlier claim.

    The plan settles an accent ahead of every claim. A frame's later claim releases its earlier one,
    so an author who changes their mind frees the word; otherwise the first claim wins."""
    problems, warnings = [], []
    planned = {}
    for _, seg in spines(plan):
        for f in seg['frames']:
            accent = plan.get('frames', {}).get(f, {}).get('accent')
            if not accent:
                continue
            word = accent_word(accent)
            if word in planned:
                problems.append(f'frames.{f}: accent "{word}" is already planned for {planned[word]}')
                continue
            planned[word] = f
            other = next((g for g, fr in sorted(written.items())
                          if g != f and accent_word((fr.get('scene') or {}).get('accent', '')) == word), None)
            if other:
                problems.append(f'frames.{f}: accent "{word}" is already frames/{other}\'s')
            have = (written.get(f) or {}).get('scene', {}).get('accent')
            if have and accent_word(have) != word:
                warnings.append(f'frames.{f}: the plan\'s accent is {word!r}, the frame\'s {accent_word(have)!r}')
    latest = {}
    for claim in claims:
        latest[claim[2]] = claim
    claimed = {}
    for claim in claims:
        word, part, f, at = claim
        if latest[f] is not claim:
            continue
        who = f'{at}: {f} ({part}) claims "{word}"'
        other = next((g for g, fr in sorted(written.items())
                      if g != f and accent_word((fr.get('scene') or {}).get('accent', '')) == word), None)
        if other:
            problems.append(f'{who}, already frames/{other}\'s')
        elif planned.get(word, f) != f:
            problems.append(f'{who}, already planned for {planned[word]}')
        elif word in claimed and claimed[word][2] != f:
            first = claimed[word]
            problems.append(f'{who}, claimed first for {first[2]} ({first[1]}) at line {first[3].rsplit(":", 1)[1]}')
        else:
            claimed.setdefault(word, claim)
    return problems, warnings


# A name id, as names.py makes them.
NAME_ID = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')


def owner_problems(plan):
    """Problems in a plan's `owners`: each a name id owned by a part the plan knows, one its frames
    name as their `part`, or else a segment or trail of the plan."""
    owners = plan.get('owners', {})
    if not isinstance(owners, dict):
        return ['owners must be {"<name id>": "<part>"}']
    parts = {e['part'] for e in plan.get('frames', {}).values() if isinstance(e, dict) and e.get('part')}
    parts = parts or {seg['id'] for seg in plan['spine']['segments']} | {t['id'] for t in plan.get('trails', [])}
    out = []
    for name, part in sorted(owners.items()):
        if not NAME_ID.match(name):
            out.append(f'owners.{name}: not a name id (lower-case words joined by "-")')
        if part not in parts:
            out.append(f'owners.{name}: "{part}" is not a part of the plan ({", ".join(sorted(parts))})')
    return out


def stand_in(plan, subject_dir, anchor, today=None):
    """Write a placeholder frame for a trail's anchor into a checking copy (sprint 033): the plan's
    topic, sort and palette, a one-line reading, no marks, media or connections. Returns what to say."""
    if anchor not in {t['anchor'] for t in plan.get('trails', [])}:
        sys.exit(f'subject_plan: --stand-in {anchor}: not the anchor of any trail in the plan')
    where = os.path.join(subject_dir, 'frames', anchor)
    if os.path.isfile(os.path.join(where, 'frame.json')):
        return f'{anchor} is written; no stand-in needed'
    seg = next(seg for seg in plan['spine']['segments'] if anchor in seg['frames'])
    entry = plan.get('frames', {}).get(anchor, {})
    with open(os.path.join(subject_dir, 'subject.json')) as fh:
        palettes = list(json.load(fh).get('palettes', {}))
    position = {'label': 'Stand-in'}
    if seg['labelKind'] == 'date':
        if not isinstance(entry.get('sort'), (int, float)):
            sys.exit(f'subject_plan: --stand-in {anchor}: the plan gives no sort, which its date segment needs')
        position = {'label': str(entry['sort']), 'sort': entry['sort']}
    frame = {
        'id': anchor,
        'topic': entry.get('topic') or f'Stand-in for {anchor}'[:TOPIC_MAX],
        'position': position,
        'scene': {'headline': 'Not yet written', 'accent': f'STANDIN-{anchor.upper()}.',
                  'palette': entry.get('palette') or seg.get('palette') or palettes[0], 'illustration': 'scene.svg', 'metadata': []},
        'citations': [{'kind': 'web', 'key': True, 'title': 'A stand-in for a frame not yet written',
                       'url': 'https://github.com/kenhia/kloom', 'accessed': (today or datetime.date.today()).isoformat()}],
    }
    os.makedirs(where, exist_ok=True)
    write(os.path.join(where, 'frame.json'), frame)
    # Every frame of a subject is held to an illustration; a frame's rule, drawn on.
    with open(os.path.join(where, 'scene.svg'), 'w') as fh:
        fh.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 10">'
                 '<path d="M0 5 H100" stroke="currentColor" fill="none" pathLength="1"/></svg>\n')
    with open(os.path.join(where, 'reading.md'), 'w') as fh:
        fh.write(f'A stand-in for {anchor}, in a checking copy only, until its own frame is written.\n')
    return f'wrote a stand-in for {anchor} into the copy'


def keep(spine, have):
    segments = []
    for seg in spine['segments']:
        frames = [f for f in seg['frames'] if f in have]
        if frames:
            segments.append({**seg, 'frames': frames})
    return {'segments': segments}


def write(path, value):
    tmp = f'{path}.tmp'
    with open(tmp, 'w') as fh:
        fh.write(json.dumps(value, ensure_ascii=False, indent='\t') + '\n')
    os.replace(tmp, path)


def merge_drafts(dirs, names):
    """Copy each drafts directory's name files into `names`, in order. Two directories holding
    one id differently is said, not hidden: the last passed wins, and in sprint 028 a draft
    lost its `home` that way without a word. A draft whose `kind` or `description` is still
    empty (straight from `lookup --write-draft`) is left out and named, since it would fail the
    copy's registry for every borrower (sprint 051), and so is a directory not made yet.
    Returns the warnings."""
    seen, out = {}, []
    for d in dirs:
        if not os.path.isdir(d):
            out.append(f'no drafts directory {d} yet; nothing merged from it')
            continue
        half = []
        for f in sorted(os.listdir(d)):
            if not f.endswith('.json'):
                continue
            with open(os.path.join(d, f)) as fh:
                body = fh.read()
            try:
                draft = json.loads(body)
            except ValueError:
                draft = {}
            if isinstance(draft, dict) and any(k in draft and not draft[k] for k in ('kind', 'description')):
                half.append(f)
                continue
            if f in seen and seen[f][1] != body:
                out.append(f'{f} is drafted in both {seen[f][0]} and {d}; the copy holds {d}\'s')
            seen[f] = (d, body)
            shutil.copy(os.path.join(d, f), names)
        # One line a directory: an owner's 37 unfinished drafts once printed 37 lines (sprint 055).
        if len(half) == 1:
            out.append(f'{half[0]} in {d} is unfinished (no kind or description yet); the copy leaves it out')
        elif half:
            more = f' and {len(half) - 3} more' if len(half) > 3 else ''
            out.append(f'{len(half)} unfinished drafts in {d} (no kind or description yet), left out of '
                       f'the copy: {", ".join(half[:3])}{more}')
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('plan')
    ap.add_argument('subject')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--accents', metavar='FILE',
                    help='with --check: the authors\' accent claims, "ACCENT part frame" a line; a clash is a problem')
    ap.add_argument('--complete', metavar='DIR',
                    help='write a copy holding only the finished frames to DIR/<subject>, to validate one author\'s work while others are still writing')
    ap.add_argument('--drafts', action='append', default=[], metavar='DIR',
                    help='with --complete: a directory of name drafts to merge into the copy\'s registry (repeatable)')
    ap.add_argument('--only', nargs='+', metavar='FRAME',
                    help='with --complete: only these frames and those already committed, so another author\'s '
                         'half-written frame cannot fail this one\'s check')
    ap.add_argument('--with-drafts', action='store_true',
                    help='with --complete: a frame\'s frame.json.draft goes into the copy as its frame.json')
    ap.add_argument('--names', default=None, metavar='DIR',
                    help='with --complete: the name registry (default: the repository\'s names/)')
    ap.add_argument('--stand-in', action='append', default=[], metavar='ANCHOR',
                    help='with --complete: a placeholder in the copy for a trail\'s anchor not yet written (repeatable)')
    a = ap.parse_args()
    if a.accents and not a.check:
        ap.error('--accents is read by --check')
    if a.stand_in and not a.complete:
        ap.error('--stand-in writes into a checking copy only: give --complete DIR')
    with open(a.plan) as fh:
        plan = json.load(fh)
    if a.complete:
        src = a.subject
        a.subject = os.path.join(a.complete, os.path.basename(os.path.normpath(src)))
        shutil.rmtree(a.subject, ignore_errors=True)
        os.makedirs(os.path.join(a.subject, 'frames'))
        shutil.copy(os.path.join(src, 'subject.json'), a.subject)
        wanted_frames = None
        if a.only:  # sprint 021: five authors asked for this, having pruned their copies by hand
            listed = subprocess.run(['git', 'ls-files', os.path.join(src, 'frames')], capture_output=True,
                                    text=True, check=True).stdout.split()
            wanted_frames = {f.split('/')[-2] for f in listed if f.endswith('/frame.json')} | set(a.only)
        for d in sorted(os.listdir(os.path.join(src, 'frames'))):
            if wanted_frames is not None and d not in wanted_frames or d.startswith('.'):
                continue
            there, here = os.path.join(src, 'frames', d), os.path.join(a.subject, 'frames', d)
            draft = a.with_drafts and os.path.isfile(os.path.join(there, 'frame.json.draft'))
            if draft or os.path.isfile(os.path.join(there, 'frame.json')):
                shutil.copytree(there, here)
            if draft:
                # The draft is the newer work: it replaces a live frame.json in the copy, and says so.
                if os.path.isfile(os.path.join(there, 'frame.json')):
                    print(f'subject_plan: {d}: the copy holds its frame.json.draft, not its live frame.json')
                os.replace(os.path.join(here, 'frame.json.draft'), os.path.join(here, 'frame.json'))
        # The other subjects, whole (copies, never links: Prettier on the copy must not reach them), and the registry.
        parent = os.path.dirname(os.path.abspath(os.path.normpath(src)))
        for other in os.listdir(parent):
            there, here = os.path.join(parent, other), os.path.join(a.complete, other)
            if other != os.path.basename(os.path.normpath(src)) and os.path.isfile(os.path.join(there, 'subject.json')):
                shutil.rmtree(here, ignore_errors=True)
                shutil.copytree(there, here)
        names = os.path.join(a.complete, '.names')
        shutil.rmtree(names, ignore_errors=True)
        shutil.copytree(a.names or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'names'), names)
        for line in merge_drafts(a.drafts, names):
            print(f'subject_plan: warning: {line}', file=sys.stderr)
        for anchor in a.stand_in:
            print(f'subject_plan: {stand_in(plan, a.subject, anchor)}')
    frames_dir = os.path.join(a.subject, 'frames')
    have = {d for d in os.listdir(frames_dir)
            if not d.startswith('.') and os.path.isfile(os.path.join(frames_dir, d, 'frame.json'))} \
        if os.path.isdir(frames_dir) else set()

    planned = [f for s in plan['spine']['segments'] for f in s['frames']]
    planned += [f for t in plan.get('trails', []) for s in t['spine']['segments'] for f in s['frames']]
    missing = [f for f in planned if f not in have]
    if a.check:
        print(f'{len(planned) - len(missing)} of {len(planned)} planned frames written')
        for f in missing:
            print(f'  to write: {f}')
        extra = sorted(have - set(planned))
        for f in extra:
            print(f'  not in the plan: {f}')
        with open(os.path.join(a.subject, 'subject.json')) as fh:
            palettes = set(json.load(fh).get('palettes', {}))
        written = {}
        for f in have:
            with open(os.path.join(frames_dir, f, 'frame.json')) as fh:
                written[f] = json.load(fh)
        problems, warnings = plan_problems(plan, palettes, written)
        problems += owner_problems(plan)
        claims = []
        if a.accents:
            with open(a.accents) as fh:
                claims, bad = parse_claims(fh.read(), a.accents)
            problems += bad
        more, warned = accent_problems(plan, written, claims)
        problems += more
        warnings += warned
        bare = [f for f in planned if f not in plan.get('frames', {})]
        if bare:
            print(f'  {len(bare)} planned frames have no topic, sort or palette in the plan')
        for w in warnings:
            print(f'  warning: {w}')
        for p in problems:
            print(f'  problem: {p}', file=sys.stderr)
        sys.exit(1 if problems else 0)

    spine = keep(plan['spine'], have)
    write(os.path.join(a.subject, 'spine.json'), spine)
    on_main = {f for s in spine['segments'] for f in s['frames']}
    trails_dir = os.path.join(a.subject, 'trails')
    os.makedirs(trails_dir, exist_ok=True)
    wanted = set()
    for t in plan.get('trails', []):
        tspine = keep(t['spine'], have)
        if t['anchor'] in on_main and tspine['segments']:
            write(os.path.join(trails_dir, f'{t["id"]}.json'), {**t, 'spine': tspine})
            wanted.add(f'{t["id"]}.json')
    # A planned trail with nothing to show yet is not left behind from an earlier run.
    for t in plan.get('trails', []):
        name = f'{t["id"]}.json'
        if name not in wanted and os.path.exists(os.path.join(trails_dir, name)):
            os.remove(os.path.join(trails_dir, name))
    if a.complete:
        # In a copy, a finished frame on no spine (its trail's anchor is not written yet) would fail
        # validation for every author, so it is left out of the copy and named.
        placed = on_main | {f for t in plan.get('trails', []) if f'{t["id"]}.json' in wanted
                            for s in keep(t['spine'], have)['segments'] for f in s['frames']}
        for f in sorted(have - placed):
            shutil.rmtree(os.path.join(frames_dir, f))
            print(f'subject_plan: left {f} out of the copy: it is on no spine yet (is its trail\'s anchor written?)')
        have &= placed
    if a.complete:
        # A draft's home may be a frame another author has not written yet; in the copy only,
        # such a home is dropped rather than failing everyone's check (sprint 021).
        names = os.path.join(a.complete, '.names')
        for f in os.listdir(names):
            path = os.path.join(names, f)
            with open(path) as fh:
                name = json.load(fh)
            subject, _, frame = name.get('home', '').partition('/')
            if frame and not os.path.isfile(os.path.join(a.complete, subject, 'frames', frame, 'frame.json')):
                del name['home']
                with open(path, 'w') as fh:
                    json.dump(name, fh, ensure_ascii=False, indent='\t')
    if a.complete:
        # The copy's count, not the live tree's: three authors in sprint 049 read the live count as theirs.
        print(f'subject_plan: the copy at {a.subject} holds {len(have)} of {len(planned)} planned frames, '
              f'on its spine and trails')
    else:
        print(f'subject_plan: {len(planned) - len(missing)} of {len(planned)} planned frames on the spine and trails')


if __name__ == '__main__':
    main()
