"""The making subject (How We Build)'s scene plates (sprint 026).

    python3 create-tools/draw-plates/making.py [frame ...]

Writes subjects/making/frames/<frame>/scene.svg; with no arguments, redraws
every frame. A module that fails to import is named and skipped, so it
stops only its own frames. The plates live in `making_<part>.py` modules beside this one, each
exporting `PLATES = {frame id: function returning a D}`, so several authors
can draw at once without editing one file. Unlike western_civ.py, a plate
function returns its drawing and this script saves it.
"""
import importlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FRAMES = os.path.join(HERE, '..', '..', 'subjects', 'making', 'frames')


def plates():
    """Every plate, and the modules that failed to import (each named with its error).

    A module another author is halfway through can be broken; it costs only its
    own frames, not everyone's (sprint 026: three authors were stopped by one).
    """
    found, broken = {}, {}
    for name in sorted(f[:-3] for f in os.listdir(HERE) if f.startswith('making_') and f.endswith('.py')):
        try:
            module = importlib.import_module(name)
        except Exception as e:  # noqa: BLE001 - any error in someone else's module
            broken[name] = f'{type(e).__name__}: {e}'
            continue
        for frame, fn in module.PLATES.items():
            if frame in found:
                sys.exit(f'making.py: {frame} is drawn by two modules')
            found[frame] = fn
    return found, broken


if __name__ == '__main__':
    all_plates, broken = plates()
    for name, err in broken.items():
        print(f'making.py: skipped {name}.py ({err})', file=sys.stderr)
    for frame in sys.argv[1:] or sorted(all_plates):
        if frame not in all_plates:
            sys.exit(f'making.py: no plate for {frame}' + (' (a module failed to import, above)' if broken else ''))
        all_plates[frame]().save(os.path.join(FRAMES, frame, 'scene.svg'))
        print(f'drew {frame}')
