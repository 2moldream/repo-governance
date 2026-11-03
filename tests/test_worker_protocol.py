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

    def test_protocol_requires_real_model_executors(self):
        text = (ROOT / "references/worker-protocol.md").read_text(encoding="utf-8")
        self.assertIn("真实模型执行体", text)
        self.assertIn("后台进程", text)
        self.assertIn("executor_id", text)
        self.assertIn("实际模型", text)
        self.assertIn("收口证据", text)


if __name__ == "__main__":
    unittest.main()
