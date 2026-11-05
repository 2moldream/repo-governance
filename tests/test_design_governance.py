import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references/design-governance.md"


class DesignGovernanceTests(unittest.TestCase):
    def test_detailed_design_impact_requires_a_reason(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for needle in (
            "详设影响：有 / 无 + 理由",
            "高风险路径时，不得声明 `详设影响=无`",
            "只写“无影响”不算理由",
            "design_delta_ref",
        ):
            self.assertIn(needle, text)

    def test_design_delta_is_append_only_and_traceable(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for needle in (
            "append-only",
            "不得修改、删除、压缩或重排历史",
            "纠错、撤回或替代必须新增 entry",
            "WO/TD：",
            "影响类型：",
            "域：",
            "设计章节：",
            "code_map_ref：",
            "验收引用：",
            "决议引用：",
        ):
            self.assertIn(needle, text)

    def test_service_interface_map_fails_closed(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for needle in (
            "服务接口地图",
            "生成视图 stale",
            "外键缺失",
            "接口治理 finding 未解决",
            "全部 fail-closed",
            "检查工具不可用、输入不完整或地图未生成时",
            "不默认通过",
        ):
            self.assertIn(needle, text)

    def test_declaration_and_automation_have_separate_defaults(self):
        text = REFERENCE.read_text(encoding="utf-8")
        bootstrap = (ROOT / "references/bootstrap.md").read_text(encoding="utf-8")
        self.assertIn("详设影响声明与必要的增量声明义务随 L1 基线启用", text)
        self.assertIn("自动台账、生成视图和接口检查工具默认关闭", text)
        self.assertIn("design-delta 自动台账工具", bootstrap)
        self.assertIn("接口地图自动检查", bootstrap)

    def test_workorder_template_requires_design_and_evidence_references(self):
        workorder = (ROOT / "assets/templates/WO.template.md").read_text(encoding="utf-8")
        self.assertIn("详设影响：{{yes_or_no_with_reason}}", workorder)
        self.assertIn("design_delta_ref：{{ref_or_not_applicable}}", workorder)
        self.assertIn("证据清单：{{evidence_manifest}}", workorder)


if __name__ == "__main__":
    unittest.main()
