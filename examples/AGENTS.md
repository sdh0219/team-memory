# 示例：某 Web 项目的 AGENTS.md（节选）

下面是一个典型项目 `AGENTS.md` 的样子：上半部分是普通的项目规则，
下半部分是 team-memory 的协议段落。协议段落由 skill 初始化时自动写入，
不装 skill 也可以手动粘进去。

```markdown
# 项目规则

构建：npm run build；测试：npm test（改动后必跑）。
src/core/ 目录重构前先问维护者。
所有金额字段一律用分（int）表示，禁止浮点。

## Agent 记忆协议（每个会话必做）

开工前：
1. 读 .memory/STATE.md（必读，很短）
2. 仅当任务需要历史细节时，再查 .memory/LOG.md 和 git log --oneline -15

收工前（阶段性工作结束）：
1. 更新 .memory/STATE.md：完成项移出"正在做"，更新"下一步"
2. 在 .memory/LOG.md 顶部追加一条记录（日期/agent 名/结论/改动文件/遗留），≤ 10 行

纪律：STATE.md 直接改写不追加；LOG.md 只追加；细节写进 commit message；
「正在做」两周没动就更新或回退；不把密钥、token 等敏感信息写入记忆文件。
```
