# Worker 分发协议

L2 多 worker 能力默认关闭。只有用户明确要求并行、任务边界清晰且文件范围不重叠时，才可启用本协议。执行体类型、可见性和兜底规则先按 [collaboration-governance.md](collaboration-governance.md) 裁决；无目标政策时主会话串行。

## 1. 启用前检查

1. 用户明确要求并行执行。
2. 方案已确认，并已拆成多张 WO。
3. 每张 WO 已通过共享 registry 分配编号。
4. 每张 WO 有独立分支和明确 base。
5. 每张 WO 的允许修改文件清单互不重叠。
6. 依赖关系和合并顺序已声明。
7. 目标仓库执行体政策已读取并可执行。
8. 执行体启动、留痕和收口方式已确定。

任一条件不满足时主会话串行、停止询问或登记延期，不得降级成伪并行。

## 2. 主会话职责

主会话是唯一调度和收敛点：

1. 统一分配 WO/TD，不允许多方发号。
2. 检查文件范围、依赖和分支冲突。
3. 按目标政策选择 `main-session-serial`、invisible executor、native visible child 或 independent worker。
4. 生成标准化 worker prompt。
5. 保存执行体身份、启动方法、实际模型、边界、输入版本和输出位置。
6. 跟踪 `running / completed / failed / interrupted`。
7. 执行结束后记录关闭、归档或逻辑收口证据。
8. 只基于产物和验收结果收敛结论。
9. 汇总共识、分歧、证据缺口和后续动作。

## 3. Worker Prompt 契约

每份 prompt 必须包含：

```text
WO 编号
TD 编号
仓库路径或 worktree
分支名
base commit 或 base branch
允许修改文件
禁止修改项
行为变化边界
架构边界
配置边界
验收命令
输出位置
停止条件
```

使用 [worker-prompt.template.md](../assets/templates/worker-prompt.template.md) 生成，未填字段不得分发给 worker。

Worker 输出必须包含架构影响、配置影响、是否触及屎山或兼容层，以及对应证据；不得只写“无影响”。

## 4. Worker 禁止事项

1. 自行取号或推导编号。
2. 修改共享 registry。
3. 扩大允许修改范围。
4. 修改其他 WO 的文件。
5. 创建、合并、rebase 或删除分支。
6. 声称完成但未运行验收命令。
7. 将技术缺口改为业务通过。
8. 伪装独立评审或冒充其他 worker。

发现范围外问题时，worker 只登记发现并停止相关部分。

## 5. 执行体要求

1. Worker 必须是真实模型执行体，不能由主持人自答、普通命令输出或后台进程替代。
2. 目标仓库要求不可见执行体时，不得改用可见 worker。
3. 目标仓库首选 native visible child 时，必须记录原生 child 证据和父子关系。
4. `thread/start` 等独立会话是 independent worker，不得登记为 native child。
5. 只有真实 child 启动失败才允许一次性 fallback，并记录失败证据、原因和 worker 身份。
6. 模型选择遵循用户显式配置或目标仓库规范；没有配置时先询问。
7. 每个 WO 只绑定一个执行体；重启或兜底必须追加记录。

## 6. 分发留痕

每次分发记录：

```text
WO：
TD：
executor_type：
launch_method：
executor_id：
visibility：
模型：
parent_execution_id：
subagent_start_status：
仓库/worktree：
分支：
输入版本：
输出位置：
状态：
开始时间：
结束时间：
收口证据：
```

状态只允许：

```text
running / completed / failed / interrupted
```

## 7. 收敛规则

1. 逐张 WO 检查范围内文件和验收结果。
2. 任一 worker failed 或 interrupted 时，不声称整体完成。
3. 出现矛盾结论时先列证据和分歧，不直接择优。
4. 需要圆桌时按 [roundtable-protocol.md](roundtable-protocol.md) 另行安排；不把单 worker 输出称为圆桌。
5. 主会话不得代填 worker 验收结果。
6. 全部合并前保持 registry 中对应 WO 为 active；验收和收口完成后再 complete。
