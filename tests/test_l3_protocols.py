import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class L3ProtocolTests(unittest.TestCase):
    def test_worktree_protocol_is_opt_in_and_safe(self):
        text = (ROOT / "references/worktree-protocol.md").read_text(encoding="utf-8")
        self.assertIn("默认关闭", text)
        self.assertIn("用户明确确认", text)
        self.assertIn("每张 WO", text)
        self.assertIn("独立分支", text)
        self.assertIn("git worktree list", text)
        self.assertIn("脏文件", text)
        self.assertIn("不得使用强制删除", text)

    def test_merge_protocol_fails_closed_before_merge(self):
        text = (ROOT / "references/merge-protocol.md").read_text(encoding="utf-8")
        self.assertIn("worker 不得合并", text)
        self.assertIn("范围内文件", text)
        self.assertIn("无未提交文件", text)
        self.assertIn("实施与验收记录", text)
        self.assertIn("fail-closed", text)
        self.assertIn("依赖 WO", text)

    def test_merge_conflict_preserves_workspace(self):
        text = (ROOT / "references/merge-protocol.md").read_text(encoding="utf-8")
        self.assertIn("保留冲突现场", text)
        self.assertIn("破坏性 reset", text)
        self.assertIn("新增修复 WO", text)


if __name__ == "__main__":
    unittest.main()
