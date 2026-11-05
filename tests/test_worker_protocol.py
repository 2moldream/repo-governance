import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WorkerProtocolTests(unittest.TestCase):
    def test_protocol_is_disabled_by_default_and_requires_user_request(self):
        text = (ROOT / "references/worker-protocol.md").read_text(encoding="utf-8")
        self.assertIn("默认关闭", text)
        self.assertIn("用户明确要求并行", text)
        self.assertIn("文件范围不重叠", text)

    def test_protocol_preserves_registry_and_scope_boundaries(self):
        text = (ROOT / "references/worker-protocol.md").read_text(encoding="utf-8")
        self.assertIn("主会话", text)
        self.assertIn("自行取号", text)
        self.assertIn("修改共享 registry", text)
        self.assertIn("扩大允许修改范围", text)
        self.assertIn("合并", text)

    def test_worker_prompt_has_complete_dispatch_contract(self):
        text = (ROOT / "assets/templates/worker-prompt.template.md").read_text(encoding="utf-8")
        for needle in (
            "{{workorder_id}}",
            "{{todo_id}}",
            "{{repository_or_worktree}}",
            "{{branch}}",
            "{{base}}",
            "{{allowed_files}}",
            "{{forbidden_changes}}",
            "{{acceptance_commands}}",
            "{{output_location}}",
            "Stop Conditions",
        ):
            self.assertIn(needle, text)

    def test_parallel_work_is_an_obligation_without_enabling_parallel_by_default(self):
        text = (ROOT / "references/worker-protocol.md").read_text(encoding="utf-8")
        bootstrap = (ROOT / "references/bootstrap.md").read_text(encoding="utf-8")
        for needle in (
            "多工单并行开发义务",
            "效果优先于并行效率",
            "判定核心、证据链、发布路径上的工单该串行就串行",
            "文件面交叠",
            "队列不空转",
            "队列空 + 阻塞原因",
            "触发条件自动重估",
            "条件已经满足而无人回头检查，视同治理违规",
            "子代理执行与主会话让位",
            "主会话负责范围裁决、发号、监控、证据核对和收口",
            "并行开发、串行合并",
            "热点文件同一时间只允许一个写入方",
            "在途工单上限",
        ):
            self.assertIn(needle, text)
        self.assertIn("并行义务不等于默认并行执行", text)
        self.assertIn("多工单并行义务（默认串行 + 义务条款）", bootstrap)

    def test_protocol_requires_real_model_executors(self):
        text = (ROOT / "references/worker-protocol.md").read_text(encoding="utf-8")
        self.assertIn("真实模型执行体", text)
        self.assertIn("后台进程", text)
        self.assertIn("executor_id", text)
        self.assertIn("实际模型", text)
        self.assertIn("收口证据", text)


if __name__ == "__main__":
    unittest.main()
