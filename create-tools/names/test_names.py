"""names.py: ids, mark placement and `mark --check` (sprint 027). Run by `just check`; no network."""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import names  # noqa: E402
from pathlib import Path  # noqa: E402

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
        # the dotless ı has no decomposition, and was dropped: Nevalı Çori was neval-cori (sprint 051)
        self.assertEqual(names.slug('Nevalı Çori'), 'nevali-cori')


class Lookup(unittest.TestCase):
    def test_untex_drops_a_formulas_tex(self):
        self.assertEqual(names.untex('π 4 = 1 {\\displaystyle {\\frac {\\pi }{4}}=1,} a series.'), 'π 4 = 1 a series.')

    def test_expect_warns_on_a_namesake(self):
        found = {'id': 'hideo-kodama', 'name': 'Hideo Kodama', 'description': 'Japanese politician',
                 'first_line': 'Count Hideo Kodama was a Japanese official and politician.'}
        self.assertIn('namesake', names.unexpected(found, 'stereolithography'))
        self.assertIsNone(names.unexpected(found, 'Politician'))
        self.assertIsNone(names.unexpected({'missing': 'x'}, 'anything'))

    def test_expect_item_warns_on_an_item_that_is_something_else(self):
        # "Duffy antigen system"'s article is the blood group; its Wikidata item is the protein (sprint 029).
        found = {'id': 'duffy-antigen-system', 'name': 'Duffy antigen system', 'wikidata': 'Q205042',
                 'description': 'Human blood group classification',
                 'first_line': 'The Duffy antigen system is a blood group system.',
                 'item_description': 'mammalian protein found in Homo sapiens', 'instance_of': ['protein']}
        # --expect checks the article only (sprint 033): the item is opt-in, with --expect-item.
        self.assertIsNone(names.unexpected(found, 'blood'))
        why = names.unexpected(found, None, 'blood')
        self.assertIn('Q205042 is a protein', why)
        self.assertIsNone(names.unexpected({**found, 'instance_of': ['blood group system']}, 'blood', 'blood'))
        # Without what Wikidata says, only the article is checked.
        self.assertIsNone(names.unexpected({k: v for k, v in found.items() if k not in ('instance_of',)}, None, 'blood'))

    def test_a_title_carries_its_own_expectation(self):
        found = {'id': 'hideo-kodama', 'name': 'Hideo Kodama', 'description': 'Japanese politician', 'first_line': ''}
        (title, keyword), = names.expectations(['Hideo Kodama=stereolithography'], 'politician')
        self.assertEqual(title, 'Hideo Kodama')
        self.assertIn('namesake', names.unexpected(found, keyword))

    def test_a_set_index_page_is_ambiguous(self):
        data = {'pages': {
            '1': {'title': 'Sodium citrate', 'pageprops': {'wikibase_item': 'Q6460572'},
                  'categories': [{'ns': 14, 'title': names.SET_INDEX}]},
            '2': {'title': 'Trisodium citrate', 'pageprops': {'wikibase_item': 'Q409728'}, 'extract': 'A salt.'},
        }}
        found = names.rows(['Sodium citrate', 'Trisodium citrate'], data)
        self.assertEqual(found['Sodium citrate'], {'ambiguous': 'Sodium citrate', 'page': 'Sodium citrate'})
        self.assertEqual(found['Trisodium citrate']['id'], 'trisodium-citrate')


