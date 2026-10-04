"""commons_media.py's metadata and JPEG conversion (sprint 027). Run by `just check`; no network."""
import io, json, os, sys, unittest

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

    def test_turns_a_sideways_page_upright_before_the_box(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest('Pillow is not installed (uv run installs it)')
        # A portrait plate printed sideways: a landscape scan whose black corner is the plate's top right.
        sideways = Image.new('RGB', (400, 300), 'white')
        sideways.paste((0, 0, 0), (0, 0, 60, 60))
        png = io.BytesIO()
        sideways.save(png, 'PNG')
        upright = Image.open(io.BytesIO(cm.to_jpeg(png.getvalue(), rotate=90)))
        self.assertEqual(upright.size, (300, 400))
        corner = Image.open(io.BytesIO(cm.to_jpeg(png.getvalue(), box=(240, 0, 300, 60), rotate=90)))
        self.assertEqual(corner.size, (60, 60))
        self.assertLess(max(corner.getpixel((30, 30))), 10)
        self.assertGreater(min(upright.getpixel((30, 30))), 245)


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


    def test_reads_a_png_with_a_large_text_chunk(self):
        # A Commons scan of Beethoven's Ninth carried metadata past Pillow's 1 MB default (sprint 049).
        try:
            from PIL import Image, PngImagePlugin
        except ImportError:
            self.skipTest('Pillow is not installed (uv run installs it)')
        info = PngImagePlugin.PngInfo()
        info.add_itxt('XML:com.adobe.xmp', 'x' * (2 * 1024 * 1024), zip=True)
        png = io.BytesIO()
        Image.new('RGB', (4, 4), (255, 255, 255)).save(png, 'PNG', pnginfo=info)
        self.assertEqual(Image.open(io.BytesIO(cm.to_jpeg(png.getvalue()))).format, 'JPEG')

def fixture(name):
    """A real Keeping Watch file's Commons metadata, wikitext and catalogue record (sprint 030), kept
    so the institutional patterns are tested without the network."""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', f'{name}.json')) as fh:
        f = json.load(fh)
    said = []
    found = cm.institution(f['title'], f['meta'], f['tags'], f['wikitext'], f.get('wellcome'), said.append)
    return found, said


class Institutions(unittest.TestCase):
    """NARA, the US Navy and the Wellcome Collection (sprint 033, korg 3478 item 9)."""

    def test_nara_series_is_the_container_and_agency_the_author(self):
        found, said = fixture('nara-cadet-nurse-poster')
        self.assertEqual(found, {'container': 'World War II Posters, National Archives and Records Administration',
                                 'number': 'NAID 514214, 44-PA-726A',
                                 'authors': [{'name': 'Bureau of Special Services'}]})
        self.assertIn('Office of War Information', said[0])
        found, _ = fixture('nara-navy-nurses-oath')
        self.assertEqual(found['authors'], [{'name': 'Naval Photographic Center'}])
        self.assertEqual(found['number'], 'NAID 520618, 80-G-48365')
        self.assertTrue(found['container'].startswith('General Photographic File of the Department of Navy, National'))

    def test_a_nara_creator_who_is_a_person_is_not_the_author(self):
        found, said = fixture('nara-fdr-library')
        self.assertNotIn('authors', found)
        self.assertEqual(found['number'], 'NAID 195934')
        self.assertIn('a person', said[0])

    def test_navy_photographer_from_photo_by(self):
        found, _ = fixture('navy-hand-hygiene')
        self.assertEqual(found, {'container': 'Naval History and Heritage Command', 'number': '060824-N-3714J-044',
                                 'authors': [{'family': 'Jones', 'given': 'Erika N.'}]})
        # The author field is a Flickr account; the photographer is in the description.
        found, _ = fixture('navy-mercy-perioperative')
        self.assertEqual(found['authors'], [{'family': 'Greenberg', 'given': 'Jake'}])
        self.assertEqual(found['number'], '200417-N-DA693-1065')

    def test_wellcome_is_the_container_and_a_book_plate_names_its_book(self):
        found, said = fixture('wellcome-wardroper')
        self.assertEqual(found, {'container': 'The history of nursing in the British Empire, Wellcome Collection',
                                 'number': 'L0000024'})
        self.assertIn('Sarah Anne Tooley', said[0])
        found, _ = fixture('wellcome-lister-spray')
        self.assertEqual(found, {'container': 'Wellcome Collection', 'number': 'M0003436'})
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures',
                               'wellcome-lister-spray.json')) as f:
            person = json.load(f)
        work = {**person['wellcome'], 'contributors': [{'label': 'Joseph Lister', 'primary': True}]}
        found = cm.institution(person['title'], person['meta'], person['tags'], person['wikitext'], work)
        self.assertEqual(found['authors'], [{'family': 'Lister', 'given': 'Joseph'}])

    def test_every_other_file_is_as_before(self):
        self.assertEqual(cm.institution('File:Seacole - Challen.jpg', {'Artist': 'Albert Charles Challen'},
                                        ['PD-old-100'], '{{Artwork |artist=Albert Charles Challen}}'), {})


if __name__ == '__main__':
    unittest.main()
