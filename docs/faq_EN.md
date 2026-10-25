# FAQ

**Q1: Won't memory files pollute repo history?**
They enter history — by design. It's the project's operating ledger, versioned alongside
code. If it grows too long, archive `.memory/LOG.md` into `LOG-archive.md` past 100
entries and keep only recent ones in the main file.

**Q2: What if two agents finish simultaneously and both edit STATE.md?**
True concurrent writes are rare (most flows are sequential). If it happens, resolve the
git conflict: keep both LOG entries, hand-merge STATE — its four-section structure makes
that fast.

**Q3: How is this different from built-in memory in Claude Code / ZCode?**
Built-in user memory is "one per tool, follows the user" — it holds your preferences.
team-memory is "one per project, follows the repo" — it holds project progress and
handoffs. One answers "what does this person like", the other "where is this project".
They complement each other.

**Q4: Why not a vector DB / memory service (MemOS, mem0)?**
Those are the heavyweight end of the spectrum, solving storage and scheduling for huge
memory volumes. "Help the next agent resume with minimal tokens" is solved better and
cheaper by one 50-line living document than by any retrieval system. If your memory
volume eventually demands retrieval, upgrade then — these two Markdown files are the
seed data.

**Q5: Isn't STATE.md redundant with git log?**
git log records which files changed; STATE records where the project stands and what
comes next. The latter requires synthesis across commits — exactly the conclusion an
agent re-derives from full history every time, and exactly what's worth caching.

**Q6: How often should LOG be cleaned?**
Never, by default. It's an append-only ledger read only a few entries deep when tracing
history. Archive per Q1 if it bothers you.

**Q7: Can I use this on private repos / company projects?**
The protocol is a few files plus a paragraph — works in any git environment with any
agent. Just make sure `.memory/` doesn't leak into public mirrors for sensitive projects.

**Q8: The agent won't write memory. Now what?**
Three layers of enforcement: the skill (active trigger) → the AGENTS.md protocol section
(passive constraint) → you saying "update the project memory" in the conversation (manual
fallback). The third always works.
