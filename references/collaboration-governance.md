# 协作执行体治理

本协议治理 WO / 开发子任务的执行体选择、降级、留痕和收口。圆桌分析会话不属于 WO 执行体，见 [roundtable-protocol.md](roundtable-protocol.md)。

## 1. 默认与优先级

1. 目标仓库显式执行体政策优先。
2. 用户明确指令优先于仓库默认，但不得违反安全底线。
3. 无目标政策和用户指令时，主会话串行执行。
4. 不因吞吐压力把可见分析会话、后台进程或普通命令输出伪装成执行体。

执行体模式：

| 模式 | 含义 | 使用条件 |
|---|---|---|
| `main-session-serial` | 主会话串行执行 | 默认；目标政策缺失、执行体能力缺失或任务不适合隔离 |
| `invisible-executor` | 主持人会话内置不可见子代理或用户确认的等价受控执行器 | 目标仓库要求 WO 执行体不可见 |
| `visible-subagent` | 客户端原生 visible child | 目标仓库明确允许或首选可见子智能体 |
| `independent-worker` | 独立 worker 会话 | 目标仓库允许，或作为真实 child 启动失败后的一次性兜底 |

## 2. 启动前检查

1. 读取目标仓库 `AGENTS.md`、流程规范和工单中的执行体政策。
2. 确认用户是否显式指定执行体或模型。
3. 确认 WO、分支、worktree、允许修改文件、验收命令和输出位置完整。
4. 确认执行体工具真实可用。
5. 确认目标政策允许当前执行体类型。
6. 确认文件范围不与其他 active WO 重叠。

任一条件缺失时使用主会话串行、停止询问或登记延期；不得静默替换执行体类型。

## 3. 身份与启动证据

每次执行体分发必须记录：

```text
WO：
TD：
executor_type：
launch_method：
executor_id：
visibility：
model：
parent_execution_id：
subagent_start_status：
branch：
worktree：
allowed_files：
output_location：
status：
started_at：
ended_at：
```

规则：

1. `visible-subagent` 只能来自客户端原生 child 创建能力，例如 `collaboration.spawn_agent`，并记录真实 parent/child 关系。
2. `app-server thread/start` 或其他独立会话启动方式是 `independent-worker`，不得登记为 `visible-subagent`。
3. `invisible-executor` 必须是主持人内置不可见子代理或用户确认的等价受控执行器。
4. `subagent_start_status=started` 必须有真实启动响应或平台元数据。
5. 模型、任务边界、输出位置不得由主会话推测代填。

## 4. 一次性兜底

只有目标政策允许、且真实 child 启动失败时，才允许从 child 降级为 independent worker。

必须记录：

```text
executor_type=fallback-worker
launch_method=<independent-worker-launch-method>
subagent_start_status=failed
subagent_start_error：
fallback_reason：
worker_id：
worker_model：
worker_scope：
worker_output：
```

以下情况不构成 child 启动失败：

1. 主会话调用参数错误。
2. 主会话误触发无关工具。
3. 任务暂停、用户转向或证据不足。
4. 未尝试启动 child。

不允许连续兜底。fallback worker 结束后不得再启动第二个 fallback 替代同一 WO；继续执行只能回到主会话串行或重新按目标政策启动合格 child。

## 5. 状态与收口

状态只允许：

```text
running / completed / failed / interrupted
```

执行结束或确定终止后必须记录：

1. 最终状态。
2. 验收结果或失败原因。
3. 输出位置。
4. 范围外发现。
5. 未完成项。
6. 文档逻辑归档声明。
7. 关闭、归档或终止执行体的证据。

收口证据包括平台响应、会话状态、最终消息、归档响应或目标仓库要求的等价记录。归档或关闭失败必须登记待确认事项，不得伪造成功。

## 6. 禁止事项

1. 用 shell 后台进程、普通命令输出或主持人自答冒充模型执行体。
2. 把 independent worker 登记为 native child。
3. 在目标政策禁止可见执行体时改用可见 worker。
4. 未证明 child 失败就使用 fallback。
5. 主会话代填执行体验收结果。
6. 执行体结束后不记录收口证据。
7. 用圆桌分析会话承担 WO 实施工单。

## 7. 与工单和 registry 的关系

1. 主会话仍是唯一发号和 registry 写入方。
2. 执行体只使用 prompt 中显式给定的 WO/TD。
3. WO 保持 `active` 直到验收和执行体收口完成。
4. 合并后才能置为 `completed`。
5. 执行体身份记录可保存在 WO 的执行记录、独立过程文档或目标仓库指定的治理台账，但必须可追溯。
