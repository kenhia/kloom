"""Count the prose in a subject's readings, as the grow skill counts it.

    python3 create-tools/subject-plan/prose_words.py SUBJECT_DIR [FRAME ...] [--min N] [--max N]
    python3 create-tools/subject-plan/prose_words.py PATH [PATH ...] [--min N] [--max N]

Tables, image lines (their alt text), raw chart lines and headings are not
counted. Prints one line per frame with a reading, marks
those outside --min/--max (default 550–900, a subject authored with tools),
and exits 1 if any is. A subject's directory counts its frames (or the
FRAMEs named); otherwise each PATH is a frame's directory, a reading file,
or a directory holding frame directories, such as a checking copy or a
draft kept outside the subject (sprint 025's authors could not count one).
Standard library only (sprint 015: four authors had each written their own).
"""
import argparse, os, re, sys


def prose_words(text):
    kept = [line for line in text.splitlines()
            if not line.lstrip().startswith(('|', '![', '<', '#'))]
    # A link's words are prose; its target (a name mark's kloom:e/<id>, a URL) is not (sprint 021).
    prose = re.sub(r'\]\([^)]*\)', ']', '\n'.join(kept))
    return len(re.findall(r"[\w’'-]+", prose))


def readings(paths):
    """(name, path of reading.md) for each path: a reading file, a frame's directory, or a directory
    of frame directories."""
    for p in paths:
        if os.path.isfile(p):
            yield os.path.basename(os.path.dirname(os.path.abspath(p))) if os.path.basename(p) == 'reading.md' else p, p
        elif os.path.isfile(os.path.join(p, 'reading.md')):
            yield os.path.basename(os.path.normpath(p)), os.path.join(p, 'reading.md')
        elif os.path.isdir(p):
            found = sorted(d for d in os.listdir(p) if os.path.isfile(os.path.join(p, d, 'reading.md')))
            if not found:
                sys.exit(f'prose_words: no reading.md in {p} or the directories in it')
            for d in found:
                yield d, os.path.join(p, d, 'reading.md')
        else:
            sys.exit(f'prose_words: no such file or directory: {p}')


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('subject', help="a subject's directory, or a path to count")
    ap.add_argument('frames', nargs='*', help="with a subject's directory, its frames; otherwise more paths")
    ap.add_argument('--min', type=int, default=550)
    ap.add_argument('--max', type=int, default=900)
    a = ap.parse_args()
    frames_dir = os.path.join(a.subject, 'frames')
    if os.path.isdir(frames_dir):
        found = [(f, os.path.join(frames_dir, f, 'reading.md')) for f in a.frames] if a.frames else \
            readings([frames_dir])
    else:
        found = readings([a.subject, *a.frames])
    outside = 0
    for name, path in found:
        with open(path) as fh:
            n = prose_words(fh.read())
        flag = '' if a.min <= n <= a.max else f'  outside {a.min}–{a.max}'
        outside += bool(flag)
        print(f'{n:5d}  {name}{flag}')
    sys.exit(1 if outside else 0)


if __name__ == '__main__':
    main()
