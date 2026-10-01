"""Draw a subject's scene plates from its `<subject>_<part>.py` modules (sprint 027).

    python3 create-tools/draw-plates/plates_for.py <subject> <frame> [<frame> ...]
    python3 create-tools/draw-plates/plates_for.py <subject> --all

Writes subjects/<subject>/frames/<frame>/scene.svg for each frame named. A
subject's plates live in modules beside this one, `<subject>_<part>.py` (a
dash in the subject id is an underscore), each exporting `PLATES = {frame id:
function returning a D}`, so several authors can draw at once without editing
one file. One collector serves every subject: sprints 006 to 026 copied a
`<subject>.py` collector seven times.

Which module draws a frame is read from its `PLATES` keys without importing
it, and only the modules that draw the frames named are imported. So another
author's half-written module costs nothing unless it draws a frame you named,
and a module that fails to import is named and skipped (sprint 026: one stray
character stopped nine authors). A bare run is refused: it would redraw every
author's plates, so say `--all` to mean that.
Standard library only.
"""
import argparse, ast, importlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SUBJECTS = os.path.join(HERE, '..', '..', 'subjects')


def prefix(subject):
    return subject.replace('-', '_') + '_'


def modules(subject, here=HERE):
    """{module name: [frame ids it draws]} for the subject's modules, read without importing them,
    and {module name: why it could not be read} for those that do not parse."""
    found, broken = {}, {}
    for f in sorted(os.listdir(here)):
        if not (f.startswith(prefix(subject)) and f.endswith('.py')):
            continue
        name = f[:-3]
        try:
            with open(os.path.join(here, f)) as fh:
                tree = ast.parse(fh.read(), f)
        except SyntaxError as e:
            broken[name] = f'SyntaxError: {e.msg} (line {e.lineno})'
            continue
        keys = None
        for node in tree.body:
            # `PLATES = {...}`, then any `PLATES['frame'] = fn` (sprint 026's modules grew that way).
            for t in node.targets if isinstance(node, ast.Assign) else []:
                if isinstance(t, ast.Name) and t.id == 'PLATES' and isinstance(node.value, ast.Dict):
                    keys = [k.value for k in node.value.keys if isinstance(k, ast.Constant)]
                elif (isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == 'PLATES'
                      and isinstance(t.slice, ast.Constant) and keys is not None):
                    keys.append(t.slice.value)
        if keys is None:
            broken[name] = 'no PLATES = {...} with frame ids as its keys'
        else:
            found[name] = keys
    return found, broken


def plates(subject, frames, here=HERE):
    """{frame: function} for the frames named, and {module: error} for each that failed.

    Exits naming a frame two modules draw or one no module draws."""
    found, broken = modules(subject, here)
    if not found and not broken:
        sys.exit(f'plates_for.py: no {prefix(subject)}*.py modules beside plates_for.py')
    owner = {}
    for name, keys in found.items():
        for frame in keys:
            if frame in owner:
                sys.exit(f'plates_for.py: {frame} is drawn by both {owner[frame]}.py and {name}.py')
            owner[frame] = name
    all_frames = frames is None
    frames = sorted(owner) if all_frames else frames
    if here not in sys.path:
        sys.path.insert(0, here)
    out, failed = {}, {}
    for frame in frames:
        name = owner.get(frame)
        if name is None:
            sys.exit(f'plates_for.py: no plate for {frame}'
                     + (f' (and {", ".join(sorted(broken))} could not be read, below)' if broken else ''))
        if name in failed:
            continue
        try:
            module = importlib.import_module(name)
        except Exception as e:  # noqa: BLE001 - any error in someone else's module
            failed[name] = f'{type(e).__name__}: {e}'
            continue
        out[frame] = module.PLATES[frame]
    # With frames named, a module that does not parse matters only if it might have drawn one (above).
    return out, {**broken, **failed} if all_frames else failed


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('subject')
    ap.add_argument('frames', nargs='*')
    ap.add_argument('--all', action='store_true', help="redraw every plate of the subject (every author's)")
    a = ap.parse_args(argv)
    if not a.frames and not a.all:
        ap.error("name the frames to draw, or --all to redraw every author's plates")
    if a.frames and a.all:
        ap.error('name frames or --all, not both')
    drawn, broken = plates(a.subject, None if a.all else a.frames)
    for name, err in broken.items():
        print(f'plates_for.py: skipped {name}.py ({err})', file=sys.stderr)
    for frame, fn in drawn.items():
        fn().save(os.path.join(SUBJECTS, a.subject, 'frames', frame, 'scene.svg'))
        print(f'drew {frame}')
    # A frame not drawn (its module failed) is a failure, however many others were drawn.
    return 1 if broken else 0


if __name__ == '__main__':
    sys.exit(main())
