"""Count the prose in a subject's readings, as the grow skill counts it.

    python3 create-tools/subject-plan/prose_words.py SUBJECT_DIR [FRAME ...] [--min N] [--max N]

Tables, image lines (their alt text), raw chart lines and headings are not
counted. Prints one line per frame with a reading, marks
those outside --min/--max (default 550–900, a subject authored with tools),
and exits 1 if any is. Standard library only (sprint 015: four authors had
each written their own).
"""
import argparse, os, re, sys


def prose_words(text):
    kept = [line for line in text.splitlines()
            if not line.lstrip().startswith(('|', '![', '<', '#'))]
    # A link's words are prose; its target (a name mark's kloom:e/<id>, a URL) is not (sprint 021).
    prose = re.sub(r'\]\([^)]*\)', ']', '\n'.join(kept))
    return len(re.findall(r"[\w’'-]+", prose))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('subject')
    ap.add_argument('frames', nargs='*')
    ap.add_argument('--min', type=int, default=550)
    ap.add_argument('--max', type=int, default=900)
    a = ap.parse_args()
    frames_dir = os.path.join(a.subject, 'frames')
    frames = a.frames or sorted(d for d in os.listdir(frames_dir)
                                if os.path.isfile(os.path.join(frames_dir, d, 'reading.md')))
    outside = 0
    for f in frames:
        with open(os.path.join(frames_dir, f, 'reading.md')) as fh:
            n = prose_words(fh.read())
        flag = '' if a.min <= n <= a.max else f'  outside {a.min}–{a.max}'
        outside += bool(flag)
        print(f'{n:5d}  {f}{flag}')
    sys.exit(1 if outside else 0)


if __name__ == '__main__':
    main()
