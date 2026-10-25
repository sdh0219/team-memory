#!/usr/bin/env bash
# team-memory 技能家族安装脚本：遍历 skills/ 下所有技能目录（team-memory、team-digest……），
# 逐一复制到各 agent 的技能目录。
# 用法: ./install.sh [--zcode|--agents|--claude]   不带参数则装到全部三个目录。
set -euo pipefail

SKILLS_DIR="$(cd "$(dirname "$0")/.." && pwd)/skills"

install_skill_to() {
  local skill="$1" base="$2"
  local dest="$base/$skill"
  # 只允许写入家目录之下，防御 HOME 被设为空值或异常路径
  case "$dest" in
    "$HOME"/*) ;;
    *) echo "拒绝异常目标目录: $dest"; exit 1 ;;
  esac
  mkdir -p "$base"
  rm -rf "$dest"
  cp -r "$SKILLS_DIR/$skill" "$dest"
  echo "OK 已安装 $skill 到 $dest"
}

install_all_to() {
  local base="$1" skill_path
  [ -d "$SKILLS_DIR" ] || { echo "找不到技能目录: $SKILLS_DIR"; exit 1; }
  for skill_path in "$SKILLS_DIR"/*/; do
    install_skill_to "$(basename "$skill_path")" "$base"
  done
}

only=""
if [ $# -gt 0 ]; then
  case "$1" in
    --zcode|--agents|--claude) only="${1#--}" ;;
    *) echo "用法: $0 [--zcode|--agents|--claude]"; exit 1 ;;
  esac
fi

case "$only" in
  zcode)  install_all_to "$HOME/.zcode/skills" ;;
  agents) install_all_to "$HOME/.agents/skills" ;;
  claude) install_all_to "$HOME/.claude/skills" ;;
  "")     install_all_to "$HOME/.zcode/skills"
          install_all_to "$HOME/.agents/skills"
          install_all_to "$HOME/.claude/skills" ;;
esac
