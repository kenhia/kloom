"""Plates for Sound and Score's part classic2 (sprint 058): the Eroica and the virtuoso. See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def eroica():
    d = D()
    # Above: the first movement's 690 bars to scale, numbered as the Mutopia Project's edition counts
    # them with the exposition's second-time bars (development from 154, as Wikipedia gives it;
    # recapitulation from 398; Grove's 140-bar coda from 551). Below: bars 392-398 as pitch against
    # time, from the same edition: the violins' tremolo on A-flat and B-flat, the horn's E-flat, G,
    # E-flat, B-flat over it, the tutti's two bars on the dominant, and the return at 398.
    x0, x1, total = 22, 378, 690
    sx = lambda bar: x0 + (bar - 1) / total * (x1 - x0)
    secs = [(1, 154, 'EXPOSITION'), (154, 398, 'DEVELOPMENT'), (398, 551, 'RECAP'), (551, 691, 'CODA')]
    by, bh = 44, 30

    d.group('thin')
    for b in range(50, 691, 50):                                    # a tick every fifty bars
        d.line((sx(b), by + bh + 4), (sx(b), by + bh + 8))
    d.line((x0, by + bh + 6), (sx(691), by + bh + 6))
    for b in (154, 398, 551):                                         # the section lines, carried down
        d.line((sx(b), by - 6), (sx(b), by + bh + 10))

    d.group()
    for a, b, _ in secs:
        _box(d, sx(a), by, sx(b) - sx(a), bh)

    d.group('mid')
    # the exposition is played twice: a repeat sign at its end
    xr = sx(154) - 4
    d.line((xr, by + 6), (xr, by + bh - 6))
    d.circle(xr - 4, by + bh / 2 - 4, 1.2); d.circle(xr - 4, by + bh / 2 + 4, 1.2)
    # the two opening chords
    for b in (1, 2):
        d.line((sx(b) + 2 + b * 2, by + 6), (sx(b) + 2 + b * 2, by + bh - 6))
    # 248-279: the sforzando chords against the beat, a stroke every other bar
    for b in range(248, 280, 2):
        d.line((sx(b), by + 7), (sx(b), by + bh - 7))
    # 284: the new theme in E minor
    d.circle(sx(284) + 3, by + bh / 2, 3)
    # 394: the horn
    d.line((sx(394), by + bh + 14), (sx(394), by + bh))
    _arrow(d, (sx(394), by + bh + 14), (sx(394), by + bh), 4)

    # below: the horn passage, pitch (MIDI numbers) against time, four beats to a 3/4 bar's width
    gx0, gx1, gy0, gy1 = 40, 360, 140, 248                     # bars 392 to 399, pitches 44 to 72
    tx = lambda bar, beat=0: gx0 + ((bar - 392) + beat / 3) / 7 * (gx1 - gx0)
    py = lambda p: gy1 - (p - 44) / (72 - 44) * (gy1 - gy0)
    d.group('thin')
    for bar in range(392, 400):
        d.line((tx(bar), gy0), (tx(bar), gy1))
    d.line((gx0, gy1), (gx1, gy1))
    for p in (46, 51, 55, 68, 70):                                  # B-flat, E-flat, G, A-flat, B-flat
        d.line((gx0 - 4, py(p)), (gx0, py(p)))
    # the zoom from the band to the passage
    d.dashed((sx(392), by + bh + 18), (gx0 + 6, gy0 - 22), dash=3, gap=3)
    d.dashed((sx(399), by + bh + 18), (gx1 - 6, gy0 - 22), dash=3, gap=3)

    d.group('mid')
    # violins: a tremolo on A-flat and B-flat, bars 392-395, drawn as a fine zigzag
    for p in (68, 70):
        pts = []
        n = 48
        for i in range(n + 1):
            x = tx(392) + (tx(396) - tx(392)) * i / n
            pts.append((x, py(p) + (1.6 if i % 2 else -1.6)))
        d.line(*pts)
    # the tutti on the dominant seventh, bars 396-397: B-flat, D, F, A-flat, struck together
    for bar in (396, 397):
        x = tx(bar) + 4
        d.line((x, py(46)), (x, py(70)))
        for p in (46, 50, 53, 58, 62, 65, 68, 70):
            d.line((x - 3, py(p)), (x + 3, py(p)))

    d.group()
    # the horn: E-flat (two beats), G, E-flat (two beats), B-flat, bars 394-395
    notes = [(394, 0, 2, 51), (394, 2, 1, 55), (395, 0, 2, 51), (395, 2, 1, 46)]
    path = []
    for bar, beat, dur, p in notes:
        a, b = tx(bar, beat), tx(bar, beat + dur)
        path += [(a, py(p)), (b, py(p))]
    d.line(*path)
    # the recapitulation at 398: the same four notes, in the cellos, on E-flat
    d.line((tx(398), py(51)), (tx(398, 2), py(51)), (tx(398, 2), py(55)), (tx(399), py(55)))

    d.group('mid')
    d.text(sx(77), by - 10, 'EXPOSITION ×2', size=7)
    d.text(sx(276), by - 10, 'DEVELOPMENT', size=7)
    d.text(sx(474), by - 10, 'RECAP', size=7)
    d.text(sx(620), by - 10, 'CODA', size=7)
    d.text(x0, by + bh + 18, '1', size=7, anchor='start')
    d.text(sx(154), by + bh + 18, '154', size=7)
    d.text(sx(551), by + bh + 18, '551', size=7)
    d.text(x1, by + bh + 18, '690', size=7, anchor='end')
    d.text(sx(264), by + bh + 18, 'SF 248-79', size=7)
    d.text(tx(392, 0.2), py(70) - 8, 'VIOLINS A♭ B♭ · PP', size=7, anchor='start')
    d.text(tx(394, 0.2), py(55) - 8, 'HORN E♭ G E♭ B♭', size=7, anchor='start')
    d.text((tx(396) + tx(398)) / 2 + 4, gy0 - 4, 'TUTTI FF', size=7)
    d.text(tx(398, 0.2), py(55) - 8, 'RECAP 398', size=7, anchor='start')
    d.text(200, 292, 'FIRST MOVEMENT · 690 BARS · BARS 392-398 BELOW', size=7)
    return d


def virtuoso():
    d = D()
    # Above: a violin's G string, nut to bridge, drawn five times, once for each of its first five
    # modes of vibration, with the node where a light finger makes that mode sound alone: the natural
    # harmonics Paganini built passages from (frequencies from the open G's 196 Hz, times 1 to 5).
    # Below: two octaves and a third of a keyboard, with the stretches of Liszt's Paganini etudes:
    # the eleventh the 1838 version asks for, and the tenth the 1851 revision keeps to.
    nx, bx = 52, 300
    L = bx - nx
    rows = [(1, 'G3 196'), (2, 'G4 392'), (3, 'D5 588'), (4, 'G5 784'), (5, 'B5 980')]
    ys = [30 + i * 21 for i in range(5)]

    d.group('thin')
    for (n, _), y in zip(rows, ys):
        d.line((nx, y), (bx, y))                                        # each string at rest
    for n in (2, 3, 4, 5):                                              # the touch point, carried up
        x = nx + L / n
        d.line((x, ys[0] - 10), (x, ys[n - 1]))

    d.group()
    d.line((nx, ys[0] - 10), (nx, ys[-1] + 10))                         # nut
    d.line((bx, ys[0] - 10), (bx, ys[-1] + 10))                         # bridge

    d.group('mid')
    for (n, _), y in zip(rows, ys):
        A = 7
        up = [(nx + L * i / 160, y - A * math.sin(math.pi * n * i / 160)) for i in range(161)]
        dn = [(nx + L * i / 160, y + A * math.sin(math.pi * n * i / 160)) for i in range(161)]
        d.line(*up); d.line(*dn)
        if n > 1:
            d.circle(nx + L / n, y, 2.2)

    # the keyboard: white keys from C to the E two octaves and a third above (17 keys)
    kw = 14.0
    k0, ky, kh, bkh = 200 - 17 * kw / 2, 196, 62, 38
    whites = ['C', 'D', 'E', 'F', 'G', 'A', 'B'] * 3
    d.group()
    _box(d, k0, ky, 17 * kw, kh)
    for i in range(1, 17):
        d.line((k0 + i * kw, ky), (k0 + i * kw, ky + kh))
    for i in range(16):
        if whites[i] in ('C', 'D', 'F', 'G', 'A'):
            _box(d, k0 + (i + 1) * kw - kw * 0.3, ky, kw * 0.6, bkh)

    d.group('mid')
    c = k0 + kw / 2
    d.line((c, ky - 40), (c, ky + kh - 8))
    d.circle(c, ky + kh - 10, 2.4)
    for steps, y in ((9, ky - 12), (10, ky - 30)):
        e = c + steps * kw
        d.line((c, y), (e, y))
        _arrow(d, (c + 10, y), (c, y), 4); _arrow(d, (e - 10, y), (e, y), 4)
        d.line((e, y - 4), (e, ky + kh - 8))
        d.circle(e, ky + kh - 10, 2.4)

    d.group('mid')
    for (n, lab), y in zip(rows, ys):
        d.text(bx + 10, y + 3, lab, size=7, anchor='start')
    d.text(nx, ys[-1] + 22, 'NUT', size=7)
    d.text(bx, ys[-1] + 22, 'BRIDGE', size=7)
    d.text(176, ys[-1] + 22, 'TOUCH AT 1/2 1/3 1/4 1/5', size=7)
    d.text(c + 10 * kw + 8, ky - 27, 'ELEVENTH 1838', size=7, anchor='start')
    d.text(c + 10 * kw + 8, ky - 9, 'TENTH 1851', size=7, anchor='start')
    d.text(200, 286, "PAGANINI'S HARMONICS · LISZT'S STRETCH", size=7)
    return d


PLATES = {
    'eroica': eroica,
    'virtuoso': virtuoso,
}
