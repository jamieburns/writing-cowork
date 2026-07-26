# Memory Prototype — Test Plan

**Status:** Ready to run. No results recorded yet.
**Date:** 2026-07-25
**Covers:** commit `953e588` — memory store reconciliation, `CLAUDE.md` Tier-1 router with managed-block markers, armed memory gating settings.
**Purpose:** verify the prototype before stage 3 (porting to the plugin), and catch the things that are easy to miss.

**How to use:** work top-down. Tier 1 gates everything else — if a Tier-1 test fails, stop and record rather than pushing on. Fill in the Actual column as you go; the Result Log at the bottom is what gets promoted into `Decisions.md`.

---

## Pre-flight — confirm what actually landed

Cheap, do first. These verify the 2026-07-25 changes are really on disk, not just believed to be.

| # | Check | Expected | Actual |
|---|---|---|---|
| P1 | `cat .claude/settings.json` parses as JSON, has `enabledPlugins` + `autoMemoryEnabled` + `autoMemoryDirectory` | 3 keys present, valid JSON | |
| P2 | `git log --oneline -1` and `git status` | `953e588`, clean except the untracked handoff | |
| P3 | Open the repo in Obsidian | `CLAUDE.md` visible at root; `1_Project/Memory/` shows 9 files incl. the new release-checklist one | |
| P4 | Ask any session: read the hidden platform memory index | Opens with **"READ FIRST — this store is NOT authoritative"** | |

If P4 shows the *old* index instead, my reconciliation writes didn't land and everything downstream is measuring the wrong thing.

---

## Tier 1 — Blocking. One fresh **Cowork** session, in this project

Settings and instruction files are read at session start, so this cannot be run in the session that armed it. Accept the workspace-trust dialog if one appears; note whether it did.

**T1.1 — Does Cowork load repo-root `CLAUDE.md` at all?**
Ask: *"Is there a CLAUDE.md in your context right now? Quote its first heading and the first invariant listed."*
- **Pass:** quotes `# writing-cowork — router` and a memory invariant.
- **Fail:** no CLAUDE.md in context. **This is the single most consequential possible failure** — the entire Tier-1 router design (spine §5) assumes it loads. If it fails, find what Cowork *does* load as project instructions and retarget before porting anything.

**T1.2 — Regression: does the plugin still load?**
Run `pm-version`, or just check whether `writing-cowork:*` skills appear in the session's skill list.
- **Pass:** skills present.
- **Fail:** adding unknown keys (`autoMemoryEnabled`, `autoMemoryDirectory`) to `.claude/settings.json` broke Cowork's parsing of `enabledPlugins`. **Easy to overlook and high-impact** — you'd lose the plugin you use daily. If this fails, remove the two keys immediately; the rollback is in §Rollback.

**T1.3 — The gating question: does memory load, and from where?**
Ask: *"Do you have a project memory index loaded from session start? If so, paste it and say which path it came from."*

| Observation | Meaning | Next |
|---|---|---|
| No memory index at all | `autoMemoryEnabled: false` binds Cowork | Later, flip it back to `true` to test whether `autoMemoryDirectory` alone gives Option B |
| Index loads from `1_Project/Memory/` | `autoMemoryDirectory` binds — **Option B achieved** | Resolve `MEMORY.md` vs `INDEX.md` collision (T3.4) |
| Index loads, shows the "READ FIRST" banner | Neither setting binds; still the hidden store | Fall back to router + discipline + mandatory audit diff; record as a hard plugin constraint |

**T1.4 — Are the HTML comment markers actually stripped?**
Ask: *"In the CLAUDE.md you have in context, do you see any text about a marker convention or the words WRITING-COWORK MANAGED? Answer only from what's in your context — do not open the file."*
- **Stripped (expected):** says no.
- **Not stripped:** the markers are costing context tokens every turn. Not fatal, but shrink the header comment and re-measure.

---

## Tier 2 — Same four questions in **Claude Code CLI**

Do not skip this. You develop in CLI and ship to Cowork; **the divergence map between the two runtimes is the real deliverable of this pass**, and it's what determines what the plugin can safely promise.

| # | Check | Expected (per docs) | Actual |
|---|---|---|---|
| T2.1 | `/context` → is `CLAUDE.md` under **Memory files**? | Yes | |
| T2.2 | Is auto memory off? (`/memory` shows the toggle state) | Off — `autoMemoryEnabled: false` | |
| T2.3 | `/memory` → open the auto memory folder. Where does it point? | `1_Project/Memory/` if `autoMemoryDirectory` bound | |
| T2.4 | Same stripped-comments probe as T1.4 | Stripped | |

**Then write down, explicitly: for each of the four behaviors, does CLI agree with Cowork?** Any disagreement is a plugin-level constraint, not a local quirk.

---

## Tier 3 — Does it actually change behavior?

Settings binding is necessary but not sufficient. These test whether the design does its job.

**T3.1 — Does the router produce correct orientation?**
In a fresh session ask: *"What's the current state of this project and what's next?"*
- **Pass:** reads `Decisions.md` first, cites v0.1.15, doesn't go spelunking `1_Project/Handoff/` or `History/`.
- **Fail:** wanders through handoffs or reports a stale version — the router isn't steering.

**T3.2 — Marker convention efficacy. This is the one you specifically asked for.**
In a fresh session: *"Add a note to CLAUDE.md that we're currently prototyping memory management."*
- **Pass:** writes inside `BEGIN/END PROJECT-OWNED`.
- **Fail:** writes into a MANAGED block, or at the top of the file. Since comments are stripped, the *only* thing steering it is the one visible line — if this fails, that line needs to be stronger or moved.
- Revert whatever it writes afterward; this is a probe, not a change.

