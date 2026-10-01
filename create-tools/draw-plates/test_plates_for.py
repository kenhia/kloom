"""plates_for.py: one collector for every subject (sprint 027). Run by `just check`."""
import contextlib, io, os, shutil, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plates_for  # noqa: E402

GOOD = 'PLATES = {"alpha": lambda: "a", "beta": lambda: "b"}\n'


class PlatesFor(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        # A test subject's modules, named so they cannot shadow a real one on sys.path.
        self.write('zz_test_good.py', GOOD)
        self.write('zz_test_other.py', 'PLATES = {}\nPLATES["gamma"] = lambda: "g"\n')

    def tearDown(self):
        for m in [m for m in sys.modules if m.startswith('zz_test')]:
            del sys.modules[m]
        if self.dir in sys.path:
            sys.path.remove(self.dir)
        shutil.rmtree(self.dir)

    def write(self, name, text):
        with open(os.path.join(self.dir, name), 'w') as fh:
            fh.write(text)

    def test_reads_which_module_draws_each_frame_without_importing(self):
        self.write('zz_test_raises.py', 'raise RuntimeError("half written")\nPLATES = {"delta": None}\n')
        found, broken = plates_for.modules('zz-test', self.dir)
        self.assertEqual(found['zz_test_good'], ['alpha', 'beta'])
        self.assertEqual(found['zz_test_raises'], ['delta'])
        self.assertEqual(broken, {})
        self.assertNotIn('zz_test_raises', sys.modules)

    def test_imports_only_the_modules_of_the_frames_named(self):
        self.write('zz_test_raises.py', 'raise RuntimeError("half written")\nPLATES = {"delta": None}\n')
        self.write('zz_test_syntax.py', 'PLATES = {"eps": \n')
        drawn, broken = plates_for.plates('zz-test', ['alpha', 'gamma'], self.dir)
        self.assertEqual(sorted(drawn), ['alpha', 'gamma'])
        self.assertEqual(broken, {})
        self.assertNotIn('zz_test_raises', sys.modules)

    def test_names_and_skips_a_module_that_fails_to_import(self):
        self.write('zz_test_raises.py', 'raise RuntimeError("half written")\nPLATES = {"delta": None}\n')
        drawn, broken = plates_for.plates('zz-test', ['alpha', 'delta'], self.dir)
        self.assertEqual(sorted(drawn), ['alpha'])
        self.assertIn('half written', broken['zz_test_raises'])

    def test_all_reports_a_module_that_does_not_parse(self):
        self.write('zz_test_syntax.py', 'PLATES = {"eps": \n')
        drawn, broken = plates_for.plates('zz-test', None, self.dir)
        self.assertEqual(sorted(drawn), ['alpha', 'beta', 'gamma'])
        self.assertIn('SyntaxError', broken['zz_test_syntax'])

    def test_refuses_a_frame_two_modules_draw(self):
        self.write('zz_test_dup.py', 'PLATES = {"alpha": None}\n')
        with self.assertRaises(SystemExit) as e:
            plates_for.plates('zz-test', ['beta'], self.dir)
        self.assertIn('alpha is drawn by both', str(e.exception))

    def test_refuses_a_frame_no_module_draws(self):
        with self.assertRaises(SystemExit) as e:
            plates_for.plates('zz-test', ['nope'], self.dir)
        self.assertIn('no plate for nope', str(e.exception))

    def test_refuses_a_bare_run(self):
        with contextlib.redirect_stderr(io.StringIO()) as err, self.assertRaises(SystemExit) as e:
            plates_for.main(['physics'])
        self.assertEqual(e.exception.code, 2)
        self.assertIn('--all', err.getvalue())


if __name__ == '__main__':
    unittest.main()
