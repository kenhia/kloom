"""Plates for the chemistry subject's Industry segment, part industry1 (sprint 025):
the soda processes, Perkin's mauveine and the Haber-Bosch process."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _offset(a, b, c, k=3.2):
    """A second, shorter line inside a double bond ab, on the side of point c (a ring's centre)."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = c[0] - mx, c[1] - my
    n = math.hypot(dx, dy)
    ox, oy = dx / n * k, dy / n * k
    t = 0.18
    return [(a[0] + (b[0] - a[0]) * t + ox, a[1] + (b[1] - a[1]) * t + oy),
            (a[0] + (b[0] - a[0]) * (1 - t) + ox, a[1] + (b[1] - a[1]) * (1 - t) + oy)]


def _parallel(a, b, k=3.2):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * k, dx / n * k
    return [[(a[0] + ox / 2, a[1] + oy / 2), (b[0] + ox / 2, b[1] + oy / 2)],
            [(a[0] - ox / 2, a[1] - oy / 2), (b[0] - ox / 2, b[1] - oy / 2)]]


def _hexagon(c, r, rot=-90):
    """The six vertices of a regular hexagon about c, the first at angle `rot` (degrees, SVG sense)."""
    return [_pt(c, rot + 60 * k, r) for k in range(6)]


def _trim(a, b, ta=0, tb=0):
    """The segment ab, shortened by ta at a and tb at b, to leave room for an atom's letter."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    return [(a[0] + dx / n * ta, a[1] + dy / n * ta), (b[0] - dx / n * tb, b[1] - dy / n * tb)]


def mauveine():
    """Mauveine A, 3-amino-2-methyl-5-phenyl-7-(p-tolylamino)phenazinium, from regular hexagons,
    as Meth-Cohn and Smith (1994) found it in Perkin's factory samples, with its Kekule bonds
    as PubChem's SMILES for the cation gives them."""
    d = D()
    L = 24                                           # bond length
    w = L * math.sqrt(3)                             # distance between fused ring centres
    cy = 100
    cm = (168, cy)                                   # the central, pyrazine ring
    cl, cr = (cm[0] - w, cy), (cm[0] + w, cy)        # the left (amino, methyl) and right (tolylamino) rings
    # pointy-top hexagons: vertex k at -90 + 60k, i.e. top, upper right, lower right, bottom, lower left, upper left
    top, ur, lr, bot, ll, ul = range(6)
    M, Lf, R = _hexagon(cm, L), _hexagon(cl, L), _hexagon(cr, L)
    n_top, n_bot = M[top], M[bot]                    # N5 (=N-) and N10 (N+, carrying the phenyl)
    c4, cd, ce, cf, cg, ch = Lf[ur], Lf[top], Lf[ul], Lf[ll], Lf[bot], Lf[lr]
    ct, ca, cb, c2, cc, c3 = R[ul], R[top], R[ur], R[lr], R[bot], R[ll]
    me = _pt(ce, -150, L)                            # the methyl, from the o-toluidine
    nh2 = _pt(cf, 150, L)                            # the amino group
    ph_n = _pt(n_bot, 90, L)                         # the phenyl's ipso carbon, below N+
    ph_c = (ph_n[0], ph_n[1] + L)
    PH = _hexagon(ph_c, L)
    nh = _pt(c2, 30, L)                              # the NH of the p-tolylamino group
    tol_i = _pt(nh, -30, L)
    tol_c = _pt(tol_i, 0, L)
    TOL = _hexagon(tol_c, L, rot=180)
    tol_me = _pt(TOL[3], 0, L)
    g = 7                                            # the gap left round a lettered atom

    d.group('thin')
    for c in (cl, cm, cr, ph_c, tol_c):
        d.circle(*c, L * 1.18)
    d.line((cm[0], cy - 62), (cm[0], ph_c[1] + L + 14))
    d.line((cl[0] - 58, cy), (cr[0] + 40, cy))
    d.group()
    bonds = [_trim(M[ul], n_top, 0, g), _trim(n_top, M[ur], g, 0), _trim(M[lr], n_bot, 0, g),
             _trim(n_bot, M[ll], g, 0), [M[ul], M[ll]], [M[ur], M[lr]],
             [c4, cd, ce, cf, cg, ch], [ct, ca, cb, c2, cc, c3],
             PH + [PH[0]], TOL + [TOL[0]],
             _trim(ce, me, 0, g + 3), _trim(cf, nh2, 0, g + 3), _trim(n_bot, ph_n, g, 0),
             _trim(c2, nh, 0, g), _trim(nh, tol_i, g, 0), _trim(TOL[3], tol_me, 0, g + 3)]
    d.lines(bonds)
    d.group('mid')
    # double bonds: the quinoid left ring and the two C=N of the centre, the aromatic right ring,
    # and Kekule pairs in the phenyl and tolyl
    d.lines([_offset(cd, ce, cl), _offset(cf, cg, cl),
             _trim(*_offset(n_top, c4, cm), 3, 0), _trim(*_offset(ch, n_bot, cm), 0, 3),
             _offset(c3, ct, cr), _offset(ca, cb, cr), _offset(c2, cc, cr),
             _offset(PH[0], PH[1], ph_c), _offset(PH[2], PH[3], ph_c), _offset(PH[4], PH[5], ph_c),
             _offset(TOL[0], TOL[1], tol_c), _offset(TOL[2], TOL[3], tol_c), _offset(TOL[4], TOL[5], tol_c)])
    d.group('mid')
    d.text(n_top[0], n_top[1] + 3.5, 'N', size=10)
    d.text(n_bot[0], n_bot[1] + 3.5, 'N', size=10)
    d.text(n_bot[0] + 7, n_bot[1] - 3, '+', size=8, anchor='start')
    d.text(nh2[0] + 3, nh2[1] + 3.5, 'H₂N', size=9, anchor='end')
    d.text(me[0] + 3, me[1] + 3.5, 'H₃C', size=9, anchor='end')
    d.text(nh[0], nh[1] + 3.5, 'N', size=10)
    d.text(nh[0], nh[1] + 15, 'H', size=9)
    d.text(tol_me[0] - 3, tol_me[1] + 3.5, 'CH₃', size=9, anchor='start')
    d.text(200, 250, 'MAUVEINE A · C₂₆H₂₃N₄⁺', size=8)
    d.text(200, 270, '2 C₁₀H₁₃N + 3 O → C₂₀H₂₄N₂O₂ + H₂O', size=8)
    d.text(200, 284, 'PERKIN’S QUININE, 1856: IT BALANCES, AND FAILS', size=7)
    return d


def _arrow(d, tip, ang, s=5):
    """An open arrowhead at `tip`, pointing along angle `ang` (degrees, SVG sense)."""
    d.line(_pt(tip, ang + 180 - 28, s), tip, _pt(tip, ang + 180 + 28, s))


def _arc_arrow(d, c, r, a0, a1, n=30):
    """An arc about c from angle a0 to a1, with an arrowhead at a1."""
    d.arc(c[0], c[1], r, a0, a1, n=n)
    tip = _pt(c, a1, r)
    tangent = a1 + (90 if a1 > a0 else -90)
    _arrow(d, tip, tangent)


def leblanc_solvay():
    """Solvay's ammonia-soda process as a loop: four vessels on a circle, the ammonia and carbon
    dioxide going round, and only salt and limestone going in."""
    d = D()
    C, r = (200, 122), 76
    top, rgt, bot, lft = _pt(C, -90, r), _pt(C, 0, r), _pt(C, 90, r), _pt(C, 180, r)
    d.group('thin')
    d.circle(*C, r)
    d.line((C[0], C[1] - r - 26), (C[0], C[1] + r + 26))
    d.line((C[0] - r - 40, C[1]), (C[0] + r + 40, C[1]))
    d.group()
    # the carbonating tower (top), tall, with its plates
    tw, th = 16, 44
    d.line((top[0] - tw / 2, top[1] - th / 2), (top[0] + tw / 2, top[1] - th / 2),
           (top[0] + tw / 2, top[1] + th / 2), (top[0] - tw / 2, top[1] + th / 2), closed=True)
    # the calciner (right), a drum
    d.circle(*rgt, 13)
    # the ammonia still (bottom), a column
    sw, sh = 18, 30
    d.line((bot[0] - sw / 2, bot[1] - sh / 2), (bot[0] + sw / 2, bot[1] - sh / 2),
           (bot[0] + sw / 2, bot[1] + sh / 2), (bot[0] - sw / 2, bot[1] + sh / 2), closed=True)
    # the lime kiln (left), a shaft narrowing upward
    d.line((lft[0] - 8, lft[1] - 18), (lft[0] + 8, lft[1] - 18), (lft[0] + 13, lft[1] + 18),
           (lft[0] - 13, lft[1] + 18), closed=True)
    d.group('mid')
    d.lines([[(top[0] - tw / 2, top[1] - th / 2 + k * th / 6), (top[0] + tw / 2, top[1] - th / 2 + k * th / 6)]
             for k in range(1, 6)])
    d.lines([[(bot[0] - sw / 2, bot[1] - sh / 2 + k * sh / 4), (bot[0] + sw / 2, bot[1] - sh / 2 + k * sh / 4)]
             for k in range(1, 4)])
    d.circle(*rgt, 6)
    d.group()
    # the flows round the loop: gas and solids on the circle, the liquor across it
    _arc_arrow(d, C, r, 196, 258)                  # CO2, kiln to tower
    _arc_arrow(d, C, r, 288, 346)                  # NaHCO3, tower to calciner
    _arc_arrow(d, C, r - 14, 340, 290)             # CO2 back from the calciner to the tower
    _arc_arrow(d, C, r, 164, 106)                  # CaO, kiln to still
    d.line((C[0] - 6, top[1] + th / 2 + 4), (C[0] - 6, bot[1] - sh / 2 - 4))
    _arrow(d, (C[0] - 6, bot[1] - sh / 2 - 4), 90)  # NH4Cl liquor down to the still
    d.line((C[0] + 6, bot[1] - sh / 2 - 4), (C[0] + 6, top[1] + th / 2 + 4))
    _arrow(d, (C[0] + 6, top[1] + th / 2 + 4), -90)  # NH3 back up to the tower
    # what goes in and what comes out
    d.line((top[0], top[1] - th / 2 - 22), (top[0], top[1] - th / 2 - 3))
    _arrow(d, (top[0], top[1] - th / 2 - 3), 90)
    d.line((lft[0] - 58, lft[1]), (lft[0] - 16, lft[1]))
    _arrow(d, (lft[0] - 16, lft[1]), 0)
    d.line((rgt[0] + 16, rgt[1]), (rgt[0] + 58, rgt[1]))
    _arrow(d, (rgt[0] + 58, rgt[1]), 0)
    d.line((bot[0], bot[1] + sh / 2 + 3), (bot[0], bot[1] + sh / 2 + 22))
    _arrow(d, (bot[0], bot[1] + sh / 2 + 22), 90)
    d.group('mid')
    d.text(top[0] + 14, top[1] - th / 2 - 12, 'BRINE, NaCl', size=8, anchor='start')
    d.text(lft[0] - 60, lft[1] - 6, 'CaCO₃', size=8, anchor='start')
    d.text(rgt[0] + 60, rgt[1] - 6, 'Na₂CO₃', size=8, anchor='end')
    d.text(bot[0] + 14, bot[1] + sh / 2 + 18, 'CaCl₂', size=8, anchor='start')
    d.text(*_pt(C, 222, r + 12), 'CO₂', size=7, anchor='end')
    d.text(*_pt(C, 318, r + 14), 'NaHCO₃', size=7, anchor='start')
    d.text(*_pt(C, 138, r + 12), 'CaO', size=7, anchor='end')
    d.text(*_pt(C, 318, r - 30), 'CO₂', size=7, anchor='end')
    d.text(C[0] - 10, C[1] + 22, 'NH₄Cl', size=7, anchor='end')
    d.text(C[0] + 10, C[1] - 16, 'NH₃', size=7, anchor='start')
    d.text(200, 272, '2 NaCl + CaCO₃ → Na₂CO₃ + CaCl₂', size=8)
    d.text(200, 286, 'THE AMMONIA GOES ROUND AND COMES BACK', size=7)
    return d


def haber_bosch():
    """Bosch's converter in section, after his Nobel lecture: a thick steel jacket that holds the
    pressure, drilled with holes, round a thin soft-steel liner that holds the gas; and the loop
    that takes the ammonia out and sends the rest round again."""
    d = D()
    cx, top, bot = 96, 34, 236                  # the converter's axis, top and bottom
    ro, ri, rl = 36, 26, 24                     # jacket outside, jacket inside, liner inside
    cat0, cat1 = 70, 160                        # the catalyst bed
    d.group('thin')
    d.line((cx, top - 14), (cx, bot + 14))
    for y in (cat0, cat1):
        d.line((cx - ro - 10, y), (cx + ro + 10, y))
    # dimension line across the jacket's wall
    d.line((cx + ri, bot + 20), (cx + ro, bot + 20))
    d.line((cx + ri, bot + 4), (cx + ri, bot + 24))
    d.line((cx + ro, bot + 4), (cx + ro, bot + 24))
    d.group()
    # the jacket, in section: two walls each side, closed at the ends
    for sgn in (-1, 1):
        d.line((cx + sgn * ri, top), (cx + sgn * ri, bot))
        d.line((cx + sgn * ro, top + 8), (cx + sgn * ro, bot - 8))
    d.line((cx - ro, top + 8), (cx - ri, top), (cx + ri, top), (cx + ro, top + 8))
    d.line((cx - ro, bot - 8), (cx - ri, bot), (cx + ri, bot), (cx + ro, bot - 8))
    # the liner, thin, just inside the jacket
    d.line((cx - rl, top + 2), (cx - rl, bot - 2))
    d.line((cx + rl, top + 2), (cx + rl, bot - 2))
    d.group('mid')
    # the holes drilled through the jacket, where the hydrogen that leaks through the liner escapes
    holes = []
    for k in range(9):
        y = top + 22 + k * (bot - top - 44) / 8
        for sgn in (-1, 1):
            holes.append([(cx + sgn * ri, y), (cx + sgn * ro, y)])
            holes.append([(cx + sgn * ri, y + 3), (cx + sgn * ro, y + 3)])
    d.lines(holes)
    # the catalyst: lumps packed in the bed
    for j in range(7):
        for i in range(4):
            x = cx - 15 + i * 10 + (5 if j % 2 else 0)
            y = cat0 + 8 + j * 12.5
            if abs(x - cx) < 20:
                d.circle(x, y, 3.2)
    # the heat exchanger below the bed: tubes that warm the incoming gas with the outgoing
    d.lines([[(cx + dx, cat1 + 8), (cx + dx, bot - 12)] for dx in (-14, -7, 0, 7, 14)])
    d.group()
    # the loop: out of the top, through the cooler and separator, round the pump, back in at the bottom
    xc, xs, xp = 214, 290, 214                  # cooler, separator, pump
    d.line((cx, top), (cx, top - 10), (xc, top - 10), (xc, 60))
    coil = [(xc + (10 if k % 2 else -10), 60 + k * 8) for k in range(11)]
    d.line((xc, 60), *coil, (xc, 148))
    d.line((xc, 148), (xc, 156), (xs - 8, 156), (xs - 8, 150))
    d.line((xs - 18, 150), (xs - 18, 214), (xs + 18, 214), (xs + 18, 150), (xs - 18, 150))
    d.line((xs + 8, 150), (xs + 8, 120), (340, 120))                      # unreacted gas out of the separator's top
    d.line((340, 120), (340, 256), (xp + 14, 256))                # and round to the pump
    d.circle(xp, 256, 14)
    d.line((xp - 14, 256), (cx, 256), (cx, bot))                  # back into the converter
    d.line((xs, 214), (xs, 236))                                  # liquid ammonia drawn off
    _arrow(d, (xs, 236), 90)
    d.line((372, 188), (340, 188))                                # fresh N2 + 3 H2
    _arrow(d, (340, 188), 180)
    _arrow(d, (xc, 56), 90)
    _arrow(d, (cx + 2, 244), -90)
    d.group('mid')
    d.line((xs - 18, 196), (xs + 18, 196))                        # the liquid's surface
    d.lines([[(xs - 12 + 6 * k, 202), (xs - 9 + 6 * k, 202)] for k in range(5)])
    d.line((xp - 7, 250), (xp + 7, 256), (xp - 7, 262))           # the pump's vane
    d.group('mid')
    d.text(cx, top - 16, 'CONVERTER', size=7)
    d.text(cx + ro + 8, cat0 + 50, 'CATALYST', size=7, anchor='start')
    d.text(cx + ro + 8, bot - 30, 'HEAT', size=7, anchor='start')
    d.text(cx + ro + 8, bot - 21, 'EXCHANGE', size=7, anchor='start')
    d.text(cx + (ri + ro) / 2, bot + 32, 'JACKET', size=7)
    d.text(xc - 16, 104, 'COOLER', size=7, anchor='end')
    d.text(xs + 24, 206, 'LIQUID', size=7, anchor='start')
    d.text(xs + 24, 215, 'NH₃', size=7, anchor='start')
    d.text(346, 180, 'N₂ + 3 H₂', size=7, anchor='start')
    d.text(xp, 280, 'PUMP', size=7)
    d.text(250, 36, 'N₂ + 3 H₂ ⇌ 2 NH₃', size=9, anchor='start')
    d.text(250, 50, '200 ATM · 500 °C', size=7, anchor='start')
    return d


PLATES = {'haber-bosch': haber_bosch, 'leblanc-solvay': leblanc_solvay, 'mauveine': mauveine}
