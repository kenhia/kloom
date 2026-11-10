"""Plates for Sound and Score's part piano1 (the piano trail: cristofori, stein-piano,
double-escapement), sprint 058. See plates_for.py."""
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


def _rot(p, c, deg):
    """Rotate p about c by deg degrees, clockwise on the page (y runs down)."""
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def _poly(d, pts, c, deg, dashed=False):
    q = [_rot(p, c, deg) for p in pts]
    if dashed:
        d.dashed(*q, q[0], dash=3, gap=2.5)
    else:
        d.line(*q, closed=True)


def cristofori():
    d = D()
    # Maffei's plate of 1711 (Tav. I) redrawn at 0.4 of the engraving's 960-unit scan, with its
    # letters. The parts are where Maffei drew them; the struck position (dashed) is computed:
    # the hammer turns about its pivot N until its head meets the string A, and the second lever
    # E turns about F far enough for the hopper G to carry the hammer's projection to let-off.
    A_y = 39
    N = (246, 76)                                   # hammer pivot, the rotella in the comb
    F = (98, 162)                                   # second lever's pivot
    head0, hr = (62, 116), 7
    L = math.hypot(head0[0] - N[0], head0[1] - N[1])
    a_rest = math.degrees(math.atan2(head0[1] - N[1], N[0] - head0[0]))       # below horizontal
    a_hit = math.degrees(math.asin((N[1] - (A_y + hr)) / L))                    # above horizontal
    theta = a_rest + a_hit                          # the hammer's swing, head rising
    # hopper top under the projection; the hammer is carried through 80% of its swing, then flies
    proj = (224, 86)
    lift = proj[1] - _rot(proj, N, theta * 0.8)[1]
    phi = math.degrees(math.asin(lift / (proj[0] - F[0])))   # lever E's turn (head end up)

    d.group('thin')
    d.line((18, A_y), (386, A_y))                                             # A: the string
    _box(d, 18, 184, 330, 52)                                                 # B: the key frame
    d.line((296, 184), (300, 172), (304, 184))                                # key balance (schematic)
    d.dashed((N[0], N[1]), (head0[0], head0[1]), dash=2, gap=3)
    d.arc(N[0], N[1], L, 180 - a_rest - 2, 180 + a_hit + 2)                   # path of the head
    d.arc(F[0], F[1], proj[0] - F[0], -phi - 3, 3)                            # path of the hopper
    d.dashed((70, 136), (94, 112), dash=1.5, gap=1.5)                          # P: crossed silk threads
    d.dashed((70, 112), (94, 136), dash=1.5, gap=1.5)

    d.group()
    # C: the key, with its block D and its front end under the finger
    d.line((128, 164), (340, 164), (340, 158), (386, 158), (386, 178), (340, 178), (340, 171), (128, 171), closed=True)
    _box(d, 136, 158, 20, 6)
    # Q-F-E: the second lever, one piece turning about F; Q its tail, E its arm
    lever = [(18, 160), (70, 160), (70, 138), (250, 138), (250, 158), (120, 158),
             (110, 168), (90, 184), (70, 184), (70, 168), (18, 168)]
    d.line(*lever, closed=True)
    d.circle(F[0], F[1], 2.2)
    # G: the hopper, between its cheeks H, on the arm
    hopper = [(218, 88), (230, 88), (230, 138), (218, 138)]
    d.line(*hopper, closed=True)
    d.line((200, 138), (206, 120), (214, 112), (214, 138))
    d.line((232, 138), (232, 112), (238, 112), (238, 138))
    # M, S: the comb and its rail; N the hammer's pivot in it
    _box(d, 240, 54, 52, 58)
    _box(d, 292, 60, 56, 52)
    d.arc(272, 94, 16, 180, 360)
    # O: the hammer, butt block, shank and leathered head
    butt = [(222, 56), (252, 56), (252, 86), (222, 86)]
    d.line(*butt, closed=True)
    ang = math.atan2(head0[1] - N[1], head0[0] - N[0])
    nx, ny = -math.sin(ang) * 3, math.cos(ang) * 3
    s0 = (222, 72)
    d.line((s0[0] + nx, s0[1] + ny), (head0[0] + nx + 5, head0[1] + ny - 1))
    d.line((s0[0] - nx, s0[1] - ny), (head0[0] - nx + 5, head0[1] - ny - 1))
    head = [(head0[0] - 8, head0[1] - 6), (head0[0] + 6, head0[1] - 9), (head0[0] + 9, head0[1] + 5), (head0[0] - 5, head0[1] + 8)]
    d.line(*head, closed=True)
    # R: the damper, a jack standing on the tail Q, cloth against the string
    _box(d, 24, A_y + 2, 8, 118)
    d.line((22, A_y + 2), (34, A_y + 2))

    d.group('mid')
    # I, L: the fixed wire behind the hopper and the spring under it
    d.line((233, 90), (233, 136))
    d.line((150, 137), (190, 135), (217, 128))
    d.circle(N[0], N[1], 2.2)
    # the struck position: hammer up to the string, lever raised, damper down off the string
    rot_head = [_rot(p, N, theta) for p in head]
    d.dashed(*rot_head, rot_head[0], dash=2.5, gap=2)
    sh0, sh1 = _rot(s0, N, theta), _rot(head0, N, theta)
    d.dashed(sh0, sh1, dash=4, gap=3)
    _poly(d, butt, N, theta, dashed=True)
    _poly(d, [(70, 138), (250, 138), (250, 158), (70, 158)], F, -phi, dashed=True)
    drop = (F[0] - 28) * math.sin(math.radians(phi))
    d.dashed((24, A_y + 2 + drop), (32, A_y + 2 + drop), dash=2, gap=2)
    d.line((363, 146), (363, 156)); _arrow(d, (363, 146), (363, 156), 4)

    d.group('mid')
    for s, x, y in (('A', 200, 33), ('B', 60, 214), ('C', 356, 172), ('D', 146, 154), ('E', 180, 152),
                    ('F', 104, 178), ('G', 224, 82), ('H', 196, 122), ('I', 240, 100), ('L', 160, 132),
                    ('M', 266, 66), ('N', 272, 106), ('O', 54, 132), ('P', 100, 128), ('Q', 44, 176),
                    ('R', 40, 100), ('S', 320, 90)):
        d.text(x, y, s, size=7)
    d.text(200, 262, 'MAFFEI 1711 · TAV. I REDRAWN · STRUCK POSITION DASHED', size=7)
    d.text(200, 276, 'KEY C LIFTS LEVER E · HOPPER G THROWS HAMMER O · THEN ESCAPES', size=7)
    d.text(200, 290, f'HAMMER SWING {theta:.0f} DEGREES · LEVER TURN {phi:.0f} DEGREES', size=7)
    return d


