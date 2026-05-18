---
name: pm-init-todos
description: >
  This skill should be used when the user asks to "initialize todos",
  "create the todos file", "set up todos.md", or any variant of creating
  the writing-cowork todos tracking document. Creates an empty (header-only)
  todos.md in the vault's process/active/ directory. Invoked by
  pm-setup-project; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-init-todos

Create an initially-empty `process/active/todos.md` with a minimal header.
This file is the task list — granular work items, not roadmap milestones.
Used by task skills in MVP Planning (`pm-add-task`, `pm-update-task`,
`pm-list-tasks`, `pm-close-task`, `pm-show-kanban`).

The file starts empty (header only). Tasks are appended via
`pm-add-task`.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/active/` exists.
3. Verify `<vault-path>/process/active/todos.md` does NOT already exist.

## Execution

Atomic-write the following content to
`<vault-path>/process/active/todos.md`:

```markdown
# Todos — <title>

Created: <date_iso>

Granular task list for <title>. One row per task. Distinct from roadmap.md:
the roadmap captures milestones; this captures the work items inside
milestones.

Task IDs are 8-char short hashes (per writing-cowork locked decision #9).
Status values: `planned` → `in-progress` → `done`.

| ID | Description | Milestone | Status | Added | Notes |
|----|-------------|-----------|--------|-------|-------|
```

## Output on success

```
Initialized todos.md at <vault-path>/process/active/todos.md
```

## Output on failure

- `process/active directory missing; run pm-init-vault first`
- `todos.md already exists at <path>; remove it first or skip this step`

## Standalone use

Same preconditions.
