"""plates.py's primitives (sprint 050). Run by `just check`; no browser."""
import os, re, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plates import D, clip, clip_polygon, hatch  # noqa: E402


def segments(d):
    """The dashes of the last path drawn, as (x0, y0, x1, y1)."""
    path = d.groups[-1][1][-1][1]
    return [tuple(map(float, m)) for m in re.findall(r'M([-\d.]+) ([-\d.]+) L([-\d.]+) ([-\d.]+)', path)]


class Dashed(unittest.TestCase):
    """A dashed line (korg 3554: a stemma's hypothetical link was drawn dash by dash in sprint 049)."""

    def test_dashes_a_straight_line_as_one_path(self):
        d = D().group()
        d.dashed((0, 0), (20, 0), dash=4, gap=4)
        self.assertEqual(segments(d), [(0, 0, 4, 0), (8, 0, 12, 0), (16, 0, 20, 0)])
        self.assertEqual(len(d.groups[-1][1]), 1)

    def test_a_dash_turns_a_corner_and_the_last_is_cut_short(self):
        d = D().group()
        d.dashed((0, 0), (3, 0), (3, 5), dash=4, gap=2)
        path = d.groups[-1][1][-1][1]
        self.assertEqual(path, 'M0 0 L3 0 L3 1 M3 3 L3 5')

    def test_a_line_of_no_length_draws_nothing(self):
        d = D().group()
        d.dashed((5, 5), (5, 5))
        self.assertEqual(d.groups[-1][1], [])


def close(pts, places=6):
    return [tuple(round(c, places) + 0.0 for c in p) for p in pts]


class Arc(unittest.TestCase):
    """korg 3557 #8: arc() takes degrees, and sprint 051 passed radians to it."""

    def test_takes_degrees_clockwise_on_the_page_from_east(self):
        d = D().group()
        d.arc(100, 100, 10, 0, 90, n=2)
        self.assertEqual(d.groups[-1][1][-1][1], 'M110 100 L107.1 107.1 L100 110')


class Clip(unittest.TestCase):
    """korg 3576 #7 and 3557 #8: lines clipped to a polygon (sprint 051's enclosure fields, sprint 055's
    hatching), where four authors each wrote their own Cyrus-Beck for a convex one."""

    SQUARE = [(0, 0), (10, 0), (10, 10), (0, 10)]
    # an L: the square with its top-right quarter cut away, so not convex
    ELL = [(0, 0), (5, 0), (5, 5), (10, 5), (10, 10), (0, 10)]

    def test_keeps_the_part_of_a_line_inside_either_winding(self):
        self.assertEqual([close(p) for p in clip([(-5, 5), (15, 5)], self.SQUARE)], [[(0, 5), (10, 5)]])
        self.assertEqual([close(p) for p in clip([(-5, 5), (15, 5)], self.SQUARE[::-1])], [[(0, 5), (10, 5)]])
        self.assertEqual(clip([(20, 20), (30, 30)], self.SQUARE), [])

    def test_a_polyline_stays_one_piece_while_it_stays_inside(self):
        self.assertEqual([close(p) for p in clip([(2, -2), (2, 2), (8, 2), (8, 12)], self.SQUARE)],
                         [[(2, 0), (2, 2), (8, 2), (8, 10)]])

    def test_a_line_across_a_concave_polygon_comes_out_in_pieces(self):
        self.assertEqual([close(p) for p in clip([(-1, 2.5), (11, 2.5)], self.ELL)], [[(0, 2.5), (5, 2.5)]])
        self.assertEqual([close(p) for p in clip([(2.5, -1), (2.5, 11)], self.ELL)], [[(2.5, 0), (2.5, 10)]])
        self.assertEqual([close(p) for p in clip([(7.5, -1), (7.5, 11)], self.ELL)], [[(7.5, 5), (7.5, 10)]])
        # a line through the notch: in, out, in again
        u = [(0, 0), (10, 0), (10, 10), (7, 10), (7, 3), (3, 3), (3, 10), (0, 10)]
        self.assertEqual([close(p) for p in clip([(-1, 6), (11, 6)], u)], [[(0, 6), (3, 6)], [(7, 6), (10, 6)]])

    def test_hatches_a_polygon(self):
        segs = hatch(self.SQUARE, step=2.5, angle=0)
        self.assertEqual([close(s) for s in segs], [[(0, y), (10, y)] for y in (2.5, 5, 7.5)])
        ell = sorted(sorted(close(s)) for s in hatch(self.ELL, step=3, angle=90))
        self.assertEqual(ell, [[(3, 0), (3, 10)], [(6, 5), (6, 10)], [(9, 5), (9, 10)]])

    def test_clips_a_polygon_to_a_convex_window(self):
        tri = [(-5, 5), (5, -5), (15, 5)]
        out = clip_polygon(tri, self.SQUARE)
        self.assertEqual(len(out), 4)
        self.assertEqual(set(close(out)), {(0, 0), (10, 0), (10, 5), (0, 5)})
        self.assertEqual(clip_polygon([(20, 20), (30, 20), (30, 30)], self.SQUARE), [])


if __name__ == '__main__':
    unittest.main()
