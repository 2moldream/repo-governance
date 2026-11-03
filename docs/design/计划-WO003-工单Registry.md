# WO-003 实施计划：工单 Registry

## 目标

实现跨 worktree 共享的 WO/TD registry、文件锁、原子发号、状态流转和 placeholder-first 校验，解决并行会话撞号与占位提交不可追溯的问题。

## 行为设计

1. Registry 固定存放在目标仓库 Git common dir 下的 `repo-governance/workorder-registry.json`，锁文件为同目录 `workorder.lock`。
2. Registry 和锁不进入业务分支。
3. CLI 位于 `scripts/workorder_registry.py`，只依赖 Python 标准库和 Git。
4. 支持 `init`、`show`、`allocate`、`activate`、`complete`、`abandon`、`validate`。
5. `allocate` 在锁内分配下一组 `WO-xxx/TD-xxx`，状态为 `reserved`，`placeholder` 必须为空。
6. `activate` 必须提交非空 placeholder，并在目标仓库验证该 commit 存在。
7. `active/completed` 记录必须有 placeholder；`reserved` 记录不得有 placeholder。
8. 编号单调递增，不复用；`abandoned` 永久保留。
9. 写入使用临时文件加 `os.replace`，同目录锁使用 `fcntl.flock`。
10. `validate` 检查 schema、状态、编号、序列、字段、时间、placeholder、分支和 worktree 路径。

## 文件职责

1. `scripts/workorder_registry.py`：数据模型、锁、原子写入、Git 校验和 CLI。
2. `references/workorder-registry.md`：主会话和 worker 的使用边界。
3. `tests/test_workorder_registry.py`：初始化、发号、状态流转、非法占位、并发不撞号和当前 registry 校验。
4. `references/bootstrap.md`：从“人工登记”切换为优先使用 CLI。
5. `SKILL.md`：入口声明 bundled allocator。
6. `README.md`：当前阶段更新。

## 验收

```bash
python3 -m unittest discover -s tests -v
python3 scripts/workorder_registry.py --repo . show
python3 scripts/workorder_registry.py --repo . validate
python3 /Users/2mol/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git diff --check
```

## 不做什么

1. 不实现多 worker 分发。
2. 不创建或管理 worktree。
3. 不解析工单 Markdown 的完整治理格式。
4. 不把 registry 写入业务分支。
