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


if __name__ == '__main__':
    unittest.main()
