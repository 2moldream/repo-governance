# Worktree 治理协议

L3 多 worktree 能力默认关闭。只有多工单并行、单工作区存在覆盖或串单风险、且用户确认启用时，才使用本协议。

## 1. 启用条件

1. 用户明确确认使用多 worktree。
2. 多张 WO 需要并行执行。
3. 目标仓库存在稳定集成分支。
4. 每张 WO 有独立分支、base、范围和验收命令。
5. Registry 可用且校验通过。
6. 本机磁盘、路径权限和 Git worktree 能力满足要求。

单人顺序任务不强制创建 worktree。

## 2. 创建前检查

1. 记录当前仓库路径、集成分支和 HEAD。
2. 执行 `git worktree list --porcelain`，确认分支未在其他 worktree 检出。
3. 检查目标 worktree 路径不存在或为空。
4. 检查相关 worktree 是否有脏文件；有脏文件先停止并报告。
5. 确认 WO 已 `reserved`，分支由主会话分配。
6. 确认允许修改文件范围不与其他 active WO 重叠。

## 3. 路径与创建

推荐路径：

```text
<repository-name>.worktrees/<WO-number>-<slug>
```

也可使用用户显式指定的路径，但必须满足：

1. 位于仓库工作区之外。
2. 不位于 `.git` 内。
3. 不覆盖既有目录。
4. 路径可写且剩余空间充足。
5. 不使用网络挂载的模糊路径。

创建形态：

```bash
git -C <target-repo> worktree add -b <branch> <worktree-path> <base>
```

如分支已存在但未检出，可去掉 `-b` 并显式指定既有分支。创建后必须在 registry 中记录绝对 worktree 路径，再提交工单占位并执行 `activate`。

## 4. 执行边界

1. Worker 只能进入 prompt 指定的 worktree。
2. Worker 不得创建、切换、删除或复用其他 worktree。
3. Worker 不得修改 `.git/repo-governance/workorder-registry.json`。
4. 主会话定期检查 worktree 脏文件和分支状态。
5. 发现范围外修改时停止该 WO，不自动清理。

## 5. 清理

只有满足以下全部条件才可清理：

1. WO 已完成验收并合入，或已明确 `abandoned`。
2. worktree 无未提交文件。
3. 无用户声明的保留调试材料。
4. 清理方式已获用户确认。

优先使用：

```bash
git -C <target-repo> worktree remove <worktree-path>
```

不得使用强制删除、`git reset --hard`、`git checkout --` 或直接删除目录来清理脏 worktree。清理后保留 registry 记录，`worktree` 字段不得清空历史路径，可追加清理说明到工单记录。
