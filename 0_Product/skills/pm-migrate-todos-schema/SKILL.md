---
name: pm-migrate-todos-schema
description: >
  This skill should be used when the user asks to "migrate todos to the plugin
  schema", "convert a legacy checkbox todos.md", "my todos.md is in the old
  format", "enable task CRUD on this vault", or any variant of converting a
  checkbox-style todos file into the writing-cowork task table. Required before
  pm-add-task / pm-update-task / pm-close-task will work on a vault scaffolded
  before the table schema existed.
metadata:
  version: "0.1.0"
  role: pm
  subset: information-architecture
---

# pm-migrate-todos-schema

Convert a legacy checkbox `todos.md` into the plugin's task table so the task
CRUD skills work against it.

## Why this exists

`pm-list-tasks` and `pm-show-composite-kanban` both detect a **legacy checkbox
schema** — section headings followed by `- [ ]` / `- [x]` lines, no ID column —
and special-case it. `pm-list-tasks` can render it read-only and prints a
warning pointing at a migration that **did not exist**. Every write skill
(`pm-add-task`, `pm-update-task`, `pm-close-task`) requires the 8-char hash ID
that the legacy format has no room for.

So a vault in the legacy format was permanently read-only for task management,
and the tooling told the user to migrate without shipping a way to do it. This
is that way.

## What it does not do

It does not touch `roadmap.md`, and it does not invent dependencies. Legacy
checkboxes carry no dependency information; `Depends-On` is written empty and
filled in by hand afterwards if wanted.

## Arguments

- **`[vault-path]`** (optional) — vault root. Default: cwd.
- **`--todos=[rel]`** (optional) — override the todos path. Default: the
  `todos:` key from `drift_check.yaml` if present, else
  `process/active/todos.md`.
- **`--assignee=[role]`** (optional) — assignee for every migrated row.
  Default `pm`. Legacy checkboxes carry no ownership.
- **`--dry-run`** (optional) — print the converted table, write nothing.

## Preconditions

1. The todos file exists.
2. **It is actually legacy.** If a table header with an `ID` column is already
   present, stop with `already on the plugin schema; nothing to migrate`.
   Migration must be idempotent — running it twice must not double rows or
   regenerate IDs, because IDs are referenced from `roadmap.md`, `Decisions.md`
   and commit messages once they exist.
3. The vault is a git repository **with a clean working tree for this file**.
   This rewrites the file wholesale; an uncommitted edit would be lost with no
   diff to recover it. Stop and say so rather than proceeding.

## Execution

1. Read the file. Preserve everything above the first section heading verbatim
   — that is the file's own header prose, not data.
2. Parse:
   - `## [text]` → **Milestone** for every task under it, until the next heading.
   - `- [ ] [text]` → status `planned`; `- [x] [text]` → status `done`.
     The legacy format has no in-progress state; do not invent one.
   - A leading `**B1.**`-style label, where present, is kept at the front of
     **Description** rather than discarded — those labels are referenced from
     other documents.
3. Generate an 8-char hash **ID** per row (locked decision #9). Derive it from
   the description text so a re-run over the same input is stable, and check for
   collisions within the file before accepting one.
4. Set **Added** to the migration date, and note in **Notes**:
   `migrated from checkbox schema [date]`. The original creation date is not
   recoverable from the legacy format — record what is true rather than
   guessing.
5. Emit the table:

```
| ID | Description | Milestone | Assignee | Status | Added | Depends-On | Notes |
|----|-------------|-----------|----------|--------|-------|------------|-------|
```

6. **Escape any `|` inside cell text as `\|`.** A raw pipe in a description
   silently shifts every column to its right — the failure fixed in
   `drift_check` 0.5.1. Descriptions from prose bullets routinely contain them.
7. Atomic-write.

## After migrating

Point `drift_check.yaml`'s `todos:` key at the file if it is not at the default
path, then run `pm-run-drift-check` and confirm the preflight reports no missing
input for the todos check. A migration that produces a file the checker cannot
read has not finished.

## Output on success

```
Migrated [path] to the plugin task schema
  [n] task(s): [p] planned, [d] done
  [m] milestone(s): [names]
  Original preserved in git history at [current-HEAD]
Next: pm-list-tasks to verify, then task CRUD is available.
```

## Output on failure

- `[path] not found`
- `already on the plugin schema; nothing to migrate`
- `[path] has uncommitted changes; commit or stash first — this rewrites the file`
- `no checkbox items found; nothing to migrate`

## Related skills

- `pm-list-tasks` — detects the legacy schema and warns; run it before and after.
- `pm-add-task` / `pm-update-task` / `pm-close-task` — unblocked by this.
- `pm-run-drift-check` — confirms the result is machine-readable.
