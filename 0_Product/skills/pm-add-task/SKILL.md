---
name: pm-add-task
description: >
  This skill should be used when the user asks to "add a task",
  "create a task", "track this work item", or any variant of appending a
  new row to `<vault>/process/active/todos.md`. Generates a short hash
  task ID per writing-cowork locked decision #9. Supports optional assignee
  field for role-based task ownership (v0.1.4+).
metadata:
  version: "0.1.4"
  role: pm
  subset: mvp-planning
---

# pm-add-task

Append a new task row to `<vault>/process/active/todos.md`. Generates a
fresh 8-character short hash as the task ID (writing-cowork locked
decision #9 — task IDs are short hashes, not auto-incrementing integers).
Supports optional assignee field to link tasks to roles (pm, analysis,
review, voice, substance, writer, librarian, or custom).

## Arguments

- **`<description>`** (required) — short task description (one line).
- **`--milestone=<name>`** (optional) — link to a milestone in roadmap.md.
- **`--assignee=<value>`** (optional) — role or person owning this task.
  Validates against role_taxonomy.md if it exists; accepts any string if
  not (e.g., "pm", "analysis+voice", or custom roles from the project).
- **`--notes=<text>`** (optional) — additional context for the Notes
  column.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root and verify todos.md exists.
2. If `--milestone=<name>` is supplied, verify the milestone exists in
   roadmap.md. If not, warn but proceed.
3. If `--assignee=<value>` is supplied, read role_taxonomy.md if it exists
   and validate that <value> matches a defined role. Warn if not found but
   proceed (allows custom roles to be created ad-hoc).

## Execution

1. Generate an 8-character short hash. Pick a random hash (e.g., first 8
   chars of SHA1 of timestamp + description). Verify the hash doesn't
   collide with an existing task ID in todos.md; regenerate if collision.
2. Today's date in YYYY-MM-DD (local timezone).
3. Append a row to the Markdown table in todos.md:

   ```
   | <id> | <description> | <milestone-or-"-"> | <assignee-or-""> | planned | <date> | <notes-or-"-"> |
   ```

   The Assignee column is empty if not supplied; no dash or placeholder
   is written (Assignee is truly optional).

4. Atomic-write todos.md.

## Output on success

```
Added task <id>: <description>
  Milestone: <name-or-"unassigned">
  Assignee: <value-or-"unassigned">
  Status: planned
  Added: <date>
```

## Output on failure

- `todos.md not found at <vault>/process/active/`
- `milestone <name> not found in roadmap.md (task added anyway with milestone="<name>")`
- `assignee <value> not found in role_taxonomy.md (custom role allowed; task added)`
- `permission denied writing to todos.md`

## Standalone use

Same preconditions. Useful for ad-hoc task creation without invoking the full skill system.
