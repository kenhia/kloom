"""Stage one author's finished frames, with a spine that holds only committed ones.

    python3 create-tools/subject-plan/stage_segment.py PLAN SUBJECT_DIR FRAME ... [--also PATH ...]

With several authors writing at once, `spine.json` in the working tree names
every frame that has a `frame.json`, including other authors' that are not
reviewed yet. Committing it as it stands would commit a spine naming frames
the commit does not hold. This stages the frames named (their whole
directories), any `--also` paths (a plate module, a chart spec), and a
`spine.json` and trails built from the plan for exactly the frames already
committed plus these, formatted by Prettier. The working tree is untouched;
only the index changes. Validate the index before committing (sprint 014
checked out the index into a scratch directory and ran the subject tests
there with `KLOOM_TEST_SUBJECTS`). Standard library only, plus `npx prettier`
and git.
"""
import argparse, json, os, subprocess, sys


def run(args, **kw):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kw).stdout


def keep(spine, have):
    return {'segments': [{**s, 'frames': [f for f in s['frames'] if f in have]}
                         for s in spine['segments'] if any(f in have for f in s['frames'])]}


def stage(path, value):
    text = json.dumps(value, ensure_ascii=False, indent='\t') + '\n'
    text = run(['npx', 'prettier', '--stdin-filepath', path], input=text)
    blob = run(['git', 'hash-object', '-w', '--stdin'], input=text).strip()
    run(['git', 'update-index', '--add', '--cacheinfo', f'100644,{blob},{path}'])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('plan')
    ap.add_argument('subject')
    ap.add_argument('frames', nargs='+')
    ap.add_argument('--also', nargs='*', default=[])
    a = ap.parse_args()
    subject = os.path.relpath(a.subject)
    frames_dir = os.path.join(subject, 'frames')
    for f in a.frames:
        if not os.path.isfile(os.path.join(frames_dir, f, 'frame.json')):
            sys.exit(f'stage_segment: {f} has no frame.json')
    committed = {p.split('/')[-2] for p in run(['git', 'ls-files', frames_dir]).split()
                 if p.endswith('/frame.json')}
    have = committed | set(a.frames)
    plan = json.load(open(a.plan))
    spine = keep(plan['spine'], have)
    stage(os.path.join(subject, 'spine.json'), spine)
    on_main = {f for s in spine['segments'] for f in s['frames']}
    for t in plan.get('trails', []):
        tspine = keep(t['spine'], have)
        if t['anchor'] in on_main and tspine['segments']:
            stage(os.path.join(subject, 'trails', f'{t["id"]}.json'), {**t, 'spine': tspine})
    run(['git', 'add', '--'] + [os.path.join(frames_dir, f) for f in a.frames] + a.also)
    print(f'stage_segment: staged {len(a.frames)} frames; the committed subject will hold {len(have)}')


if __name__ == '__main__':
    main()