def _hammer(d, piv, tail, head, w=2.2, dashed=False):
    """A hammer shank from tail to head, its head a rounded block, as lines (or dashes)."""
    ang = math.atan2(head[1] - tail[1], head[0] - tail[0])
    nx, ny = -math.sin(ang) * w, math.cos(ang) * w
    a1, a2 = (tail[0] + nx, tail[1] + ny), (head[0] + nx, head[1] + ny)
    b1, b2 = (tail[0] - nx, tail[1] - ny), (head[0] - nx, head[1] - ny)
    ux, uy = math.cos(ang), math.sin(ang)
    hd = [(head[0] - nx * 3 - ux * 2, head[1] - ny * 3 - uy * 2), (head[0] - nx * 3 + ux * 9, head[1] - ny * 3 + uy * 9),
          (head[0] + nx * 3 + ux * 9, head[1] + ny * 3 + uy * 9), (head[0] + nx * 3 - ux * 2, head[1] + ny * 3 - uy * 2)]
    if dashed:
        d.dashed(a1, a2, dash=3, gap=2); d.dashed(b1, b2, dash=3, gap=2); d.dashed(*hd, hd[0], dash=2.5, gap=2)
    else:
        d.line(a1, a2); d.line(b1, b2); d.line(*hd, closed=True)


