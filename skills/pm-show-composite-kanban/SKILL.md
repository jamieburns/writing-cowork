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

**v0.1.15 TODO:** Update this skill to support the same `--by=` and
`--show=` options as pm-show-kanban (v0.1.14). Currently only supports
grouping by status; will add support for grouping by assignee and milestone
with optional column display.

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

Per writing-cowork locked decision #11: **always re-pull on view; no
static snapshot.** The artifact must fetch fresh task data each time
it's opened, not just once at creation time. This is enforced by the
artifact's HTML calling `window.cowork.callMcpTool` (or
`window.cowork.askClaude` if file-read happens through Claude rather
than a direct MCP) on every open / reload, not by embedding static
data in the HTML at creation.

1. Build the artifact HTML with these properties:
   - On page load, the HTML calls `window.cowork.callMcpTool` (or
     equivalent) to read each enabled project's `todos.md` from disk.
   - For each project, detect the schema (plugin schema vs legacy
     checkbox vs empty) — same detection as pm-list-tasks.
   - Aggregate tasks across projects, group by status, render columns.
   - For projects with non-schema todos.md (e.g., Reconciliation legacy
     format), either render them as a separate "(legacy format)" column
     OR omit them with a note in the artifact header. Pick one
     consistently.
   - Project name visible on every card.
2. Apply user's `--status-filter` and `--project-filter` at render time
   (within the artifact's JavaScript, against the freshly-fetched data).
3. The Cowork artifact framework auto-caches reads transparently — the
   `callMcpTool` results are cached per-open, refreshed on Reload button.

Call `mcp__cowork__create_artifact` with the HTML. If that tool is
unavailable, fall back to a static markdown table covering the same
data (acknowledge the regression in the output: "Live-refresh
unavailable in this Cowork build; rendered static snapshot.").

**The static-snapshot fallback is NOT the default behavior.** It's the
last-resort path when the artifact framework isn't available. MVP
gating found the skill defaulting to static; v0.1.4 fixes the default
to live-refresh.

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
