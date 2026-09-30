"""Write a subject's spine and trails from a plan, keeping only frames that exist.

    python3 create-tools/subject-plan/subject_plan.py PLAN.json SUBJECT_DIR [--check]

A plan is the whole intended shape of a subject before its frames are
written: `{"spine": {"segments": [...]}, "trails": [{"id", "title", "anchor",
"spine": {...}}]}`, in exactly the shape of `spine.json` and `trails/*.json`.
This writes `spine.json` and one `trails/<id>.json` per trail, holding only
the frames whose directories exist under `SUBJECT_DIR/frames/`: an empty
segment is left out, and so is a trail whose anchor or every frame is
missing. So a subject authored segment by segment (or by several authors at
once) validates at every step, and the plan says what is still to come.

`--check` writes nothing and lists the planned frames not yet written.
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
import argparse, json, os, shutil, sys


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
    ap.add_argument('--names', default=None, metavar='DIR',
                    help='with --complete: the name registry (default: names/ beside the subject\'s parent)')
    a = ap.parse_args()
    if a.complete:
        src = a.subject
        a.subject = os.path.join(a.complete, os.path.basename(os.path.normpath(src)))
        shutil.rmtree(a.subject, ignore_errors=True)
        os.makedirs(os.path.join(a.subject, 'frames'))
        shutil.copy(os.path.join(src, 'subject.json'), a.subject)
        for d in os.listdir(os.path.join(src, 'frames')):
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
        shutil.copytree(a.names or os.path.join(os.path.dirname(parent), 'names'), names)
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
        sys.exit(0)

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
