# Research: What does the platform actually offer for memory control?

**Date:** 2026-07-25
**Purpose:** Blocks the §6c memory pass per `information_architecture_spine_2026-07-24.md` §6e. Answers the three research questions before any of 6c-1/2/3 can be decided. This is research input, not a decision — nothing here is locked.

**Scope note (important):** there are two distinct "auto memory" systems in play, and the spine's §6a distinction between "platform memory" and "vault memory" undersells how split this actually is:

1. **Claude Code CLI auto memory** — `~/.claude/projects/<project>/memory/MEMORY.md` + topic files, on the machine running Claude Code. This is what the official docs at `code.claude.com/docs/en/memory` describe, and what both GitHub issues below are about.
2. **This Cowork session's memory tool** — `mcp__remote-devices__project_memory_read` / `project_memory_write`, which the system prompt describes as "persistent project memory on the user's desktop." Functionally similar (an index file + topic files, written autonomously), but it is a different mechanism, not necessarily governed by the same settings, env vars, or docs. I could not find separate public documentation specifically for the Cowork desktop-bridge memory tool's controls (no disable setting, hook, or audit surface distinct from what's below) — treat that as an open sub-question, not a "confirmed absent."

The three questions below are answered for system (1), where there's an authoritative doc. Whether the same answers hold for system (2) is unverified and should be asked directly rather than assumed.

---

## (a) Is there a setting to disable project memory?

**Yes, for Claude Code CLI auto memory — and it's a real, documented, three-layer control, not just a workaround.**

- **In-session toggle:** `/memory` command has an auto memory on/off toggle. Writes `autoMemoryEnabled` to user settings (`~/.claude/settings.json`).
- **Per-project override:** set `"autoMemoryEnabled": false` in that project's `.claude/settings.json`.
- **Environment variable:** `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` disables it without touching settings files.
- **Redirect instead of disable:** `autoMemoryDirectory` in settings (any scope: user/project/local/policy/`--settings`) moves the storage location — e.g. you could in principle point it at a path inside the vault, though it's still gitignored-by-convention machine-local storage, not a git-tracked vault file, and note per-project settings values are only honored after the workspace-trust dialog is accepted for that folder.

This directly resolves the "is there a setting" half of 6c-1 for the CLI. It's a real, current, supported control — not deprecated, not a rumor. **Auto memory is on by default.**

The two GitHub issues (#23750, #23544) asking for exactly this were filed against an *earlier* version (2.1.32-era) where no such setting existed and only a blunt `--no-memory` flag (which also killed CLAUDE.md loading) was available. Both issues are effectively obsoleted by the current docs page — the feature they asked for has since shipped. Worth noting for calibration: the spine's instinct to "not assert without reading the docs" was correct — behavior here changed materially between when those issues were filed and now.

## (b) Is there a hook that can intercept/gate memory writes?

**Not a dedicated one — but a generic mechanism gets you there.**

- There is no hook event named specifically for memory writes.
- `PreToolUse` is the general pre-write gate: it fires before any tool call (including `Write`/`Edit`), can match by tool name and by an `if` path-pattern condition (e.g. matching `MEMORY.md` or a memory-directory glob), and can **block** the write (exit code 2, or JSON `{"decision":"block","reason":"..."}`) or ask for confirmation. This is a true enforcement layer — the docs explicitly contrast it with CLAUDE.md/instructions: "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead."
- `PostToolUse` fires after the write already happened — useful for **logging/auditing**, not for consent-gating, since the write can't be undone from there (though it could trigger a "flag for review" side effect).

So: **consent-on-write (6c-1) is achievable, but requires custom hook configuration** (a `PreToolUse` hook matched to the memory path, presumably prompting for confirmation or requiring an explicit allow), not a built-in "ask before saving a memory" toggle. Nothing ships that pauses and asks the user before an auto-memory write; you'd build it.

This is a meaningfully different answer than "the platform will always write regardless" from §6c-1's framing — it's controllable, just not out-of-the-box in the way the spine hoped.

## (c) Is there an audit surface listing what's in the hidden store?

**Yes — and "hidden" undersells it.** Auto memory files are plain markdown on disk (`~/.claude/projects/<project>/memory/`), not opaque or encrypted. Concretely:

- `/memory` command lists CLAUDE.md/CLAUDE.local.md/memory file locations across scopes, toggles auto memory, and opens the auto memory folder directly — this is a built-in audit UI.
- The docs' own troubleshooting section poses almost exactly 6c-3's question ("I don't know what auto memory saved") and answers it: "Run `/memory` and select the auto memory folder to browse what Claude has saved. Everything is plain markdown you can read, edit, or delete."
- There's no periodic/automatic surfacing (no built-in "here's what accumulated this month, keep/promote/delete" prompt) — that part of 6c-3 (a drift-check-style Attention flag) is *not* built in and would still need to be custom, e.g. a scheduled task or drift-check step that reads the memory directory and reports growth/staleness.

So the "silent junk drawer" framing in §6b is partly right and partly not: the store isn't invisible or unauditable (it's readable markdown, one command away), but there's no *proactive* surfacing — the user has to think to run `/memory` and look. The risk is closer to "out of sight, in you don't go looking" than "genuinely hidden and inspectable."

---

## Net effect on the spine's open questions (§6c)

This doesn't decide anything, but it changes the shape of what's left to decide:

- **6c-1 (consent on write):** Achievable via a custom `PreToolUse` hook gate. Not shipped by default. Real build, not a dead end.
- **6c-2 (suppress/redirect):** `autoMemoryEnabled: false` fully suppresses CLI auto memory (per-project even). `autoMemoryDirectory` redirects storage location. Both are real settings, not workarounds.
- **6c-3 (audit/cleanup of accumulation):** The store is already inspectable (`/memory`), just not proactively surfaced. The gap is specifically *periodic surfacing*, not *visibility* — a narrower, more tractable build than "make the invisible visible."
- **6c-4 (memory vs. decision vs. charter-rule boundary):** Untouched by this research — still Jamie's call, as the spine already said.
- **6c-5 (cross-session trust in unprovenanced memory):** Slightly informed: auto memory files as of CLI v2.1.214+ carry a `modified` frontmatter timestamp when Claude writes them, so there's at least a recency signal, though still no "why"/inputs provenance like the activity log design in §4.

**Important caveat to carry into the pass:** all of the above is confirmed for **Claude Code CLI auto memory**. This Cowork session's actual memory mechanism is the `mcp__remote-devices__project_memory_*` tool pair — a similar but distinct system, and I found no equivalent public documentation confirming it has the same `autoMemoryEnabled` setting, `PreToolUse`-hookability, or `/memory`-equivalent audit command. **Before locking any 6c decision that assumes a control exists, verify it against the Cowork/desktop-bridge memory tool specifically, not just the CLI docs** — this is exactly the kind of divergence the spine's own §6e already warned about ("behavior here has repeatedly diverged from expectation").

## Sources

- [How Claude remembers your project — Claude Code Docs](https://code.claude.com/docs/en/memory)
- [Hooks reference](https://code.claude.com/docs/en/hooks)
- [FEATURE: Option to disable auto-memory · Issue #23750](https://github.com/anthropics/claude-code/issues/23750) — superseded by the shipped `autoMemoryEnabled` setting
- [Need ability to disable auto-memory (MEMORY.md) · Issue #23544](https://github.com/anthropics/claude-code/issues/23544) — superseded by the shipped `autoMemoryEnabled` setting
