import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
import os
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validation', ROOT / 'scripts/validate.py')
validation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validation)

class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.previous = Path.cwd()
        os.chdir(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.email', 'test@example.com')
        self.git('config', 'user.name', 'Test')
        self.write('scripts/existing.py', '# trusted')
        self.write('Practical-01/Student/old.py', 'print(1)')
        self.git('add', '.')
        self.git('commit', '-qm', 'base')
        self.base = self.git('rev-parse', 'HEAD').strip()
        self.config = yaml.safe_load((ROOT / 'submission-config.yml').read_text())

    def tearDown(self):
        os.chdir(self.previous)
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.check_output(['git', *args], text=True)

    def write(self, path, data):
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data)

    def check(self):
        self.git('add', '-A')
        self.git('commit', '--allow-empty', '-qm', 'submission')
        return validation.validate(self.base, 'HEAD', self.config)[1]

    def test_valid_submission_with_spaces(self):
        self.write('Practical-01/Student Name/new file.cpp', 'int main() {}')
        self.assertEqual(self.check(), [])

    def test_practical_range(self):
        self.write('Practical-11/Student/new.py', '')
        self.assertTrue(self.check())

    def test_protected_deletion(self):
        Path('scripts/existing.py').unlink()
        self.assertTrue(any('Protected' in x for x in self.check()))

    def test_protected_rename(self):
        self.git('mv', 'scripts/existing.py', 'Practical-01/Student/moved.py')
        self.assertTrue(any('Protected' in x for x in self.check()))

    def test_symlink(self):
        Path('Practical-01/Student/link.py').symlink_to('/etc/passwd')
        self.assertTrue(any('regular' in x for x in self.check()))

    def test_empty_diff(self):
        self.assertTrue(self.check())

    def test_file_limit(self):
        self.config['max_file_size_mb'] = 0.000001
        self.write('Practical-01/Student/new.py', '123456')
        self.assertTrue(any('size limit' in x for x in self.check()))

    def test_prohibited_pattern(self):
        self.config['prohibited_patterns'].append('blocked*.py')
        self.write('Practical-01/Student/blocked_file.py', '')
        self.assertTrue(any('Prohibited' in x for x in self.check()))

    def test_source_deletion(self):
        Path('Practical-01/Student/old.py').unlink()
        self.assertEqual(self.check(), [])

    def test_bad_revision_fails_closed(self):
        result = subprocess.run(['python', str(ROOT / 'scripts/validate.py'), 'missing', 'HEAD'], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('STATUS=FAIL', Path('validation_result.txt').read_text())

if __name__ == '__main__':
    unittest.main()
