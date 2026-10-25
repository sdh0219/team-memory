# -*- coding: utf-8 -*-
"""team-memory token benchmark：实测"无记忆层接手"vs"team-memory 接手"的读取开销。

口径：
- 无记忆层：agent 冷启动需要通读仓库全部 git 跟踪的文本文件
  （.md/.txt/.ts/.tsx/.js/.py/.json/.yml/.html/.css/.sh/.toml/.cfg/.svg 等）。
- team-memory：只读 .memory/STATE.md（协议规定 ≤50 行的活文档）。
- token 估算：CJK 字符按 1 token/字，其余按 3.8 字符/token（GPT 系分词器的常见比例）。
  这是可复现的近似口径，不是某家 API 的精确计数。

用法：
  python scripts/benchmark.py                    # 测本仓库自己
  python scripts/benchmark.py --repo <path>      # 测任意 git 仓库
输出：JSON 一行（stdout），含 files/tokens/bytes 与对比倍数。
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TEXT_EXT = {
    ".md", ".txt", ".rst", ".ts", ".tsx", ".js", ".jsx", ".mjs", "cjs",
    ".py", ".json", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".html",
    ".css", ".scss", ".sh", ".ps1", ".svg", ".xml", ".sql", ".go", ".java",
}
CJK = re.compile(r"[\u3000-\u9fff\uff00-\uffef]")


def approx_tokens(text: str) -> int:
    cjk = len(CJK.findall(text))
    other = len(text) - cjk
    return cjk + (other * 10 + 37) // 380


def measure(repo: Path):
    files = subprocess.run(
        ["git", "-C", str(repo), "ls-files"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    total_tokens = total_bytes = n = 0
    for rel in files:
        p = repo / rel
        if p.suffix.lower() not in TEXT_EXT or not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        total_tokens += approx_tokens(text)
        total_bytes += len(text.encode("utf-8"))
        n += 1
    return n, total_tokens, total_bytes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parent.parent))
    args = ap.parse_args()
    repo = Path(args.repo).resolve()

    n, repo_tokens, repo_bytes = measure(repo)
    state = repo / ".memory" / "STATE.md"
    state_tokens = approx_tokens(state.read_text(encoding="utf-8")) if state.exists() else 0
    ratio = round(repo_tokens / state_tokens, 1) if state_tokens else None

    print(json.dumps({
        "repo": repo.name,
        "files_read": n,
        "repo_tokens": repo_tokens,
        "repo_kb": round(repo_bytes / 1024, 1),
        "state_tokens": state_tokens,
        "ratio": ratio,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
