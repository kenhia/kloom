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
DIR/<subject> that holds only the frames with a `frame.json`, so one author
can validate their frames while others are mid-write:
`KLOOM_TEST_SUBJECTS=DIR npx vitest --run engine/subjects.test.ts engine/svg.test.ts`.
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
    print(f'subject_plan: {len(planned) - len(missing)} of {len(planned)} planned frames on the spine and trails')


if __name__ == '__main__':
    main()
