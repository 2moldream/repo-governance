# repo-governance

给 Codex 与 Claude 加一层可复用的仓库治理能力。

它解决的问题很具体：**AI 写代码很快，但如果没有治理层，长期仓库会被并行会话、无边界修改、漂移文档和屎山代码拖垮。**

## 它在 Codex / Claude 中解决什么

| 痛点 | repo-governance 的处理 |
|---|---|
| 新仓库没有规则，Codex / Claude 每次都临场发挥 | 一套命令初始化治理基线：工单、分支、范围、验收、待办 |
| 已有仓库已经有 AGENTS/CLAUDE 规范 | 不覆盖、不强套，先做只读诊断，输出一致/重复/缺失/冲突/例外矩阵 |
| 多会话并行时撞工单号、抢分支、改同一批文件 | 共享 WO/TD registry、文件锁、原子发号和 placeholder-first |
| 工单范围不清晰，最后改出一堆范围外文件 | 每张工单必须声明范围内文件，范围外问题只登记不顺手改 |
| 验收靠嘴说，“应该可以了” | 分级验收 L0/L1/L2、漂移自动升级、验收命令与真实结果；禁止只改等级字段冒充已验收 |
| 多 worker / 多 worktree 容易串单 | 执行体协议、worktree 协议、合并前 fail-closed 检查 |
| Codex worker 与 Claude subagent 各记各的、互相冒充 | 统一执行体协议：Codex native child / worker / fallback 与 `claude-subagent` 并列登记；Claude 路径无 fallback，关闭须双证据 |
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
7. **分级验收**：L0/L1/L2 三级 + 漂移自动升级，禁止改字段冒充已验收；验收等级与能力分层显式消歧。
8. **证据边界**：输入/预期/产物三目录隔离，预期结果永不进生产输入，历史运行产物不冒充新证据。
9. **双宿主执行体**：Codex（native child / worker / fallback）与 Claude（子代理）双协议，谁执行就按谁的口径登记，不冒充；Claude 路径无 fallback，关闭须有完成通知和入仓报告。

## 怎么用

Codex 中显式使用 `$repo-governance`；Claude 中让宿主助手显式调用已安装的 repo-governance skill。两者都先诊断目标仓库，不因宿主不同改变目标仓库政策。

初始化一个新仓库：

```text
使用 $repo-governance 初始化当前仓库治理
```

诊断一个已有仓库：

```text
使用 $repo-governance 诊断当前仓库治理并输出适配方案
```

## 一句话

它让 Codex 与 Claude 从“能写代码”变成“能在一个长期演进的仓库里安全协作”。

## 当前状态

- 版本：`0.5.0`
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
4. [acceptance-governance.md](references/acceptance-governance.md)
5. [design-governance.md](references/design-governance.md)
6. [evidence-governance.md](references/evidence-governance.md)
7. [workorder-registry.md](references/workorder-registry.md)
8. [code-governance.md](references/code-governance.md)
9. [collaboration-governance.md](references/collaboration-governance.md)
10. [roundtable-protocol.md](references/roundtable-protocol.md)
11. [worker-protocol.md](references/worker-protocol.md)
12. [worktree-protocol.md](references/worktree-protocol.md)
13. [merge-protocol.md](references/merge-protocol.md)
14. [document-governance.md](references/document-governance.md)
15. [deployment.md](references/deployment.md)
16. [AGENTS.md](AGENTS.md)
