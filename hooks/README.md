# hooks/ — 第三道保险：会话结束自动提醒

team-memory 的三道保险：

1. **skill 主动触发**：装了 team-memory 技能的 agent 会在开工/收工时走协议
2. **AGENTS.md 被动约束**：协议写在项目 AGENTS.md 里，没装技能的 agent 也遵守
3. **hooks 强制提醒**（本目录）：会话结束时工具自动弹提醒，"更新记忆了吗？"——前两道都失守时兜底

## 文件

- `zcode-hooks.json` — ZCode 的 hooks 配置模板
- `claude-hooks.json` — Claude Code 的 hooks 配置模板

## 用法

把对应 JSON 的内容合并进工具的 settings 配置（ZCode：`~/.zcode/settings.json`；
Claude Code：`~/.claude/settings.json`），具体字段以各工具当前文档为准——本目录文件是
**模板**，作用是让 agent 在会话结束/停止时收到一句提醒：

> 收工前更新 .memory/STATE.md 并在 .memory/LOG.md 顶部追加交接记录（≤10 行）。

提醒文案可按项目需要改写。配置完成后新会话生效。