**T3.3 — Provoke a memory write.**
Give a durable correction it would normally save (e.g. *"remember: always run `claude plugin validate .` before committing a version bump"*). Then check: did anything get written? Where? Does it appear in `git status`?
- This is the **core validation of the git-as-consent model**. If the write lands somewhere `git status` shows, the model works. If it lands invisibly, it doesn't.

**T3.4 — Index collision** (only if T1.3 showed Option B).
Does a `MEMORY.md` now appear in `1_Project/Memory/` alongside `INDEX.md`? Two indexes is two piles again at file level. Converge on one — likely `MEMORY.md`, since the mechanism writes that name regardless, with `INDEX.md` folded in or reduced to a pointer.

---

## Tier 4 — Soak. The failure mode is slow

The problem this whole exercise targets is **quiet accumulation over months**. A control that looks fine on day one and stops binding on day thirty is exactly what you're trying to catch, and no single session can detect it.

- **T4.1** — After ~5 working sessions, diff the two stores again: read the platform store, list `1_Project/Memory/`, compare. Anything new in the platform store that isn't in the vault is a leak.
- **T4.2** — After those sessions, check `git log -- 1_Project/Memory/`. Did memory changes arrive as reviewable commits, or did nothing ever show up (which would mean either nothing was learned, or writes are going somewhere invisible)?
- **T4.3** — Set a calendar reminder for ~30 days out to repeat T4.1. The whole point is the long tail.

---

## Tier 5 — Port readiness. Run before stage 3, not after

These are the ones most likely to be skipped and most likely to bite in a consumer vault.

**T5.1 — The `.claude/` write block.**
Found during execution: `device_commit_files` refuses to write anything under `.claude/` ("Writing to .claude is not permitted via remote tools"). `pm-init-project-cowork-settings` writes `<vault>/.claude/settings.json`. **Test whether that skill works when run from a Cowork session.** If it doesn't, it's already broken for consumer vaults today, independent of this memory work — and worth a GitHub issue via `pm-escalate-issue`.

**T5.2 — Path portability. Easy to miss, and it's a real bug in what I just committed.**
`.claude/settings.json` is **git-tracked** and now contains `"autoMemoryDirectory": "~/code/writing-cowork/1_Project/Memory"` — a path that is correct only on this machine, with this clone location. Clone the repo elsewhere (or check out on another machine) and that path won't resolve. Test what happens: silent fallback, error, or memory written to a stray location?
- For the plugin port this is disqualifying as-is. A shipped template cannot hardcode an absolute path. Options: put the setting in `.claude/settings.local.json` (gitignored, per-machine), or have `pm-sync-project-to-plugin` compute it at install time. **Decide this before porting.**

**T5.3 — Worktrees.** Docs say CLI auto memory is shared across all worktrees of a repo. If you use worktrees here, confirm the redirect doesn't cause two worktrees to fight over one memory directory.

**T5.4 — End-to-end on a throwaway vault.** Scaffold a scratch project with `pm-setup-project`, apply the memory model by hand, and confirm the whole thing works from nothing. Catches assumptions this repo satisfies by accident (it's the plugin source, not a normal vault — no `process/active/`, no `drift_check.yaml`).

---

## Rollback drill — test it, don't assume it

Practice this once *before* you need it:

1. `git revert 953e588` (or remove just the two memory keys from `.claude/settings.json`).
2. Fresh session → confirm the plugin loads and memory behaves as it did on 2026-07-24.

The router and the store reconciliation are independently useful and worth keeping even if the memory settings turn out to be inert — revert selectively rather than wholesale.

---

## Easy to overlook — the short list

1. **T1.2, the plugin-loading regression.** New keys in `settings.json` could break `enabledPlugins`. Highest blast radius of anything here.
2. **T5.2, the hardcoded path** in a git-tracked file. Already a latent bug; disqualifying for the plugin port.
3. **Tier 2 at all.** The temptation is to test in Cowork, see it work, and port. CLI/Cowork divergence is the whole reason this pass exists.
4. **T3.2/T3.3 — behavior, not just configuration.** A setting that binds but doesn't change what the agent does has bought nothing.
5. **Tier 4 soak.** One passing session proves almost nothing about a months-long accumulation problem.
6. **Recording negative results.** "Neither setting binds Cowork" is a valuable, portable finding — write it into `Decisions.md` with the same care as a success.

---

## Result log — fill in, then promote to `Decisions.md`

| Test | Date | Result | Follow-up |
|---|---|---|---|
| T1.1 CLAUDE.md loads (Cowork) | | | |
| T1.2 Plugin still loads | | | |
| T1.3 Memory source | | | |
| T1.4 Comments stripped | | | |
| T2.x CLI comparison | | | |
| T3.1 Router orientation | | | |
| T3.2 Marker respected | | | |
| T3.3 Memory write visible in git | | | |
| T5.1 `.claude/` write block | | | |
| T5.2 Path portability | | | |

**Stop conditions — halt the stage-3 port if any of these hold:**
- T1.1 fails (Cowork doesn't load `CLAUDE.md`) — the router doesn't work in the runtime consumer vaults use.
- T1.2 fails and can't be fixed — the settings approach breaks plugin loading.
- T5.2 has no clean answer — you'd be shipping a template with a machine-specific path in it.
