---
name: pm-init-todos
description: >
  This skill should be used when the user asks to "initialize todos",
  "create the todos file", "set up todos.md", or any variant of creating
  the writing-cowork todos tracking document. Creates a header + example
  tasks per detected role in todos.md in the vault's process/active/
  directory. Invoked by pm-setup-project; also usable standalone.
  
  **Lift Procedure Integration:** Invoked during project setup (stage 2).
  See ~/code/cowork-tools/lift/README.md for full lift workflow.
metadata:
  version: "0.1.4"
  role: pm
  subset: mvp-foundation
---

# pm-init-todos

Create `process/active/todos.md` with the task table schema (includes
Assignee column for role-based task ownership) and example tasks per
detected role. This file is the task list — granular work items, not
roadmap milestones. Used by task skills in MVP Planning (`pm-add-task`,
`pm-update-task`, `pm-list-tasks`, `pm-close-task`, `pm-show-kanban`).

The file includes header + role-based example tasks that project authors
should delete or customize. Tasks are appended/modified via `pm-add-task`,
`pm-update-task`, etc.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title.
- **`--skip-examples`** (optional, flag) — create header-only todos.md
  without role-based example tasks.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/active/` exists.
3. Verify `<vault-path>/process/active/todos.md` does NOT already exist.
4. Read `<vault-path>/process/data_management/role_taxonomy.md` if it
   exists; otherwise use the hardcoded DEFAULT_ROLES list.

## Execution

1. Detect available roles by reading `role_taxonomy.md` if it exists;
   otherwise use the default baseline roles (pm, analysis, review, voice,
   substance, writer, librarian, + standard combinations).

2. Unless `--skip-examples` is set, generate one example task per detected
   role (up to 5 for brevity). Example task IDs are generated as short
   hashes; descriptions note the role and ask the author to delete them.

3. Atomic-write the following content to
`<vault-path>/process/active/todos.md`:

```markdown
# Todos — <title>

Created: <date_iso>

Granular task list for <title>. One row per task. Distinct from roadmap.md:
the roadmap captures milestones; this captures the work items inside
milestones.

Task IDs are 8-char short hashes (per writing-cowork locked decision #9).
Assignee field links tasks to roles (pm, analysis, review, voice, substance,
writer, librarian, or custom roles). See process/data_management/role_taxonomy.md
for local role definitions.
Status values: `planned` → `in-progress` → `done`.

| ID | Description | Milestone | Assignee | Status | Added | Notes |
|----|-------------|-----------|----------|--------|-------|-------|
| fk9d2c | [Example: pm task — delete this] | phase-1 | pm | planned | <date_iso> | |
| g2k4e1 | [Example: analysis task — delete this] | phase-1 | analysis | planned | <date_iso> | |
| h3l5f2 | [Example: voice task — delete this] | phase-1 | voice | planned | <date_iso> | |
```

If `--skip-examples` is set, omit the example rows and just include the header.

## Output on success

```
Initialized todos.md at <vault-path>/process/active/todos.md
  Schema: Assignee-enabled (includes pm, analysis, review, voice, substance, writer, librarian)
  Example tasks: 7 tasks generated per detected roles
  Note: Delete or replace example tasks before adding real work.
```

Or, if using `--skip-examples`:

```
Initialized todos.md at <vault-path>/process/active/todos.md
  Schema: Assignee-enabled (header only, no examples)
  Use pm-add-task to add your first task.
```

## Output on failure

- `process/active directory missing; run pm-init-vault first`
- `todos.md already exists at <path>; remove it first or skip this step`
- `role_taxonomy.md exists but is malformed; unable to parse roles`

## Standalone use

Same preconditions. Useful if pm-setup-project was invoked with
`--skip-todos` and you want to scaffold it later.
