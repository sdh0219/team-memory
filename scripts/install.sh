#!/usr/bin/env bash
# team-memory 安装脚本：把 skills/team-memory 复制到各 agent 的技能目录。
# 用法: ./install.sh [--zcode|--agents|--claude]   不带参数则装到全部三个目录。
set -euo pipefail

SRC="$(cd "$(dirname "$0")/.." && pwd)/skills/team-memory"

install_to() {
  local base="$1" dest="$base/team-memory"
  # 只允许写入家目录之下，防御 HOME 被设为空值或异常路径
  case "$dest" in
    "$HOME"/*) ;;
    *) echo "拒绝异常目标目录: $dest"; exit 1 ;;
  esac
  mkdir -p "$base"
  rm -rf "$dest"
  cp -r "$SRC" "$dest"
  echo "OK 已安装到 $dest"
}

only=""
if [ $# -gt 0 ]; then
  case "$1" in
    --zcode|--agents|--claude) only="${1#--}" ;;
    *) echo "用法: $0 [--zcode|--agents|--claude]"; exit 1 ;;
  esac
fi

case "$only" in
  zcode)  install_to "$HOME/.zcode/skills" ;;
  agents) install_to "$HOME/.agents/skills" ;;
  claude) install_to "$HOME/.claude/skills" ;;
  "")     install_to "$HOME/.zcode/skills"
          install_to "$HOME/.agents/skills"
          install_to "$HOME/.claude/skills" ;;
esac
