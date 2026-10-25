# team-memory Protocol Specification

This is the complete definition of the protocol. Agents with the skill installed are
driven by the skill; agents without it follow the protocol section in the project's
`AGENTS.md` — the two are identical in content.

## 1. Overview

Three pieces:

| Component | Location | Purpose |
|---|---|---|
| State snapshot | `.memory/STATE.md` | Current project status; the only required read for a new agent |
| Handoff log | `.memory/LOG.md` | Append-only journal; read history details on demand |
| Protocol section | `AGENTS.md` | Tells every agent when to read, when to write, and how |

## 2. STATE.md rules

Four fixed sections, none may stay empty for long:

| Section | Content |
|---|---|
| `## Doing` | What is in progress, one item per line, including where it is stuck |
| `## Next steps` | What the successor should do, by priority, with entry points (files/docs) |
| `## Recently done` | Last 3-5 items, one line each: date + one-sentence conclusion + who |
| `## Pitfalls & conventions` | Past mistakes and binding project rules — the most valuable section |

- Whole file **≤ 50 lines**; if it doesn't fit, you are recording process instead of conclusions
- **Rewrite in place, never append**: replacing old content with current status is by design; history belongs to LOG.md and git
- Header notes last update time and author, so staleness is visible at a glance

## 3. LOG.md rules

Fixed three fields per entry, newest at the top:

```
## YYYY-MM-DD HH:mm · <agent or tool name>
- Did: <one-sentence conclusion>
- Touched: <files/directories>
- Leftover: <unfinished work, pitfalls, reminders for the next agent; "none" if empty>
```

- Each entry **≤ 10 lines**; details go into commit messages — entries carry conclusions and file lists only
- **Append-only, never rewrite**: to correct an old entry, append a correction, don't touch the original
- On takeover, read only the first 3-5 entries; dig deeper only if genuinely needed

## 4. The AGENTS.md section

Written into the project's `AGENTS.md` at init time (created if missing):

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

## 5. Division of labor with git

- The final home of detail is the **commit message**: LOG entries keep conclusions, cite commits when needed
- Memory files **must be tracked**: don't exclude `.memory/` in `.gitignore`; they travel with the clone
- On concurrent-finish git conflicts, keep both log entries and let the next agent merge
- Long-lived experiment branches may skip logging; add one summary entry when merging back

## 6. Anti-patterns

| Anti-pattern | Consequence | Do instead |
|---|---|---|
| Appending to STATE.md like a log | Hundreds of lines nobody reads | Rewrite in place, ≤ 50 lines |
| Process narratives in LOG entries | Dozens of lines each, tokens wasted | Conclusions only, details in commits |
| Finishing without updating memory | Next agent starts blind | Updating memory matters as much as the code |
| Secrets/tokens in memory files | In git history forever | Environment variables only |
| Skill installed but no AGENTS.md section | Agents without the skill don't comply | Put the protocol in AGENTS.md too |
