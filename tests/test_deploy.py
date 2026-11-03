import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/deploy.py"


class DeployTests(unittest.TestCase):
    def deploy(self, destination: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--destination", str(destination), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_symlink_install_points_to_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "skills" / "repo-governance"
            result = self.deploy(destination)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["mode"], "symlink")
            self.assertTrue(destination.is_symlink())
            self.assertEqual(destination.resolve(), ROOT.resolve())
            self.assertTrue((destination / "SKILL.md").is_file())

    def test_existing_destination_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "repo-governance"
            destination.write_text("existing", encoding="utf-8")
            result = self.deploy(destination)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing to overwrite", result.stderr)
            self.assertEqual(destination.read_text(encoding="utf-8"), "existing")

    def test_copy_mode_excludes_git_and_caches(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "repo-governance"
            result = self.deploy(destination, "--mode", "copy")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((destination / "SKILL.md").is_file())
            self.assertFalse((destination / ".git").exists())
            self.assertFalse((destination / "tests/__pycache__").exists())

    def test_dry_run_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "repo-governance"
            result = self.deploy(destination, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(os.path.lexists(destination))


if __name__ == "__main__":
    unittest.main()
