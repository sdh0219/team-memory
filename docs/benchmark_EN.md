# team-memory token benchmark: measured takeover cost

> How many tokens does a cold-start agent burn reading a repo with no memory layer —
> and with team-memory? Reproducible numbers below.

## TL;DR

| Scenario | What gets read | Measured tokens | Ratio |
|---|---|---|---|
| ❄️ No memory layer (cold read) | All 261 text files of susu-tools | **447,024** | — |
| ⚡ team-memory takeover | Only `.memory/STATE.md` (≤50-line living doc) | **221** | **≈ 1/2000** |
| team-memory repo, self-test | Its own 24 files vs its own STATE.md | 8,384 vs 221 | ≈ 1/38 |

The 447k tokens are not a one-time cost — **every new session, every agent shift burns them
again**. team-memory turns that into a 221-token read, pinned at ≤50 lines by protocol, so it
never grows with the project.

## Method & reproduction

```bash
python scripts/benchmark.py                    # measure this repo
python scripts/benchmark.py --repo <any-git-repo>
```

- **Cold side**: every text file tracked by git (.md/.ts/.py/.json/.yml and 20+ more extensions)
  — a conservative lower bound for "agent figures out the project"; real sessions add
  dependency docs and exploratory searches.
- **Memory side**: only `.memory/STATE.md` (the sole required read at takeover, by protocol).
  LOG.md / git log are on-demand deep reads, not counted.
- **Token estimate**: 1 token per CJK char, 3.8 chars/token otherwise (typical GPT-family
  ratio). An approximation — it does not affect the ~2000× order of magnitude.

## Why this comparison is honest

- The cold side is not inflated: no binaries or lockfiles; exploratory multi-pass searching
  that real agents do is excluded.
- The memory side is not deflated: STATE.md is the complete required read; 221 tokens is
  measured from this repo's own STATE.md.
- The gap widens with size: susu-tools is a mid-size 261-file repo; thousand-file repos put
  the cold side in the millions.

## Limitations

- Estimate deviates ±20% from real tokenizers; magnitude unaffected.
- "Cold start reads everything" depends on agent strategy — but any sufficiently careful
  takeover covers core code and docs; a full read is the common-strategy lower bound.
- Write-side cost (updating STATE/LOG at handoff) is excluded: ≤10 lines per LOG entry,
  ≤50 lines per STATE — roughly 1/1000 of one cold read.
