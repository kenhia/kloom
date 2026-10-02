"""openalex.py without the network: the key's sources, that it is never shown, and the parsing."""
import os, sys, tempfile, unittest, urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
import openalex as oa  # noqa: E402


class Key(unittest.TestCase):
    def file(self, text):
        f = tempfile.NamedTemporaryFile('w', delete=False, suffix='.env')
        f.write(text)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def test_environment_wins(self):
        path = self.file("OPENALEX_API_KEY='from-file'\n")
        self.assertEqual(oa.api_key({'OPENALEX_API_KEY': 'from-env'}, path), 'from-env')

    def test_file_single_quoted_as_khomelab_writes_it(self):
        path = self.file("# comment\nHF_TOKEN='x'\nOPENALEX_API_KEY='abc=def'\n")
        self.assertEqual(oa.api_key({}, path), 'abc=def')

    def test_file_unquoted_and_double_quoted(self):
        self.assertEqual(oa.read_env_file(self.file('OPENALEX_API_KEY=plain\n')), 'plain')
        self.assertEqual(oa.read_env_file(self.file('OPENALEX_API_KEY="dq"\n')), 'dq')

    def test_prefix_is_not_a_match(self):
        self.assertIsNone(oa.read_env_file(self.file("OPENALEX_API_KEY_OLD='no'\n")))

    def test_missing_or_unreadable(self):
        self.assertIsNone(oa.api_key({}, '/nonexistent/secrets.env'))


class NeverShown(unittest.TestCase):
    key = 'k3y/with+chars='

    def test_url_carries_it_encoded(self):
        url = oa.url_for('works?search=x', self.key)
        self.assertIn('&api_key=' + urllib.parse.quote(self.key, safe=''), url)
        self.assertEqual(oa.url_for('works/W1', self.key).count('?api_key='), 1)

    def test_redact_raw_and_encoded(self):
        url = oa.url_for('works/W1', self.key)
        for text in (url, f'error for {self.key}'):
            self.assertNotIn(self.key, oa.redact(text, self.key))
            self.assertNotIn(urllib.parse.quote(self.key, safe=''), oa.redact(text, self.key))

    def test_no_key_no_param(self):
        self.assertEqual(oa.url_for('works/W1'), oa.API + 'works/W1')
        self.assertEqual(oa.redact('anything', None), 'anything')


class Parsing(unittest.TestCase):
    def test_work_refs(self):
        for ref in ('10.1038/171737a0', 'doi:10.1038/171737a0', 'https://doi.org/10.1038/171737a0'):
            self.assertEqual(oa.work_path(ref), 'works/doi:10.1038/171737a0')
        self.assertEqual(oa.work_path('w2741809807'), 'works/W2741809807')
        self.assertEqual(oa.work_path('https://openalex.org/W2741809807'), 'works/W2741809807')
        with self.assertRaises(ValueError):
            oa.work_path('not a reference')

    def test_abstract_rebuilt_in_order(self):
        self.assertEqual(oa.abstract({'helix': [3], 'We': [0], 'a': [2], 'propose': [1]}), 'We propose a helix')
        self.assertIsNone(oa.abstract(None))

    def test_summary_names_open_copies(self):
        w = {'display_name': 'T', 'publication_year': 1953, 'type': 'article', 'doi': 'https://doi.org/10.1/x',
             'id': 'https://openalex.org/W1', 'authorships': [{'author': {'display_name': 'A'}}],
             'open_access': {'oa_status': 'green', 'oa_url': 'https://repo/x.pdf'},
             'locations': [{'is_oa': True, 'landing_page_url': 'https://repo/x', 'pdf_url': 'https://repo/x.pdf',
                            'version': 'acceptedVersion'}, {'is_oa': False, 'landing_page_url': 'https://pub/x'}],
             'abstract_inverted_index': {'Hi': [0]}}
        s = oa.summary(w)
        self.assertIn('open access: green — https://repo/x.pdf', s)
        self.assertIn('open copy: https://repo/x.pdf (acceptedVersion)', s)
        self.assertNotIn('https://pub/x', s)
        self.assertIn('abstract: Hi', s)


if __name__ == '__main__':
    unittest.main()
