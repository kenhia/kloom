"""american.py: kloom's words respelled, quotations, titles and names left alone (sprint 044). No network."""
import json, os, sys, tempfile, unittest
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import american as A  # noqa: E402


class Words(unittest.TestCase):
    def test_families(self):
        self.assertEqual(A.respell('the colour of the centre'), 'the color of the center')
        self.assertEqual(A.respell('they organised a reorganisation'), 'they organized a reorganization')
        self.assertEqual(A.respell('she analysed it; the travellers modelled it'),
                         'she analyzed it; the travelers modeled it')
        self.assertEqual(A.respell('haemoglobin, anaesthesia, oestrogen'), 'hemoglobin, anesthesia, estrogen')
        self.assertEqual(A.respell('thalassaemia and immunohaematology'), 'thalassemia and immunohematology')
        self.assertEqual(A.respell('a 27-kilometre tunnel, 200 litres'), 'a 27-kilometer tunnel, 200 liters')

    def test_keeps_case(self):
        self.assertEqual(A.respell('Colour. COLOUR. colour.'), 'Color. COLOR. color.')

    def test_leaves_words_it_does_not_know_or_that_are_both(self):
        text = 'an hour of flour; the contour, the glamour; two analyses; the advertised rise'
        self.assertEqual(A.respell(text), text)


class NotKlooms(unittest.TestCase):
    def test_quotations(self):
        text = 'He wrote "the colour of\nthe sky", a colour.\n\n> The centre holds.\n'
        self.assertEqual(A.respell(text), 'He wrote "the colour of\nthe sky", a color.\n\n> The centre holds.\n')

    def test_titles_but_not_terms(self):
        self.assertEqual(A.respell('in _Notes on Nursing for the Labouring Classes_ a _tokeniser_ cuts'),
                         'in _Notes on Nursing for the Labouring Classes_ a _tokenizer_ cuts')

    def test_proper_names(self):
        self.assertEqual(A.respell('at the Royal Theatre and the Ministry of Defence, the theatre'),
                         'at the Royal Theatre and the Ministry of Defence, the theater')
        # Starting a sentence, a capital proves nothing: KEEP and the next word decide.
        self.assertEqual(A.respell('Ministry of Defence papers. Labour Party men. Colour came.'),
                         'Ministry of Defence papers. Labour Party men. Color came.')
        self.assertEqual(A.respell('MINISTRY OF DEFENCE · COLOUR'), 'MINISTRY OF DEFENCE · COLOR')

    def test_a_wrapped_line_starts_no_sentence(self):
        self.assertEqual(A.respell('a treaty, the\nMetre Convention, and the\n\nCentre of it'),
                         'a treaty, the\nMetre Convention, and the\n\nCenter of it')

    def test_a_table_cell_starts_one(self):
        self.assertEqual(A.respell('| Colour | Labelled |'), '| Color | Labeled |')

    def test_only_the_changing_part_of_a_compound_counts(self):
        self.assertEqual(A.respell("Aristarchus's Sun-centred cosmos in DEHP-plasticised bags"),
                         "Aristarchus's Sun-centered cosmos in DEHP-plasticized bags")

    def test_marks_links_code(self):
        text = ('the [haemophilia](kloom:e/haemophilia) of the [Metre Convention](kloom:e/metre-convention), '
                'see [colour](https://example.org/colour) and `colour`')
        self.assertEqual(A.respell(text),
                         'the [hemophilia](kloom:e/haemophilia) of the [Metre Convention](kloom:e/metre-convention), '
                         'see [color](https://example.org/colour) and `colour`')


