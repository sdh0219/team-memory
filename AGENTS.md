# AGENTS.md — team-memory 仓库规则

这是 team-memory 的源码仓库，同时是 team-memory 协议的**活样例**：本仓库用自己的协议管理自己
（见 `.memory/`）。

## 项目结构

- `skills/team-memory/` — 记忆层技能本体；`skills/team-digest/` — 周报蒸馏技能
- `docs/` — 协议规范与 FAQ（中英双语）；`examples/` — 示例项目记忆文件
- `scripts/` — 安装脚本（install.sh / install.ps1）与记忆校验/归档工具（validate_memory.py / archive_log.py）
- `hooks/` — Stop 钩子模板（第三道保险）；`.github/workflows/` — CI 校验记忆文件

## 硬规矩

1. **协议六处同步**：改协议文字必须同步 skills/team-memory/SKILL.md、docs/protocol.md、
   docs/protocol_EN.md、README.md、README_EN.md、examples/AGENTS.md，缺一即回工。
2. CI 会跑 `scripts/validate_memory.py` 校验 `.memory/` 与 `examples/memory/`，红线：STATE ≤50 行、
   LOG 单条 ≤10 行、日期新在上、不写密钥。
3. 仓库维护者本机 git 推 GitHub 需走本地代理（127.0.0.1:7897）。

## Agent 记忆协议（每个会话必做）

开工前：
1. 读 .memory/STATE.md（必读，很短）
2. 仅当任务需要历史细节时，再查 .memory/LOG.md 和 git log --oneline -15

收工前（阶段性工作结束）：
1. 更新 .memory/STATE.md：完成项移出"正在做"，更新"下一步"
2. 在 .memory/LOG.md 顶部追加一条记录（日期/agent 名/结论/改动文件/遗留），≤ 10 行

纪律：STATE.md 直接改写不追加；LOG.md 只追加；细节写进 commit message；
「正在做」两周没动就更新或回退；不把密钥、token 等敏感信息写入记忆文件。
