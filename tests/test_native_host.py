import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('setup', Path(__file__).resolve().parents[1] / 'scripts/configure_native_host.py')
setup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(setup)
ID = 'aomjjhallfgjeglblehebfpbcfeobpgk'


class NativeHostTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        executable = root / 'helper'
        executable.touch()
        self.path = root / 'host.json'
        self.data = dict(name=setup.HOST, type='stdio', path=str(executable), allowed_origins=['chrome-extension://' + 'b' * 32 + '/'], extra='preserve')
        self.write()

    def write(self):
        self.path.write_text(json.dumps(self.data))

    def test_public_key_id(self):
        manifest = json.loads((setup.ROOT / 'manifest.json').read_text())
        self.assertEqual(setup.extension_id(manifest), ID)

    def test_check_does_not_write(self):
        original = self.path.read_bytes()
        self.assertTrue(setup.configure(self.path, ID).startswith('MISSING:'))
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(self.path.parent.glob('*.backup-*')), [])

    def test_apply_preserves_and_backs_up_and_is_idempotent(self):
        original = self.path.read_bytes()
        setup.configure(self.path, ID, True)
        result = json.loads(self.path.read_text())
        self.assertEqual(result['extra'], 'preserve')
        self.assertEqual(result['allowed_origins'][0], self.data['allowed_origins'][0])
        self.assertEqual(result['allowed_origins'][-1], f'chrome-extension://{ID}/')
        backups = list(self.path.parent.glob('*.backup-*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), original)
        self.assertTrue(setup.configure(self.path, ID, True).startswith('OK:'))
        self.assertEqual(list(self.path.parent.glob('*.backup-*')), backups)

    def test_wrong_host_rejected(self):
        self.data['name'] = 'com.1password.1password7'
        self.write()
        with self.assertRaises(ValueError): setup.configure(self.path, ID, True)

    def test_missing_executable_rejected(self):
        self.data['path'] += '-missing'
        self.write()
        with self.assertRaises(ValueError): setup.configure(self.path, ID, True)

    def test_invalid_id_rejected(self):
        with self.assertRaises(ValueError): setup.configure(self.path, '../invalid', True)

    def test_invalid_origins_rejected(self):
        self.data['allowed_origins'] = 'not an array'
        self.write()
        with self.assertRaises(ValueError): setup.configure(self.path, ID, True)


if __name__ == '__main__': unittest.main()
