# repo-governance

跨仓库沉淀可复用的开发治理方法论，形成可安装到 Codex 的 `repo-governance` Skill。源码独立管理，不绑定来源项目分支、编号、数据集或业务规则。

## 当前状态

- 阶段：WO-011，公开信息清理完成。
- 运行时安装：已执行；`~/.codex/skills/repo-governance` 是指向本仓库的 symlink，版本 `0.3.0`。
- 调用策略：explicit-only；普通开发任务不自动加载，仅用户明确要求仓库治理初始化或历史仓库治理诊断时通过 `$repo-governance` 调用。
- 默认能力：L1 仓库基线，含配置与架构影响声明。
- 保留但默认不启动：L2 多 worker、L3 多 worktree / 多分支长期演进、L4 文档与发布治理、巨石规模 ratchet 与结构自动门禁。

## 核心目标

1. 进入已有约束的仓库时，先诊断现有规范，不强行覆盖。
2. 进入无约束仓库或新仓库时，直接建立最小可执行治理基线。
3. 保留统一发号、placeholder-first、一工单一分支、工单分发和合并治理，避免并行冲突。
4. 缺证据、超范围、未验收时 fail-closed，不得声称完成。

## 文档入口

1. [AGENTS.md](AGENTS.md)
2. [方案-repo-governance.md](docs/design/方案-repo-governance.md)
3. [WO-001.md](docs/workorders/WO-001.md)
4. [registry/README.md](registry/README.md)
5. [SKILL.md](SKILL.md)
6. [diagnose.md](references/diagnose.md)
7. [bootstrap.md](references/bootstrap.md)
8. [workorder-registry.md](references/workorder-registry.md)
9. [worker-protocol.md](references/worker-protocol.md)
10. [worktree-protocol.md](references/worktree-protocol.md)
11. [merge-protocol.md](references/merge-protocol.md)
12. [document-governance.md](references/document-governance.md)
13. [deployment.md](references/deployment.md)
14. [code-governance.md](references/code-governance.md)
15. [collaboration-governance.md](references/collaboration-governance.md)
16. [roundtable-protocol.md](references/roundtable-protocol.md)

## 安装

```bash
python3 scripts/deploy.py --destination ~/.codex/skills/repo-governance
```

目标路径已存在时脚本会拒绝覆盖。