class Strip(unittest.TestCase):
    def test_takes_out_marks_and_keeps_their_words(self):
        reading = ('**[William Harvey](kloom:e/william-harvey)** showed in [De Motu\nCordis](kloom:e/de-motu-cordis) '
                   'that [the blood](https://example.org/) goes round.')
        self.assertEqual(names.strip(reading), '**William Harvey** showed in De Motu\nCordis that '
                                               '[the blood](https://example.org/) goes round.')

    def test_strips_frames_to_a_directory_or_one_text(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        d = os.path.join(root, 's', 'frames', 'f')
        os.makedirs(d)
        with open(os.path.join(d, 'reading.md'), 'w') as f:
            f.write('A [name](kloom:e/name).\n')
        text, problems = names.strip_frames(root, ['s/f', 's/nope'])
        self.assertEqual(text, '<!-- s/f -->\n\nA name.\n')
        self.assertEqual(len(problems), 1)
        out = os.path.join(root, 'out')
        self.assertEqual(names.strip_frames(root, ['s/f'], out), (None, []))
        with open(os.path.join(out, 's-f.md')) as f:
            self.assertEqual(f.read(), 'A name.\n')


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

    def test_bold_elsewhere_sees_an_italic_name_in_bold(self):
        # A spec's words keep the italics of a species or a title; the bold run is the same words
        # in bold (sprint 030, where the mark landed on a passing mention with no warning).
        reading = 'It was _Staphylococcus aureus_ again. **_Staphylococcus aureus_** lives on skin.'
        a, b = names.place(reading, '_Staphylococcus aureus_', 'staphylococcus-aureus')
        self.assertEqual(names.bold_elsewhere(reading, '_Staphylococcus aureus_', a, b),
                         '**_Staphylococcus aureus_**')

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

    def test_a_frame_not_in_the_copy_is_skipped_with_a_note(self):
        # An author's copy built with --only leaves other frames out (sprint 049, where it crashed).
        self.write(self.spec, {'subj/f': [['Aristotle', 'aristotle']], 'subj/unwritten': [['Aristotle', 'aristotle']]})
        r = self.mark('--check')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('subj/unwritten: not in', r.stderr)

    def test_placed_fails_on_a_frame_that_is_not_there(self):
        self.write(self.spec, {'subj/unwritten': [['Aristotle', 'aristotle']]})
        self.assertEqual(self.mark('--check', '--placed').returncode, 1)

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

    def test_a_name_no_file_holds_stops_the_frame_being_marked(self):
        # Placing went ahead after naming the unknown name, and wrote the frame (sprint 030).
        self.write(self.spec, {'subj/f': [['Aristotle', 'aristotle'], ['Plato', 'plato']]})
        r = self.mark()
        self.assertEqual(r.returncode, 1)
        self.assertIn('plato is not in the registry or a draft', r.stderr)
        with open(os.path.join(self.frame, 'reading.md')) as fh:
            self.assertNotIn('kloom:e/', fh.read())

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

    def test_an_unfinished_draft_is_not_yet_known(self):
        # `--check` passed a mark on a draft whose kind and description were still empty, which the
        # checking copy (`subject_plan.py --complete`) leaves out, so the copy refused the whole
        # frame; five of sprint 055's authors met the two disagreeing.
        drafts = os.path.join(self.dir, 'drafts')
        os.makedirs(drafts)
        self.write(os.path.join(drafts, 'plato.json'), {'id': 'plato', 'wikidata': 'Q859', 'kind': '', 'description': ''})
        self.write(self.spec, {'subj/f': [['Aristotle', 'aristotle'], ['Plato', 'plato']]})
        r = self.mark('--check', '--drafts', drafts)
        self.assertEqual(r.returncode, 1)
        self.assertIn('plato is drafted but unfinished', r.stderr)
        self.write(os.path.join(drafts, 'plato.json'),
                   {'id': 'plato', 'wikidata': 'Q859', 'kind': 'person', 'description': 'Greek philosopher.'})
        self.assertEqual(self.mark('--check', '--drafts', drafts).returncode, 0)



class Drafts(unittest.TestCase):
    """`drafts` (sprint 033): who drafted which name, and what was drafted twice or by a non-owner."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        for part, name, item, home in (('nightingale', 'florence-nightingale', 'Q37103', 'nursing/scutari'),
                                       ('nightingale', 'scutari', 'Q1', ''),
                                       ('war', 'florence-nightingale', 'Q37103', ''),
                                       ('war', 'scutari-barracks', 'Q1', ''),
                                       ('war', 'red-cross', 'Q2', '')):
            os.makedirs(os.path.join(self.dir, f'nursing-{part}'), exist_ok=True)
            with open(os.path.join(self.dir, f'nursing-{part}', f'{name}.json'), 'w') as fh:
                json.dump({'id': name, 'wikidata': item, **({'home': home} if home else {})}, fh)
        os.makedirs(os.path.join(self.dir, 'blood-other'))

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_lists_each_draft_with_its_part(self):
        rows, _, _ = names.drafts('nursing', self.dir)
        self.assertEqual(len(rows), 5)
        self.assertIn({'id': 'florence-nightingale', 'wikidata': 'Q37103', 'home': 'nursing/scutari',
                       'part': 'nightingale'}, rows)

    def test_flags_a_name_drafted_twice_and_by_a_part_that_does_not_own_it(self):
        _, problems, _ = names.drafts('nursing', self.dir, {'owners': {'red-cross': 'nightingale'}})
        self.assertEqual(problems[0], 'florence-nightingale is drafted by 2 parts: nightingale, war')
        self.assertIn('red-cross is drafted by war, but the plan gives it to nightingale', problems[1])
        self.assertEqual(problems[2], 'Q1 is drafted under 2 ids: scutari, scutari-barracks')

    def test_notes_a_draft_the_registry_already_holds(self):
        registry = os.path.join(self.dir, 'names')
        os.makedirs(registry)
        with open(os.path.join(registry, 'red-cross.json'), 'w') as fh:
            json.dump({'id': 'red-cross', 'wikidata': 'Q2'}, fh)
        _, _, notes = names.drafts('nursing', self.dir, None, {'red-cross': Path(registry) / 'red-cross.json'})
        self.assertIn('already in the registry', notes[0])

    def test_one_part_sees_its_own_drafts_and_problems(self):
        # sprint 051: with 24 parts at once, every author's run failed on another part's problem.
        result = names.drafts('nursing', self.dir, {'owners': {'red-cross': 'nightingale'}})
        rows, problems, _ = names.for_part(*result, 'nightingale')
        self.assertEqual({r['id'] for r in rows}, {'florence-nightingale', 'scutari'})
        self.assertEqual(len(problems), 3)  # its name drafted twice, the item under two ids, its owned name
        rows, problems, _ = names.for_part(*names.drafts('nursing', self.dir), 'nobody')
        self.assertEqual((rows, problems), ([], []))


class DraftsUnmarked(unittest.TestCase):
    """A draft no spec marks (korg 3554: in sprint 049 late2 drafted a name and never marked it)."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.specs = os.path.join(self.dir, 'specs')
        os.makedirs(self.specs)
        for part, name in (('one', 'marked'), ('one', 'forgotten'), ('two', 'early')):
            os.makedirs(os.path.join(self.dir, f'subj-{part}'), exist_ok=True)
            with open(os.path.join(self.dir, f'subj-{part}', f'{name}.json'), 'w') as fh:
                json.dump({'id': name, 'wikidata': f'Q{len(name)}{part}'}, fh)
        # Part one has a spec; part two has not written one yet.
        with open(os.path.join(self.specs, 'subj-one.json'), 'w') as fh:
            json.dump({'subj/a': [['Marked', 'marked']]}, fh)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_a_draft_its_parts_spec_does_not_mark_is_a_problem(self):
        _, problems, notes = names.drafts('subj', self.dir, specs=self.specs)
        self.assertEqual(problems, ['forgotten is drafted by one, and no spec marks it: '
                                    'add it to a spec, or drop the draft'])
        self.assertIn('early is drafted by two, which has no spec yet (subj-two.json)', notes)

    def test_another_parts_spec_marking_it_is_enough(self):
        with open(os.path.join(self.specs, 'shared.json'), 'w') as fh:
            json.dump({'subj/b': [['forgotten', 'forgotten']]}, fh)
        _, problems, _ = names.drafts('subj', self.dir, specs=self.specs)
        self.assertEqual(problems, [])


class WriteDraft(unittest.TestCase):
    """`lookup --write-draft DIR` (korg 3554): no Wikidata id typed by hand."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_writes_a_skeleton_add_refuses_until_it_is_written(self):
        row = {'id': 'edward-gibbon', 'wikidata': 'Q312627', 'name': 'Edward Gibbon',
               'description': 'English historian (1737-1794)', 'first_line': 'Edward Gibbon was...'}
        said = names.write_drafts({'Edward Gibbon': row, 'Mercury': {'ambiguous': 'Mercury', 'page': 'Mercury'}},
                                  self.dir, doubtful={'Nobody'})
        with open(os.path.join(self.dir, 'edward-gibbon.json')) as fh:
            draft = json.load(fh)
        self.assertEqual((draft['id'], draft['wikidata'], draft['name']), ('edward-gibbon', 'Q312627', 'Edward Gibbon'))
        self.assertEqual(said, [f'wrote {self.dir}/edward-gibbon.json', 'Mercury: ambiguous, not written'])
        # Kind and description are the author's to write; add refuses the skeleton until they are.
        self.assertEqual(names.name_problems(draft), ['description is required', f'kind must be one of {", ".join(names.KINDS)}'])

    def test_leaves_a_draft_already_there_and_a_doubtful_row(self):
        path = os.path.join(self.dir, 'edward-gibbon.json')
        with open(path, 'w') as fh:
            fh.write('{"kept": true}')
        row = {'id': 'edward-gibbon', 'wikidata': 'Q312627', 'name': 'Edward Gibbon'}
        said = names.write_drafts({'Edward Gibbon': row, 'Gibbon': {**row, 'id': 'gibbon'}}, self.dir, doubtful={'Gibbon'})
        self.assertEqual(said, [f'{path} is already there, left alone', 'Gibbon: warned of, not written'])
        with open(path) as fh:
            self.assertEqual(json.load(fh), {'kept': True})


class Add(unittest.TestCase):
    """`add` writes drafts into the registry (sprint 049: since sprint 033 a second `drafts` shadowed the
    helper `add` read its files with, and every `add` failed with a TypeError)."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.drafts = os.path.join(self.dir, 'drafts')
        self.registry = os.path.join(self.dir, 'names')
        os.makedirs(self.drafts)
        os.makedirs(self.registry)
        with open(os.path.join(self.registry, 'babylon.json'), 'w') as fh:
            json.dump({'id': 'babylon', 'wikidata': 'Q5684', 'name': 'Babylon', 'kind': 'place',
                       'description': 'An ancient city.'}, fh)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def draft(self, name, item):
        with open(os.path.join(self.drafts, f'{name}.json'), 'w') as fh:
            json.dump({'id': name, 'wikidata': item, 'name': name.title(), 'kind': 'person',
                       'description': 'Someone who matters.'}, fh)

    def test_writes_a_new_name(self):
        self.draft('hammurabi', 'Q36359')
        self.assertEqual(names.add([self.drafts], self.registry), [])
        self.assertTrue(os.path.exists(os.path.join(self.registry, 'hammurabi.json')))

    def test_refuses_an_item_another_file_holds(self):
        self.draft('babylon-city', 'Q5684')
        refused = names.add([self.drafts], self.registry)
        self.assertIn('Q5684 is already names/babylon.json', refused[0])


if __name__ == '__main__':
    unittest.main()
