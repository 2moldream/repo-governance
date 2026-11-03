# repo-governance

给 Codex 加一层可复用的仓库治理能力。

它解决的问题很具体：**AI 写代码很快，但如果没有治理层，长期仓库会被并行会话、无边界修改、漂移文档和屎山代码拖垮。**

## 它在 Codex 中解决什么

| 痛点 | repo-governance 的处理 |
|---|---|
| 新仓库没有规则，Codex 每次都临场发挥 | 一套命令初始化治理基线：工单、分支、范围、验收、待办 |
| 已有仓库已经有 AGENTS/CLAUDE 规范 | 不覆盖、不强套，先做只读诊断，输出一致/重复/缺失/冲突/例外矩阵 |
| 多会话并行时撞工单号、抢分支、改同一批文件 | 共享 WO/TD registry、文件锁、原子发号和 placeholder-first |
| 工单范围不清晰，最后改出一堆范围外文件 | 每张工单必须声明范围内文件，范围外问题只登记不顺手改 |
| 验收靠嘴说，“应该可以了” | 每张工单必须写验收命令，并记录真实执行结果 |
| 多 worker / 多 worktree 容易串单 | 执行体协议、worktree 协议、合并前 fail-closed 检查 |
| 文档漂移，目标和现状混在一起 | 事实源矩阵、生命周期、目标/现状分离、发布证据链 |
| 配置散落、魔法参数满天飞 | 配置分类、唯一事实源、优先级、安全默认值、example/config 边界 |
| 屎山代码越改越大 | 屎山识别、基线 ratchet、切片迁移、兼容层删除条件 |
| 关键治理文档被随手改 | 关键文档变更前置评审，评审提交先于实现提交 |

## 特色

1. **目标仓库规则优先**：不是把模板硬塞进仓库。已有约束时先诊断，用户确认后才落地。
2. **explicit-only**：普通开发任务不会自动加载它，避免和目标仓库自己的 AGENTS/CLAUDE 冲突。只有明确写 `$repo-governance` 时才调用。
3. **治理不是口号，而是可执行协议**：WO/TD 编号、锁、状态流转、placeholder、worker、worktree、merge、roundtable 都有明确规则。
4. **不只管流程，也管代码健康**：包含配置治理、架构分层、依赖方向、屎山 ratchet、兼容层退出条件。
5. **fail-closed**：缺证据、超范围、未验收、归档失败，都不能被说成完成。
6. **执行体防伪**：不用后台进程、普通命令输出或主持人自答冒充模型执行体；独立 worker 不会被误登记为 native child。

## 怎么用

初始化一个新仓库：

```text
使用 $repo-governance 初始化当前仓库治理
```

诊断一个已有仓库：

```text
使用 $repo-governance 诊断当前仓库治理并输出适配方案
```

## 一句话

它让 Codex 从“能写代码”变成“能在一个长期演进的仓库里安全协作”。

## 当前状态

- 版本：`0.4.0`
- 全局入口：`~/.codex/skills/repo-governance`
- 调用策略：explicit-only
- 默认能力：L1 仓库基线，含配置与架构影响声明
- 默认不启动：L2 多 worker、L3 多 worktree / 多分支长期演进、L4 文档与发布治理、屎山规模 ratchet 与结构自动门禁

## 安装

```bash
python3 scripts/deploy.py --destination ~/.codex/skills/repo-governance
```

目标路径已存在时脚本会拒绝覆盖。

## 文档入口

1. [SKILL.md](SKILL.md)
2. [diagnose.md](references/diagnose.md)
3. [bootstrap.md](references/bootstrap.md)
4. [workorder-registry.md](references/workorder-registry.md)
5. [code-governance.md](references/code-governance.md)
6. [collaboration-governance.md](references/collaboration-governance.md)
7. [roundtable-protocol.md](references/roundtable-protocol.md)
8. [worker-protocol.md](references/worker-protocol.md)
9. [worktree-protocol.md](references/worktree-protocol.md)
10. [merge-protocol.md](references/merge-protocol.md)
11. [document-governance.md](references/document-governance.md)
12. [deployment.md](references/deployment.md)
13. [AGENTS.md](AGENTS.md)
