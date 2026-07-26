# Memory Gating Test — does Cowork honor Claude Code memory settings?

**Status:** Armed 2026-07-25, awaiting a fresh session. **Result: not yet recorded.**
**Owner:** Jamie (must be run in a *new* Cowork session — cannot be self-tested from the session that armed it).
**Blocks:** the choice between Option A and Option B in `memory_management_recommendation_2026-07-25.md`, and everything in stage 3 (porting to the plugin).

---

## Why this test exists

Every memory control found in the 2026-07-25 research — `autoMemoryEnabled`, `autoMemoryDirectory`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY`, `/memory`, `PreToolUse` hooks — is documented for **Claude Code CLI**. Cowork's memory runs through a different mechanism (`mcp__remote-devices__project_memory_read` / `project_memory_write`, an MCP tool on the desktop bridge). Whether CLI settings bind it is unverified, and Cowork has diverged from documented CLI behavior before (marketplace cache, `extraKnownMarketplaces`, plugin validation).

This matters beyond this repo: **consumer vaults run in Cowork.** If settings don't bind there, the plugin must not ship advice premised on a control that doesn't work.

## What has been armed

`.claude/settings.json` now contains:

```json
"autoMemoryEnabled": false,
"autoMemoryDirectory": "~/code/writing-cowork/1_Project/Memory"
```

Both are set deliberately. They produce **distinguishable** outcomes rather than confounding each other (see below). Note that `.claude/settings.json` is JSON and cannot carry comments — this is the one place the plugin's managed-block marker convention cannot be applied, so its provenance is documented here instead.

Also newly present: a repo-root `CLAUDE.md` router, which this test doubles as a check on.

## Procedure

1. **Start a brand-new Cowork session** in this project. Do not continue the session that armed the test — settings are read at session start.
2. If a **workspace trust dialog** appears, accept it. Per the docs, a project-level `autoMemoryDirectory` is only honored after the folder is trusted. If no dialog appears, note that.
3. In the new session, ask the agent, verbatim:
   > Without changing anything: do you have a project memory index loaded from your session start? If so, paste it and tell me which file path it came from. Also: is there a CLAUDE.md in your context, and what does its first heading say?
4. Record the answer against the outcome table below.
5. **Optional second probe** (only if a memory index still loads): give the agent a durable correction — something it would normally save — and see whether a write lands, and where.

## Outcomes and what each means

| Observation | Meaning | Next step |
|---|---|---|
| **No memory index loaded at all** | `autoMemoryEnabled: false` binds Cowork. Settings work. This is Option A's end state and is safe. | Flip `autoMemoryEnabled` back to `true` in a later test to check whether `autoMemoryDirectory` also binds — that would deliver Option B (single store, auto-loaded, git-visible). |
| **Memory index loads, sourced from `1_Project/Memory/`** | `autoMemoryDirectory` binds; `autoMemoryEnabled` does not. **Option B achieved.** One store, git-tracked, auto-loaded. | Resolve the `MEMORY.md` vs `INDEX.md` naming collision — converge on one index. Then build the audit diff (step 4). |
| **Memory index loads, still from the hidden platform store** (i.e. it shows the reconciled content written 2026-07-25, including the "READ FIRST — this store is NOT authoritative" banner) | **Neither setting binds Cowork.** Confirms another CLI/Cowork divergence. | Fall back to router-plus-discipline (Option A without the mechanism) plus a mandatory audit diff. Record as a hard plugin-level constraint: consumer vaults cannot rely on settings-based memory control. |
| **`CLAUDE.md` not in context** | Cowork does not load repo-root `CLAUDE.md`. This would be a significant finding — the entire Tier-1 router design (spine section 5) depends on it. | Find what Cowork *does* load as project instructions, and retarget the router at that. Do not port the router to the plugin until resolved. |

Any of these is a real result. There is no wasted branch.

## Recording the result

Write the outcome into `1_Project/Decisions.md` under "Memory management" — replacing the "gating test armed, result pending" row — and note the date. Then update this file's Status line at the top.

## Rollback

Delete the two memory keys from `.claude/settings.json` and the repo returns to its 2026-07-24 behavior. The router and the memory reconciliation are independently useful and should be kept regardless of the outcome.
