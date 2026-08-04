# Memory Gating Test — does Cowork honor Claude Code memory settings?

**Status:** Armed 2026-07-25. **Row 3 confirmed and independently replicated 2026-08-04 (two separate sessions).** Neither memory setting binds Cowork — and the reason is now understood: Cowork memory is a *different subsystem*, not a broken setting. Row 4 (`CLAUDE.md` loading) is still **NOT settled**. See Result at the bottom.
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
| **No memory index loaded at all** | `autoMemoryEnabled: false` binds Cowork. Settings work. This is Option A's end state and is safe. | ~~Flip `autoMemoryEnabled` back to `true` in a later test to check whether `autoMemoryDirectory` also binds.~~ **STRUCK 2026-08-04** — this branch did not occur, and the follow-up retest is now known to be untestable in principle: see the subsystem finding in the Result. |
| **Memory index loads, sourced from `1_Project/Memory/`** | `autoMemoryDirectory` binds; `autoMemoryEnabled` does not. **Option B achieved.** One store, git-tracked, auto-loaded. | Resolve the `MEMORY.md` vs `INDEX.md` naming collision — converge on one index. Then build the audit diff (step 4). |
| **Memory index loads, still from the hidden platform store** (i.e. it shows the reconciled content written 2026-07-25, including the "READ FIRST — this store is NOT authoritative" banner) | **Neither setting binds Cowork.** Confirms another CLI/Cowork divergence. | Fall back to router-plus-discipline (Option A without the mechanism) plus a mandatory audit diff. Record as a hard plugin-level constraint: consumer vaults cannot rely on settings-based memory control. |
| **`CLAUDE.md` not in context** | Cowork does not load repo-root `CLAUDE.md`. This would be a significant finding — the entire Tier-1 router design (spine section 5) depends on it. | Find what Cowork *does* load as project instructions, and retarget the router at that. Do not port the router to the plugin until resolved. |

Any of these is a real result. There is no wasted branch.

## Recording the result

Write the outcome into `1_Project/Decisions.md` under "Memory management" — replacing the "gating test armed, result pending" row — and note the date. Then update this file's Status line at the top.

## Rollback

Delete the two memory keys from `.claude/settings.json` and the repo returns to its 2026-07-24 behavior. The router and the memory reconciliation are independently useful and should be kept regardless of the outcome.

---

## Result — 2026-08-04

Run in a fresh Cowork session (cloud, desktop-bridged). Settings verified still
armed at run time: `.claude/settings.json` carries both `autoMemoryEnabled: false`
and `autoMemoryDirectory`, unmodified since 2026-07-26.

**Outcome row 3 — neither setting binds.** A memory index *did* load at session
start, and it came from the hidden platform store reached via
`mcp__remote-devices__project_memory_read`, not from `1_Project/Memory/`. Its
content was the store's own retirement note — "Retired 2026-07-26. Zero memories.
Do not write here." — which is distinct from `1_Project/Memory/INDEX.md`
("# Memory Index / Visible, user-manageable memory…"), so the two are
positively distinguishable and this is not an ambiguous read.

