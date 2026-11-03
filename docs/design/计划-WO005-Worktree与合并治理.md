# WO-005 实施计划：Worktree 与合并治理

## 目标

沉淀 L3 多 worktree 和长期分支治理协议，避免并行任务覆盖同一工作区、误合并未验收分支或破坏集成分支。本工单不启动 L3，不创建 worktree，不实现自动合并。

## 设计要点

1. L3 默认关闭；仅在多工单并行、单工作区风险高且用户确认时启用。
2. 每张 WO 一个独立 worktree 和一个分支。
3. Worktree 创建前检查既有 worktree、分支占用和脏状态。
4. Registry 记录 worktree、branch、base、placeholder 和状态。
5. 合并前检查范围、验收记录、脏状态、分支差异和依赖顺序。
6. 集成分支禁直推；合并后必须复跑验收。
7. 冲突时停止并保留现场，禁止破坏性 reset/checkout。

## 文件职责

1. `references/worktree-protocol.md`：启用条件、创建、登记、执行、清理和安全边界。
2. `references/merge-protocol.md`：合并前检查、顺序、执行、验收和记录。
3. `tests/test_l3_protocols.py`：验证默认关闭、路径/分支/registry/合并/冲突约束。
4. `SKILL.md`：增加 L3 显式入口。
5. `README.md`：更新当前阶段。

## 验收

```bash
python3 -m unittest discover -s tests -v
python3 /Users/2mol/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git diff --check
```

## 不做什么

1. 不创建或删除 worktree。
2. 不执行 merge、rebase 或 push。
3. 不实现分支范围自动检查脚本。
