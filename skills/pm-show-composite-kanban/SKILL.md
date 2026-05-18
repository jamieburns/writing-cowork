---
name: pm-show-composite-kanban
description: >
  This skill should be used when the user asks to "show the composite
  kanban", "render a cross-project kanban", "what tasks are open across
  all my projects", or any variant of rendering an aggregated kanban
  pulling from all registered writing-cowork projects.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-planning
---

# pm-show-composite-kanban

Render a cross-project kanban as a Cowork artifact. Pulls task data
from every registered project's todos.md (via the cowork registry),
groups by status across projects, displays in an interactive web view.

Distinct from pm-show-kanban (per-project, Obsidian-rendered):
composite is cross-project, Cowork-rendered.

## Arguments

- **`--status-filter=<list>`** (optional) — comma-separated statuses to
  include (default: `planned,in-progress`; excludes done by default).
- **`--project-filter=<list>`** (optional) — comma-separated project
  names to include. Default: all enabled projects in the registry.

## Preconditions

1. Verify `~/.config/cowork/registry.yaml` exists.
2. For each registered+enabled project, verify its todos.md exists
   under the registry-recorded vault. Skip projects whose todos.md is
   missing (warn but continue).

## Execution

Per writing-cowork locked decision #11: always re-pull on view; no
caching. The artifact's open should fetch fresh task data each time
(via the Cowork artifact's `window.cowork.callMcpTool` mechanism to
read each todos.md).

Render as a Cowork artifact (via `mcp__cowork__create_artifact` if
available):

1. Aggregate tasks across all registered projects.
2. Group by status (or apply user's filters).
3. Render as an HTML kanban with one card per task, columns per status,
   project name visible on each card.

If `mcp__cowork__create_artifact` is unavailable, fall back to a
markdown table output covering the same data (less visually nice but
functional).

## Output on success

```
Rendered composite kanban as Cowork artifact:
  Projects included: <list>
  Tasks shown: <count>
  Status breakdown: planned=<n>, in-progress=<n>
```

The artifact appears in the chat view.

## Output on failure

- `registry not found at ~/.config/cowork/registry.yaml`
- `no enabled projects in registry`
- `mcp__cowork__create_artifact unavailable; falling back to markdown output`

## Standalone use

Same preconditions. Useful as a "what's everything on my plate" view
when juggling multiple writing projects.
