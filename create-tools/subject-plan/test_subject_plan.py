"""subject_plan.py's plan checks (sprint 027). Run by `just check`."""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from subject_plan import merge_drafts, owner_problems, plan_problems  # noqa: E402

PALETTES = {'flint', 'chalk'}


def plan(frames=None, kind='date', ids=('a', 'b', 'c')):
    return {'spine': {'segments': [{'id': 's', 'title': 'S', 'labelKind': kind, 'frames': list(ids)}]},
            'trails': [], **({'frames': frames} if frames is not None else {})}


class PlanProblems(unittest.TestCase):
    def test_a_plan_without_frames_is_fine(self):
        self.assertEqual(plan_problems(plan(), PALETTES), ([], []))

    def test_sorts_must_rise_within_a_date_segment(self):
        problems, _ = plan_problems(plan({'a': {'sort': 1859}, 'b': {'sort': 1850}}), PALETTES)
        self.assertEqual(problems, ['spine segment s: b (1850) comes after a (1859)'])

    def test_a_sort_outside_a_date_segment_is_refused(self):
        problems, _ = plan_problems(plan({'a': {'sort': 1}}, kind='category'), PALETTES)
        self.assertIn('only a date segment sorts', problems[0])

    def test_topics_fit_the_cap_and_are_unique(self):
        problems, _ = plan_problems(plan({'a': {'topic': 'x' * 41}, 'b': {'topic': 'Same'},
                                          'c': {'topic': 'same'}}), PALETTES)
        self.assertEqual(len(problems), 2)
        self.assertIn('41 characters', problems[0])
        self.assertIn('already b', problems[1])

    def test_a_topic_is_a_title(self):
        problems, _ = plan_problems(plan({'a': {'topic': 'Knapping.'}}), PALETTES)
        self.assertIn('no closing', problems[0])

    def test_palettes_must_be_the_subjects(self):
        problems, _ = plan_problems(plan({'a': {'palette': 'ember'}}), PALETTES)
        self.assertIn('unknown palette "ember"', problems[0])

    def test_warns_where_a_palette_repeats_down_a_segment(self):
        problems, warnings = plan_problems(plan({'a': {'palette': 'flint'}, 'b': {'palette': 'flint'}}), PALETTES)
        self.assertEqual(problems, [])
        self.assertEqual(warnings, ['spine segment s: b repeats the palette "flint" of the frame before it'])

    def test_an_entry_for_a_frame_on_no_spine_is_refused(self):
        problems, _ = plan_problems(plan({'z': {'topic': 'Zed'}}), PALETTES)
        self.assertEqual(problems, ['frames.z: not on the spine or a trail'])

    def test_warns_where_a_written_frame_differs_from_its_plan(self):
        written = {'a': {'topic': 'Other', 'position': {'sort': 1}, 'scene': {'palette': 'flint'}}}
        _, warnings = plan_problems(plan({'a': {'topic': 'Planned', 'sort': 1, 'palette': 'flint'}}), PALETTES, written)
        self.assertEqual(warnings, ["frames.a: the plan's topic is 'Planned', the frame's 'Other'"])


class Check(unittest.TestCase):
    """`--check` exits 1 on a problem, 0 on warnings alone."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, 'subj', 'frames'))
        with open(os.path.join(self.dir, 'subj', 'subject.json'), 'w') as fh:
            json.dump({'palettes': {p: {} for p in PALETTES}}, fh)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def run_check(self, p):
        path = os.path.join(self.dir, 'plan.json')
        with open(path, 'w') as fh:
            json.dump(p, fh)
        return subprocess.run([sys.executable, os.path.join(HERE, 'subject_plan.py'), path,
                               os.path.join(self.dir, 'subj'), '--check'], capture_output=True, text=True)

    def test_exits_1_on_a_problem(self):
        r = self.run_check(plan({'a': {'sort': 2}, 'b': {'sort': 1}}))
        self.assertEqual(r.returncode, 1)
        self.assertIn('problem: spine segment s: b (1) comes after a (2)', r.stderr)

    def test_exits_0_on_warnings(self):
        r = self.run_check(plan({'a': {'palette': 'flint'}, 'b': {'palette': 'flint'}}))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('warning:', r.stdout)


class MergeDrafts(unittest.TestCase):
    """--complete's name drafts (sprint 028): two directories drafting one id differently are said."""

    def test_says_when_two_directories_draft_one_id(self):
        root = tempfile.mkdtemp()
        try:
            a, b, names = (os.path.join(root, x) for x in ('a', 'b', 'names'))
            for d in (a, b, names):
                os.makedirs(d)
            for d, home in ((a, 'blood/x'), (b, None)):
                with open(os.path.join(d, 'factor.json'), 'w') as fh:
                    json.dump({'id': 'factor', 'home': home}, fh)
            with open(os.path.join(b, 'same.json'), 'w') as fh:
                fh.write('{}')
            with open(os.path.join(a, 'same.json'), 'w') as fh:
                fh.write('{}')
            out = merge_drafts([a, b], names)
            self.assertEqual(len(out), 1)
            self.assertIn('factor.json is drafted in both', out[0])
            self.assertEqual(sorted(os.listdir(names)), ['factor.json', 'same.json'])
        finally:
            shutil.rmtree(root)


