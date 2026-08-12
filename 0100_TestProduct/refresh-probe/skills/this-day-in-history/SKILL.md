---
name: this-day-in-history
description: >
  Report one random "on this day" historical fact for today's date, from
  some random number of years ago. **Added in refresh-probe v0.0.3** — this
  skill's mere existence (not just a version number) is the refresh signal:
  if a session can invoke this skill at all, the plugin refresh delivered a
  brand-new file, not just an edited one. Use when the user asks "what
  happened today in history", "this day in history", "random historical
  fact for today", or any variant of testing whether refresh-probe's newest
  skill landed.
metadata:
  version: "0.0.1"
  role: test
  temporary: true
---

# this-day-in-history

Second probe skill for exercising the Cowork plugin-refresh cycle
(writing-cowork task `7c1b9e04`). Complements `test-version`: that skill
proves a version *number* updated; this skill proves a *new file* arrived,
which is a stronger signal — a stale cache could plausibly still serve an
old file with the version string hand-edited in place, but it can't serve a
skill that never existed in the old cache at all.

**This whole plugin is throwaway.** See `test-version`'s SKILL.md for full
context on why refresh-probe exists and its cleanup plan.

## Arguments

None.

## Execution

1. Determine today's date (ask the user's local session for it, or use
   whatever the current date context already provides — do not guess).
2. Pick a random number of years ago, between 5 and 500.
3. Use a web search to find one real, verifiable historical event that
   occurred on today's month and day, that many years ago (or the closest
   well-documented event you can find for that date if nothing notable
   happened in that exact year — say so explicitly if you substitute).
4. Report it plainly, in the output template below. Do not fabricate a fact
   — if search comes back empty or unclear, say that instead of inventing
   one.

## Output template

```
this-day-in-history (refresh-probe v0.0.3)
  Date checked: <today's date>
  Years ago: <N>
  Year: <today's year - N>
  Event: <one or two sentence factual summary>
  Source: <url or publication, if available>
```

## Standalone use

Requires a web search capability in the invoking session. If none is
available, report that plainly rather than guessing a historical fact from
memory — this skill exists to test refresh delivery, not to demonstrate
recall, and a fabricated "fact" would defeat the point of the test.
