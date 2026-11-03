import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocumentGovernanceTests(unittest.TestCase):
    def test_l4_is_opt_in(self):
        text = (ROOT / "references/document-governance.md").read_text(encoding="utf-8")
        self.assertIn("默认关闭", text)
        self.assertIn("用户确认", text)
        self.assertIn("先只读盘点", text)
        self.assertIn("不得为了 L4 直接移动", text)

    def test_fact_sources_are_domain_specific(self):
        text = (ROOT / "references/document-governance.md").read_text(encoding="utf-8")
        for needle in (
            "事实源矩阵",
            "当前实现行为",
            "目标设计",
            "开放事项",
            "发布行为",
            "历史解释",
            "事实：",
            "约束：",
            "偏差：",
        ):
            self.assertIn(needle, text)

    def test_lifecycle_and_target_current_separation_are_required(self):
        text = (ROOT / "references/document-governance.md").read_text(encoding="utf-8")
        for needle in (
            "draft -> active -> superseded -> historical",
            "目标不得证明已落地",
            "superseded",
            "historical",
        ):
            self.assertIn(needle, text)

    def test_heavy_extensions_and_release_checks_have_boundaries(self):
        text = (ROOT / "references/document-governance.md").read_text(encoding="utf-8")
        self.assertIn("document map", text)
        self.assertIn("code map", text)
        self.assertIn("release manifest", text)
        self.assertIn("单独立项", text)
        self.assertIn("文档检查通过不等于", text)


if __name__ == "__main__":
    unittest.main()
