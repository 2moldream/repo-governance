# WO-004 实施计划：Worker 分发协议

## 目标

沉淀 L2 多 worker 分发协议和标准化 prompt 模板，保证并行任务边界清晰、编号统一、范围不重叠、结果可追溯。本工单只保留能力，不自动启动 worker，也不实现调度器。

## 设计要点

1. L2 默认关闭；仅用户明确要求并行且任务边界清晰时启用。
2. 主会话统一方案、发号、拆分、分发和收敛。
3. Worker prompt 必须包含 WO/TD、仓库、分支、base、范围、禁止项、行为边界、验收、输出位置和停止条件。
4. Worker 禁止取号、修改 registry、扩大范围、合并分支或冒充其他 worker。
5. 文件范围重叠任务禁止并行。
6. 使用真实独立会话；无法创建时停止并报告，不用后台进程或主持人自答替代。
7. 记录会话标识、实际模型、任务边界、输出位置和最终状态。

## 文件职责

1. `references/worker-protocol.md`：启用条件、分发前检查、prompt 契约、禁止事项、留痕与收敛。
2. `assets/templates/worker-prompt.template.md`：可复制的 worker 任务提示模板。
3. `tests/test_worker_protocol.py`：验证关键安全边界与 prompt 字段。
4. `SKILL.md`：增加 L2 显式启用入口。
5. `README.md`：更新当前阶段。

## 验收

```bash
python3 -m unittest discover -s tests -v
python3 /Users/2mol/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git diff --check
```

## 不做什么

1. 不启动 worker。
2. 不创建 worktree。
3. 不合并分支。
4. 不实现自动调度或会话管理脚本。
