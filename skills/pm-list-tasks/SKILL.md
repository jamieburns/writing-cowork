---
name: pm-list-tasks
description: >
  This skill should be used when the user asks to "list tasks",
  "show my todos", "what tasks are open", or any variant of querying
  `<vault>/process/active/todos.md` with optional filters.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-planning
---

# pm-list-tasks

Read todos.md, apply optional filters, render as a scannable table.

## Arguments

- **`--status=planned|in-progress|done|all`** (optional, default `all`
  if no other filter is set; default exclude-done if other filters set) —
  filter by status.
- **`--milestone=<name>`** (optional) — filter to tasks linked to a
  specific milestone.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root and verify todos.md exists.

## Execution

1. Parse todos.md table.
2. Apply filters.
3. Render as a table: `ID | Status | Description | Milestone | Added`.
4. At the bottom, summary line: total tasks matching filter, plus
   breakdown by status.

## Output on success

```
Tasks in <vault>/process/active/todos.md (filter: <description>):

  ID        Status        Description                    Milestone     Added
  --------  ------------  -----------------------------  ------------  ----------
  a1b2c3d4  in-progress   Voice pass on §3.5             Phase 2       2026-05-15
  e5f6g7h8  planned       Reader-review packet draft     Phase 3       2026-05-16

  Showing 2 of 12 total tasks.
  Status breakdown: planned=1, in-progress=1, done=10 (hidden by filter).
```

## Output on failure

- `todos.md not found`
- `invalid filter: <value>`

## Standalone use

Pure read. Useful at session start for "where was I."
