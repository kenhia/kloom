"""read_source.py's page and crop arguments (sprint 050). Run by `just check`; no PDF library needed."""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import read_source as rs  # noqa: E402


class Pages(unittest.TestCase):
    def test_pages_and_ranges_round_trip(self):
        self.assertEqual(rs.pages('1-3,7,99', 10), [0, 1, 2, 6])
        self.assertEqual(rs.ranges([1, 2, 3, 7]), '1-3,7')


class Crop(unittest.TestCase):
    """--crop (korg 3554): a region of a page, in the pixels of the page rendered at --scale."""

    def test_reads_a_box(self):
        self.assertEqual(rs.box_arg('10,20,300,400'), (10, 20, 300, 400))
        for bad in ('10,20,300', '300,20,10,400', 'a,b,c,d'):
            with self.assertRaises(ValueError, msg=bad):
                rs.box_arg(bad)

    def test_a_box_past_the_page_is_refused_with_the_pages_size(self):
        self.assertIsNone(rs.box_problem((0, 0, 1224, 1584), (1224, 1584), 2))
        self.assertEqual(rs.box_problem((0, 0, 1300, 1584), (1224, 1584), 2),
                         'the box runs past the page, which is 1224 by 1584 pixels at --scale 2: '
                         'measure the box on a page rendered at the same scale')


if __name__ == '__main__':
    unittest.main()
