---
name: pm-close-task
description: >
  This skill should be used when the user asks to "close a task",
  "complete a task and archive it", "finish task X", or any variant of
  marking a task done AND optionally moving it out of the active todos
  list. Distinct from pm-update-task (which just changes status); this
  also handles the archive step.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-planning
---

# pm-close-task

Mark a task done and optionally archive it from the active todos.md to
a history table. The archive step prevents the active todos list from
growing unbounded over a long project.

## Arguments

- **`<id>`** (required) — 8-char task ID.
- **`--notes=<text>`** (optional) — closure notes (e.g., "moved to
  Phase 3 backlog" or "completed early via voice pass"). Appended to
  the task's Notes column before archive.
- **`--archive`** (optional, flag, default true) — move the task row
  out of the active table to a "Closed tasks" section at the bottom of
  todos.md. Pass `--no-archive` to keep it in the active table with
  status=done (useful if the writer prefers a single growing list).
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root and verify todos.md exists.
2. Locate the task by ID. If not found, abort.
3. If the task is already done, warn — still proceed (in case the
   archive step is what's needed).

## Execution

1. Read todos.md.
2. Update the task row: set status to `done`, append `--notes=` to the
   Notes column.
3. If `--archive` (default): move the row to a "## Closed tasks" section
   at the bottom of the file. Create the section if it doesn't exist.
4. Atomic-write.

## Output on success

```
Closed task <id>: <description>
  Status: <prev> → done
  Notes: <appended-text>
  Action: <archived to Closed tasks section | kept in active>
```

## Output on failure

- `todos.md not found`
- `task <id> not found in todos.md`

## Standalone use

Same preconditions. Common end-of-session ritual: close any tasks
completed during the session.
