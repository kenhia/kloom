"""Give a subject a palette per section, and its frames that palette (sprint 038, korg 3495).

    python3 create-tools/palette-switches/repalette.py SECTIONS.json [--subject ID ...] [--dry-run]

SECTIONS.json maps each subject to its sections' palettes:

    {"physics": {"segments": {"greeks": "bronze", ...},
                 "trails": {"the-field": "foolscap", "measure": {"constants": "night", ...}},
                 "keep": ["a-frame-that-stands-apart"],
                 "frames": true}}

Each named segment of `spine.json` gets `palette`, and so does every segment
of each named trail (or each of its segments, where the trail maps them). Unless `"frames": false` (western-civ, whose frames keep
their hand-curated palettes), every frame in a section is rewritten to wear
the section's palette, except the frames in `keep`. The subject's plan under
create-tools/subject-plan/, if it has one, gets the same palettes, so
`subject_plan.py --check` sees no drift. A segment or trail left out of the
map is an error: a re-palette covers the whole subject. Files are rewritten
in place; run Prettier over them after. Standard library only.
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
PALETTE = re.compile(r'("palette":\s*")([^"]+)(")')


def with_palette(seg, palette):
    """The segment with `palette` placed after `labelKind`, so the file reads in its usual order."""
    out = {}
    for k, v in seg.items():
        if k == 'palette':
            continue
        if k == 'frames':
            out['palette'] = palette
        out[k] = v
    return out


def trail_palette(spec, trail, segment):
    """A trail's palette, or its segment's where the map gives the trail one per segment."""
    v = spec['trails'][trail]
    if isinstance(v, dict):
        if segment not in v:
            sys.exit(f'repalette: trail "{trail}" segment "{segment}" has no palette in the map')
        return v[segment]
    return v


def dump(path, value, dry):
    if not dry:
        with open(path, 'w') as fh:
            fh.write(json.dumps(value, indent='\t', ensure_ascii=False) + '\n')


def repalette(subject, spec, dry=False):
    d = os.path.join(ROOT, 'subjects', subject)
    with open(os.path.join(d, 'subject.json')) as fh:
        palettes = json.load(fh)['palettes']
    wanted = list(spec.get('segments', {}).values())
    for v in spec.get('trails', {}).values():
        wanted += list(v.values()) if isinstance(v, dict) else [v]
    for name in wanted:
        if name not in palettes:
            sys.exit(f'repalette: {subject}: unknown palette "{name}"')
    section_of = {}  # frame -> palette
    changed = []

    with open(os.path.join(d, 'spine.json')) as fh:
        spine = json.load(fh)
    for i, seg in enumerate(spine['segments']):
        if seg['id'] not in spec.get('segments', {}):
            sys.exit(f'repalette: {subject}: segment "{seg["id"]}" has no palette in the map')
        p = spec['segments'][seg['id']]
        spine['segments'][i] = with_palette(seg, p)
        section_of.update({f: p for f in seg['frames']})
    dump(os.path.join(d, 'spine.json'), spine, dry)

    trails_dir = os.path.join(d, 'trails')
    for t in sorted(os.listdir(trails_dir)) if os.path.isdir(trails_dir) else []:
        path = os.path.join(trails_dir, t)
        with open(path) as fh:
            trail = json.load(fh)
        if trail['id'] not in spec.get('trails', {}):
            sys.exit(f'repalette: {subject}: trail "{trail["id"]}" has no palette in the map')
        trail['spine']['segments'] = [with_palette(s, trail_palette(spec, trail['id'], s['id']))
                                      for s in trail['spine']['segments']]
        section_of.update({f: s['palette'] for s in trail['spine']['segments'] for f in s['frames']})
        dump(path, trail, dry)

    if spec.get('frames', True):
        keep = set(spec.get('keep', []))
        for f, p in sorted(section_of.items()):
            if f in keep:
                continue
            path = os.path.join(d, 'frames', f, 'frame.json')
            with open(path) as fh:
                text = fh.read()
            found = PALETTE.findall(text)
            if len(found) != 1:
                sys.exit(f'repalette: {subject}/{f}: expected one "palette" in frame.json, found {len(found)}')
            if found[0][1] != p:
                changed.append((f, found[0][1], p))
                if not dry:
                    with open(path, 'w') as fh:
                        fh.write(PALETTE.sub(lambda m: m.group(1) + p + m.group(3), text))

    plan_path = os.path.join(ROOT, 'create-tools', 'subject-plan', f'{subject}.json')
    if os.path.isfile(plan_path):
        with open(plan_path) as fh:
            plan = json.load(fh)
        for s in plan['spine']['segments']:
            if s['id'] not in spec['segments']:
                sys.exit(f'repalette: {subject}: the plan\'s segment "{s["id"]}" has no palette in the map')
        plan['spine']['segments'] = [with_palette(s, spec['segments'][s['id']]) for s in plan['spine']['segments']]
        for t in plan.get('trails', []):
            t['spine']['segments'] = [with_palette(s, trail_palette(spec, t['id'], s['id']))
                                      for s in t['spine']['segments']]
        keep = set(spec.get('keep', []))
        for f, e in plan.get('frames', {}).items():
            if 'palette' in e and f in section_of and f not in keep and spec.get('frames', True):
                e['palette'] = section_of[f]
        dump(plan_path, plan, dry)
    return changed


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument('sections')
    p.add_argument('--subject', action='append')
    p.add_argument('--dry-run', action='store_true')
    a = p.parse_args()
    with open(a.sections) as fh:
        sections = json.load(fh)
    for subject in a.subject or sorted(sections):
        changed = repalette(subject, sections[subject], a.dry_run)
        print(f'{subject}: {len(changed)} frame(s) {"would change" if a.dry_run else "changed"}')


if __name__ == '__main__':
    main()
