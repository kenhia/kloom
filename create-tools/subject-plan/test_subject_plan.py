"""subject_plan.py's plan checks (sprint 027). Run by `just check`."""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from subject_plan import accent_problems, merge_drafts, owner_problems, parse_claims, plan_problems  # noqa: E402

PALETTES = {'flint', 'chalk'}


def plan(frames=None, kind='date', ids=('a', 'b', 'c'), palette=None):
    seg = {'id': 's', 'title': 'S', 'labelKind': kind, 'frames': list(ids)}
    if palette:
        seg['palette'] = palette
    return {'spine': {'segments': [seg]},
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

    def test_a_section_keeps_one_palette_without_a_warning(self):
        # The old rule (dark and light alternating) is gone: a repeat is the point (korg 3495).
        frames = {'a': {'palette': 'flint'}, 'b': {'palette': 'flint'}}
        self.assertEqual(plan_problems(plan(frames, palette='flint'), PALETTES), ([], []))

    def test_warns_where_a_frame_leaves_its_section_with_no_reason(self):
        frames = {'a': {'palette': 'flint'}, 'b': {'palette': 'chalk'}}
        problems, warnings = plan_problems(plan(frames, palette='flint'), PALETTES)
        self.assertEqual(problems, [])
        self.assertEqual(warnings, ['spine segment s: b wears "chalk", not its section\'s "flint"; '
                                    'match it, or say why in frames.b.paletteWhy'])
        frames['b']['paletteWhy'] = 'the frame is a night scene'
        self.assertEqual(plan_problems(plan(frames, palette='flint'), PALETTES), ([], []))

    def test_warns_where_a_segment_names_no_palette_of_its_own(self):
        problems, warnings = plan_problems(plan({'a': {'palette': 'flint'}}), PALETTES)
        self.assertEqual(problems, [])
        self.assertEqual(warnings, ['spine segment s: give the segment its section\'s "palette"; its frames name theirs'])

    def test_a_section_palette_must_be_the_subjects(self):
        problems, _ = plan_problems(plan(palette='ember'), PALETTES)
        self.assertIn('segment s: unknown palette "ember"', problems[0])

    def test_an_entry_for_a_frame_on_no_spine_is_refused(self):
        problems, _ = plan_problems(plan({'z': {'topic': 'Zed'}}), PALETTES)
        self.assertEqual(problems, ['frames.z: not on the spine or a trail'])

    def test_warns_where_a_written_frame_differs_from_its_plan(self):
        written = {'a': {'topic': 'Other', 'position': {'sort': 1}, 'scene': {'palette': 'flint'}}}
        _, warnings = plan_problems(plan({'a': {'topic': 'Planned', 'sort': 1, 'palette': 'flint'}}, palette='flint'),
                                    PALETTES, written)
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

    def test_reads_an_accents_file(self):
        claims = os.path.join(self.dir, 'accents.txt')
        with open(claims, 'w') as fh:
            fh.write('BALLOT ind2 a\nBALLOT mod2 b\n')
        path = os.path.join(self.dir, 'plan.json')
        with open(path, 'w') as fh:
            json.dump(plan(), fh)
        r = subprocess.run([sys.executable, os.path.join(HERE, 'subject_plan.py'), path,
                            os.path.join(self.dir, 'subj'), '--check', '--accents', claims], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn('accents.txt:2: b (mod2) claims "BALLOT", claimed first for a (ind2) at line 1', r.stderr)

    def test_exits_0_on_warnings(self):
        r = self.run_check(plan({'a': {'palette': 'flint'}, 'b': {'palette': 'flint'}}))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('warning:', r.stdout)


class Accents(unittest.TestCase):
    """Accents claimed before writing, enforced (korg 3554: four clashes in sprint 049 found only at commit)."""

    def written(self, **accents):
        return {f: {'scene': {'accent': a}} for f, a in accents.items()}

    def test_the_plans_accents_are_unique(self):
        problems, _ = accent_problems(plan({'a': {'accent': 'Ballot.'}, 'b': {'accent': 'BALLOT'}}), {}, [])
        self.assertEqual(problems, ['frames.b: accent "BALLOT" is already planned for a'])

    def test_a_planned_accent_another_frame_wears_is_refused(self):
        problems, _ = accent_problems(plan({'a': {'accent': 'DEAD.'}}), self.written(c='DEAD.', a='DEAD.'), [])
        self.assertEqual(problems, ['frames.a: accent "DEAD" is already frames/c\'s'])

    def test_a_written_frame_that_left_its_planned_accent_is_a_warning(self):
        self.assertEqual(accent_problems(plan({'a': {'accent': 'DEAD.'}}), self.written(a='DOWN.'), []),
                         ([], ['frames.a: the plan\'s accent is \'DEAD\', the frame\'s \'DOWN\'']))

    def test_the_first_claim_wins(self):
        claims, bad = parse_claims('PEOPLE. mod2 holocaust\n\n# a comment\npeople mod1 fascism\nDOWN mod1\n', 'acc.txt')
        self.assertEqual(bad, ['acc.txt:5: write "ACCENT part frame"'])
        problems, _ = accent_problems(plan(), {}, claims)
        self.assertEqual(problems, ['acc.txt:4: fascism (mod1) claims "PEOPLE", claimed first for holocaust (mod2) at line 1'])

    def test_a_frames_later_claim_releases_its_earlier_one(self):
        claims, _ = parse_claims('BALLOT ind2 a\nVOTE ind2 a\nBALLOT mod1 b\n', 'acc.txt')
        self.assertEqual(accent_problems(plan(), {}, claims), ([], []))

    def test_a_claim_clashing_with_a_written_frame_or_the_plan(self):
        claims, _ = parse_claims('DEAD x a\nOPEN x b\nOPEN x c\n', 'acc.txt')
        problems, _ = accent_problems(plan({'c': {'accent': 'OPEN.'}}), self.written(z='DEAD.', a='DEAD'), claims)
        # a's own written accent is no clash; z's is.
        self.assertEqual(problems, ['acc.txt:1: a (x) claims "DEAD", already frames/z\'s',
                                    'acc.txt:2: b (x) claims "OPEN", already planned for c'])


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

    def test_leaves_out_an_unfinished_draft_and_says_so(self):
        # sprint 051: a borrowed owner's draft straight from `lookup --write-draft`, its kind and
        # description still empty, failed every borrower's copy on the registry's schema.
        root = tempfile.mkdtemp()
        try:
            a, names = os.path.join(root, 'a'), os.path.join(root, 'names')
            for d in (a, names):
                os.makedirs(d)
            with open(os.path.join(a, 'half.json'), 'w') as fh:
                json.dump({'id': 'half', 'kind': '', 'description': ''}, fh)
            with open(os.path.join(a, 'done.json'), 'w') as fh:
                json.dump({'id': 'done', 'kind': 'idea', 'description': 'A thing.'}, fh)
            out = merge_drafts([a], names)
            self.assertEqual(os.listdir(names), ['done.json'])
            self.assertEqual(len(out), 1)
            self.assertIn('half.json', out[0])
            self.assertIn('unfinished', out[0])
        finally:
            shutil.rmtree(root)

    def test_many_unfinished_drafts_in_one_directory_are_one_line(self):
        # sprint 055: an owner's 37 unfinished drafts printed 37 lines, burying a borrower's own.
        root = tempfile.mkdtemp()
        try:
            a, names = os.path.join(root, 'a'), os.path.join(root, 'names')
            for d in (a, names):
                os.makedirs(d)
            for i in range(5):
                with open(os.path.join(a, f'half{i}.json'), 'w') as fh:
                    json.dump({'id': f'half{i}', 'kind': '', 'description': ''}, fh)
            out = merge_drafts([a], names)
            self.assertEqual(len(out), 1)
            self.assertIn('5 unfinished', out[0])
            self.assertIn('half0.json', out[0])
            self.assertIn('2 more', out[0])
        finally:
            shutil.rmtree(root)

    def test_a_missing_directory_is_said_not_a_crash(self):
        # sprint 051: an owner's drafts directory that did not exist yet raised FileNotFoundError.
        root = tempfile.mkdtemp()
        try:
            names = os.path.join(root, 'names')
            os.makedirs(names)
            out = merge_drafts([os.path.join(root, 'nobody')], names)
            self.assertEqual(len(out), 1)
            self.assertIn('no drafts directory', out[0])
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
        _, spine, said = self.complete()
        self.assertEqual(spine, ['a', 'c'])
        self.assertIn('holds 2 of 3 planned frames', said)  # the copy's count, not the live tree's (korg 3554)

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