- `autoMemoryEnabled: false` did **not** suppress the store.
- `autoMemoryDirectory` did **not** redirect it.
- Consistent with the low expectations recorded in `Decisions.md` (#40495 note),
  and with the CLI/Cowork divergence pattern already seen in the marketplace cache.

**Outcome row 4 — NOT SETTLED. Earlier claim retracted 2026-08-04.**

The observing session saw project instructions consisting only of *"The user is
working in their local project 'writing-cowork'."* — no `CLAUDE.md` headings,
orientation list, or invariants — and initially reported this as row 4 firing.

**That conclusion does not hold, and the reason is worth recording.** `CLAUDE.md`
is read at session start. The observing agent's context window did not
demonstrably begin at session start: the session had been running for some time,
and a resumed or compacted context presents identically whether the file was
loaded-then-dropped or never loaded. Jamie caught this.

**The asymmetry is the general lesson.** Row 3's evidence is *presence* — content
arrived that the settings should have suppressed — and presence is robust to a
truncated context. Row 4's evidence is *absence*, and absence is exactly what a
truncated context cannot distinguish from removal. **An in-session agent cannot
validly report a negative about session-start state.** Any future run of this
test must establish that the observing turn IS the first turn, or the row-4
branch is unmeasurable from inside.

### How to settle row 4 properly

Ask the question in the **first turn** of a genuinely new session, before any
other work, and note in the result that it was turn one. Alternatively, probe
positively rather than negatively: ask for something only `CLAUDE.md` contains
(e.g. "what does invariant 2 say about `git status`?") without permitting a file
read — a correct answer is presence-evidence and settles it affirmatively.

### What this forces

1. Fall back to Option A without the mechanism — router-plus-discipline, plus a
   mandatory audit diff. Record as a hard plugin-level constraint: **consumer
   vaults cannot rely on settings-based memory control in Cowork.** This follows
   from row 3 alone and does not depend on the retracted row-4 claim.
2. Row 4 remains open. Do not act on the router question — in either direction —
   until it is measured from a first turn.
3. Row 3 is the same class this project keeps meeting: a control that reports as
   configured and does nothing.

---

## Second run — 2026-08-04 (independent replication)

A fresh Cowork session, **turn one, before any tool call**. Settings verified
still armed. A memory index was already in context; its text was the hidden
store's retirement note (`Retired 2026-07-26. Zero memories. Do not write
here.`), not `1_Project/Memory/INDEX.md` (`# Memory Index / Visible,
user-manageable memory... **Authoritative**`). **Row 3 reproduced exactly.**

### The refinement — this changes what the constraint means

The store that loaded is reached via `mcp__remote-devices__project_memory_read`,
an MCP tool on the **desktop bridge**. That is not Claude Code's auto-memory
subsystem; it is a separate store owned by the desktop app.

So the accurate finding is **not** "the settings are broken." It is:
**Cowork project memory is a different subsystem, and `autoMemoryEnabled` /
`autoMemoryDirectory` have no jurisdiction over it.**

Two consequences:

1. **No value of either key will ever help** — including the flip-to-`true`
   retest this document originally proposed for outcome row 1. That retest is
   struck above: it would be testing a control that was never wired to this
   store.
2. The plugin-level constraint must be worded as *"there is no known
   setting-level control over Cowork's memory store"* — not *"these settings
   don't work."* The second wording implies a bug report might fix it; the
   first says design around it permanently. Only the first is supported by the
   evidence.

### Incidental finding — the retirement is skin-deep

The hidden store's index says *"Zero memories. Nothing of value remains in this
store."* It still holds **seven topic files**: `feedback_release_includes_
version_in_description`, `feedback_sandbox_host_lanes`, `feedback_self_
contained_quit_scripts`, `feedback_verify_agent_citations`, `feedback_
workarounds_warrant_doc_check`, `project_writing_cowork_v013_state`,
`reference_personal_plugin_marketplace`.

These are stale duplicates of files now in `1_Project/Memory/` — note the vault
carries `project_writing_cowork_v013_state_HISTORICAL.md` while the hidden copy
lacks the suffix, so the two have already diverged.

**The retirement was applied to the index, not the contents.** Any future
session calling `project_memory_read` gets seven pullable filenames back, and a
banner is the only thing discouraging it. That is a soft control on a live
store — the same "reports as configured, does nothing" class this project keeps
meeting. Open question: is `project_memory_write` also ungated? Not tested; no
write was attempted.

### Row 4 — still not settled

The same turn-one observation saw project instructions reading only *"The user
is working in their local project 'writing-cowork'."* — no `CLAUDE.md` content.
Better positioned than the retracted 2026-08-04 first attempt (this genuinely
was turn one), but still **absence evidence**, which is the category that
failed before. Do not record it as a result.

The clean test remains the positive probe: in a fresh session, turn one, ask for
a fact only `CLAUDE.md` contains — e.g. *"what does invariant 2 say about `git
status`?"* — and forbid a file read. A correct answer settles it affirmatively.
This session contaminated itself by reading the file early.
