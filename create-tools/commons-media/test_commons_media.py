"""commons_media.py's metadata and JPEG conversion (sprint 027). Run by `just check`; no network."""
import io, os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commons_media as cm  # noqa: E402


class Year(unittest.TestCase):
    def test_reads_a_date_bc_as_bc(self):
        self.assertEqual(cm.year({'DateTimeOriginal': 'c. 1504 BC'}), ('1504 BC', True))
        self.assertEqual(cm.year({'DateTimeOriginal': 'during 1650 b.C. (sources: …)'}), ('1650 BC', False))

    def test_reads_an_ordinary_and_an_early_date(self):
        self.assertEqual(cm.year({'DateTimeOriginal': '1913-00-00'}), ('1913', False))
        self.assertEqual(cm.year({'DateTimeOriginal': 'circa 1890'}), ('1890', True))
        self.assertEqual(cm.year({'DateTimeOriginal': 'AD 888'}), ('888', False))
        self.assertEqual(cm.year({'DateTimeOriginal': 'unknown'}), (None, False))


class Authors(unittest.TestCase):
    def test_leaves_out_boilerplate(self):
        for artist in ('Unknown author', 'AnonymousUnknown author', '不明', 'Scanned by Epson Perfection V600',
                       'Own work', 'unknown (c. 2000 B.C)'):
            self.assertEqual(cm.authors(artist), [], artist)

    def test_writes_a_person_as_family_and_given(self):
        self.assertEqual(cm.authors('Richard Marsden (1859–1938)'), [{'family': 'Marsden', 'given': 'Richard'}])
        self.assertEqual(cm.authors('Jan van Eyck'), [{'family': 'Eyck', 'given': 'Jan van'}])

    def test_writes_anything_else_as_a_name(self):
        self.assertEqual(cm.authors('Wellcome Library'), [{'name': 'Wellcome Library'}])
        self.assertEqual(cm.authors('NASA'), [{'name': 'NASA'}])


class Tags(unittest.TestCase):
    def test_keeps_the_licence_tags_and_drops_their_machinery(self):
        templates = ['Template:Cc-pd-mark-footer', 'Template:Information', 'Template:PD-Art', 'Template:PD-Art/en',
                     'Template:PD-Art/layout', 'Template:PD-US-expired', 'Template:PD-US-expired-text',
                     'Template:PD-art-category', 'Template:PD-old-100', 'Template:PD-old-text',
                     'Template:PD-old-warning-text', 'Template:Cc-by-sa-4.0']
        self.assertEqual(cm.licence_tags(templates), ['PD-Art', 'PD-US-expired', 'PD-old-100', 'Cc-by-sa-4.0'])


class Jpeg(unittest.TestCase):
    def test_composites_transparency_onto_white(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest('Pillow is not installed (uv run installs it)')
        png = io.BytesIO()
        Image.new('RGBA', (4, 4), (0, 0, 0, 0)).save(png, 'PNG')
        out = Image.open(io.BytesIO(cm.to_jpeg(png.getvalue())))
        self.assertEqual(out.format, 'JPEG')
        self.assertGreater(min(out.getpixel((1, 1))), 250)


if __name__ == '__main__':
    unittest.main()
