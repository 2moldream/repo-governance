import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references/evidence-governance.md"


class EvidenceGovernanceTests(unittest.TestCase):
    def test_input_expected_and_output_directories_are_isolated(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for needle in (
            "输入语料",
            "预期结果",
            "运行产物",
            "data/inputs/",
            "data/expected/",
            "outputs/",
            "目录角色不得混用",
        ):
            self.assertIn(needle, text)

    def test_expected_results_never_enter_production_or_prompts(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for needle in (
            "只用于运行完成后的独立验收对照",
            "永不进入生产输入或提示词",
            "不得把预期结果注入",
            "与生产执行路径隔离",
        ):
            self.assertIn(needle, text)

    def test_cross_case_splicing_and_historical_outputs_are_forbidden(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for needle in (
            "禁止跨用例拼接输入、答案、日志或产物",
            "禁止把历史 `outputs/` 或其派生副本作为后续运行输入、独立通过证据或基线",
            "历史输出保留为失败记录或故障调查线索",
            "不覆盖历史失败证据",
        ):
            self.assertIn(needle, text)

    def test_missing_material_fails_closed_without_substitution(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for needle in (
            "缺少输入、预期结果、原始材料、访问权限或必要运行记录时，一律 fail-closed",
            "不造数",
            "不用历史产物替代缺失材料",
            "不跳过缺失项后声称全量通过",
            "保持需确认",
        ):
            self.assertIn(needle, text)

    def test_skill_and_templates_enforce_evidence_boundaries(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        agents = (ROOT / "assets/templates/AGENTS.template.md").read_text(encoding="utf-8")
        self.assertIn("evidence-governance.md", skill)
        self.assertIn("预期结果不得进入生产输入或提示词", skill)
        self.assertIn("证据目录边界", agents)
        self.assertIn("禁止跨用例拼接", agents)
        self.assertIn("禁止把历史 outputs 作为输入、验收证据或新基线", agents)


    def test_frozen_evidence_must_live_inside_repository(self):
        text = (ROOT / "references/evidence-governance.md").read_text(encoding="utf-8")
        for needle in (
            "冻结证据入仓",
            "tests/fixtures/",
            "仓外易失路径",
            "个人目录、临时目录、挂载卷、会话工作区",
            "记录来源、迁移时间和内容校验值",
            "不接受验收时顺手替换",
        ):
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
