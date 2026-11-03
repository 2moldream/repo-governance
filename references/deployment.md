# 部署与版本

`VERSION` 是源码版本事实源。默认部署方式是 symlink，源码分支更新后运行时入口即时跟随。

## 安装

```bash
python3 scripts/deploy.py --destination ~/.codex/skills/repo-governance
```

安装脚本会：

1. 校验 `SKILL.md` 和 `VERSION` 存在。
2. 校验版本符合语义化版本格式。
3. 检查目标路径不存在。
4. 创建相对 symlink。
5. 回读目标入口和版本文件。

目标路径已存在时失败；更新或覆盖必须由用户显式处理，不由脚本静默替代。

## Copy 模式

无法使用 symlink 的环境执行：

```bash
python3 scripts/deploy.py --destination <skills-dir>/repo-governance --mode copy
```

Copy 排除：

```text
.git
__pycache__
*.py[cod]
.DS_Store
.venv
.pytest_cache
```

## 验证

```bash
python3 <skill-validator> <skills-dir>/repo-governance
test -f <skills-dir>/repo-governance/SKILL.md
test -f <skills-dir>/repo-governance/VERSION
```

Codex 已运行的会话可能不会即时刷新技能索引；安装后优先在新会话中验证能否按 description 触发。

本 Skill 是 explicit-only：

```yaml
policy:
  allow_implicit_invocation: false
```

普通开发任务不得自动加载；只有用户明确要求初始化仓库治理、诊断历史仓库治理或使用 `$repo-governance` 时才调用。

## 更新

Symlink 模式：

1. 源码仓库切到已验收版本。
2. 确认全局链接仍指向本仓库。
3. 重跑目标 quick validate。

Copy 模式：

1. 删除旧 copy 前必须确认其中没有本地改动。
2. 重新执行 copy 安装。
3. 运行 quick validate。

## 回退

删除全局入口：

```bash
unlink ~/.codex/skills/repo-governance
```

仅当确认是 copy 安装时才使用目录删除；不得对不明来源目录执行强制删除。
