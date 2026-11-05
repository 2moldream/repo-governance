import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReadmeValuePropositionTests(unittest.TestCase):
    def test_readme_leads_with_concrete_repository_problems(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Codex 和 Claude 都能用", text)
        self.assertIn("它在 Codex / Claude 中解决什么", text)
        for needle in (
            "撞工单号、抢同一分支",
            "改出一堆范围外文件",
            "验收靠嘴说",
            "目标写成现状",
            "旧实现一直删不掉",
            "一个模型的意见就直接定了",
        ):
            self.assertIn(needle, text)
        self.assertIn("目标仓库规则优先", text)
        self.assertIn("explicit-only", text)
        self.assertIn("缺证据不关闭", text)
        self.assertIn("使用 $repo-governance", text)

    def test_readme_describes_mechanisms_instead_of_slogans(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for needle in (
            "registry 加文件锁",
            "工单列允许修改的文件",
            "L0/L1/L2",
            "改等级字段不算验收",
            "L0 发现漂移自动升 L1",
            "预期结果不进生产输入",
            "旧 outputs 不当新基线",
            "谁干活就按谁的规矩登记",
            "Claude 子代理不转 worker 兜底",
            "完成通知和入仓报告",
            "整批按最高验收等级复跑",
            "独立分析（Round 1），再互相挑错（Round 2）",
            "吵不出一致就用保守方案",
            "删除条件和承接工单",
            "评审提交先于实现提交",
        ):
            self.assertIn(needle, text)
        for forbidden in ("赋能", "抓手", "闭环", "一站式", "全方位", "极致", "## 一句话"):
            self.assertNotIn(forbidden, text)

    def test_readme_gives_both_hosts_explicit_usage(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Codex 中显式使用 `$repo-governance`", text)
        self.assertIn("Claude 中让宿主助手显式调用已安装的 repo-governance skill", text)
        self.assertIn("两边都先读目标仓库规则", text)
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Explicit-only repository governance for Codex and Claude", skill)
        self.assertIn("never load it for ordinary development tasks", skill)

    def test_readme_uses_user_language_shit_mountain(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("屎山迁移", text)
        self.assertNotIn("巨石", text)

    def test_ui_metadata_is_compelling_and_explicit_only(self):
        metadata = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("Stop chaotic AI repo changes and shit mountains", metadata)
        self.assertIn("使用 $repo-governance", metadata)
        self.assertIn("allow_implicit_invocation: false", metadata)


if __name__ == "__main__":
    unittest.main()