class CompleteWithDrafts(unittest.TestCase):
    """--complete --with-drafts (sprint 029): a frame.json.draft goes into the copy as frame.json."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.subj = os.path.join(self.dir, 'subjects', 'subj')
        for f, name in (('a', 'frame.json'), ('b', 'frame.json.draft'), ('c', 'frame.json'), ('c', 'frame.json.draft')):
            os.makedirs(os.path.join(self.subj, 'frames', f), exist_ok=True)
            with open(os.path.join(self.subj, 'frames', f, name), 'w') as fh:
                json.dump({'id': f, 'from': name}, fh)
        with open(os.path.join(self.subj, 'subject.json'), 'w') as fh:
            json.dump({'palettes': {}}, fh)
        self.names = os.path.join(self.dir, 'names')
        os.makedirs(self.names)
        self.plan = os.path.join(self.dir, 'plan.json')
        with open(self.plan, 'w') as fh:
            json.dump(plan(), fh)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def complete(self, *extra):
        out = os.path.join(self.dir, 'copy')
        r = subprocess.run([sys.executable, os.path.join(HERE, 'subject_plan.py'), self.plan, self.subj,
                            '--complete', out, '--names', self.names, *extra], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(os.path.join(out, 'subj', 'spine.json')) as fh:
            spine = [f for s in json.load(fh)['segments'] for f in s['frames']]
        return out, spine, r.stdout

    def test_without_it_a_draft_is_left_out(self):
        _, spine, _ = self.complete()
        self.assertEqual(spine, ['a', 'c'])

    def test_with_it_the_draft_is_the_frame(self):
        out, spine, said = self.complete('--with-drafts')
        self.assertEqual(spine, ['a', 'b', 'c'])
        frames = os.path.join(out, 'subj', 'frames')
        for f in ('b', 'c'):
            with open(os.path.join(frames, f, 'frame.json')) as fh:
                self.assertEqual(json.load(fh)['from'], 'frame.json.draft')
            self.assertFalse(os.path.exists(os.path.join(frames, f, 'frame.json.draft')))
        self.assertIn('c: the copy holds its frame.json.draft', said)


class Owners(unittest.TestCase):
    """The plan's owners of shared names (sprint 033): what names.py drafts checks the drafts against."""

    def test_an_owner_is_a_part_of_the_plan(self):
        p = {**plan(), 'trails': [{'id': 't', 'anchor': 'a', 'spine': {'segments': []}}],
             'owners': {'reprap': 's', 'chuck-hull': 't', 'Bad Id': 's', 'x': 'nowhere'}}
        self.assertEqual(owner_problems(p), ['owners.Bad Id: not a name id (lower-case words joined by "-")',
                                             'owners.x: "nowhere" is not a part of the plan (s, t)'])
        self.assertEqual(owner_problems(plan()), [])

    def test_frames_name_their_parts(self):
        p = {**plan({'a': {'part': 'navy1'}, 'b': {'part': 'navy2'}}), 'owners': {'reprap': 'navy2', 'x': 's'}}
        self.assertEqual(owner_problems(p), ['owners.x: "s" is not a part of the plan (navy1, navy2)'])


class StandIn(unittest.TestCase):
    """--complete --stand-in (sprint 033): a trail's anchor not yet written, in the copy only."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.subj = os.path.join(self.dir, 'subjects', 'subj')
        os.makedirs(os.path.join(self.subj, 'frames', 'b'))
        os.makedirs(os.path.join(self.subj, 'frames', 't1'))
        for f in ('b', 't1'):
            with open(os.path.join(self.subj, 'frames', f, 'frame.json'), 'w') as fh:
                json.dump({'id': f}, fh)
        with open(os.path.join(self.subj, 'subject.json'), 'w') as fh:
            json.dump({'palettes': {'flint': {}, 'chalk': {}}}, fh)
        self.names = os.path.join(self.dir, 'names')
        os.makedirs(self.names)
        p = {**plan({'a': {'topic': 'The anchor', 'sort': 1850, 'palette': 'chalk'}}, ids=('a', 'b')),
             'trails': [{'id': 'trail', 'title': 'T', 'anchor': 'a',
                         'spine': {'segments': [{'id': 'ts', 'title': 'TS', 'labelKind': 'category', 'frames': ['t1']}]}}]}
        self.plan = os.path.join(self.dir, 'plan.json')
        with open(self.plan, 'w') as fh:
            json.dump(p, fh)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def run_plan(self, *extra):
        return subprocess.run([sys.executable, os.path.join(HERE, 'subject_plan.py'), self.plan, self.subj,
                               '--names', self.names, *extra], capture_output=True, text=True)

    def test_puts_the_anchor_and_its_trail_on_the_copys_spine(self):
        out = os.path.join(self.dir, 'copy')
        r = self.run_plan('--complete', out, '--stand-in', 'a')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('wrote a stand-in for a', r.stdout)
        with open(os.path.join(out, 'subj', 'frames', 'a', 'frame.json')) as fh:
            frame = json.load(fh)
        self.assertEqual((frame['topic'], frame['position'], frame['scene']['palette']),
                         ('The anchor', {'label': '1850', 'sort': 1850}, 'chalk'))
        self.assertNotIn('connections', frame)
        self.assertTrue(os.path.exists(os.path.join(out, 'subj', 'trails', 'trail.json')))
        # The live subject is untouched.
        self.assertFalse(os.path.exists(os.path.join(self.subj, 'frames', 'a')))

    def test_refuses_without_a_copy_and_for_a_frame_no_trail_hangs_from(self):
        self.assertNotEqual(self.run_plan('--stand-in', 'a').returncode, 0)
        r = self.run_plan('--complete', os.path.join(self.dir, 'copy'), '--stand-in', 'b')
        self.assertIn('not the anchor of any trail', r.stderr)


if __name__ == '__main__':
    unittest.main()
