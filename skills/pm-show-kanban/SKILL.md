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
- **`--by=status|milestone`** (optional, default `milestone`) — what to
  group columns by. v0.1.8 changed the default from `status` to
  `milestone` based on writer feedback that milestone is the more
  useful default lens for an active project.
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

Example file content (uses `dataviewjs` for a true horizontal kanban
layout with scrollable columns; the previous TABLE-grouped-by-status
approach stacked groups vertically, which was unreadable in narrow
viewports):

```markdown
# Kanban — <title>

(Generated <date>. Regenerable via pm-show-kanban; writer-notes block
below survives regeneration. Horizontal scroll if columns exceed
viewport width.)

<!-- WRITER-NOTES-START -->
(Add notes here that should survive kanban regeneration — context for
the columns, links to related files, etc.)
<!-- WRITER-NOTES-END -->

\`\`\`dataviewjs
// Parse todos.md markdown table rows
const todosPath = "process/active/todos.md";
const file = await dv.io.load(todosPath);
const lines = file.split("\n");
const tasks = [];
let inTable = false;
for (const line of lines) {
  if (line.match(/^\|\s*-+\s*\|/)) { inTable = true; continue; }
  if (!inTable) continue;
  if (!line.trim().startsWith("|")) { inTable = false; continue; }
  const cells = line.split("|").slice(1, -1).map(c => c.trim());
  if (cells.length >= 6 && cells[0] && cells[0] !== "ID") {
    tasks.push({
      id: cells[0],
      description: cells[1],
      milestone: cells[2] || "unassigned",
      status: cells[3] || "planned",
      added: cells[4],
      notes: cells[5],
    });
  }
}

// Group by configured key (status or milestone) — set by skill at gen time
const GROUP_BY = "{{GROUP_KEY}}";  // skill substitutes "status" or "milestone"
const groups = {};
for (const t of tasks) {
  const key = t[GROUP_BY] || "unassigned";
  if (!groups[key]) groups[key] = [];
  groups[key].push(t);
}

// Render horizontal kanban
const container = dv.el("div", "");
container.style.display = "flex";
container.style.overflowX = "auto";
container.style.gap = "1em";
container.style.paddingBottom = "1em";

for (const [key, taskList] of Object.entries(groups)) {
  const column = container.createDiv();
  column.style.minWidth = "250px";
  column.style.flex = "0 0 auto";
  column.style.border = "1px solid var(--background-modifier-border)";
  column.style.borderRadius = "6px";
  column.style.padding = "0.5em";

  const header = column.createEl("h4", { text: `${key} (${taskList.length})` });
  header.style.marginTop = "0";

  for (const t of taskList) {
    const card = column.createDiv();
    card.style.background = "var(--background-secondary)";
    card.style.padding = "0.5em";
    card.style.marginBottom = "0.5em";
    card.style.borderRadius = "4px";
    card.style.fontSize = "0.9em";

    card.createEl("div", { text: t.description });

    const meta = card.createDiv();
    meta.style.fontSize = "0.8em";
    meta.style.opacity = "0.7";
    meta.style.marginTop = "0.3em";

    if (GROUP_BY === "milestone") {
      meta.createSpan({ text: `[${t.status}] ` });
    } else {
      meta.createSpan({ text: `[${t.milestone}] ` });
    }
    meta.createSpan({ text: `${t.id} · ${t.added}` });
  }
}
\`\`\`
```

The skill substitutes `{{GROUP_KEY}}` with `status` or `milestone`
depending on the `--by` argument. Other substitutions: `<title>` for
project title, `<date>` for generation timestamp.

If Dataview / dataviewjs isn't available in the vault, this block
won't render — fall back to a plain markdown table grouped by the
chosen axis, and surface the missing-plugin warning in the skill
output.

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
