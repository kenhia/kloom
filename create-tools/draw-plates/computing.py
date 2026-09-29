"""The computing subject's scene plates (sprint 015).

    python3 create-tools/draw-plates/computing.py [frame ...]

Writes subjects/computing/frames/<frame>/scene.svg; with no arguments, redraws
every frame. The plates live in `computing_<part>.py` modules beside this one, each
exporting `PLATES = {frame id: function returning a D}`, so several authors
can draw at once without editing one file. Unlike western_civ.py, a plate
function returns its drawing and this script saves it.
"""
import importlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FRAMES = os.path.join(HERE, '..', '..', 'subjects', 'computing', 'frames')


def plates():
    found = {}
    for name in sorted(f[:-3] for f in os.listdir(HERE) if f.startswith('computing_') and f.endswith('.py')):
        for frame, fn in importlib.import_module(name).PLATES.items():
            if frame in found:
                sys.exit(f'computing.py: {frame} is drawn by two modules')
            found[frame] = fn
    return found


if __name__ == '__main__':
    all_plates = plates()
    for frame in sys.argv[1:] or sorted(all_plates):
        if frame not in all_plates:
            sys.exit(f'computing.py: no plate for {frame}')
        all_plates[frame]().save(os.path.join(FRAMES, frame, 'scene.svg'))
        print(f'drew {frame}')
