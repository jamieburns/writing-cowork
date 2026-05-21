---
name: pm-create-issue-report
description: >
  This skill should be used when a specialist context (substance, voice,
  reader-review, librarian, analysis, etc.) asks to "log an issue",
  "report a process issue", "file a feedback note", "flag a plugin gap",
  or any variant of producing an inbox/issues/ cover-note describing
  something observed that ought to be tracked or escalated. The librarian
  later decides whether to handle locally or escalate to GitHub via
  pm-escalate-issue.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-create-issue-report

Drop an issue-report cover-note into `<vault>/inbox/issues/`. Captures
observations about the writing-cowork plugin, the project's process, or
the vault's documentation, so they don't get lost in chat scrollback.
Sender-side counterpart to pm-escalate-issue (librarian-side).

## Arguments

- **`--title=<text>`** (required) — short title (one line, ~80 chars max).
- **`--description=<text>`** (required) — longer body describing the
  observation. Markdown is fine.
- **`--severity=low|medium|high`** (optional, default `medium`) — caller's
  assessment of significance. Librarian may reclassify.
- **`--scope=plugin|vault`** (optional, default `plugin`) — `plugin` means
  the issue should ultimately surface to the writing-cowork repo;
  `vault` means it's specific to this project's setup and shouldn't be
  escalated. The librarian makes the final call but this is the
  caller's intent.
- **`--from=<context>`** (optional, default `substance`) — the
  observing context (`substance`, `voice`, `librarian`,
  `reader-review`, `analysis`, etc.).
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify `<vault>/inbox/issues/` exists. If not, fall back to
   `<vault>/inbox/promotion/` (older vaults predating the issues
   convention) and note this in output. If neither exists, abort with
   `inbox not initialized; run pm-init-vault`.
3. Read the plugin version from the most-recent matching
   `~/Library/Application Support/Claude/local-agent-mode-sessions/*/rpm/plugin_*/.claude-plugin/plugin.json`
   where `name == writing-cowork`. If multiple, pick most recently
   modified. If not found, record `plugin-version: unknown`.
4. Generate a short slug from the title (kebab-case, ~40 chars max) for
   the filename.

## Execution

Write the cover-note at
`<vault>/inbox/issues/<YYYY-MM-DD>_<from>_<slug>.md`:

```markdown
# Issue report

**From:** <from>
**Date:** YYYY-MM-DD
**Severity:** <severity>
**Scope:** <scope>
**Plugin version:** <X.Y.Z or "unknown">

## <title>

<description>
```

Atomic-write (`.tmp` then `mv`).

## Output on success

```
Created issue report at <vault>/inbox/issues/<filename>:
  Title:    <title>
  Severity: <severity>
  Scope:    <scope>
  From:     <from>

Librarian will review via pm-process-inbox-item. Plugin-scope issues
typically get escalated to github.com/jamieburns/writing-cowork/issues
via pm-escalate-issue.
```

## Output on failure

- `inbox/issues/ not found at <vault>/inbox/; run pm-init-vault first`
- `cover-note destination collision; supply a different --title`
- `permission denied writing to inbox/issues/`

## Standalone use

Any specialist context can call this directly when they notice
something worth tracking. Examples:

- substance context notices a skill description is misleading
- librarian context notices a doc gap (like the inbox/README.md
  hub-updates omission)
- reader-review context notices the voice-handoff template doesn't
  cover a case they hit
- voice context notices the drift_check.yaml has a stale pattern

The threshold for filing should be low. Issues that don't matter get
closed by the librarian; issues that do get escalated. The cost of
filing a noisy issue is much lower than the cost of losing a real one.
