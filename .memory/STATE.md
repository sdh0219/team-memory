# 项目状态（活文档 · 最后更新：2026-10-25 · ZCode）

## 正在做

- 抖音宣传片制作（ai-video 工厂 team-memory-promo 项目，8 场景已编码，渲染中）
- 探索家族新成员 team-rules / team-review 的可行性

## 下一步

- 量化 benchmark 文档：实测"有/无记忆层"的 agent 接手 token 对比
- 把 hooks 自动提醒推广给常用项目（模板在 hooks/）
- 宣传片发布后回填真实数据（播放/星标）

## 近期完成

- 2026-10-25：家族扩展（team-digest + 校验/归档工具 + 分层术语 + 生命周期纪律）
- 2026-10-25：示例自洽修复（技术栈统一 Maven、LOG 日期引用补齐）
- 2026-10-25：安装脚本 set -u 展开顺序 bug 修复（db7f8c2）

## 坑与约定

- 改协议必须六处同步：skills/team-memory/SKILL.md、docs/protocol.md、docs/protocol_EN.md、
  README.md、README_EN.md、examples/AGENTS.md
- 本机 git 推 GitHub 走代理：git -c http.proxy=http://127.0.0.1:7897
- 本机 `python` 是商店占位符，跑脚本用 anaconda 或 bilinote 运行时
