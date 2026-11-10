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


class Rounding(unittest.TestCase):
    """korg 3557 #2: a value over 100 was rounded whole (159.7 shown as 160); a label keeps the data's
    own decimals, and a whole number none (28, not 28.0: sprint 015)."""

    def test_a_label_keeps_the_datas_decimals(self):
        self.assertEqual(bar_chart.label(159.7, ''), '159.7')
        self.assertEqual(bar_chart.label(2.25, '%'), '2.25%')
        self.assertEqual(bar_chart.label(1234.5, ''), '1,234.5')

    def test_a_whole_number_has_none(self):
        self.assertEqual(bar_chart.label(28.0, ''), '28')
        self.assertEqual(bar_chart.label(12000, 'M'), '12,000M')
        self.assertEqual(bar_chart.label(-3.5, ''), '−3.5')


class Signed(unittest.TestCase):
    """korg 3557 #1: China's net grain imports of 1961–62 were negative before, and could not be charted."""

    SPEC = {**SPEC, 'axis': {'min': -6, 'max': 8, 'ticks': [[-6, '−6'], [0, '0'], [8, '8']]},
            'bars': [{'label': '1959', 'value': -4}, {'label': '1962', 'value': 4}]}

    def test_a_negative_bar_hangs_below_zero(self):
        svg = bar_chart.chart(self.SPEC)
        # zero sits 6/14 of the way up the plot (y 36 to 250): at 250 − 214 × 6 / 14 = 158.3
        self.assertIn('<rect x="135.0" y="158.3" width="56" height="61.1" fill-opacity="0.85"/>', svg)
        self.assertIn('<rect x="333.0" y="97.1" width="56" height="61.1" fill-opacity="0.85"/>', svg)
        # its value's label under its end, the axis's zero line drawn strong
        self.assertIn('<text x="163.0" y="233.4" text-anchor="middle">−4</text>', svg)
        self.assertIn('y1="158.3" y2="158.3" stroke="currentColor" stroke-opacity="0.9"', svg)
        self.assertEqual(bar_chart.problems(self.SPEC), [])

    def test_refuses_a_negative_label_that_meets_the_bar_labels(self):
        deep = {**self.SPEC, 'axis': {**self.SPEC['axis'], 'min': -4}}
        self.assertIn('lower the axis min below -4', ' '.join(bar_chart.problems(deep)))

    def test_refuses_a_negative_value_below_the_axis_min_or_on_a_log_axis(self):
        low = {**self.SPEC, 'axis': {**self.SPEC['axis'], 'min': -2}}
        self.assertIn('below the axis min', ' '.join(bar_chart.problems(low)))
        log = {**self.SPEC, 'scale': 'log', 'axis': {'min': 1, 'max': 10, 'ticks': [[1, '1']]}}
        self.assertIn('log axis', ' '.join(bar_chart.problems(log)))


class Series(unittest.TestCase):
    """korg 3576 #5 and 3557 #1: grouped bars, two or more series side by side, with a legend (sprint
    051 drew horses against tractors by hand)."""

    SPEC = {**SPEC, 'width': 480, 'heading': 'FARM POWER',
            'series': [{'label': 'HORSES'}, {'label': 'TRACTORS'}],
            'bars': [{'label': '1920', 'values': [25, 0.2]}, {'label': '1960', 'values': [3, 4.7]}]}

    def test_draws_each_series_side_by_side_with_a_legend(self):
        svg = bar_chart.chart(self.SPEC)
        self.assertEqual(svg.count('<rect '), 4 + 2)                       # four bars, two legend keys
        self.assertEqual(svg.count('class="accent"'), 2 + 1)               # the second series, and its key
        self.assertIn('>HORSES</text>', svg)
        self.assertIn('>TRACTORS</text>', svg)
        self.assertIn('>0.2</text>', svg)
        self.assertEqual(bar_chart.problems(self.SPEC), [])

    def test_refuses_a_group_with_the_wrong_number_of_values(self):
        bad = {**self.SPEC, 'bars': [{'label': '1920', 'values': [25]}, {'label': '1960', 'values': [3, 4.7]}]}
        self.assertIn('"1920" has 1 values for 2 series', ' '.join(bar_chart.problems(bad)))

    def test_refuses_a_legend_that_meets_the_heading(self):
        long = {**self.SPEC, 'heading': 'WORKING HORSES AND TRACTORS ON US FARMS'}
        self.assertIn('legend', ' '.join(bar_chart.problems(long)))

    def test_a_single_series_chart_is_drawn_as_before(self):
        # every committed spec renders byte for byte as before (checked against the charts in the repo
        # when series were added); here, that a spec without `series` has no legend
        self.assertNotIn('<rect x="', bar_chart.chart(SPEC).split('<g class="muted">')[0])
        self.assertEqual(bar_chart.chart(SPEC).count('<rect '), 2)


class SourceUrl(unittest.TestCase):
    """korg 3576 #5: a Wikipedia page as the data's source is cited by revision (oldid=)."""

    def test_warns_of_a_wikipedia_url_without_oldid(self):
        spec = {**SPEC, 'source': {'container': 'c', 'url': 'https://en.wikipedia.org/wiki/Grain'}}
        self.assertIn('oldid=', ' '.join(bar_chart.source_warnings(spec)))
        ok = {**SPEC, 'source': {'container': 'c', 'url': 'https://en.wikipedia.org/w/index.php?title=Grain&oldid=1'}}
        self.assertEqual(bar_chart.source_warnings(ok), [])
        self.assertEqual(bar_chart.source_warnings({**SPEC, 'source': {'container': 'c', 'url': 'https://fao.org/x'}}), [])


if __name__ == '__main__':
    unittest.main()
