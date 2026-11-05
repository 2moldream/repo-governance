import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references/acceptance-governance.md"


class AcceptanceGovernanceTests(unittest.TestCase):
    def test_three_acceptance_tiers_have_distinct_evidence_requirements(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for needle in (
            "L0：零行为变化",
            "L1：默认行为变化",
            "L2：关键路径",
            "生成视图一致性检查",
            "全量测试",
            "既有快照零漂移",
            "相关回归测试",
            "fast gate",
            "代表性数据集或 live E2E",
            "双模型完整圆桌",
            "full gate",
            "发布证据",
        ):
            self.assertIn(needle, text)

    def test_drift_and_repeated_misclassification_force_escalation(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for needle in (
            "发现任何行为漂移",
            "自动升级为 L1",
            "触及关键路径，则升级为 L2",
            "同一工单累计发生两次验收等级误判",
            "至少以 L1 起报",
            "补齐新等级的全部证据",
        ):
            self.assertIn(needle, text)

    def test_acceptance_tiers_are_not_capability_levels(self):
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("验收等级 L0/L1/L2 与能力分层 L1-L4 同名不同义", text)
        self.assertIn("前者描述单张工单的验证深度", text)
        self.assertIn("后者描述仓库启用的治理能力", text)

    def test_tier_fields_cannot_substitute_for_acceptance_evidence(self):
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("禁止只修改验收等级字段", text)
        self.assertIn("冒充已完成验收", text)
        self.assertIn("字段变化不是证据", text)
        self.assertIn("缺命令、缺输出、缺材料或结果失败时", text)

    def test_templates_and_bootstrap_carry_the_acceptance_contract(self):
        workorder = (ROOT / "assets/templates/WO.template.md").read_text(encoding="utf-8")
        agents = (ROOT / "assets/templates/AGENTS.template.md").read_text(encoding="utf-8")
        bootstrap = (ROOT / "references/bootstrap.md").read_text(encoding="utf-8")
        self.assertIn("验收等级：{{acceptance_tier}}", workorder)
        self.assertIn("验收分级", agents)
        self.assertIn("不得只改验收等级字段冒充已验收", agents)
        self.assertIn("验收等级声明（默认 L1）", bootstrap)


if __name__ == "__main__":
    unittest.main()
