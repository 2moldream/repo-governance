# WO-002 实施计划：Skill 入口与 L1

## 目标

实现 Codex Skill 入口、已有约束仓库的诊断规则，以及无约束仓库的 L1 初始化模板。L2 多 worker、L3 多 worktree / 多分支长期演进、L4 文档与发布治理只保留启用条件，默认不启动。

## 结构

1. `SKILL.md`：只保留入口路由、安全边界和默认分层结论。
2. `references/diagnose.md`：已有开发约束仓库的只读诊断流程、证据格式和冲突裁决。
3. `references/bootstrap.md`：三类仓库状态的 L1 初始化流程与写入边界。
4. `assets/templates/`：目标仓库可落地的 AGENTS、文档入口、工单和待办模板。
5. `tests/`：普通契约测试，验收 Skill 元数据、关键行为、模板完整性和来源项目规则隔离。

## 实施步骤

1. 清理外部流程要求，保留测试作为验收工具。
2. 新增 `SKILL.md`，要求先判断目标仓库状态；已有约束必须只读诊断。
3. 新增诊断参考，扫描代理规范、贡献文档、Issue/PR 模板、CI、测试命令、分支和外部工单系统。
4. 新增初始化参考，区分已有约束、无约束已有仓库、空仓库或新项目。
5. 新增四类 L1 模板：执行约束、文档入口、工单契约、开放事项登记。
6. 更新 README 当前状态。
7. 运行单元测试、Skill quick validate 和 `git diff --check`。
8. 将实施和验收结果写回 WO-002。

## 验收

```bash
python3 -m unittest discover -s tests -v
python3 /Users/2mol/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git diff --check
```

## 不做什么

1. 不安装到 `~/.codex/skills`。
2. 不对任何目标仓库执行写入。
3. 不实现发号器、锁、多 worker 调度和 worktree 管理。
4. 不启动 L2/L3/L4。
