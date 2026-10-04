"""plates.py's primitives (sprint 050). Run by `just check`; no browser."""
import os, re, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plates import D  # noqa: E402


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


if __name__ == '__main__':
    unittest.main()
