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


class PerPlate(unittest.TestCase):
    """Sprint 029: above two plates, a PNG per plate, so none is shrunk past reading."""

    def test_the_default_turns_at_three_plates(self):
        self.assertFalse(cs.per_plate(2))
        self.assertTrue(cs.per_plate(3))
        self.assertTrue(cs.per_plate(1, True))
        self.assertFalse(cs.per_plate(9, False))

    def test_names_each_plate_and_chart_after_the_png(self):
        self.assertEqual(cs.plate_png('.scratch/me.png', 'abo', 'scene.svg', 'scene.svg'), '.scratch/me-abo.png')
        self.assertEqual(cs.plate_png('me.png', 'abo', 'chart.svg', 'scene.svg'), 'me-abo-chart.png')
        self.assertEqual(cs.plate_png('me', 'abo'), 'me-abo.png')


class TextFit(unittest.TestCase):
    """A plate's text that runs off its edge (korg 3554), estimated as bar_chart.py does a chart's."""

    def svg(self, *texts):
        return ('<svg viewBox="0 0 400 300">' + ''.join(
            f'<text x="{x}" y="{y}" font-size="9" text-anchor="{a}" letter-spacing="1">{t}</text>'
            for x, y, a, t in texts) + '</svg>')

    def test_text_inside_the_plate_is_fine(self):
        self.assertEqual(cs.text_overflows(self.svg((200, 150, 'middle', 'A LABEL'), (10, 20, 'start', 'LEFT'),
                                                    (390, 290, 'end', 'RIGHT'))), [])

    def test_says_which_edge_and_by_how_much(self):
        self.assertEqual(cs.text_overflows(self.svg((380, 150, 'start', 'RUNS OFF THE RIGHT'))),
                         ['"RUNS OFF THE RIGHT" runs ~94 units past the right edge (400)'])
        self.assertEqual(cs.text_overflows(self.svg((20, 150, 'end', 'LEFT'), (200, 4, 'middle', 'TOP'))),
                         ['"LEFT" runs ~5 units past the left edge', '"TOP" runs ~3 units past the top edge'])

    def test_reads_escapes_and_skips_a_turned_label(self):
        svg = '<svg viewBox="0 0 100 50"><text x="90" y="20" transform="rotate(-90 90 20)">A LONG TURNED LABEL</text>' \
              '<text x="50" y="20" font-size="9" text-anchor="middle">&amp;</text></svg>'
        self.assertEqual(cs.text_overflows(svg), [])


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
