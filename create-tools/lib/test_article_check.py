"""article_check.py, shared by names.py and wiki_cite.py (sprint 033). Run by `just check`; no network."""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import article_check as ac  # noqa: E402


class Expectations(unittest.TestCase):
    def test_a_title_may_carry_its_own_keyword(self):
        self.assertEqual(ac.expectations(['Army Medical School=Washington', 'Walter Reed'], 'army'),
                         [('Army Medical School', 'Washington'), ('Walter Reed', 'army')])

    def test_an_equals_sign_with_nothing_after_it_is_the_title(self):
        self.assertEqual(ac.expectations(['E=', 'Title'], None), [('E=', None), ('Title', None)])


class Mismatch(unittest.TestCase):
    def test_the_article_check_reads_the_description_and_first_line(self):
        self.assertIn('namesake', ac.article_mismatch('Hideo Kodama', 'Japanese politician',
                                                      'Count Hideo Kodama was a politician.', 'stereolithography'))
        self.assertIsNone(ac.article_mismatch('Hideo Kodama', 'Japanese politician', '', 'Politician'))
        self.assertIsNone(ac.article_mismatch('Hideo Kodama', 'Japanese politician', '', None))

    def test_the_item_check_reads_the_items_description_and_class(self):
        why = ac.item_mismatch('Duffy antigen system', 'Q1', 'mammalian protein found in Homo sapiens',
                               ['protein'], 'blood')
        self.assertIn('Q1 is a protein', why)
        self.assertIsNone(ac.item_mismatch('Duffy antigen system', 'Q1', '', ['blood group system'], 'blood'))

    def test_untex_drops_a_formulas_tex(self):
        self.assertEqual(ac.untex('π 4 = 1 {\\displaystyle {\\frac {\\pi }{4}}=1,} a series.'), 'π 4 = 1 a series.')


if __name__ == '__main__':
    unittest.main()
