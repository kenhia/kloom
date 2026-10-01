"""contact_sheet.py's page size and palettes (sprint 027). Run by `just check`; no browser."""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contact_sheet as cs  # noqa: E402


class Window(unittest.TestCase):
    def test_one_plate_is_one_plate_wide(self):
        self.assertEqual(cs.window(1), (428, 372))

    def test_rows_of_four_at_most(self):
        self.assertEqual(cs.window(3)[0], 3 * 416 + 4 * 6)
        self.assertEqual(cs.window(9), (4 * 416 + 5 * 6, 3 * 366 + 6))


class Palettes(unittest.TestCase):
    known = {'flint': {}, 'chalk': {}}

    def test_a_palette_for_unwritten_plates_and_one_per_frame(self):
        self.assertEqual(cs.palettes_for(['chalk', 'knapping=flint'], self.known), ('chalk', {'knapping': 'flint'}))
        self.assertEqual(cs.palettes_for(None, self.known), (None, {}))

    def test_refuses_an_unknown_palette(self):
        with self.assertRaises(SystemExit):
            cs.palettes_for(['knapping=ember'], self.known)


if __name__ == '__main__':
    unittest.main()
