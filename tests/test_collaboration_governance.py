import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CollaborationGovernanceTests(unittest.TestCase):
    def test_executor_policy_is_target_first_with_serial_default(self):
        text = (ROOT / "references/collaboration-governance.md").read_text(encoding="utf-8")
        self.assertIn("目标仓库显式执行体政策优先", text)
        self.assertIn("主会话串行执行", text)
        self.assertIn("main-session-serial", text)
        self.assertIn("invisible-executor", text)
        self.assertIn("visible-subagent", text)
        self.assertIn("independent-worker", text)
        self.assertIn("claude-subagent", text)

    def test_claude_subagent_records_real_identity_and_has_no_fallback(self):
        text = (ROOT / "references/collaboration-governance.md").read_text(encoding="utf-8")
        for needle in (
            "宿主平台子代理工具",
            "真实 task id",
            "实际模型",
            "prompt 摘要",
            "输出文件",
            "worktree",
            "allowed scope",
            "Claude 路径无 fallback",
            "不得降级为 independent worker",
            "不得静默替换执行体类型",
        ):
            self.assertIn(needle, text)

    def test_claude_subagent_close_method_requires_dual_evidence(self):
        text = (ROOT / "references/collaboration-governance.md").read_text(encoding="utf-8")
        workorder = (ROOT / "assets/templates/WO.template.md").read_text(encoding="utf-8")
        for needle in (
            "close_method",
            "双证据",
            "宿主平台完成通知",
            "实施报告已入仓",
            "两者缺一不得关闭",
        ):
            self.assertIn(needle, text)
        self.assertIn("close_method：{{closure_method}}", workorder)

    def test_executor_identity_and_fallback_need_evidence(self):
        text = (ROOT / "references/collaboration-governance.md").read_text(encoding="utf-8")
        for needle in (
            "executor_type",
            "launch_method",
            "executor_id",
            "parent_execution_id",
            "subagent_start_status",
            "subagent_start_error",
            "fallback_reason",
            "一次性兜底",
            "主会话调用参数错误",
        ):
            self.assertIn(needle, text)

    def test_independent_worker_is_not_native_child(self):
        text = (ROOT / "references/collaboration-governance.md").read_text(encoding="utf-8")
        worker = (ROOT / "references/worker-protocol.md").read_text(encoding="utf-8")
        self.assertIn("collaboration.spawn_agent", text)
        self.assertIn("app-server thread/start", text)
        self.assertIn("不得登记为 `visible-subagent`", text)
        self.assertIn("独立会话是 independent worker", worker)

    def test_executors_must_be_closed_or_archived(self):
        text = (ROOT / "references/collaboration-governance.md").read_text(encoding="utf-8")
        for needle in (
            "收口证据",
            "关闭、归档或终止执行体的证据",
            "归档或关闭失败必须登记待确认事项",
            "不得伪造成功",
        ):
            self.assertIn(needle, text)

    def test_fake_executors_are_forbidden(self):
        text = (ROOT / "references/collaboration-governance.md").read_text(encoding="utf-8")
        self.assertIn("shell 后台进程", text)
        self.assertIn("普通命令输出", text)
        self.assertIn("主持人自答", text)
        self.assertIn("不得静默替换执行体类型", text)

    def test_roundtable_requires_two_rounds_and_archive(self):
        text = (ROOT / "references/roundtable-protocol.md").read_text(encoding="utf-8")
        for needle in (
            "Round 1",
            "Round 2",
            "交叉互评",
            "独立评审初稿",
            "fail-closed",
            "归档本次创建的全部可见子智能体或 worker",
            "归档失败时保留 ID",
        ):
            self.assertIn(needle, text)

    def test_subagent_roundtable_requires_independent_committed_reports(self):
        text = (ROOT / "references/roundtable-protocol.md").read_text(encoding="utf-8")
        for needle in (
            "至少 2 个子代理，推荐 4 个",
            "跨模型独立分析",
            "Round 1 独立分析与 Round 2 交叉互评语义不变",
            "每个子代理必须生成独立报告文件",
            "报告入仓",
            "缺任一报告时保持开放",
        ):
            self.assertIn(needle, text)

    def test_roundtable_models_are_configured_not_hardcoded(self):
        text = (ROOT / "references/roundtable-protocol.md").read_text(encoding="utf-8")
        self.assertIn("本 Skill 不内置模型名", text)
        self.assertIn("无模型配置时先询问用户", text)
        for forbidden in ("模型A", "模型B", "外部执行 CLI", "来源项目", "来源项目"):
            self.assertNotIn(forbidden, text)

    def test_worker_protocol_defers_to_collaboration_governance(self):
        text = (ROOT / "references/worker-protocol.md").read_text(encoding="utf-8")
        self.assertIn("collaboration-governance.md", text)
        self.assertIn("主会话串行", text)
        self.assertIn("目标仓库执行体政策", text)
        self.assertIn("收口证据", text)
        self.assertIn("roundtable-protocol.md", text)

    def test_diagnosis_and_bootstrap_cover_collaboration(self):
        diagnosis = (ROOT / "references/diagnose.md").read_text(encoding="utf-8")
        bootstrap = (ROOT / "references/bootstrap.md").read_text(encoding="utf-8")
        for text in (diagnosis, bootstrap):
            self.assertIn("协作执行体政策", diagnosis)
            self.assertIn("圆桌政策", diagnosis)
            self.assertIn("关键治理文档评审", diagnosis)
            self.assertIn("collaboration-governance.md", bootstrap)
            self.assertIn("roundtable-protocol.md", bootstrap)
            self.assertIn("主会话串行执行", bootstrap)

    def test_templates_require_critical_review_and_executor_record(self):
        agents = (ROOT / "assets/templates/AGENTS.template.md").read_text(encoding="utf-8")
        workorder = (ROOT / "assets/templates/WO.template.md").read_text(encoding="utf-8")
        self.assertIn("关键治理文档评审", agents)
        self.assertIn("评审提交必须先于实现提交", agents)
        self.assertIn("协作执行体与圆桌", agents)
        self.assertIn("Round 1", agents)
        self.assertIn("Round 2", agents)
        self.assertIn("关键治理文档评审", workorder)
        self.assertIn("executor_type", workorder)
        self.assertIn("收口证据", workorder)


if __name__ == "__main__":
    unittest.main()
