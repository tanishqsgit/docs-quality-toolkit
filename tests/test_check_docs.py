import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_docs import check_file

class DocsChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.file = self.root / 'guide.md'

    def check(self, text, **kwargs):
        self.file.write_text(text, encoding='utf-8')
        return check_file(self.file, self.root, **kwargs)

    def test_missing_title(self):
        self.assertEqual(self.check('## Setup')[0]['rule'], 'title')

    def test_valid_metadata(self):
        self.assertEqual(self.check('---\ntitle: Setup\naudience: Users\nstatus: draft\n---\n# Setup', metadata=True), [])

    def test_missing_metadata(self):
        self.assertEqual(len(self.check('# Setup', metadata=True)), 3)

    def test_links_and_fragments(self):
        (self.root / 'another file.md').write_text('# Other')
        self.assertEqual(self.check('# Guide\n[Other](another%20file.md#other) [Web](https://example.com) [Here](#guide)'), [])
        self.assertEqual(self.check('# Guide\n[Other](missing.md)')[0]['line'], 2)

    def test_reference_and_image(self):
        self.assertEqual(len(self.check('# Guide\n![Image](missing.png)\n[ref]: absent.md')), 2)

    def test_fenced_examples_are_ignored(self):
        self.assertEqual(self.check('# Guide\n~~~~md\n[Broken](missing.md)\n~~~\n[Still fenced](missing.md)\n~~~~'), [])

    def test_repository_escape(self):
        self.assertIn('leaves the repository', self.check('# Guide\n[Parent](../outside.md)')[0]['message'])

    def test_terminology_is_advisory(self):
        issues = self.check('# Guide\nWhitelist the domain.\n`whitelist` is a code identifier.', terms={'whitelist': 'allowlist'})
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['severity'], 'warning')

    def test_cli_json_and_exit_codes(self):
        self.file.write_text('# Guide\n[Broken](missing.md)')
        script = str(Path(__file__).resolve().parents[1] / 'check_docs.py')
        result = subprocess.run([sys.executable, script, str(self.root), '--json'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['files_checked'], 1)

    def test_cli_rejects_empty_input(self):
        script = str(Path(__file__).resolve().parents[1] / 'check_docs.py')
        self.assertEqual(subprocess.run([sys.executable, script, str(self.root)], capture_output=True).returncode, 1)

if __name__ == '__main__':
    unittest.main()
