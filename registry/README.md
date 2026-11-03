# Workorder Registry 说明

## 位置

运行时 registry 不提交进业务分支，保存于 Git 共享层：

```text
$(git rev-parse --git-common-dir)/repo-governance/workorder-registry.json
$(git rev-parse --git-common-dir)/repo-governance/workorder.lock
```

这样多个 worktree 共享同一份编号状态，避免并行分支各自维护 registry 造成合并冲突。

## 状态

```text
reserved -> active -> completed
                -> abandoned
```

规则：

1. 编号只顺延，不复用。
2. `abandoned` 永久不得复用。
3. Placeholder-first：实现前必须先提交 WO 占位文档并登记 placeholder。
4. 所有跨进程写入必须持有 `workorder.lock`。
5. 发号器落地前由主会话人工维护，worker 禁止写入。

## 记录字段

| 字段 | 含义 |
|---|---|
| `workorder_id` | 本地稳定工单 ID |
| `todo_id` | 关联待办 ID，可为空 |
| `status` | `reserved` / `active` / `completed` / `abandoned` |
| `owner` | 主会话或 worker 标识 |
| `base` | 起点 commit 或 ref |
| `branch` | 工单分支 |
| `worktree` | 独立 worktree 路径；未启用 L3 时为空 |
| `placeholder` | 占位提交 |
| `external_id` | Jira、TAPD、GitHub Issue 等外部映射 |

## 冲突规则

1. 文件范围重叠的工单不得同时 active。
2. 依赖任务必须按 base 和合并顺序执行。
3. Worker 只能使用主会话分配的编号。
4. 撞号时后启动会话停止并报告，不得静默改号。
5. Registry 冲突未裁决前 fail-closed。
