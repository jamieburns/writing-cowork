---
name: pm-init-log
description: >
  This skill should be used when the user asks to "initialize the activity
  log", "create Log.md", "set up the project log", "add the activity log to
  this vault", or any variant of creating the shared append-only activity log.
  Creates `process/Log.md` — the semantic layer over git history, recording
  what changed, why, from what inputs, and which commit carried it. Invoked by
  pm-setup-project; also usable standalone for retrofitting.
metadata:
  version: "0.1.0"
  role: pm
  subset: information-architecture
---

# pm-init-log

Create `<vault>/process/Log.md` from `${CLAUDE_PLUGIN_ROOT}/templates/log.md`.

The activity log is the **Log** kind in the record taxonomy: append-only,
chronological, never overwritten. It answers "what happened, why, and from what
inputs" — the half of traceability that git alone does not give you. Git records
*what bytes changed*; the log records *why, and what the author had read when
they decided*.

## Placement and ordering

- **Location:** `process/Log.md` — the process root, alongside `active/`,
  `data_management/`, `memory/`, and `history/`. Not inside `active/`: the log
  is not a planning artifact, it is the project's activity record.
- **Ordering:** newest-**last**. Sessions orient by reading the tail.

Both are settled conventions — do not vary them per project. Consumer vaults
inheriting a different shape would break the "same skeleton in every vault"
consistency goal.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title; default title-cased `<name>`.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/` exists (created by `pm-init-vault`).
3. Verify `<vault-path>/process/Log.md` does NOT already exist. An existing log
   is append-only history — **never overwrite it.** Abort and report.
4. Verify `${CLAUDE_PLUGIN_ROOT}/templates/log.md` exists.

## Execution

1. Read `${CLAUDE_PLUGIN_ROOT}/templates/log.md`.
2. Substitute `{{title}}`, `{{date_iso}}`, `{{plugin_version}}` (the `version`
   field from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`).
3. Atomic-write to `<vault-path>/process/Log.md` with the Write file tool.

The log ships with **no entries**. A scaffolded project has no history yet, and
a fabricated first entry would be exactly the kind of fiction the log exists to
prevent.

## Rolling at phase close

When a phase or version closes, move the current `Log.md` to
`process/history/Log_<phase-or-version>.md` and start a fresh `Log.md` from this
template. That keeps the live file bounded without losing anything — the history
directory holds the closed segments.

This skill does not roll the log; it only creates the first one.

## Output on success

```
Initialized activity log at <vault-path>/process/Log.md
```

## Output on failure

- `process/ not found at <vault-path>; run pm-init-vault first`
- `Log.md already exists at <vault-path>/process/Log.md — the log is append-only and will not be overwritten; roll it to process/history/ first if you intend to start a new one`
- `${CLAUDE_PLUGIN_ROOT}/templates/log.md not found in plugin install`

## Standalone use

Retrofitting onto an existing vault is the common standalone case. Do **not**
try to reconstruct past entries from git history — the log's value is the *why*
and the *inputs read*, neither of which is recoverable from a diff. Start the
log from today and let it accumulate honestly.

## Related skills

- `pm-archive-to-history` — moves closed files into `process/history/`.
- `pm-install-router` — the router names the log's location for orientation.
