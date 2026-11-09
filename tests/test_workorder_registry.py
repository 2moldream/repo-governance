import json
import os
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/workorder_registry.py"


class WorkorderRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "repository"
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "--allow-empty", "-m", "init")

    def tearDown(self):
        self.temporary.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()

    def cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.repo), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_allocate_activate_and_complete_use_placeholder_first(self):
        initialized = self.cli("init")
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        self.assertTrue((self.repo / ".git/repo-governance/workorder-registry.json").exists())

        allocated = self.cli("allocate", "--owner", "main-session", "--slug", "feature")
        self.assertEqual(allocated.returncode, 0, allocated.stderr)
        record = json.loads(allocated.stdout)
        self.assertEqual(record["workorder_id"], "WO-001")
        self.assertEqual(record["todo_id"], "TD-001")
        self.assertEqual(record["status"], "reserved")
        self.assertEqual(record["branch"], "wo/001-feature")
        self.assertIsNone(record["placeholder"])

        placeholder = self.git("rev-parse", "HEAD")
        activated = self.cli(
            "activate",
            "--workorder",
            "WO-001",
            "--placeholder",
            placeholder,
        )
        self.assertEqual(activated.returncode, 0, activated.stderr)
        self.assertEqual(json.loads(activated.stdout)["status"], "active")

        completed = self.cli("complete", "--workorder", "WO-001")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "completed")
        self.assertEqual(self.cli("validate").returncode, 0)

    def test_activation_rejects_missing_placeholder_commit(self):
        self.cli("init")
        self.cli("allocate", "--owner", "main-session", "--slug", "feature")
        result = self.cli(
            "activate",
            "--workorder",
            "WO-001",
            "--placeholder",
            "0" * 40,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("placeholder commit does not exist", result.stderr)

    def test_reserved_record_requires_empty_placeholder(self):
        self.cli("init")
        self.cli("allocate", "--owner", "main-session", "--slug", "feature")
        result = self.cli("validate")
        self.assertEqual(result.returncode, 0, result.stderr)
        registry_path = self.repo / ".git/repo-governance/workorder-registry.json"
        payload = json.loads(registry_path.read_text(encoding="utf-8"))
        payload["records"][0]["placeholder"] = "1" * 40
        registry_path.write_text(json.dumps(payload), encoding="utf-8")
        invalid = self.cli("validate")
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("reserved record must not have a placeholder", invalid.stderr)

    def test_allocate_rejects_invalid_fields_without_write(self):
        self.cli("init")
        missing_worktree = self.repo / "does-not-exist"
        result = self.cli(
            "allocate",
            "--owner",
            "main-session",
            "--slug",
            "feature",
            "--worktree",
            str(missing_worktree),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("worktree does not exist", result.stderr)
        registry_path = self.repo / ".git/repo-governance/workorder-registry.json"
        payload = json.loads(registry_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["sequence"]["workorder"], 0)
        self.assertEqual(payload["records"], [])

    def test_complete_fails_closed_when_active_placeholder_is_missing(self):
        self.cli("init")
        self.cli("allocate", "--owner", "main-session", "--slug", "feature")
        registry_path = self.repo / ".git/repo-governance/workorder-registry.json"
        payload = json.loads(registry_path.read_text(encoding="utf-8"))
        payload["records"][0]["status"] = "active"
        registry_path.write_text(json.dumps(payload), encoding="utf-8")
        result = self.cli("complete", "--workorder", "WO-001")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires a 40-character placeholder commit", result.stderr)

    def test_activation_rejects_integration_branch_override(self):
        self.cli("init")
        self.cli("allocate", "--owner", "main-session", "--slug", "feature")
        placeholder = self.git("rev-parse", "HEAD")
        result = self.cli(
            "activate",
            "--workorder",
            "WO-001",
            "--placeholder",
            placeholder,
            "--branch",
            "main",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("implementation branch cannot be the integration branch", result.stderr)

    def test_concurrent_allocation_does_not_duplicate_ids(self):
        self.cli("init")
        commands = [
            ["allocate", "--owner", f"worker-{index}", "--slug", f"task-{index}"]
            for index in range(8)
        ]
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(lambda command: self.cli(*command), commands))
        self.assertTrue(all(result.returncode == 0 for result in results))
        records = [json.loads(result.stdout) for result in results]
        ids = [record["workorder_id"] for record in records]
        self.assertEqual(len(set(ids)), 8)
        self.assertEqual(set(ids), {f"WO-{number:03d}" for number in range(1, 9)})
        self.assertEqual(self.cli("validate").returncode, 0)

    def test_current_repository_registry_is_valid(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(ROOT), "validate", "--workorder", "WO-003"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


    def test_registry_reference_documents_allocator_worktree_binding(self):
        text = (ROOT / "references/workorder-registry.md").read_text(encoding="utf-8")
        self.assertIn("发号器绑定目标 worktree", text)
        self.assertIn("目标 worktree 根运行", text)
        self.assertIn("受保护的共享工作区", text)
        self.assertIn("直接拒绝", text)
        self.assertIn("worktree-protocol.md", text)


if __name__ == "__main__":
    unittest.main()
