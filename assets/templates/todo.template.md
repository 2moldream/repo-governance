# 全局待办登记册

本登记册是开放事项索引，不替代设计决策或工单验收记录。

| ID | 状态 | 事项 | 来源 | 负责人 | 验收证据 | 结果 |
|---|---|---|---|---|---|---|
| TD-{{todo_number}} | open | {{item}} | {{source}} | {{owner}} | {{evidence_required}} | pending |

## 规则

1. 状态只使用 `open` 或 `closed`。
2. 新事项默认 `open`。
3. 关闭必须有验收证据和命令或产物引用。
4. 缺证据保持 open 或需确认。
5. 未解决技术失败不得转成业务通过。
6. 历史行不删除，关闭结果原地记录。

## 关闭记录

| ID | 关闭日期 | 证据 | 结果 |
|---|---|---|---|
| TD-{{todo_number}} | {{closed_date_or_empty}} | {{evidence_or_empty}} | {{closed_result_or_empty}} |
