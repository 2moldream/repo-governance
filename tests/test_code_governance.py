import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CodeGovernanceTests(unittest.TestCase):
    def test_skill_routes_config_and_architecture_changes(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        reference = (ROOT / "references/code-governance.md").read_text(encoding="utf-8")
        self.assertIn("code-governance.md", skill)
        self.assertIn("配置、模块边界、依赖方向", skill)
        self.assertIn("配置与架构影响", skill)
        self.assertIn("屎山 ratchet", skill)
        self.assertIn("配置治理", reference)
        self.assertIn("架构与依赖治理", reference)
        self.assertIn("屎山代码治理", reference)

    def test_configuration_has_single_source_priority_and_safe_defaults(self):
        text = (ROOT / "references/code-governance.md").read_text(encoding="utf-8")
        for needle in (
            "唯一事实源",
            "覆盖优先级",
            "安全默认值",
            "提交 example",
            "secret manager",
            "不得硬编码在业务分支中",
            "缺配置不得变成无限制、无等待或自动通过",
        ):
            self.assertIn(needle, text)

    def test_architecture_direction_and_external_io_are_bounded(self):
        text = (ROOT / "references/code-governance.md").read_text(encoding="utf-8")
        for needle in (
            "Interface / Entry",
            "Application / Use Case",
            "Domain / Policy",
            "Infrastructure / Adapter",
            "禁止反向导入",
            "领域层不得直接发起外部 IO",
            "adapter/gateway",
            "禁止循环 import",
            "只读状态并呈现结果",
        ):
            self.assertIn(needle, text)

    def test_monolith_uses_baseline_and_double_ratchet(self):
        text = (ROOT / "references/code-governance.md").read_text(encoding="utf-8")
        for needle in (
            "屎山风险",
            "不可变基线",
            "单个屎山对象规模或复杂度不得上升",
            "聚合规模不得上升",
            "一个缩小、另一个膨胀",
            "禁止继续新增业务逻辑",
            "薄 adapter",
            "characterization test",
            "不设置跨语言统一行数阈值",
        ):
            self.assertIn(needle, text)

    def test_compatibility_layers_require_exit_conditions(self):
        text = (ROOT / "references/code-governance.md").read_text(encoding="utf-8")
        for needle in (
            "兼容层与影子实现",
            "删除条件",
            "承接工单",
            "影子包",
            "动态 import 别名",
            "没有删除条件的兼容层",
        ):
            self.assertIn(needle, text)

    def test_workorder_and_agents_templates_require_impact_fields(self):
        agents = (ROOT / "assets/templates/AGENTS.template.md").read_text(encoding="utf-8")
        workorder = (ROOT / "assets/templates/WO.template.md").read_text(encoding="utf-8")
        worker_prompt = (ROOT / "assets/templates/worker-prompt.template.md").read_text(encoding="utf-8")
        self.assertIn("配置治理", agents)
        self.assertIn("架构与代码结构", agents)
        self.assertIn("屎山内禁止新增业务逻辑", agents)
        self.assertIn("架构影响：", workorder)
        self.assertIn("配置影响：", workorder)
        self.assertIn("{{architecture_boundary}}", worker_prompt)
        self.assertIn("{{configuration_boundary}}", worker_prompt)
        self.assertIn("Architecture impact.", worker_prompt)
        self.assertIn("Configuration impact.", worker_prompt)

    def test_diagnosis_covers_config_architecture_and_monolith(self):
        text = (ROOT / "references/diagnose.md").read_text(encoding="utf-8")
        for needle in (
            "配置治理",
            "代码结构",
            "屎山风险",
            "配置唯一事实源",
            "架构分层",
            "屎山识别",
            "兼容层",
        ):
            self.assertIn(needle, text)

    def test_code_rules_are_not_source_specific(self):
        paths = [
            ROOT / "references/code-governance.md",
            ROOT / "assets/templates/AGENTS.template.md",
            ROOT / "assets/templates/WO.template.md",
        ]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for forbidden in (
                "来源项目",
                "来源项目",
                "performance.env",
                "quality_audit_cli.py",
                "Tool/Model Gateway",
                "44,611",
                "来源数据集路径",
            ):
                self.assertNotIn(forbidden, text, f"{path.name} contains {forbidden}")

    def test_version_is_bumped_for_skill_behavior_change(self):
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.5.0")


if __name__ == "__main__":
    unittest.main()
