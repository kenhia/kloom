"""Plates for Daily Bread's part modern3 (sprint 051): gm-crops, hunger-now. See plates_for.py."""
import math
from statistics import NormalDist
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def gm_crops():
    d = D()
    # How a crop is transformed, as a flow. Top: the construct, the stretch of DNA between the T-DNA's
    # left and right borders (a promoter, the gene, a selectable marker). Middle: the two ways in, an
    # Agrobacterium carrying it on its plasmid into a wounded leaf disc, or a gene gun firing DNA-coated
    # gold into tissue. Bottom: selection on a medium only transformed cells survive, regeneration of a
    # whole plant in tissue culture, and the plant that is tested and crossed into elite varieties.
    # Proportions are schematic.
    d.group('thin')
    d.line((40, 44), (360, 44))                                           # the construct's axis
    d.line((105, 72), (105, 112))                                          # down to each route
    d.line((295, 72), (295, 112))
    d.line((105, 172), (110, 210))                                         # the routes converge
    d.line((295, 172), (110, 210))
    d.line((60, 252), (340, 252))                                          # the bench line

    d.group()
    # the construct: border, promoter, gene, marker, border
    segs = [(70, 120, 'PROMOTER'), (128, 248, 'GENE'), (256, 320, 'MARKER')]
    for x0, x1, _ in segs:
        _box(d, x0, 36, x1 - x0, 16)
    for x in (56, 334):                                                    # the left and right borders
        d.line((x, 34), (x + 8, 44), (x, 54), closed=True)
    # the Agrobacterium: a rod with its circular plasmid
    d.ellipse(80, 132, 34, 13)
    d.circle(92, 132, 7)
    # the leaf disc it infects, its rim nicked where it was cut
    rim = []
    for i in range(49):
        a = 2 * math.pi * i / 48
        r = 18 + (1.5 if i % 4 == 0 else 0)
        rim.append((150 + r * math.cos(a), 140 + r * math.sin(a)))
    d.line(*rim, closed=True)
    # the gene gun: a barrel and its stopping screen
    _box(d, 250, 118, 48, 18)
    d.line((298, 112), (298, 142))
    # the target tissue on its gel
    d.ellipse(340, 160, 26, 6)
    d.ellipse(340, 152, 14, 6)

    d.group('mid')
    _arrow(d, (105, 72), (105, 112))
    _arrow(d, (295, 72), (295, 112))
    d.line((115, 134), (130, 138))                                         # the bacterium meets the leaf
    _arrow(d, (115, 134), (130, 138), size=4)
    for i in range(5):                                                     # gold particles in flight
        t = i / 4
        x, y = 304 + 30 * t, 126 + 22 * t * t
        d.circle(x, y, 1.6)
    _arrow(d, (105, 172), (110, 210))
    _arrow(d, (295, 172), (110, 210))

    d.group()
    # selection: a dish in which a few calli survive
    d.ellipse(110, 228, 40, 12)
    d.line((70, 228), (70, 236))
    d.line((150, 228), (150, 236))
    d.arc(110, 236, 40, 0, 180, ry=12)
    # regeneration: a culture vessel with a shoot
    _box(d, 186, 206, 28, 46)
    d.line((200, 246), (200, 224))
    d.curve('M 200 232 Q 192 226 190 218')
    d.curve('M 200 228 Q 208 222 210 214')
    # the whole plant
    d.line((300, 252), (300, 196))
    for k, y in enumerate((236, 222, 208)):
        s = 1 if k % 2 == 0 else -1
        d.curve(f'M 300 {y} Q {300 + s * 14} {y - 10} {300 + s * 26} {y - 6}')
    d.ellipse(300, 192, 3, 5)

    d.group('mid')
    for x, y in ((96, 226), (118, 230), (128, 224)):                       # the surviving calli
        d.circle(x, y, 3)
    for x, y in ((84, 230), (104, 224), (140, 229), (114, 226)):           # cells that died
        d.line((x - 2, y - 2), (x + 2, y + 2))
        d.line((x - 2, y + 2), (x + 2, y - 2))
    d.line((154, 230), (182, 230))
    _arrow(d, (154, 230), (182, 230), size=4)
    d.line((218, 230), (282, 230))
    _arrow(d, (218, 230), (282, 230), size=4)

    d.group('mid')
    for x0, x1, s in segs:
        d.text((x0 + x1) / 2, 47, s, size=7)
    d.text(48, 66, 'LB', size=7)
    d.text(342, 66, 'RB', size=7)
    d.text(200, 22, 'THE CONSTRUCT · BETWEEN THE T-DNA BORDERS', size=7)
    d.text(80, 160, 'AGROBACTERIUM', size=7)
    d.text(150, 172, 'LEAF DISC', size=7)
    d.text(258, 106, 'GENE GUN', size=7)
    d.text(340, 178, 'GOLD INTO TISSUE', size=7)
    d.text(110, 270, 'SELECT', size=7)
    d.text(200, 270, 'REGENERATE', size=7)
    d.text(300, 270, 'TEST AND BREED', size=7)
    d.text(200, 290, 'ONLY CELLS CARRYING THE MARKER GROW', size=7)
    return d


