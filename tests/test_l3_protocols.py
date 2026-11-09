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

    def test_shared_workspace_protection_is_unconditional(self):
        text = (ROOT / "references/worktree-protocol.md").read_text(encoding="utf-8")
        for needle in (
            "共享工作区保护",
            "不受 L3 开关限制",
            "共享基线",
            "零操作",
            "未跟踪文件",
            "只登记报告",
            "integration worktree",
            "不得借主会话、子代理、worker 或任何工具间接绕过",
        ):
            self.assertIn(needle, text)

    def test_merge_protocol_fails_closed_before_merge(self):
        text = (ROOT / "references/merge-protocol.md").read_text(encoding="utf-8")
        self.assertIn("worker 不得合并", text)
        self.assertIn("范围内文件", text)
        self.assertIn("无未提交文件", text)
        self.assertIn("实施与验收记录", text)
        self.assertIn("fail-closed", text)
        self.assertIn("依赖 WO", text)

    def test_merge_batch_window_revalidates_at_highest_tier(self):
        text = (ROOT / "references/merge-protocol.md").read_text(encoding="utf-8")
        for needle in (
            "合并攒批窗口",
            "同族工单必须串行合并",
            "异族工单只有允许修改文件不重叠",
            "事实源、配置、生成视图和行为语义均无冲突",
            "每批按其中最高验收等级复跑验收",
            "出现冲突、非预期漂移",
            "立即停止攒批",
            "重新执行整批复验",
        ):
            self.assertIn(needle, text)

    def test_stable_main_records_baseline_and_rollback_point(self):
        text = (ROOT / "references/merge-protocol.md").read_text(encoding="utf-8")
        self.assertIn("stable main 禁止 force push", text)
        self.assertIn("当前 baseline commit", text)
        self.assertIn("可执行回滚点", text)

    def test_merge_conflict_preserves_workspace(self):
        text = (ROOT / "references/merge-protocol.md").read_text(encoding="utf-8")
        self.assertIn("保留冲突现场", text)
        self.assertIn("破坏性 reset", text)
        self.assertIn("新增修复 WO", text)


if __name__ == "__main__":
    unittest.main()
