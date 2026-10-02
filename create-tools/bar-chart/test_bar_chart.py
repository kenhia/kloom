"""bar_chart.py's fit checks (sprint 027). Run by `just check`."""
import glob, json, os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bar_chart  # noqa: E402

SPEC = {'title': 't', 'description': 'd', 'heading': 'H', 'axis': {'max': 100, 'ticks': [[0, '0'], [100, '100']]},
        'bars': [{'label': 'a', 'value': 10}, {'label': 'b', 'value': 20}]}


class Fit(unittest.TestCase):
    def test_refuses_a_tick_label_wider_than_the_space_left_of_the_axis(self):
        wide = {**SPEC, 'axis': {'max': 100, 'ticks': [[0, '0'], [100, '1,000,000']]}}
        self.assertEqual(len(bar_chart.problems(wide)), 1)
        self.assertIn('tick label "1,000,000"', bar_chart.problems(wide)[0])
        self.assertEqual(bar_chart.problems({**SPEC, 'axis': {'max': 100, 'ticks': [[100, '1M']]}}), [])

    def test_every_committed_spec_fits(self):
        for path in glob.glob(os.path.join(HERE, 'examples', '*.json')):
            with open(path) as fh:
                self.assertEqual(bar_chart.problems(json.load(fh)), [], path)


class Citation(unittest.TestCase):
    def test_prints_the_charts_media_citation_with_its_datas_doi(self):
        import datetime
        spec = {**SPEC, 'source': {'container': 'Chart drawn for kloom from Egan et al. (2021), Table 2',
                                   'doi': '10.1289/EHP7932'}}
        c = bar_chart.media_citation(spec, 'subjects/x/frames/y/blood-lead.svg', datetime.date(2026, 10, 2))
        self.assertEqual(c, {'kind': 'media', 'title': 't', 'authors': [{'name': 'kloom contributors'}],
                             'published': '2026', 'container': 'Chart drawn for kloom from Egan et al. (2021), Table 2',
                             'doi': '10.1289/EHP7932', 'accessed': '2026-10-02', 'licence': 'MIT',
                             'file': 'blood-lead.svg'})
        self.assertIsNone(bar_chart.media_citation(SPEC, 'x.svg'))

    def test_refuses_a_source_without_a_link_or_with_a_doi_link(self):
        self.assertEqual(bar_chart.source_problems({**SPEC, 'source': {'container': 'c', 'doi': 'https://doi.org/10.1/x'}}),
                         ['source.doi is the bare DOI, 10.…, not a link'])
        self.assertEqual(len(bar_chart.source_problems({**SPEC, 'source': {}})), 2)


if __name__ == '__main__':
    unittest.main()