def stein_piano():
    d = D()
    # Two actions in section, schematic, the player at the left of each, at rest (solid) and at the
    # moment of the blow (dashed, computed by turning the parts about their pivots).
    # Left, the Viennese Prellmechanik: the hammer rides in a fork (Kapsel) on the key, its head toward
    # the player; the key's far end rises, the beak behind the hammer's pivot catches under a sprung
    # hopper fixed behind the keys, and the hammer flips up. Right, the English grand action: the
    # hammer hinged on a fixed rail, head away from the player, thrown by a jack in the key.
    sy = 104                                                  # the string, in both panels
    # Viennese
    bal_v, kv0, kv1 = (104, 186), 20, 186
    piv_v = (160, 160)
    head_v = (70, 160)
    beak = (172, 152)
    d.group('thin')
    d.line((14, sy), (196, sy))
    d.line((bal_v[0] - 5, bal_v[1] + 8), (bal_v[0], bal_v[1]), (bal_v[0] + 5, bal_v[1] + 8))
    d.line((204, 40), (204, 230))                             # the panels' divide
    Lv = math.hypot(head_v[0] - piv_v[0], head_v[1] - piv_v[1])
    th_v = math.degrees(math.asin((piv_v[1] - (sy + 4)) / Lv))   # hammer swing to the string
    d.arc(piv_v[0], piv_v[1], Lv, 180, 180 + th_v + 3)
    d.group()
    _box(d, kv0, 178, kv1 - kv0, 8)                           # key
    d.line((150, 178), (150, 164), (154, 164), (154, 178)); d.line((166, 178), (166, 164), (170, 164), (170, 178))  # Kapsel
    _hammer(d, piv_v, (piv_v[0] - 4, piv_v[1]), head_v)
    d.line((piv_v[0], piv_v[1] - 3), (beak[0], beak[1] + 4), (beak[0] + 3, beak[1]), (beak[0] - 1, beak[1] - 2))  # beak
    _box(d, 178, 128, 18, 12)                                 # the hopper's rail, fixed to the frame
    d.group('mid')
    d.circle(piv_v[0], piv_v[1], 2)
    d.line((176, 140), (176, 150), (180, 150))                # the hinged hopper
    d.line((186, 140), (184, 150), (180, 150))                # its spring
    # struck: the key's far end up by the beak's travel, the hammer turned up to the string
    _hammer(d, piv_v, (piv_v[0] - 4, piv_v[1] - 6), (piv_v[0] - Lv * math.cos(math.radians(th_v)), piv_v[1] - 6 - Lv * math.sin(math.radians(th_v)) + 6), dashed=True)
    d.line((30, 168), (30, 176)); _arrow(d, (30, 168), (30, 176), 4)

    # English
    bal_e, ke0, ke1 = (262, 186), 212, 386
    piv_e = (282, 150)
    head_e = (366, 150)
    d.group('thin')
    d.line((206, sy), (390, sy))
    d.line((bal_e[0] - 5, bal_e[1] + 8), (bal_e[0], bal_e[1]), (bal_e[0] + 5, bal_e[1] + 8))
    Le = math.hypot(head_e[0] - piv_e[0], head_e[1] - piv_e[1])
    th_e = math.degrees(math.asin((piv_e[1] - (sy + 4)) / Le))
    d.arc(piv_e[0], piv_e[1], Le, 360 - th_e - 3, 360)
    d.group()
    _box(d, ke0, 178, ke1 - ke0, 8)                           # key
    _box(d, 268, 136, 24, 8)                                  # the hammer rail
    _hammer(d, piv_e, (piv_e[0] + 4, piv_e[1]), head_e)
    _box(d, 294, 154, 6, 24)                                  # the jack, in the key
    d.line((350, 178), (350, 162), (362, 158))                # the check, on the key
    d.group('mid')
    d.circle(piv_e[0], piv_e[1], 2)
    d.line((296, 150), (306, 152))                            # the butt's notch over the jack
    a = math.radians(th_e)
    _hammer(d, piv_e, (piv_e[0] + 4, piv_e[1]), (piv_e[0] + Le * math.cos(a), piv_e[1] - Le * math.sin(a)), dashed=True)
    d.line((222, 168), (222, 176)); _arrow(d, (222, 168), (222, 176), 4)

    d.group('mid')
    d.text(105, 60, 'VIENNESE · STEIN', size=7)
    d.text(297, 60, 'ENGLISH · BROADWOOD', size=7)
    d.text(105, 98, 'STRING', size=7)
    d.text(60, 176, 'KEY', size=7)
    d.text(84, 152, 'HEAD', size=7, anchor='end')
    d.text(160, 196, 'KAPSEL', size=7)
    d.text(187, 122, 'HOPPER', size=7)
    d.text(240, 176, 'KEY', size=7)
    d.text(280, 130, 'RAIL', size=7)
    d.text(297, 196, 'JACK', size=7)
    d.text(352, 196, 'CHECK', size=7)
    d.text(105, 222, f'HEAD SWINGS {th_v:.0f} DEGREES', size=7)
    d.text(297, 222, f'HEAD SWINGS {th_e:.0f} DEGREES', size=7)
    d.text(200, 262, 'HAMMER ON THE KEY · HAMMER ON A FIXED RAIL', size=7)
    d.text(200, 276, 'AT REST SOLID · AT THE BLOW DASHED · SCHEMATIC', size=7)
    return d


