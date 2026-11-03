---
name: repo-governance
description: Explicit-only skill that turns Codex into a safe long-term repository collaborator; use $repo-governance only for governance bootstrap or legacy-repository diagnosis, with shared workorder IDs, scoped branches, verified acceptance, anti-drift docs, configuration governance, and shit-mountain ratchets. Never load it for ordinary development tasks.
---

# 仓库治理适配

使用本 Skill 时，先判断目标仓库状态，再决定只读诊断或 L1 初始化；不得为了套用方法论覆盖目标仓库的显式规则。普通开发任务不使用本 Skill。

## 入口裁决

1. 先确认目标仓库和用户意图。用户未指定目标仓库时，只有请求明确指向当前仓库才可使用当前仓库；否则先询问。
2. 任何写入前先做只读约束盘点，检查 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、贡献文档、Issue/PR 模板、CI、测试命令、分支约定和外部工单系统。
3. 仓库已有开发约束时，读取 [diagnose.md](references/diagnose.md)，输出诊断报告并等待用户确认；不得直接覆盖或合并现有规则。
4. 仓库没有显式约束且用户要求初始化治理时，读取 [bootstrap.md](references/bootstrap.md)。空仓库或新项目在轻量盘点后直接创建 L1；无约束的已有仓库先做轻量盘点，再只创建 L1 文件。
5. 保留仓库专属约定。除安全底线外，冲突默认按目标仓库显式规则裁决。
6. 涉及配置、模块边界、依赖方向、外部调用、状态机、屎山入口或兼容层时，读取 [code-governance.md](references/code-governance.md)。
7. 涉及 WO 执行体、开发子任务、worker 可见性、fallback 或执行收口时，读取 [collaboration-governance.md](references/collaboration-governance.md)；目标仓库显式政策优先，无政策时主会话串行。
8. 需要重大决策圆桌、根因圆桌或交叉评审时，读取 [roundtable-protocol.md](references/roundtable-protocol.md)；Round 1 独立评审和 Round 2 交叉互评必做，结束后归档可见分析会话。
9. L1 初始化后如需发号，使用 [workorder-registry.md](references/workorder-registry.md) 和 bundled CLI；主会话统一发号，worker 不得改 registry。
10. 用户明确要求多 worker 并行时，先读取 [worker-protocol.md](references/worker-protocol.md)；L2 默认关闭，范围重叠任务必须串行。
11. 用户明确要求多 worktree 或长期分支治理时，读取 [worktree-protocol.md](references/worktree-protocol.md) 和 [merge-protocol.md](references/merge-protocol.md)；L3 默认关闭，合并前必须 fail-closed 检查。
12. 用户明确要求文档事实源、发布证据链或长期文档治理时，读取 [document-governance.md](references/document-governance.md)；L4 默认关闭，不自动创建 Heavy 门禁。

## 硬边界

1. 已有约束必须先只读诊断，并获得用户确认后才能写入。
2. 不得覆盖 `AGENTS.md`、`CLAUDE.md`、贡献文档、模板或 CI 以强行套用本方法。
3. 不得静默启用多 worker、多 worktree、发布门禁或文档地图治理。
4. 默认只启用 L1：先方案后开发、根因先行、工单范围、一工单一分支、配置与架构影响、验收命令和 fail-closed 汇报。
5. L2 多 worker、L3 多 worktree / 长期分支治理、L4 文档与发布治理保留设计但默认不启动。
6. 屎山 ratchet 和结构自动门禁默认不启动；必须先建立目标仓库基线并单独确认。
7. 不把 independent worker 登记为 native child；不用后台进程、普通命令输出或主持人自答冒充模型执行体。
8. 未记录命令结果不得声称完成；缺证据保持开放或需确认。

## 输出契约

- 已有约束仓库：输出 `diagnose.md` 规定的诊断报告，批准前不写仓库。
- 无约束仓库：输出 L1 文件计划、生成文件、验收命令和仍处关闭状态的分层能力。
- 每次都说明启用了哪些治理层、哪些治理层保持关闭。
