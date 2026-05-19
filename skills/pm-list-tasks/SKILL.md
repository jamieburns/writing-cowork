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
2. Detect the file's schema by inspecting the first 30 lines:
   - **Plugin schema:** has a markdown table header with columns
     `| ID | Description | Milestone | Status | Added | Notes |` (or
     equivalent — the leading column is `ID` with 8-char hash values).
   - **Legacy checkbox schema:** uses section headings followed by
     `- [ ] <text>` or `- [x] <text>` lines. No ID column.
   - **Empty / header-only:** just the file header, no rows or items.

## Execution

Based on detected schema:

**If plugin schema:**

1. Parse todos.md table.
2. Apply filters.
3. Render as a table: `ID | Status | Description | Milestone | Added`.
4. At the bottom, summary line: total tasks matching filter, plus
   breakdown by status.

**If legacy checkbox schema (Reconciliation pattern):**

1. Parse section headings as implicit milestones; parse `- [ ]` /
   `- [x]` lines as tasks with statuses inferred from checkbox state
   (unchecked → planned; checked → done; no in-progress state in this
   schema).
2. Apply status filter if compatible.
3. Render as a table with synthetic IDs derived from the line position
   (e.g., `B1`, `B2` from `**B1.**` prefixes if present, otherwise
   sequential), or surface the original bullet text.
4. Prepend a soft warning to the output:
   `Note: todos.md is in legacy checkbox format. Full task CRUD via
   pm-add-task etc. requires migration to plugin schema. See the Phase 9
   milestone in roadmap.md (if planned).`

**If empty / header-only:**

1. Render the empty-state message: `Tasks file is empty. Use pm-add-task
   to add the first task.`

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
