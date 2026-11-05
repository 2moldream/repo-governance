import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets/templates"


class L1TemplateTests(unittest.TestCase):
    def test_agents_template_contains_l1_hard_gates(self):
        text = (TEMPLATES / "AGENTS.template.md").read_text(encoding="utf-8")
        for needle in (
            "先方案后开发",
            "根因",
            "WO-xxx",
            "wo/<编号>-<slug>",
            "范围内文件",
            "验收",
            "fail-closed",
            "范围外",
        ):
            self.assertIn(needle, text)

    def test_agents_template_contains_new_l1_governance_rules(self):
        text = (TEMPLATES / "AGENTS.template.md").read_text(encoding="utf-8")
        for needle in (
            "## 8. 验收分级",
            "## 9. 证据目录边界",
            "## 10. 并行义务",
            "验收等级与能力分层 L1-L4 同名不同义",
            "预期结果只用于验收对照",
            "队列空 + 阻塞原因",
            "design-delta 自动台账工具",
            "接口地图自动检查",
        ):
            self.assertIn(needle, text)

    def test_docs_template_declares_fact_sources_and_lifecycle(self):
        text = (TEMPLATES / "docs-README.template.md").read_text(encoding="utf-8")
        self.assertIn("事实源", text)
        self.assertIn("生命周期", text)
        self.assertIn("当前实现行为", text)
        self.assertIn("历史解释", text)
        self.assertIn("目标设计", text)

    def test_workorder_template_is_a_complete_change_contract(self):
        text = (TEMPLATES / "WO.template.md").read_text(encoding="utf-8")
        for needle in (
            "背景",
            "根因",
            "范围内文件",
            "行为变化",
            "文档影响",
            "验收",
            "发现",
            "实施与验收记录",
            "回退方案",
            "验收等级：{{acceptance_tier}}",
            "详设影响：{{yes_or_no_with_reason}}",
            "design_delta_ref：{{ref_or_not_applicable}}",
            "证据清单：{{evidence_manifest}}",
            "close_method：{{closure_method}}",
        ):
            self.assertIn(needle, text)

    def test_todo_template_never_closes_an_item_without_evidence(self):
        text = (TEMPLATES / "todo.template.md").read_text(encoding="utf-8")
        self.assertIn("开放事项", text)
        self.assertIn("open", text)
        self.assertIn("closed", text)
        self.assertIn("验收证据", text)
        self.assertIn("缺证据", text)

    def test_templates_use_explicit_replacement_tokens(self):
        for path in TEMPLATES.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("TBD", text, f"{path.name} contains TBD")
            self.assertNotIn("TODO", text, f"{path.name} contains TODO")
            self.assertNotIn("待补", text, f"{path.name} contains 待补")


if __name__ == "__main__":
    unittest.main()
