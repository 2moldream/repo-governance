# L1 初始化

目标仓库没有显式开发约束，或正在创建空仓库/新项目时使用本参考。过程中一旦发现显式约束，立即停止写入并切换到 `diagnose.md`。

## 1. 仓库状态

### 已有开发约束

不执行初始化，改用 `diagnose.md`。

### 无约束但已有仓库

1. 轻量盘点 Git 状态、包管理器、README、测试/lint/构建命令、CI、配置框架、入口结构、协作执行体期望和外部工单系统。
2. 若确实没有显式治理约束且用户要求初始化，只创建下列 L1 文件。
3. 名称和命令必须适配仓库；不创建预留未来流程的空目录。

### 空仓库或新项目

直接创建：

```text
AGENTS.md
docs/README.md
docs/design/方案-<主题>.md
docs/workorders/WO-001.md
docs/design/全局待办登记册.md
```

以 `assets/templates/` 为起点，替换占位符为仓库具体值。

## 2. L1 文件

1. `AGENTS.md`：执行约束、工单政策、分支政策、范围、配置与架构约束、验收和 fail-closed 汇报。
2. `docs/README.md`：文档入口和事实源矩阵。
3. `docs/design/方案-<主题>.md`：已确认设计与根因记录。
4. `docs/workorders/WO-001.md`：带范围的实施与验收记录。
5. `docs/design/全局待办登记册.md`：开放事项与关闭证据。

只按需创建父目录，不覆盖既有路径。任何目标路径已存在时停止并报告冲突。

## 3. 外部工单映射

仓库使用 GitHub Issues、Jira、TAPD 或其他系统时：

1. 保留外部系统作为团队流程入口。
2. 在本地工作项记录中增加 `external_id`。
3. 不在两套系统重复维护分配、优先级或发布语义。
4. 本地 `WO-xxx` 只作为仓库侧稳定执行标识。

## 4. Registry 基线

优先使用本 Skill 附带的发号器：

1. 初始化共享 registry。
2. 由主会话执行 `allocate`。
3. 实现前先提交工单占位。
4. 用占位 commit 执行 `activate`。
5. 完成验收后执行 `complete`。

详细命令和责任边界见 [workorder-registry.md](workorder-registry.md)。

CLI 不可用时的人工兜底：

```text
$(git rev-parse --git-common-dir)/repo-governance/workorder-registry.json
```

1. 主会话统一分配编号并写入工作项文档。
2. 新仓库从 `WO-001` 开始。
3. 并行会话不得自行推导编号。
4. 在工单或共享 registry 中记录占位提交。
5. 不把运行时 registry 或锁文件提交到功能分支。

## 5. 分支基线

1. 一张工单一个分支：`wo/<编号>-<slug>`。
2. 记录 base branch 或 base commit。
3. 仓库已定义集成分支时，禁止直推实现提交。
4. 工单列出允许修改文件。
5. 范围外发现只报告，不修改。

## 6. 能力分层

L1 默认启用：

1. 先方案后开发。
2. 根因先行。
3. 工单身份与 placeholder-first。
4. 一工单一分支。
5. 显式范围。
6. 行为变化声明。
7. 验收命令与结果。
8. 开放事项台账。
9. fail-closed 完成汇报。
10. 配置分类、唯一事实源、优先级和安全默认值。
11. 架构分层、依赖方向和外部调用边界。
12. 工单架构影响与配置影响声明。
13. 关键治理文档变更前置评审。
14. 默认主会话串行执行，不启动 worker、子智能体或圆桌。

详细规则见 [code-governance.md](code-governance.md)。
执行体选择、fallback 和收口见 [collaboration-governance.md](collaboration-governance.md)；圆桌触发与归档见 [roundtable-protocol.md](roundtable-protocol.md)。

以下能力保留设计但默认不启动：

1. L2 多 worker 分发。
2. L3 多 worktree 与长期分支治理。
3. L4 文档地图、代码地图、发布证据链和自动治理门禁。
4. 屎山规模 ratchet 与结构自动门禁；启用前必须先建立目标仓库基线。
5. 独立执行体和自动圆桌；必须先获得用户确认并配置模型、输出位置和归档方式。

启用任一层必须先单独诊断、设计并获得用户确认。

## 7. 初始化报告

完成后输出：

```markdown
# L1 初始化结果

## 创建文件

<路径>

## 适配的仓库取值

<基线分支、命令、工单映射、命名>

## 验收

<命令与结果>

## 关闭分层

L2 / L3 / L4：disabled

## 下一步需要决策

<发号器、worker 分发、worktree 政策；无则写“无”>
```
