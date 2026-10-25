# team-memory

![type](https://img.shields.io/badge/type-skill-9B4DE0?logo=markdown&logoColor=white)
![protocol](https://img.shields.io/badge/protocol-2_Markdown_files_%2B_AGENTS.md-2EA043?logo=git&logoColor=white)
![license](https://img.shields.io/github/license/sdh0219/team-memory)
![stars](https://img.shields.io/github/stars/sdh0219/team-memory?style=social)
![last commit](https://img.shields.io/github/last-commit/sdh0219/team-memory)

A file-based shared memory layer for multi-agent coding teams — two Markdown files and one protocol let any agent pick up where the last one left off. No server, no vector DB, git-native.

Heavyweight memory systems (MemOS, mem0, Letta…) give agents database-backed memory as infrastructure. **team-memory is the other end of the spectrum**: two plain Markdown files inside your repo, plus a short protocol in `AGENTS.md`. If your project runs on git, it already has everything team-memory needs.

## Why

When agents work on the same project one after another, each new agent starts blind: it either re-reads the whole codebase (expensive in tokens) or guesses what the last one did (dangerous). Every tool also keeps its own private memory — Claude Code, Codex, Cursor don't share it. Files inside the repo are the only storage every agent can already read and write.

## How it works

Two files under `.memory/`:

| File | Role | Rule |
|---|---|---|
| `.memory/STATE.md` | Living snapshot of current status | Rewrite in place, never append, ≤ 50 lines. The only file a new agent must read. |
| `.memory/LOG.md` | Append-only handoff log | Newest entry on top, each ≤ 10 lines. Read only when history detail is needed. |

Details too big for an entry go into git commit messages — memory files carry conclusions and file lists, not process recordings.

## Quick start

**As a skill** (your agent scaffolds and follows the protocol automatically):

```bash
# ZCode
git clone --depth 1 https://github.com/sdh0219/team-memory ~/.zcode/skills/team-memory

# Cross-agent directory (Claude Code / Codex / …)
git clone --depth 1 https://github.com/sdh0219/team-memory ~/.agents/skills/team-memory

# Claude Code
git clone --depth 1 https://github.com/sdh0219/team-memory ~/.claude/skills/team-memory
```

Then tell your agent: “初始化 team-memory 记忆层” / "set up team-memory for this project".

**Without any skill**, paste the protocol below into your project's `AGENTS.md` and create the two files.

## The protocol

```markdown
## Agent memory protocol (every session)

Before work:
1. Read .memory/STATE.md (required, very short)
2. Only if the task needs history detail, check .memory/LOG.md and git log --oneline -15

Before finishing a milestone:
1. Update .memory/STATE.md: move done items out of "doing", update "next steps"
2. Prepend one entry to .memory/LOG.md (date / agent / conclusion / files touched / leftovers), ≤ 10 lines

Discipline: rewrite STATE.md, never append to it; LOG.md is append-only; details go
into commit messages; never write secrets or tokens into memory files — they live in git history.
```

## 中文说明

让一群 agent 接力干活时不再互相失忆：每个 agent 开工只读 50 行的 `.memory/STATE.md` 就能接上，收工时往 `.memory/LOG.md` 顶部留一条 ≤10 行的蒸馏记录。协议写进项目的 `AGENTS.md`，所以不装任何东西的 agent 也会遵守；装上 skill 则由它自动搭建和执行这套协议。记忆文件随仓库进 git，克隆即共享，零基础设施。

## See also

- [MemOS](https://github.com/MemTensor/MemOS) — the heavyweight end: a memory operating system with vector/graph stores and cloud scheduling
- [AGENTS.md](https://agents.md) — the open standard for agent instruction files, which this protocol ships inside

## License

[MIT](LICENSE)
