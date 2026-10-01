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

    def test_reads_a_span_as_circa_its_first_year(self):
        self.assertEqual(cm.year({'DateTimeOriginal': '1941-01-01/1945-12-31'}), ('1941', True))
        self.assertEqual(cm.year({'DateTimeOriginal': '1941–1945'}), ('1941', True))
        # NARA writes "between 1941 and 1945"; it came out as the exact year 1941 (sprint 030).
        self.assertEqual(cm.year({'DateTimeOriginal': 'between 1941 and 1945'}), ('1941', True))
        self.assertEqual(cm.year({'DateTimeOriginal': '1945-12-31'}), ('1945-12-31', False))


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
        for org in ('Smithsonian Institution', 'NASA Johnson Space Center', 'Colegio de Fonseca',
                    'Caldesi & Montecchi'):
            self.assertEqual(cm.authors(org), [{'name': org}], org)
        self.assertEqual(cm.authors('Caldesi & Montecchi Details on Google Art Project'),
                         [{'name': 'Caldesi & Montecchi'}])

    def test_drops_the_art_projects_template_text_from_a_title(self):
        self.assertEqual(cm.clean_title('The Royal Family, Osborne 1857title QS:P1476,en:"The Royal Family"'),
                         'The Royal Family, Osborne 1857')
        self.assertEqual(cm.clean_title('Galen'), 'Galen')


class Tags(unittest.TestCase):
    def test_keeps_the_licence_tags_and_drops_their_machinery(self):
        templates = ['Template:Cc-pd-mark-footer', 'Template:Information', 'Template:PD-Art', 'Template:PD-Art/en',
                     'Template:PD-Art/layout', 'Template:PD-US-expired', 'Template:PD-US-expired-text',
                     'Template:PD-art-category', 'Template:PD-old-100', 'Template:PD-old-text',
                     'Template:PD-old-warning-text', 'Template:Cc-by-sa-4.0']
        self.assertEqual(cm.licence_tags(templates), ['PD-Art', 'PD-US-expired', 'PD-old-100', 'Cc-by-sa-4.0'])


class Licences(unittest.TestCase):
    """Sprint 029: Flickr's "No restrictions" on a stated basis; a PD-self file credits its uploader."""

    def test_takes_no_restrictions_as_public_domain_on_a_stated_basis(self):
        self.assertEqual(cm.licence_for('No restrictions'), ('Public domain', True))
        self.assertEqual(cm.licence_for('Public domain'), ('Public domain', False))
        self.assertEqual(cm.licence_for('CC BY-SA 4.0'), ('CC BY-SA 4.0', False))
        self.assertIsNone(cm.licence_for('CC BY-NC 2.0'))

    def test_names_flickrs_tag(self):
        self.assertEqual(cm.licence_tags(['Template:Flickr-no known copyright restrictions',
                                          'Template:Flickr-no known copyright restrictions/layout']),
                         ['Flickr-no known copyright restrictions'])

    def test_the_book_images_account_is_not_an_author(self):
        self.assertEqual(cm.authors('Internet Archive Book Images'), [])

    def test_credits_a_pd_self_files_uploader(self):
        self.assertEqual(cm.uploader_credit(['PD-self'], [], 'Jane'), [{'name': 'Jane (uploader)'}])
        self.assertEqual(cm.uploader_credit(['PD-self'], [{'name': 'X'}], 'Jane'), [{'name': 'X'}])
        self.assertEqual(cm.uploader_credit(['PD-old-100'], [], 'Jane'), [])


class Crop(unittest.TestCase):
    def test_reads_a_box(self):
        self.assertEqual(cm.box_arg('10,20,110,220'), (10, 20, 110, 220))
        with self.assertRaises(Exception):
            cm.box_arg('110,20,10,220')

    def test_crops_and_scales_down(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest('Pillow is not installed (uv run installs it)')
        png = io.BytesIO()
        Image.new('RGB', (400, 300), 'white').save(png, 'PNG')
        out = Image.open(io.BytesIO(cm.to_jpeg(png.getvalue(), box=(0, 0, 200, 100), width=100)))
        self.assertEqual(out.size, (100, 50))


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
