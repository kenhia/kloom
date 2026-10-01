"""names.py: ids, mark placement and `mark --check` (sprint 027). Run by `just check`; no network."""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import names  # noqa: E402

READING = '''An opening that names Plato's pupil in passing.

## Aristotle

**Aristotle** taught that heavy things fall faster. Electrons came much later, and
**electrons** are not the subject.
'''


class Slug(unittest.TestCase):
    def test_spells_greek_letters(self):
        self.assertEqual(names.slug('Leibniz formula for π'), 'leibniz-formula-for-pi')

    def test_names_a_bare_number(self):
        self.assertEqual(names.slug('0'), 'zero')
        self.assertEqual(names.slug('1729'), 'number-1729')

    def test_keeps_the_old_rules(self):
        self.assertEqual(names.slug('Hellmann–Feynman theorem'), 'hellmann-feynman-theorem')
        self.assertEqual(names.slug("Moore's law"), 'moores-law')


class Lookup(unittest.TestCase):
    def test_untex_drops_a_formulas_tex(self):
        self.assertEqual(names.untex('π 4 = 1 {\\displaystyle {\\frac {\\pi }{4}}=1,} a series.'), 'π 4 = 1 a series.')

    def test_expect_warns_on_a_namesake(self):
        found = {'id': 'hideo-kodama', 'name': 'Hideo Kodama', 'description': 'Japanese politician',
                 'first_line': 'Count Hideo Kodama was a Japanese official and politician.'}
        self.assertIn('namesake', names.unexpected(found, 'stereolithography'))
        self.assertIsNone(names.unexpected(found, 'Politician'))
        self.assertIsNone(names.unexpected({'missing': 'x'}, 'anything'))


class Place(unittest.TestCase):
    def test_matches_whole_words_only(self):
        reading = 'Two electrons, then one electron.'
        a, b = names.place(reading, 'electron', 'electron')
        self.assertEqual(reading[a:b], 'electron')
        self.assertEqual(a, reading.rindex('electron'))

    def test_skips_a_heading(self):
        a, _ = names.place(READING, 'Aristotle', 'aristotle')
        self.assertEqual(a, READING.index('**Aristotle**') + 2)

    def test_says_where_it_lands(self):
        a, b = names.place(READING, 'Aristotle', 'aristotle')
        self.assertEqual(names.sentence(READING, a, b), '**[Aristotle]** taught that heavy things fall faster.')

    def test_bold_elsewhere_names_the_bold_mention_it_missed(self):
        a, b = names.place(READING, 'Electrons', 'electron')
        self.assertEqual(names.bold_elsewhere(READING, 'Electrons', a, b), '**electrons**')
        a, b = names.place(READING, 'Aristotle', 'aristotle')
        self.assertIsNone(names.bold_elsewhere(READING, 'Aristotle', a, b))

    def test_a_bold_run_holding_another_mark_is_not_the_mention(self):
        reading = 'IBM built it. **[IBM 701](kloom:e/ibm-701)** was its first.'
        self.assertIsNone(names.bold_elsewhere(reading, 'IBM', 0, 3))


class MarkCheck(unittest.TestCase):
    """`mark --check`: success is exit 0, however many marks would place; problems exit 1."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.frame = os.path.join(self.dir, 'subjects', 'subj', 'frames', 'f')
        os.makedirs(self.frame)
        self.write(os.path.join(self.frame, 'reading.md'), READING)
        os.makedirs(os.path.join(self.dir, 'names'))
        self.write(os.path.join(self.dir, 'names', 'aristotle.json'), {'id': 'aristotle', 'wikidata': 'Q868'})
        self.specs = os.path.join(self.dir, 'specs')
        os.makedirs(self.specs)
        self.spec = os.path.join(self.specs, 'subj.json')
        self.write(self.spec, {'subj/f': [['Aristotle', 'aristotle']]})

    def tearDown(self):
        shutil.rmtree(self.dir)

    def write(self, path, value):
        with open(path, 'w') as fh:
            fh.write(value if isinstance(value, str) else json.dumps(value))

    def mark(self, *extra):
        return subprocess.run([sys.executable, os.path.join(HERE, 'names.py'), 'mark', self.spec,
                               '--root', os.path.join(self.dir, 'subjects'),
                               '--names', os.path.join(self.dir, 'names'), *extra],
                              capture_output=True, text=True)

    def test_would_place_is_success(self):
        r = self.mark('--check')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('subj/f: 1 marks would place', r.stdout)
        self.assertIn('aristotle: **[Aristotle]** taught', r.stdout)

    def test_placed_makes_an_unplaced_mark_a_problem(self):
        self.assertEqual(self.mark('--check', '--placed').returncode, 1)
        self.assertEqual(self.mark().returncode, 0)
        self.assertEqual(self.mark('--check', '--placed').returncode, 0)

    def test_a_mark_typed_by_hand_fails(self):
        self.write(os.path.join(self.frame, 'reading.md'),
                   READING.replace("Plato's", "[Plato](kloom:e/plato)'s"))
        self.write(os.path.join(self.dir, 'names', 'plato.json'), {'id': 'plato'})
        r = self.mark('--check')
        self.assertEqual(r.returncode, 1)
        self.assertIn('marks plato, which the spec does not list', r.stderr)

    def test_a_mention_it_cannot_find_fails(self):
        self.write(self.spec, {'subj/f': [['Socrates', 'aristotle']]})
        r = self.mark('--check')
        self.assertEqual(r.returncode, 1)
        self.assertIn('no prose mention of "Socrates"', r.stderr)

    def test_warns_when_the_mark_misses_the_bold_mention(self):
        self.write(os.path.join(self.dir, 'names', 'electron.json'), {'id': 'electron'})
        self.write(self.spec, {'subj/f': [['Electrons', 'electron']]})
        r = self.mark('--check')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('lands on "Electrons" before the bold **electrons**', r.stderr)

    def test_reports_a_draft_the_registry_already_holds(self):
        drafts = os.path.join(self.dir, 'drafts')
        os.makedirs(drafts)
        self.write(os.path.join(drafts, 'aristotle.json'), {'id': 'aristotle', 'wikidata': 'Q868'})
        self.write(os.path.join(drafts, 'the-philosopher.json'), {'id': 'the-philosopher', 'wikidata': 'Q868'})
        r = self.mark('--check', '--drafts', drafts)
        self.assertIn('aristotle.json is already in the registry', r.stderr)
        self.assertIn('Q868 is already names/aristotle.json', r.stderr)

    def test_counts_rather_than_names_stale_drafts_the_specs_do_not_mark(self):
        drafts = os.path.join(self.dir, 'drafts')
        os.makedirs(drafts)
        self.write(os.path.join(self.dir, 'names', 'plato.json'), {'id': 'plato', 'wikidata': 'Q859'})
        self.write(os.path.join(drafts, 'plato.json'), {'id': 'plato', 'wikidata': 'Q859'})
        r = self.mark('--check', '--drafts', drafts)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn('plato.json is already in the registry', r.stderr)
        self.assertIn('1 other drafts passed with --drafts are already in the registry', r.stderr)


if __name__ == '__main__':
    unittest.main()
