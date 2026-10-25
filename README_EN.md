<div align="center">
  <p>
    <img src="assets/banner.svg" alt="team-memory: shared memory layer for multi-agent teams" width="100%">
  </p>
  <p>
    <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/sdh0219/team-memory"></a>
    <a href="#3-quick-start"><img alt="Install" src="https://img.shields.io/badge/install-script%20%7C%20manual-111827"></a>
    <a href="#4-how-it-works"><img alt="Protocol" src="https://img.shields.io/badge/protocol-2_Markdown_files_%2B_AGENTS.md-2EA043?logo=git&amp;logoColor=white"></a>
    <a href="README.md"><img alt="Language" src="https://img.shields.io/badge/language-中文%20%7C%20English-1f6feb"></a>
    <a href="https://github.com/sdh0219/team-memory/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/sdh0219/team-memory?style=social"></a>
  </p>
  <p>
    <a href="#3-quick-start">Quick start</a>
    · <a href="#4-how-it-works">How it works</a>
    · <a href="#5-the-protocol">Protocol</a>
    · <a href="examples/">Examples</a>
    · <a href="docs/faq_EN.md">FAQ</a>
    · <a href="README.md">中文</a>
  </p>
</div>

---

**team-memory** stops your agents from losing each other's work: each agent resumes by
reading one living status file (≤ 50 lines) and leaves a distilled log entry (≤ 10 lines)
when done. The protocol lives in `AGENTS.md`, so **agents without any skill installed
still comply**. No server, no vector DB, git-native.

## Table of contents

- [1. What is this](#1-what-is-this)
- [2. Why files, not a memory service](#2-why-files-not-a-memory-service)
- [3. Quick start](#3-quick-start)
- [4. How it works](#4-how-it-works)
- [5. The protocol](#5-the-protocol)
- [6. Examples](#6-examples)
- [7. Documentation](#7-documentation)
- [8. Contributing](#8-contributing)
- [9. Star history](#9-star-history)
- [10. License](#10-license)

## 1. What is this

![How it works](assets/how-it-works.svg)

Three roles:

- **`.memory/STATE.md`** — living snapshot of current status, rewritten in place, ≤ 50 lines; the only file a new agent must read
- **`.memory/LOG.md`** — append-only handoff log, newest on top, ≤ 10 lines per entry, read on demand
- **`AGENTS.md` protocol section** — makes every agent (with or without the skill) follow the same read/write discipline

Memory files are tracked in git — they travel with the clone, in the one storage every
agent already knows how to read and write.

## 2. Why files, not a memory service

| | team-memory | MemOS / mem0 / Letta |
|---|---|---|
| Shape | Two Markdown files in your repo | Database + service + SDK |
| Dependencies | git literacy | Deployment, ops, API keys |
| Cross-tool | Shared by nature (every agent reads/writes files) | Per-tool integration |
| Memory scale | One project's handoff conclusions | Massive long-term memory |
| Best for | Solo devs / small teams running agent relays | Product-scale session memory |

Heavyweight systems solve "how to store and schedule vast memory". team-memory solves
the more common problem — **how the next agent resumes with the fewest tokens**. Opposite
ends of one spectrum; they even feed each other seed data.

## 3. Quick start

### 3.1 Script install (recommended)

```bash
git clone --depth 1 https://github.com/sdh0219/team-memory
cd team-memory
bash scripts/install.sh           # install into all three skill directories
bash scripts/install.sh --zcode   # or one only: --zcode / --agents / --claude
```

Windows (PowerShell):

```powershell
git clone --depth 1 https://github.com/sdh0219/team-memory
cd team-memory
powershell -File scripts\install.ps1               # all by default
powershell -File scripts\install.ps1 -Target zcode # or: zcode / agents / claude
```

Then tell your agent: “初始化 team-memory 记忆层” / "set up team-memory for this project".

### 3.2 Manual install

Copy `skills/team-memory/` into your agent's skill directory
(`~/.zcode/skills/`, `~/.agents/skills/`, or `~/.claude/skills/`).

### 3.3 No skill, just the protocol

Paste [the protocol](#5-the-protocol) into your project's `AGENTS.md` and create the two
files following [examples/](examples/) — the protocol depends on no tooling.

## 4. How it works

Two files under `.memory/`, strict division of labor:

| File | Role | Rule |
|---|---|---|
| `STATE.md` | Living status snapshot | Rewrite in place, never append, ≤ 50 lines |
| `LOG.md` | Append-only handoff log | Newest on top, ≤ 10 lines per entry |

Finishing a milestone means prepending one entry to `LOG.md`:

```
## 2026-10-25 21:40 · Codex
- Did: WeChat Pay callback signature verified end-to-end, notify_url persists correctly
- Touched: pay/wechat/callback.py, tests/test_wechat_callback.py
- Leftover: refund flow untouched; signing key comes from env WECHAT_PAY_KEY, never hardcode
```

Three disciplines carry the whole protocol: **rewrite STATE, never append; LOG is
append-only; details go into commit messages**. Full spec in
[docs/protocol_EN.md](docs/protocol_EN.md).

## 5. The protocol

Put this in your project's `AGENTS.md` (the skill writes it automatically at init):

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

## 6. Examples

[examples/](examples/) contains a complete realistic sample: a web project's
[AGENTS.md](examples/AGENTS.md), [STATE.md](examples/memory/STATE.md) and
[LOG.md](examples/memory/LOG.md). Copy the shape.

## 7. Documentation

- [Protocol spec](docs/protocol_EN.md) — full definitions, field tables, anti-patterns ([中文](docs/protocol.md))
- [FAQ](docs/faq_EN.md) — repo pollution? concurrent writes? vs built-in memory? misbehaving agents? ([中文](docs/faq.md))

## 8. Contributing

Issues and PRs welcome. When changing the protocol in `skills/team-memory/SKILL.md`,
please keep the protocol text consistent across both READMEs and the docs.

## 9. Star history

[![Star History Chart](https://api.star-history.com/svg?repos=sdh0219/team-memory&type=Date)](https://star-history.com/#sdh0219/team-memory&Date)

## 10. License

[MIT](LICENSE)
