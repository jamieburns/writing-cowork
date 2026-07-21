---
name: pm-show-kanban
description: >
  This skill should be used when the user asks to "show the kanban",
  "render a kanban board", "give me a planning view", or any variant of
  rendering the project's tasks as a Dataview kanban inside Obsidian.
  Supports multi-mode grouping (by status, assignee, or milestone) and
  optional column display. Per-project view; for cross-project see
  pm-show-composite-kanban.
metadata:
  version: "0.1.4"
  role: pm
  subset: mvp-planning
---

# pm-show-kanban

Render the project's tasks (from todos.md) as a kanban board with
configurable grouping (status, assignee, or milestone) and optional
additional columns. Writes the kanban as an Obsidian Dataview query
embedded in a markdown file, which Obsidian renders as a live board
when viewed.

## Arguments

- **`--vault=<path>`** (optional) — vault root. Default: cwd.
- **`--output=<path>`** (optional, default
  `process/active/kanban_view.md`) — where to write the kanban file.
- **`--by=status|assignee|milestone`** (optional, default `status` per v0.1.14;
  v0.1.8 changed from `status` to `milestone`, then v0.1.14 changed back to
  `status` based on broad user feedback that Status is the primary working
  lens) — what to group columns by. `status` = pending/in-progress/done
  columns; `assignee` = pm/analysis/voice/.../custom columns;
  `milestone` = phase-1/phase-2/.../custom columns.
- **`--show=<col1>,<col2>,...`** (optional) — additional columns to
  display on each card. Comma-separated. Example: `--show=assignee,milestone`
  shows Assignee and Milestone metadata on each card in addition to the
  grouped column. By default, whichever field is NOT the `--by` key is
  shown. Use this to show multiple fields.
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
2. Groups by `<by>` (status, assignee, or milestone).
3. Renders each group as a column with task cards.
4. On each card, display the primary grouping key + any columns specified
   in `--show`.

**Example grouping modes:**
- `--by=status` (default v0.1.14) → columns: Pending | In-Progress | Done
- `--by=assignee` → columns: PM | Analysis | Voice | Substance | ... (per
  role_taxonomy.md)
- `--by=milestone` → columns: Phase-1 | Phase-2 | Phase-3 | ... (per
  roadmap.md)
- `--by=status --show=assignee` → Status columns, each card shows Assignee
  + Status
- `--by=assignee --show=milestone` → Assignee columns, each card shows
  Milestone + Assignee

**Locked decision #10 was revised in v0.1.7, and again in v0.1.14 for
multi-mode support.** The original "install once, never overwrite" rule
was too restrictive for an active project. New behavior:

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
// Schema (v0.1.4+): | ID | Description | Milestone | Assignee | Status | Added | Notes |
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
  // Handle both old (6 col) and new (7 col) schemas
  if (cells.length >= 6 && cells[0] && cells[0] !== "ID") {
    if (cells.length === 6) {
      // Old schema: ID | Description | Milestone | Status | Added | Notes
      tasks.push({
        id: cells[0],
        description: cells[1],
        milestone: cells[2] || "unassigned",
        assignee: "",
        status: cells[3] || "planned",
        added: cells[4],
        notes: cells[5],
      });
    } else if (cells.length >= 7) {
      // New schema: ID | Description | Milestone | Assignee | Status | Added | Notes
      tasks.push({
        id: cells[0],
        description: cells[1],
        milestone: cells[2] || "unassigned",
        assignee: cells[3] || "",
        status: cells[4] || "planned",
        added: cells[5],
        notes: cells[6],
      });
    }
  }
}

// Group by configured key (status, assignee, or milestone) — set by skill at gen time
const GROUP_BY = "{{GROUP_KEY}}";  // skill substitutes "status", "assignee", or "milestone"
const SHOW_COLS = "{{SHOW_COLS}}".split(",").filter(c => c.trim());  // skill substitutes list
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

    // Build metadata line based on GROUP_BY and SHOW_COLS
    const metaParts = [];
    if (SHOW_COLS.includes("status") && GROUP_BY !== "status") {
      metaParts.push(`[${t.status}]`);
    }
    if (SHOW_COLS.includes("assignee") && GROUP_BY !== "assignee") {
      metaParts.push(`[${t.assignee || "—"}]`);
    }
    if (SHOW_COLS.includes("milestone") && GROUP_BY !== "milestone") {
      metaParts.push(`[${t.milestone}]`);
    }
    metaParts.push(`${t.id}`);
    metaParts.push(t.added);

    meta.createSpan({ text: metaParts.join(" · ") });
  }
}
\`\`\`
```

The skill substitutes:
- `{{GROUP_KEY}}` with `status`, `assignee`, or `milestone` depending on `--by`
- `{{SHOW_COLS}}` with comma-separated columns to display (e.g.,
  `milestone,status` or `assignee,status`)
- `<title>` for project title
- `<date>` for generation timestamp

If Dataview / dataviewjs isn't available in the vault, this block
won't render — fall back to a plain markdown table grouped by the
chosen axis, and surface the missing-plugin warning in the skill
output.

## Output on success

```
Rendered kanban view at <vault>/<output-path>.
  Grouped by: <status|assignee|milestone>
  Additional columns: <status|assignee|milestone>
  Open in Obsidian to see the rendered board.
```

Example outputs:
- `Grouped by: status` (default) — three columns: Pending | In-Progress | Done
- `Grouped by: assignee` — columns per detected role/person
- `Grouped by: status, Additional columns: assignee` — Status columns with Assignee metadata on each card

## Output on failure

- `todos.md not found`
- `kanban file already exists at <path>; --preserve-customizations is set so refusing to overwrite. Remove the flag to regenerate.` (only when `--preserve-customizations` is supplied)
- `Dataview plugin not installed in vault; kanban will render as plain markdown table (continuing)`

## Standalone use

Same preconditions. Run once per project to install the kanban file,
then view in Obsidian.
