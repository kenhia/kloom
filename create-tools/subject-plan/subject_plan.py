"""Write a subject's spine and trails from a plan, keeping only frames that exist.

    python3 create-tools/subject-plan/subject_plan.py PLAN.json SUBJECT_DIR [--check]

A plan is the whole intended shape of a subject before its frames are
written: `{"spine": {"segments": [...]}, "trails": [{"id", "title", "anchor",
"spine": {...}}]}`, in exactly the shape of `spine.json` and `trails/*.json`,
and optionally `"frames": {"<id>": {"topic", "sort", "palette"}}`, what the
brief settles for each frame (sprint 027), so they are checked before any
author starts rather than only in the copies of the brief.
This writes `spine.json` and one `trails/<id>.json` per trail, holding only
the frames whose directories exist under `SUBJECT_DIR/frames/`: an empty
segment is left out, and so is a trail whose anchor or every frame is
missing. So a subject authored segment by segment (or by several authors at
once) validates at every step, and the plan says what is still to come.

`--check` writes nothing and lists the planned frames not yet written. It
checks the plan's frames too: sorts rise within each `date` segment, topics
fit the 40-character cap and are unique, palettes are in `subject.json`;
it warns where a palette repeats down a segment and where a written frame
differs from its plan. It exits 1 on a problem, never on a warning.
`--complete DIR` writes the spine into a copy of the subject at
DIR/<subject> that holds only the frames with a `frame.json` that land on a
spine (a trail frame whose anchor is not written yet is left out, and named),
so one author
can validate their frames while others are mid-write. Beside it go the other
subjects, which connections may name, and the name registry at DIR/.names,
with any `--drafts` directories of names not yet added merged in (sprint
021; since sprint 017 a copy without them failed on every mark):
`KLOOM_TEST_SUBJECTS=DIR KLOOM_TEST_NAMES=DIR/.names npx vitest --run engine/subjects.test.ts engine/svg.test.ts`.
Standard library only.
"""
import argparse, json, os, shutil, subprocess, sys

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
        previous = last_palette = None
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
                elif palette == last_palette:
                    warnings.append(f'{at}: {f} repeats the palette "{palette}" of the frame before it')
            last_palette = palette
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


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('plan')
    ap.add_argument('subject')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--complete', metavar='DIR',
                    help='write a copy holding only the finished frames to DIR/<subject>, to validate one author\'s work while others are still writing')
    ap.add_argument('--drafts', action='append', default=[], metavar='DIR',
                    help='with --complete: a directory of name drafts to merge into the copy\'s registry (repeatable)')
    ap.add_argument('--only', nargs='+', metavar='FRAME',
                    help='with --complete: only these frames and those already committed, so another author\'s '
                         'half-written frame cannot fail this one\'s check')
    ap.add_argument('--names', default=None, metavar='DIR',
                    help='with --complete: the name registry (default: the repository\'s names/)')
    a = ap.parse_args()
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
        for d in os.listdir(os.path.join(src, 'frames')):
            if wanted_frames is not None and d not in wanted_frames:
                continue
            if not d.startswith('.') and os.path.isfile(os.path.join(src, 'frames', d, 'frame.json')):
                shutil.copytree(os.path.join(src, 'frames', d), os.path.join(a.subject, 'frames', d))
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
        for d in a.drafts:
            for f in os.listdir(d):
                if f.endswith('.json'):
                    shutil.copy(os.path.join(d, f), names)
    with open(a.plan) as fh:
        plan = json.load(fh)
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
    print(f'subject_plan: {len(planned) - len(missing)} of {len(planned)} planned frames on the spine and trails')


if __name__ == '__main__':
    main()
