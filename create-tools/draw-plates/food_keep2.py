"""Plates for Daily Bread's part keep2 (sprint 051): pasteurization and refrigeration. See plates_for.py."""
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


def _plates(d, x, y, w, h, n):
    """A plate heat exchanger seen edge on: n thin plates standing in a frame."""
    for i in range(1, n):
        px = x + w * i / n
        d.line((px, y + 3), (px, y + h - 3))


def pasteurization():
    d = D()
    # A high-temperature, short-time (HTST) pasteurizer as a flow diagram, after the parts the Grade "A"
    # Pasteurized Milk Ordinance names: a constant-level tank, the regenerator (cold raw milk on one side of
    # the plates, hot pasteurized milk on the other, the pasteurized side kept at the higher pressure), the
    # heater, the holding tube (72 °C for at least 15 seconds), the flow-diversion device (sends milk back to
    # the tank when the temperature at the tube's outlet is below the set point), the cooler and the filler.
    # Positions are schematic; the temperatures are the ordinance's and the usual cold-storage 4 °C.
    top, bot = 95, 200                                                    # the two rows of flow
    d.group('thin')
    d.line((20, top), (380, top))
    d.line((20, bot), (380, bot))
    d.line((140, 50), (140, 245))                                         # regenerator's axis

    d.group()
    _box(d, 22, 72, 46, 46)                                               # constant-level tank
    _box(d, 112, 70, 56, 150)                                             # regenerator, both rows
    _box(d, 200, 72, 40, 46)                                              # heater
    # holding tube: a serpentine of three passes
    xs, ys = (262, 342), (78, 95, 112)
    pts = [(xs[0], ys[0])]
    for i, y in enumerate(ys):
        a, b = (xs[0], xs[1]) if i % 2 == 0 else (xs[1], xs[0])
        pts += [(a, y), (b, y)]
    d.line(*pts[1:])
    d.circle(368, 140, 9)                                                 # flow-diversion device
    _box(d, 22, 182, 46, 36)                                              # cooler

    d.group('mid')
    _plates(d, 112, 70, 56, 150, 9)
    _plates(d, 200, 72, 40, 46, 6)
    _plates(d, 22, 182, 46, 36, 6)
    d.line((112, 145), (168, 145))                                        # raw side above, pasteurized below
    # flow lines
    d.line((68, top), (112, top)); _arrow(d, (68, top), (112, top), 4)
    d.line((168, top), (200, top)); _arrow(d, (168, top), (200, top), 4)
    d.line((240, top), (250, top), (250, 78), (262, 78))
    d.line((342, 112), (368, 112), (368, 131)); _arrow(d, (368, 112), (368, 131), 4)
    d.line((368, 149), (368, bot), (168, bot)); _arrow(d, (368, bot), (168, bot), 4)
    d.line((112, bot), (68, bot)); _arrow(d, (112, bot), (68, bot), 4)
    d.line((45, 218), (45, 250)); _arrow(d, (45, 218), (45, 250), 4)
    d.line((36, 250), (54, 250), (52, 270), (38, 270), closed=True)       # the bottle
    d.dashed((377, 140), (390, 140), (390, 42), (28, 42), (28, 72), dash=4, gap=3)
    _arrow(d, (28, 52), (28, 72), 4)

    d.group('mid')
    d.text(56, 64, 'RAW 4 °C', size=7)
    d.text(140, 62, 'REGENERATOR', size=7)
    d.text(220, 64, 'HEATER', size=7)
    d.text(302, 130, 'HOLDING TUBE', size=7)
    d.text(302, 141, '72 °C · 15 S', size=7)
    d.text(352, 166, 'FLOW-', size=7, anchor='end')
    d.text(352, 177, 'DIVERSION', size=7, anchor='end')
    d.text(218, 36, 'BELOW 72 °C: BACK TO THE TANK', size=7)
    d.text(174, 130, 'RAW SIDE, WARMED', size=7, anchor='start')
    d.text(174, 214, 'PASTEURIZED SIDE, COOLED', size=7, anchor='start')
    d.text(45, 176, 'COOLER', size=7)
    d.text(64, 266, 'BOTTLED 4 °C', size=7, anchor='start')
    d.text(220, 284, 'HTST PASTEURIZER · SCHEMATIC', size=7)
    return d