class Files(unittest.TestCase):
    def frame(self):
        return {
            'id': 'x', 'topic': 'Colour theory',
            'scene': {'headline': 'The centre', 'accent': 'COLOUR.', 'palette': 'theatre',
                      'metadata': ['A · B', 'THE CENTRE · TYRE']},
            'citations': [{'kind': 'book', 'title': 'On Colour', 'publisher': 'Defence Press'}],
            'connections': [{'to': 's/y', 'why': 'Both measure colour.'}],
        }

    def test_frame_json_changes_its_words_and_keeps_its_format(self):
        raw = json.dumps(self.frame(), indent='\t', ensure_ascii=False) + '\n'
        out = A.respell_file('frames/x/frame.json', raw)
        got = json.loads(out)
        self.assertEqual(got['topic'], 'Color theory')
        self.assertEqual(got['scene']['accent'], 'COLOR.')
        self.assertEqual(got['scene']['metadata'], ['A · B', 'THE CENTER · TYRE'])
        self.assertEqual(got['scene']['palette'], 'theatre')
        self.assertEqual(got['citations'], self.frame()['citations'])
        self.assertEqual(got['connections'][0]['why'], 'Both measure color.')
        self.assertEqual(out, raw.replace('Colour theory', 'Color theory').replace('The centre', 'The center')
                         .replace('COLOUR.', 'COLOR.').replace('THE CENTRE', 'THE CENTER')
                         .replace('measure colour', 'measure color'))

    def test_a_name_keeps_its_name_and_aliases(self):
        raw = json.dumps({'id': 'x', 'name': 'Theatre Royal', 'aliases': ['theatre'],
                          'description': 'A theatre in the centre of town.'}, indent='\t')
        got = json.loads(A.respell_file('names/x.json', raw))
        self.assertEqual(got['name'], 'Theatre Royal')
        self.assertEqual(got['aliases'], ['theatre'])
        self.assertEqual(got['description'], 'A theater in the center of town.')

    def test_svg_text_only(self):
        raw = '<svg><g id="colour"><text class="centre">COLOUR ÷4</text></g></svg>'
        self.assertEqual(A.respell_file('scene.svg', raw),
                         '<svg><g id="colour"><text class="centre">COLOR ÷4</text></g></svg>')

    def test_svelte_markup_and_labels_not_script(self):
        raw = ('<script>const colours = "colour";</script>\n'
               '<button aria-label="Scene colours" class="colours">Reading colours</button>')
        self.assertEqual(A.respell_file('X.svelte', raw),
                         '<script>const colours = "colour";</script>\n'
                         '<button aria-label="Scene colors" class="colours">Reading colors</button>')

    def test_typescript_prose_strings_only(self):
        raw = ("import { brighten } from './colour';\n"
               "// the colours of the scene\n"
               "const a = { label: 'Scene colours', id: 'colour' };\n"
               "fail(`image \"${colour}\" needs a \\`licence\\` and a centre`);\n"
               "const b = 'a media citation needs a `licence`';\n")
        out = A.respell_file('engine/settings.ts', raw)
        self.assertEqual(out, raw.replace('Scene colours', 'Scene colors').replace('a centre', 'a center'))
        self.assertEqual(A.respell_file('engine/settings.test.ts', raw), raw)

    def test_svelte_script_strings(self):
        raw = "<script>const kinds = { org: 'Organisation', x: 'colour' };</script>\n<p>{kinds.org}</p>"
        # A capitalized label is prose; a lower-case word is a key.
        self.assertEqual(A.respell_file('NameCard.svelte', raw), raw.replace("'Organisation'", "'Organization'"))
        raw = "<script>const why = 'in its catalogue record';</script>"
        self.assertEqual(A.respell_file('X.svelte', raw), "<script>const why = 'in its catalog record';</script>")

    def test_other_json_is_not_read(self):
        self.assertEqual(A.respell_file('package.json', '{"colour": "colour"}'), '{"colour": "colour"}')


class Specs(unittest.TestCase):
    def test_a_respelled_mark_respells_its_spec(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / 'examples').mkdir()
            frame = d / 'subjects' / 's' / 'frames' / 'f'
            frame.mkdir(parents=True)
            (frame / 'reading.md').write_text(
                'The [hemophilia](kloom:e/haemophilia) and the [Metre Convention](kloom:e/metre-convention).\n')
            spec = d / 'examples' / 's.json'
            spec.write_text('{\n\t"s/f": [\n\t\t["haemophilia", "haemophilia"],\n'
                            '\t\t["Metre Convention", "metre-convention"]\n\t]\n}\n')
            self.assertEqual(A.respell_specs(d / 'examples', d / 'subjects'), [spec])
            self.assertEqual(json.loads(spec.read_text())['s/f'],
                             [['hemophilia', 'haemophilia'], ['Metre Convention', 'metre-convention']])


if __name__ == '__main__':
    unittest.main()
