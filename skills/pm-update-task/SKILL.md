---
name: pm-update-task
description: >
  This skill should be used when the user asks to "update a task",
  "mark task done", "change task status", or any variant of editing an
  existing task row in `<vault>/process/active/todos.md`. Tasks are
  identified by their 8-char hash ID.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-planning
---

# pm-update-task

Edit an existing task row in todos.md.

## Arguments

- **`<id>`** (required) — 8-char task ID.
- **`--status=planned|in-progress|done`** (optional).
- **`--description=<text>`** (optional) — replace the description.
- **`--milestone=<name>`** (optional) — change milestone link.
- **`--notes=<text>`** (optional) — replace Notes column. To append
  without replacing, use `--notes-append=<text>` instead.
- **`--notes-append=<text>`** (optional, alternative to `--notes`).
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root and verify todos.md exists.
2. Locate the task row by ID. If not found, abort with `task <id> not
   found in todos.md`.

## Execution

1. Read todos.md.
2. Apply the requested edits to the task row's columns.
3. Atomic-write.

## Output on success

```
Updated task <id>:
  <list of changes applied>
```

If status changed to `done`, note this in the output and suggest the
user invoke pm-close-task to archive the task entry (or run an
end-of-day pm-list-tasks --status=done to see all freshly-closed tasks).

## Output on failure

- `todos.md not found`
- `task <id> not found in todos.md`
- `invalid status: <value> (accepted: planned, in-progress, done)`

## Standalone use

Most common standalone use: marking tasks done as they complete.
