"""How often a subject's main spine switches between dark and light (korg 3495).

    python3 create-tools/palette-switches/palette_switches.py [SUBJECTS_DIR] [--subject ID ...]

For each subject, the share of main-spine steps (frame to next frame) whose
scheme changes: once with each frame wearing its own palette (Scene colours
Each frame), once by section (the default: a frame takes its section's
scheme, the segment's `palette` or else its first frame's), and the
sections and their palettes. Sprint 038 recorded it before and after the
re-palette. Standard library only.
"""
import argparse, json, os


def load(subject_dir):
    with open(os.path.join(subject_dir, 'subject.json')) as fh:
        palettes = json.load(fh)['palettes']
    with open(os.path.join(subject_dir, 'spine.json')) as fh:
        spine = json.load(fh)
    frames = {}
    for seg in spine['segments']:
        for f in seg['frames']:
            with open(os.path.join(subject_dir, 'frames', f, 'frame.json')) as fh:
                frames[f] = json.load(fh)['scene']['palette']
    return palettes, spine, frames


def switches(schemes):
    steps = len(schemes) - 1
    n = sum(1 for a, b in zip(schemes, schemes[1:]) if a != b)
    return n, steps


def measure(subject_dir):
    palettes, spine, frames = load(subject_dir)
    own, section, sections = [], [], []
    for seg in spine['segments']:
        name = seg.get('palette') or frames[seg['frames'][0]]
        sections.append((seg['id'], name, palettes[name]['scheme'], len(seg['frames'])))
        for f in seg['frames']:
            own.append(palettes[frames[f]]['scheme'])
            section.append(palettes[name]['scheme'])
    return switches(own), switches(section), sections


def pct(n, steps):
    return f'{round(100 * n / steps) if steps else 0}% ({n}/{steps})'


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument('subjects', nargs='?', default='subjects')
    p.add_argument('--subject', action='append')
    p.add_argument('--sections', action='store_true', help='list each section and its palette')
    a = p.parse_args()
    ids = a.subject or sorted(d for d in os.listdir(a.subjects)
                              if os.path.isfile(os.path.join(a.subjects, d, 'subject.json')))
    print('| Subject | Each frame | By section |')
    print('|---|---|---|')
    for s in ids:
        own, section, sections = measure(os.path.join(a.subjects, s))
        print(f'| {s} | {pct(*own)} | {pct(*section)} |')
        if a.sections:
            for sid, name, scheme, n in sections:
                print(f'|   {sid} | {name} ({scheme}) | {n} frames |')


if __name__ == '__main__':
    main()
