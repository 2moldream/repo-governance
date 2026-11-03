import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ExplicitInvocationTests(unittest.TestCase):
    def test_skill_is_explicit_only(self):
        policy = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: false", policy)
        self.assertIn("$repo-governance", policy)

    def test_description_excludes_ordinary_development(self):
        description = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Explicit-only", description)
        self.assertIn("ordinary development tasks", description)
        self.assertIn("legacy-repository diagnosis", description)
        self.assertIn("shit-mountain ratchets", description)

    def test_version_records_policy_change(self):
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.4.0")


if __name__ == "__main__":
    unittest.main()
