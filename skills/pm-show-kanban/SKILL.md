---
name: pm-show-kanban
description: >
  This skill should be used when the user asks to "show the kanban",
  "render a kanban board", "give me a planning view", or any variant of
  rendering the project's tasks as a Dataview kanban inside Obsidian.
  Per-project view; for cross-project see pm-show-composite-kanban.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-planning
---

# pm-show-kanban

Render the project's tasks (from todos.md) as a kanban board grouped by
status. Writes the kanban as an Obsidian Dataview query embedded in a
markdown file, which Obsidian renders as a live board when viewed.

## Arguments

- **`--vault=<path>`** (optional) — vault root. Default: cwd.
- **`--output=<path>`** (optional, default
  `process/active/kanban_view.md`) — where to write the kanban file.
- **`--by=status|milestone`** (optional, default `status`) — what to
  group columns by.
- **`--preserve-customizations`** (optional, flag) — abort if the
  file already exists (the pre-v0.1.7 "install once" behavior). Use
  when heavy customization of the Dataview query needs preserving
  beyond the writer-notes block. Default: regenerate.

## Preconditions

1. Resolve vault root and verify todos.md exists.
2. Verify Obsidian Dataview is installed in the vault (check
   `.obsidian/plugins/dataview/` exists). If not, output a warning that
   the kanban will render as plain markdown without Dataview, but
   continue.

## Execution

Write `<output-path>` with a Dataview query that:

1. Selects tasks from todos.md.
2. Groups by `<by>` (status or milestone).
3. Renders each group as a column.

**Locked decision #10 was revised in v0.1.7.** The original "install
once, never overwrite" rule was too restrictive for an active project —
plugin author may ship better query templates, writer may want to swap
the grouping axis (`--by=status` ↔ `--by=milestone`), and stale queries
become a friction point. New behavior:

- **Default:** regenerate the file on every invocation, replacing the
  Dataview query with the current template. **Preserves** the
  `<!-- WRITER-NOTES-START -->` / `<!-- WRITER-NOTES-END -->` section
  if present, by reading the existing file, extracting that marker
  block, regenerating the rest, then re-inserting the writer-notes
  block at the same position.
- **`--preserve-customizations` flag:** restores the old install-once
  behavior (abort if file exists). Use this if you've heavily
  customized the Dataview query beyond the writer-notes section and
  don't want regeneration to clobber it.

The skill writes a designated writer-notes block in the initial
template so writers know where to put surviving content:

```markdown
<!-- WRITER-NOTES-START -->
(Add notes here that should survive kanban regeneration — context for
the columns, links to related files, etc.)
<!-- WRITER-NOTES-END -->
```

Example file content:

```markdown
# Kanban — <title>

(Generated <date>. Obsidian Dataview renders this as a live kanban
when viewed. Edit the query below to customize.)

\`\`\`dataview
TABLE WITHOUT ID
  description AS "Task",
  milestone AS "Milestone",
  added AS "Added"
FROM "process/active/todos"
GROUP BY status
\`\`\`
```

(Dataview's actual syntax may differ; this is illustrative. The skill
should use Dataview syntax that matches the writer's installed version,
or fall back to a static table if Dataview isn't installed.)

## Output on success

```
Rendered kanban view at <vault>/<output-path>.
  Grouped by: <status|milestone>
  Open in Obsidian to see the rendered board.
```

## Output on failure

- `todos.md not found`
- `kanban file already exists at <path>; --preserve-customizations is set so refusing to overwrite. Remove the flag to regenerate.` (only when `--preserve-customizations` is supplied)
- `Dataview plugin not installed in vault; kanban will render as plain markdown table (continuing)`

## Standalone use

Same preconditions. Run once per project to install the kanban file,
then view in Obsidian.
