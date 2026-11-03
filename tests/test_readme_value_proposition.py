import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReadmeValuePropositionTests(unittest.TestCase):
    def test_readme_leads_with_pain_points_and_value(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("它在 Codex 中解决什么", text)
        self.assertIn("AI 写代码很快", text)
        self.assertIn("并行会话、无边界修改、漂移文档和屎山代码拖垮", text)
        self.assertIn("目标仓库规则优先", text)
        self.assertIn("explicit-only", text)
        self.assertIn("fail-closed", text)
        self.assertIn("使用 $repo-governance", text)

    def test_readme_covers_high_value_capabilities(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for needle in (
            "共享 WO/TD registry",
            "原子发号",
            "范围内文件",
            "验收命令",
            "事实源矩阵",
            "配置分类",
            "屎山识别",
            "基线 ratchet",
            "关键文档变更前置评审",
            "执行体防伪",
        ):
            self.assertIn(needle, text)

    def test_readme_uses_user_language_shit_mountain(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("屎山代码", text)
        self.assertNotIn("巨石", text)

    def test_ui_metadata_is_compelling_and_explicit_only(self):
        metadata = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("Stop chaotic AI repo changes and shit mountains", metadata)
        self.assertIn("使用 $repo-governance", metadata)
        self.assertIn("allow_implicit_invocation: false", metadata)


if __name__ == "__main__":
    unittest.main()