def _lognormal(mean, cv):
    """The density of habitual intake, lognormal with this mean and coefficient of variation."""
    s2 = math.log(1 + cv * cv)
    s, mu = math.sqrt(s2), math.log(mean) - s2 / 2

    def pdf(x):
        return math.exp(-(math.log(x) - mu) ** 2 / (2 * s2)) / (x * s * math.sqrt(2 * math.pi))

    def cdf(x):
        return NormalDist().cdf((math.log(x) - mu) / s)
    return pdf, cdf


def hunger_now():
    d = D()
    # How FAO counts the undernourished: a population's habitual dietary energy intake as a lognormal
    # curve with a mean and a coefficient of variation, and the share of it below the minimum dietary
    # energy requirement (MDER). The country is invented: mean 2,400 kcal, CV 0.30, MDER 1,800 kcal,
    # which leaves 20.2% below the line; at CV 0.25 (the dashed curve) the same mean leaves 14.8%.
    x0, x1, y0, y1 = 50, 370, 236, 46
    lo, hi = 500, 5000

    def px(k):
        return x0 + (x1 - x0) * (k - lo) / (hi - lo)

    pdf, cdf = _lognormal(2400, 0.30)
    pdf2, _ = _lognormal(2400, 0.25)
    peak = max(pdf2(k) for k in range(600, 5000, 10))

    def py(v):
        return y0 - (y0 - y1) * v / (peak * 1.08)

    mder, mean = 1800, 2400
    d.group('thin')
    for k in range(1000, 5001, 1000):                                     # kcal grid
        d.line((px(k), y0), (px(k), y1))
    d.line((px(mean), y0), (px(mean), y1 + 12))

    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))                                   # axes
    d.line(*[(px(k), py(pdf(k))) for k in range(lo, hi + 1, 25)])          # the curve, CV 0.30
    d.line((px(mder), y0), (px(mder), y1 + 4))                            # the requirement

    d.group('mid')
    d.dashed(*[(px(k), py(pdf2(k))) for k in range(lo, hi + 1, 25)], dash=4, gap=3)
    for k in range(lo + 40, mder, 40):                                    # the shaded tail
        d.line((px(k), y0), (px(k), py(pdf(k))))

    d.group('mid')
    for k in range(1000, 5001, 1000):
        d.text(px(k), y0 + 12, f'{k:,}', size=7)
    d.text((x0 + x1) / 2, y0 + 26, 'HABITUAL INTAKE · KCAL A DAY', size=7)
    d.text(px(mder) - 4, y1 + 2, 'MDER 1,800', size=7, anchor='end')
    d.text(px(mean) + 4, y1 + 14, 'MEAN 2,400', size=7, anchor='start')
    d.text(px(1450) - 4, py(pdf(1450)) - 4, f'{100 * cdf(mder):.0f}% BELOW', size=7, anchor='end')
    d.text(px(3300) + 6, py(pdf(3300)) - 6, 'CV 0.30', size=7, anchor='start')
    d.text(px(2700) + 8, py(pdf2(2700)) - 2, 'CV 0.25: 15%', size=7, anchor='start')
    d.text(200, 24, 'AN INVENTED COUNTRY · THE SHARE BELOW THE LINE', size=7)
    d.text(200, 290, 'PREVALENCE OF UNDERNOURISHMENT', size=7)
    return d


PLATES = {'gm-crops': gm_crops, 'hunger-now': hunger_now}
