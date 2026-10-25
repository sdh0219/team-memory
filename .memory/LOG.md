# 操作日志（只追加，最新在上）

## 2026-10-26 01:25 · ZCode

- 做了：第二梯队优化——协议同步检查器（正负例验证过）+ CI 第三道步骤、社交分享图 1280x640、
  GitHub topics（agent-memory/ai-agents/claude-code 等 10 个，PUT 200）
- 改动：scripts/sync_check.py、.github/workflows/validate.yml、assets/social-preview.{svg,png}、.memory/
- 遗留：social preview 需用户在仓库 Settings → Social preview 手动上传 assets/social-preview.png（API 不支持）

## 2026-10-26 00:40 · ZCode

- 做了：token benchmark 落地——scripts/benchmark.py + 双语文档；susu-tools 实测冷读 447,024 tok vs STATE 221 tok
- 改动：scripts/benchmark.py、docs/benchmark.md、docs/benchmark_EN.md、README.md、README_EN.md、.memory/
- 遗留：宣传片 82s 大扩编版渲染中；benchmark 数字已用于视频 S14 幕

## 2026-10-25 23:30 · ZCode

- 做了：抖音宣传片进入渲染（8 场景 Remotion 合成 + 三位 AI 娘原创角色）
- 改动：ai-video/projects/team-memory-promo/（不属于本仓库，此处仅记录）
- 遗留：渲染与终检未完；发布后回填数据

## 2026-10-25 19:00 · ZCode

- 做了：修复安装脚本 set -u 下 local 同行展开顺序崩溃；本机三目录重装验证
- 改动：scripts/install.sh
- 遗留：无

## 2026-10-25 17:00 · ZCode

- 做了：全仓库文档一致性体检；修复示例三处穿帮（幽灵日期引用、npm/Maven 栈冲突、.py 残留）
- 改动：examples/AGENTS.md、examples/memory/LOG.md
- 遗留：benchmark 文档待实测数据