def _coil(d, x0, x1, y, amp, n):
    """A zigzag coil along y from x0 to x1."""
    pts = [(x0, y)]
    for i in range(1, 2 * n):
        pts.append((x0 + (x1 - x0) * i / (2 * n), y + (amp if i % 2 else -amp)))
    pts.append((x1, y))
    d.line(*pts)


def refrigeration():
    d = D()
    # The vapor-compression cycle: the compressor squeezes the vapor, hot; the condenser gives its heat to the
    # air or water outside and it turns liquid; the expansion valve drops its pressure; it boils in the
    # evaporator inside the cold box, taking heat from the food. The dashed line parts the high-pressure side
    # from the low. Schematic.
    L, R, T, B = 70, 330, 80, 215                                         # the loop
    d.group('thin')
    d.dashed((30, 148), (370, 148), dash=5, gap=4)                        # high | low pressure
    d.line((200, 40), (200, 256))
    _box(d, 110, 192, 180, 62)                                            # the insulated cold box

    d.group()
    d.line((L, T), (125, T)); d.line((275, T), (R, T))                    # top run either side of the condenser
    d.line((L, B), (125, B)); d.line((275, B), (R, B))
    d.line((L, T), (L, 138)); d.line((L, 158), (L, B))                    # left run, broken by the valve
    d.line((R, T), (R, 134)); d.line((R, 162), (R, B))                    # right run, broken by the compressor
    _coil(d, 125, 275, T, 9, 7)                                           # condenser
    _coil(d, 125, 275, B, 9, 7)                                           # evaporator
    d.circle(R, 148, 14)                                                  # compressor
    d.line((L - 9, 138), (L + 9, 158), (L + 9, 138), (L - 9, 158), closed=True)   # valve, a bow tie

    d.group('mid')
    d.line((R - 8, 158), (R, 136), (R + 8, 158))                          # compressor's triangle
    _arrow(d, (R, T + 30), (R, T + 10), 5)                                # flow: up the right
    _arrow(d, (230, T - 22), (170, T - 22), 5)
    d.line((230, T - 22), (170, T - 22))                                  # leftward along the top
    _arrow(d, (L, T + 20), (L, T + 40), 5)                                # down the left
    d.line((170, B + 24), (230, B + 24)); _arrow(d, (170, B + 24), (230, B + 24), 5)
    for x in (150, 200, 250):                                             # heat leaving, above
        d.line((x, T - 32), (x, T - 48)); _arrow(d, (x, T - 32), (x, T - 48), 4)
    for x in (150, 200, 250):                                             # heat taken in, below
        d.line((x, B + 32), (x, B + 16)); _arrow(d, (x, B + 32), (x, B + 16), 4)

    d.group('mid')
    d.text(200, 22, 'HEAT OUT TO THE ROOM', size=7)
    d.text(200, T + 24, 'CONDENSER', size=7)
    d.text(R - 20, 120, 'COMPRESSOR', size=7, anchor='end')
    d.text(L + 16, 128, 'EXPANSION', size=7, anchor='start')
    d.text(L + 16, 139, 'VALVE', size=7, anchor='start')
    d.text(200, B - 18, 'EVAPORATOR', size=7)
    d.text(200, 268, 'THE COLD BOX: HEAT TAKEN IN', size=7)
    d.text(374, 142, 'HIGH', size=7, anchor='end')
    d.text(374, 160, 'LOW', size=7, anchor='end')
    d.text(40, 112, 'WARM', size=7)
    d.text(40, 123, 'LIQUID', size=7)
    d.text(40, 180, 'COLD', size=7)
    d.text(40, 191, 'MIST', size=7)
    d.text(360, 96, 'HOT', size=7)
    d.text(360, 107, 'VAPOR', size=7)
    d.text(360, 200, 'COOL', size=7)
    d.text(360, 211, 'VAPOR', size=7)
    return d


PLATES = {'pasteurization': pasteurization, 'refrigeration': refrigeration}
