# repo-governance

Codex 和 Claude 都能用。它管的是仓库里的协作规则：工单怎么编号、每张工单能改哪些文件、谁来执行、拿什么证据验收。

## 它在 Codex / Claude 中解决什么

| 痛点 | repo-governance 的处理 |
|---|---|
| 新仓库没有规则，每次都临场发挥 | 建 AGENTS、工单模板和分支规则，写清验收命令 |
| 仓库已有 AGENTS/CLAUDE 规范 | 先读现有规则，列出一致、重复、缺失和冲突；确认后才写文件 |
| 两个会话撞工单号、抢同一分支 | 主会话统一发 WO/TD 号，registry 加文件锁；先提交占位工单再实现 |
| 一张小工单改出一堆范围外文件 | 工单列允许修改的文件，超出清单的改动不得混入 |
| 验收靠嘴说，“应该可以了” | 按 L0/L1/L2 留验收命令和输出；发现行为漂移就升级，改等级字段不算验收 |
| 子代理跑完了，却说不清是谁做的、报告在哪 | 登记真实执行体、task id 和报告路径；Codex 与 Claude 各按自己的启动方式记录 |
| Codex worker 与 Claude subagent 各记各的、互相冒充 | native child、worker、fallback、`claude-subagent` 分开登记；Claude 子代理不转 worker 兜底，关闭要核对完成通知和入仓报告 |
| 多个分支一起合，出问题找不到是哪张工单引入的 | 同族工单串行合并，每批按最高验收等级复跑；冲突或漂移就停 |
| 文档把目标写成现状 | 用事实源矩阵区分当前实现、目标设计和历史说明 |
| 配置散落，默认值没人说得清 | 记录配置事实源、覆盖顺序和安全默认值，运行密钥不进 Git |
| 兼容层越垫越厚，旧实现一直删不掉 | 每个 shim 写替代路径、删除条件和承接工单 |
| 治理规范被随手改，之后才补评审 | 评审提交先于实现提交，记录确认来源和回退方式 |

## 特色

1. **目标仓库规则优先**：已有 AGENTS/CLAUDE 时先只读诊断，不拿模板覆盖原文。
2. **explicit-only**：只有显式调用 `$repo-governance` 才加载；普通开发任务不触发。
3. **共享工单编号**：WO/TD 由主会话统一分配，registry 加锁，worker 不自行取号。
4. **工单限定改动范围**：每张工单写文件清单、分支、验收命令和回退方式。
5. **分级验收**：L0 查零行为变化，L1 跑全量测试和相关回归，L2 加关键路径与发布证据；L0 发现漂移自动升 L1。
6. **证据目录分开**：输入、预期结果、运行产物各放各处；预期结果不进生产输入，旧 outputs 不当新基线。
7. **执行体按实际启动方式登记**：Codex 的 native child / worker / fallback 与 Claude 子代理不混记；谁干活就按谁的规矩登记。
8. **合并按批复验**：同族串行，异族先查文件和事实源冲突；整批按最高验收等级复跑。
9. **缺证据不关闭**：测试没跑、材料缺失、报告没入仓，都保留为开放项。
10. **代码结构有退出条件**：兼容层和影子实现必须写删除条件，屎山迁移先留等价对照。

## 怎么用

Codex 中显式使用 `$repo-governance`。Claude 中让宿主助手显式调用已安装的 repo-governance skill。调用前先装好本 Skill；两边都先读目标仓库规则。

初始化一个新仓库：

```text
使用 $repo-governance 初始化当前仓库治理
```

诊断一个已有仓库：

```text
使用 $repo-governance 诊断当前仓库治理并输出适配方案
```

## 当前状态

- 版本：`0.5.0`
- Codex 入口：`~/.codex/skills/repo-governance`
- 调用策略：explicit-only
- 默认能力：L1 仓库基线，含配置与架构影响声明
- 默认不启动：L2 多 worker、L3 多 worktree / 多分支长期演进、L4 文档与发布治理、屎山规模 ratchet 与结构自动门禁

## 安装

```bash
python3 scripts/deploy.py --destination ~/.codex/skills/repo-governance
```

目标路径已存在时脚本会拒绝覆盖。Claude 侧按宿主平台的 skill 安装方式配置，调用规则不变。

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
