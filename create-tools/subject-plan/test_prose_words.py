"""prose_words.py: what it counts, and where it reads from (sprint 027). Run by `just check`."""
import os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from prose_words import prose_words  # noqa: E402

READING = '## A heading\n\nOne two [three](kloom:e/three).\n\n| a | table |\n\n![alt text here](x.png)\n'


class Count(unittest.TestCase):
    def test_counts_prose_only(self):
        self.assertEqual(prose_words(READING), 3)


class Paths(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, 'copy', 'f'))
        with open(os.path.join(self.dir, 'copy', 'f', 'reading.md'), 'w') as fh:
            fh.write(READING)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def run_on(self, *paths):
        return subprocess.run([sys.executable, os.path.join(HERE, 'prose_words.py'), *paths, '--min', '1'],
                              capture_output=True, text=True)

    def test_reads_a_directory_of_frames_without_a_subject(self):
        r = self.run_on(os.path.join(self.dir, 'copy'))
        self.assertEqual((r.returncode, r.stdout), (0, '    3  f\n'))

    def test_reads_a_frame_or_a_reading_file(self):
        r = self.run_on(os.path.join(self.dir, 'copy', 'f'), os.path.join(self.dir, 'copy', 'f', 'reading.md'))
        self.assertEqual(r.stdout, '    3  f\n    3  f\n')

    def test_says_when_there_is_nothing_to_read(self):
        r = self.run_on(self.dir + '/nowhere')
        self.assertEqual(r.returncode, 1)
        self.assertIn('no such file', r.stderr)


if __name__ == '__main__':
    unittest.main()
