# 项目状态（活文档 · 最后更新：2026-10-26 · ZCode）

## 正在做

- 抖音宣传片大扩编（14 幕 82s 版渲染中，新增玄机 solo/校验器/实测对比三幕）

## 下一步

- 宣传片发布（勾选 AI 生成声明 + BGM CC-BY 署名），发布后回填播放/星标数据
- 家族新成员 team-rules / team-review 可行性探索

## 近期完成

- 2026-10-26：协议六处同步检查器 sync_check.py 进 CI（篡改测试能抓）；topics 上线；分享图就绪
- 2026-10-26：token benchmark 上线——susu-tools 实测冷读 447,024 tok vs STATE 221 tok（≈2000×）
- 2026-10-25：hooks/（Stop 钩子模板）+ CI 校验 + 仓库自食狗粮（.memory/ + 根 AGENTS.md）
- 2026-10-25：家族扩展（team-digest + 校验/归档工具 + 分层术语 + 生命周期纪律）
- 2026-10-25：安装脚本 set -u 展开顺序 bug 修复（db7f8c2）

## 坑与约定

- 改协议必须六处同步：skills/team-memory/SKILL.md、docs/protocol.md、docs/protocol_EN.md、
  README.md、README_EN.md、examples/AGENTS.md
- 本机 git 推 GitHub 走代理：git -c http.proxy=http://127.0.0.1:7897
- 本机 `python` 是商店占位符，跑脚本用 anaconda 或 bilinote 运行时
- 渲染 Remotion 前先杀 3000 端口残留 node（netstat 找 LISTENING PID → taskkill），否则随机 404

