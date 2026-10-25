# -*- coding: utf-8 -*-
"""team-memory 协议六处同步检查器。

协议文字有六个副本：4 处中文（skills/team-memory/SKILL.md、docs/protocol.md、
README.md、examples/AGENTS.md）+ 2 处英文（docs/protocol_EN.md、README_EN.md）。
手动同步必然漂移，本脚本机器保证一致：提取每处 markdown 代码块中的协议段
（从「## Agent 记忆协议」/「## Agent memory protocol」标题行起到块尾），
缩进归一化后要求同语言内部逐字一致。CI 在每次 push 时运行本检查。

用法: python scripts/sync_check.py    # 全部一致退出 0 并打印摘要；否则列出变体退出 1
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZH_FILES = ["skills/team-memory/SKILL.md", "docs/protocol.md", "README.md", "examples/AGENTS.md"]
EN_FILES = ["docs/protocol_EN.md", "README_EN.md"]
ZH_TITLE = "## Agent 记忆协议"
EN_TITLE = "## Agent memory protocol"


def protocol_segment(path, title):
    """提取文件中协议代码块的协议段；找不到返回 None。"""
    text = path.read_text(encoding="utf-8")
    for m in re.finditer(r"```markdown\n(.*?)```", text, re.S):
        block = m.group(1)
        if title in block:
            lines = block.splitlines()
            start = next(i for i, l in enumerate(lines) if l.strip().startswith(title))
            seg = [l.strip() for l in lines[start:] if l.strip()]
            return "\n".join(seg)
    return None


def main():
    errors = []
    for label, files, title in (("zh", ZH_FILES, ZH_TITLE), ("en", EN_FILES, EN_TITLE)):
        segments = {}
        for f in files:
            seg = protocol_segment(ROOT / f, title)
            if seg is None:
                errors.append("[error] {}: 未找到协议代码块（{}…）".format(f, title))
            else:
                segments[f] = seg
        if len(segments) > 1:
            variants = {}
            for f, seg in segments.items():
                variants.setdefault(seg, []).append(f)
            if len(variants) == 1:
                continue  # 全部文件逐字一致
            errors.append("[error] {} 协议块存在 {} 个变体:".format(label, len(variants)))
            for i, (seg, fs) in enumerate(sorted(variants.items(), key=lambda kv: -len(kv[1]))):
                errors.append("  变体{} ({} 处): {}".format(i + 1, len(fs), ", ".join(fs)))
                errors.append("    首行: " + seg.splitlines()[0][:70])
    if errors:
        print("\n".join(errors))
        n = len([e for e in errors if e.startswith("[error]")])
        print("\n{} errors".format(n))
        return 1
    print("All protocol blocks in sync ({} zh + {} en).".format(len(ZH_FILES), len(EN_FILES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
