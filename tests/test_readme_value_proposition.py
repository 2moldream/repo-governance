import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReadmeValuePropositionTests(unittest.TestCase):
    def test_readme_leads_with_pain_points_and_value(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("给 Codex 与 Claude 加一层可复用的仓库治理能力", text)
        self.assertIn("它在 Codex / Claude 中解决什么", text)
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
            "分级验收",
            "L0/L1/L2 三级 + 漂移自动升级",
            "禁止改字段冒充已验收",
            "证据边界",
            "输入/预期/产物三目录隔离",
            "预期结果永不进生产输入",
            "双宿主执行体",
            "Codex（native child / worker / fallback）与 Claude（子代理）双协议",
            "谁执行就按谁的口径登记，不冒充",
            "Claude 路径无 fallback",
            "Codex worker 与 Claude subagent 各记各的、互相冒充",
            "关闭须双证据",
        ):
            self.assertIn(needle, text)

    def test_readme_gives_both_hosts_explicit_usage(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Codex 中显式使用 `$repo-governance`", text)
        self.assertIn("Claude 中让宿主助手显式调用已安装的 repo-governance skill", text)
        self.assertIn("不因宿主不同改变目标仓库政策", text)
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("turns Codex and Claude into safe long-term repository collaborators", skill)
        self.assertIn("Explicit-only", skill)
        self.assertIn("Never load it for ordinary development tasks", skill)

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