def _act(d, ox, state):
    """One state of a grand piano's repetition action, schematic, the player at the left.
    state 0 at rest, 1 at the blow (jack tripped), 2 held by the repetition lever and back check.
    The hammer turns about its flange, the wippen about its flange at the back, the key about its
    balance; each turn is computed from the one it drives."""
    sy = 69
    piv = (ox + 26, 101)                    # hammer flange
    L = 90                                  # flange to head
    kd = 24                                 # flange to knuckle
    wp = (ox + 112, 156)                    # wippen flange
    bal = (ox + 44, 179)                    # key balance
    up = math.degrees(math.asin((piv[1] - (sy + 5)) / L))          # hammer turn to the string
    letoff = up * 0.8                                               # the jack carries it this far
    lift = kd * math.sin(math.radians(letoff))                      # the knuckle's rise at let-off
    jx = ox + 50                                                    # the jack, under the knuckle
    wip_turn = math.degrees(math.asin(lift / (wp[0] - jx)))
    cap_x = ox + 80
    cap_lift = (wp[0] - cap_x) * math.sin(math.radians(wip_turn))
    key_turn = math.degrees(math.asin(cap_lift / (cap_x - bal[0])))
    ham = (0, up, up * 0.45)[state]
    kt, wt = (0, key_turn, key_turn)[state], (0, wip_turn, wip_turn)[state]
    knuckle = _rot((piv[0] + kd, piv[1] + 4), piv, -ham)
    d.group('thin')
    d.line((ox, sy), (ox + 126, sy))                                     # string
    d.line((bal[0] - 4, bal[1] + 6), bal, (bal[0] + 4, bal[1] + 6))
    _box(d, ox + 30, 115, 12, 4)                                         # let-off button
    if state == 0:
        d.arc(piv[0], piv[1], L, 360 - up - 2, 360)
    d.group()
    key = [(ox + 4, 169), (ox + 124, 169), (ox + 124, 175), (ox + 4, 175)]
    d.line(*[_rot(p, bal, -kt) for p in key], closed=True)
    cap = _rot((cap_x, 169), bal, -kt)
    d.line(cap, (cap[0], cap[1] - 10))                                   # capstan
    wip = [(ox + 36, 153), (wp[0], 153), (wp[0], 159), (ox + 36, 159)]
    d.line(*[_rot(p, wp, wt) for p in wip], closed=True)
    jb = _rot((jx, 153), wp, wt)
    jt = (jb[0], knuckle[1] + 3) if state == 0 else (jb[0], jb[1] - (153 - 108))
    tip = 16 if state else 0                                             # tripped: the jack tips out
    jt = _rot(jt, jb, tip)
    d.line(jb, jt)
    toe0 = (jb[0], jb[1] - 30)
    d.line(_rot(toe0, jb, tip), _rot((jb[0] - 14, jb[1] - 34), jb, tip))   # toe, toward the button
    rb = _rot((ox + 92, 153), wp, wt)
    rf = (knuckle[0] + 4, knuckle[1] + 3) if state == 2 else (knuckle[0] + 4, knuckle[1] + 7 - (2 if state else 0))
    d.line(rb, rf)                                                       # repetition lever
    hd = _rot((piv[0] + L, piv[1]), piv, -ham)
    _hammer(d, piv, piv, hd)
    d.circle(knuckle[0], knuckle[1], 3)
    cb = _rot((ox + 118, 169), bal, -kt)
    top = (hd[0] + 4, hd[1] + 6) if state == 2 else (cb[0] - 2, cb[1] - 24)
    d.line(cb, top)                                                      # back check
    d.group('mid')
    d.circle(piv[0], piv[1], 2); d.circle(wp[0], wp[1], 2)
    return up, wip_turn, key_turn


def double_escapement():
    d = D()
    # A modern grand action, which descends from Erard's, in three states, schematic. The angles
    # are computed: the key turns about its balance, the wippen about its flange at the back, the
    # hammer about its flange; at the blow the jack has tipped out under the let-off button, and in
    # the third the hammer is held part way up, the key still down, ready to strike again.
    for i, ox in enumerate((6, 138, 270)):
        up, wt, kt = _act(d, ox, i)
    d.group('mid')
    for ox, t1, t2 in ((6, '1 AT REST', 'JACK UNDER THE KNUCKLE'), (138, '2 THE BLOW', 'JACK TRIPPED OUT'),
                       (270, '3 HELD', 'LEVER HOLDS THE HAMMER')):
        d.text(ox + 62, 214, t1, size=7)
        d.text(ox + 62, 226, t2, size=7)
    d.text(70, 63, 'STRING', size=7)
    d.text(90, 93, 'HAMMER', size=7)
    d.text(22, 141, 'JACK', size=7, anchor='end')
    d.text(104, 135, 'LEVER', size=7)
    d.text(24, 191, 'KEY', size=7)
    d.text(200, 266, f'HAMMER {up:.0f} DEG · WIPPEN {wt:.1f} DEG · KEY {kt:.1f} DEG', size=7)
    d.text(200, 278, 'THE KEY NEED NOT RISE FOR THE NEXT BLOW', size=7)
    d.text(200, 290, 'DOUBLE ESCAPEMENT · ERARD 1821 · SCHEMATIC', size=7)
    return d


PLATES = {
    'cristofori': cristofori,
    'stein-piano': stein_piano,
    'double-escapement': double_escapement,
}
