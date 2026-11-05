import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_skill_frontmatter_is_specific_and_non_invasive(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: repo-governance\n", text)
        self.assertIn("description:", text)
        self.assertIn("已有开发约束", text)
        self.assertIn("不得直接覆盖", text)

    def test_existing_constraints_require_read_only_diagnosis_first(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        diagnosis = (ROOT / "references/diagnose.md").read_text(encoding="utf-8")
        for text in (skill, diagnosis):
            self.assertIn("只读诊断", text)
            self.assertIn("用户确认", text)
        self.assertIn("不得直接写入", diagnosis)
        self.assertIn("不得直接覆盖", diagnosis)

    def test_diagnosis_has_stable_categories_and_evidence_contract(self):
        text = (ROOT / "references/diagnose.md").read_text(encoding="utf-8")
        for category in ("一致", "重复", "缺失", "冲突", "仓库专属例外"):
            self.assertIn(category, text)
        for needle in ("规则原文", "位置", "影响", "合并建议", "目标仓库显式规则优先"):
            self.assertIn(needle, text)

    def test_bootstrap_defines_three_repository_states(self):
        text = (ROOT / "references/bootstrap.md").read_text(encoding="utf-8")
        for needle in (
            "已有开发约束",
            "无约束但已有仓库",
            "空仓库或新项目",
            "L1",
            "L2",
            "L3",
            "L4",
            "默认不启动",
        ):
            self.assertIn(needle, text)

    def test_skill_routes_acceptance_design_and_evidence_governance(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for needle in (
            "acceptance-governance.md",
            "验收等级、分级验收、行为漂移或关键路径验收",
            "design-governance.md",
            "详设影响、design-delta、服务接口地图",
            "evidence-governance.md",
            "数据、证据、输入语料、预期结果或运行产物",
            "验收等级不得只改字段冒充已验收",
            "预期结果不得进入生产输入或提示词",
        ):
            self.assertIn(needle, text)

    def test_diagnosis_covers_all_twenty_six_governance_capabilities(self):
        text = (ROOT / "references/diagnose.md").read_text(encoding="utf-8")
        start = text.index("需比较的内置能力：")
        end = text.index("## 3. 证据契约")
        numbered = [line for line in text[start:end].splitlines() if line[:1].isdigit()]
        self.assertEqual(len(numbered), 26)
        for needle in (
            "验收分级政策",
            "design-delta 台账",
            "服务接口地图",
            "数据目录边界",
            "验收分级与漂移升级",
            "详设影响与设计增量台账",
            "数据与证据目录边界",
            "多工单并行义务",
            "合并攒批窗口",
            "子代理圆桌",
        ):
            self.assertIn(needle, text)

    def test_skill_output_does_not_include_source_domain_defaults(self):
        paths = [ROOT / "SKILL.md", *(
            ROOT / "references").glob("*.md"), *(
            ROOT / "assets/templates").glob("*.md")]
        self.assertTrue(paths)
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for forbidden in ("来源项目", "来源项目", "外部执行 CLI", "模型A", "模型B", "来源数据集路径"):
                self.assertNotIn(forbidden, text, f"{path.name} contains {forbidden}")


if __name__ == "__main__":
    unittest.main()
