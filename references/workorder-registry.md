# 工单 Registry 使用

`scripts/workorder_registry.py` 管理目标仓库 Git common dir 下的共享 registry，用于并行会话防撞号和 placeholder-first 追溯。

## 位置

```text
<target-repo>/.git/repo-governance/workorder-registry.json
<target-repo>/.git/repo-governance/workorder.lock
```

多 worktree 仓库中路径基于 `git rev-parse --git-common-dir`，所有 worktree 共享同一份状态。registry 和锁不提交到业务分支。

## 命令

以下 `<skill-root>` 表示本 Skill 安装目录；`<target-repo>` 表示目标仓库路径。

```bash
python3 <skill-root>/scripts/workorder_registry.py --repo <target-repo> init
python3 <skill-root>/scripts/workorder_registry.py --repo <target-repo> show
python3 <skill-root>/scripts/workorder_registry.py --repo <target-repo> validate
python3 <skill-root>/scripts/workorder_registry.py --repo <target-repo> allocate \
  --owner main-session --slug example --base main
python3 <skill-root>/scripts/workorder_registry.py --repo <target-repo> activate \
  --workorder WO-001 --placeholder <placeholder-commit>
python3 <skill-root>/scripts/workorder_registry.py --repo <target-repo> complete \
  --workorder WO-001
python3 <skill-root>/scripts/workorder_registry.py --repo <target-repo> abandon \
  --workorder WO-001
```

## 状态流转

```text
reserved -> active -> completed
reserved -> abandoned
active   -> abandoned
```

1. `allocate` 只创建 `reserved` 记录，placeholder 必须为空。
2. `activate` 必须提供目标仓库中存在的 commit，CLI 会规范化为完整 SHA。
3. `active` 和 `completed` 记录必须有 placeholder。
4. `abandoned` 编号永久保留，不得复用。
5. 所有写入都在 `workorder.lock` 保护下原子替换 JSON。

## 责任边界

1. 主会话是唯一发号方；worker 不得执行 `allocate`、`activate`、`complete` 或 `abandon`。
2. Worker 只使用 prompt 中显式给出的 WO/TD 和分支。
3. Registry 校验失败时 fail-closed，不得继续实现或合并。
4. 外部工单系统 ID 只写入 `external_id`，不替代本地稳定 ID。
5. Registry 只证明编号与占位关系，不证明代码质量或验收通过。
