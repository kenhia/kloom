"""wiki_cite.py's text and citations (sprint 027). Run by `just check`; no network."""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wiki_cite  # noqa: E402

MATH = ('<p>It states that <span class="mwe-math-element"><span style="display: none;">'
        '<math alttext="{\\displaystyle {\\frac {\\pi }{4}}=1-\\cdots }"><semantics><mrow><mi>π</mi>'
        '<mn>4</mn></mrow></semantics></math></span><img alt="{\\displaystyle x}"></span>, an alternating series.'
        '<sup class="reference">[1]</sup></p>')


class Text(unittest.TestCase):
    def test_writes_a_formula_once_as_its_tex(self):
        self.assertEqual(wiki_cite.readable(MATH), 'It states that ${\\frac {\\pi }{4}}=1-\\cdots$ , an alternating series.\n')


class Citation(unittest.TestCase):
    def test_another_languages_text_keeps_its_own_file(self):
        self.assertEqual(wiki_cite.text_name('Luis Agote'), 'Luis Agote.txt')
        self.assertEqual(wiki_cite.text_name('Luis Agote', 'es'), 'Luis Agote.es.txt')
        self.assertEqual(wiki_cite.text_name('AC/DC'), 'AC_DC.txt')

    def test_cites_english_wikipedia_without_a_language(self):
        c = wiki_cite.citation('Printing press', 1, '2026-09-25', '2026-09-26')
        self.assertEqual(c['url'], 'https://en.wikipedia.org/w/index.php?title=Printing_press&oldid=1')
        self.assertNotIn('language', c)

    def test_cites_another_wikipedia_with_its_language(self):
        c = wiki_cite.citation('Zaagmolen', 64339876, '2023-05-21', '2026-09-30', 'nl')
        self.assertEqual(c['url'], 'https://nl.wikipedia.org/w/index.php?title=Zaagmolen&oldid=64339876')
        self.assertEqual(c['language'], 'nl')
        self.assertEqual(c['container'], 'Wikipedia, The Free Encyclopedia')


class Expect(unittest.TestCase):
    def test_warns_of_a_namesake_naming_the_article_it_landed_on(self):
        asked = wiki_cite.expectations(['Army Medical School=London', 'Walter Reed'], 'army')
        revs = {'Army Medical School': ('Army Medical School', 1, '2026-01-01'), 'Walter Reed': ('Walter Reed', 2, '2026-01-01')}
        about = {'Army Medical School': ('Former US Army school', 'The Army Medical School was founded in Washington.'),
                 'Walter Reed': ('American Army physician', '')}
        (why,) = wiki_cite.mismatches(asked, revs, about)
        self.assertIn('"Army Medical School" does not say \'London\'', why)
        # A redirect says where it went.
        revs['Army Medical School'] = ('Walter Reed Army Institute of Research', 1, '2026-01-01')
        about['Walter Reed Army Institute of Research'] = ('US Army research institute', '')
        (why,) = wiki_cite.mismatches(asked, revs, about)
        self.assertTrue(why.startswith('"Army Medical School" landed on "Walter Reed Army Institute of Research"'))

    def test_says_nothing_without_a_keyword(self):
        asked = wiki_cite.expectations(['Walter Reed'])
        self.assertEqual(wiki_cite.mismatches(asked, {'Walter Reed': ('Walter Reed', 2, 'x')}, {}), [])


if __name__ == '__main__':
    unittest.main()
