# Worktree 治理协议

L3 多 worktree 能力默认关闭。只有多工单并行、单工作区存在覆盖或串单风险、且用户确认启用时，才使用本协议。**共享工作区保护（第 2 节）不受 L3 开关限制，只要存在共享工作区即生效。**

## 1. 启用条件

1. 用户明确确认使用多 worktree。
2. 多张 WO 需要并行执行。
3. 目标仓库存在稳定集成分支。
4. 每张 WO 有独立分支、base、范围和验收命令。
5. Registry 可用且校验通过。
6. 本机磁盘、路径权限和 Git worktree 能力满足要求。

单人顺序任务不强制创建 worktree，但共享工作区（第 2 节）例外。

## 2. 共享工作区保护

当一个工作区同时满足以下条件时，它是共享工作区，受本节保护：

1. 多个会话或执行体共用该目录。
2. 该目录承载共享基线：集成分支检出、或作为其他 worktree 的创建源。

保护规则：

1. **零操作**：任何执行体（主会话、worker、子代理、命令行工具）不得在共享工作区执行任何改变 Git 状态或文件内容的操作，包括 `switch`、`checkout`、`stash`（含 `apply`/`pop`）、`merge`、`rebase`、`reset`、`restore`、`clean`、`commit`、`push`、分支/worktree 管理，以及文件新增、修改、删除、移动。
2. **未跟踪文件只登记**：共享工作区的未跟踪文件没有 Git 保护，发现时只登记报告，不清理、不隔离、不接管、不顺手修改。
3. **工单与集成另走独立 worktree**：全部工单实施、合并与集成都必须在独立 worktree 执行；集成合并使用专门的 integration worktree。
4. **发号器绑定目标**：发号器必须从目标 worktree 根运行，或显式指定目标仓库目录；对共享工作区直接拒绝发号。
5. 不得借主会话、子代理、worker 或任何工具间接绕过上述限制。

设立理由：共享基线工作区被工单操作污染属于高发事故形态（工单合并半途废弃、基线被切换、脏状态无人认领），且未跟踪文件一旦误删无法恢复。

## 3. 创建前检查

1. 记录当前仓库路径、集成分支和 HEAD。
2. 执行 `git worktree list --porcelain`，确认分支未在其他 worktree 检出。
3. 检查目标 worktree 路径不存在或为空。
4. 检查相关 worktree 是否有脏文件；有脏文件先停止并报告。
5. 确认 WO 已 `reserved`，分支由主会话分配。
6. 确认允许修改文件范围不与其他 active WO 重叠。

## 4. 路径与创建

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

## 5. 执行边界

1. Worker 只能进入 prompt 指定的 worktree。
2. Worker 不得创建、切换、删除或复用其他 worktree。
3. Worker 不得修改 `.git/repo-governance/workorder-registry.json`。
4. 主会话定期检查 worktree 脏文件和分支状态。
5. 发现范围外修改时停止该 WO，不自动清理。

## 6. 清理

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
