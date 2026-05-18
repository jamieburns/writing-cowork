---
name: pm-schedule-review
description: >
  This skill should be used when the user asks to "schedule a review",
  "set a reminder to revisit", "schedule a task for later", or any variant
  of creating a Cowork scheduled task pointed at a follow-up activity for
  this project. Wraps mcp__scheduled-tasks__create_scheduled_task with
  writing-cowork conventions.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-planning
---

# pm-schedule-review

Create a scheduled task in Cowork's scheduler that fires at a future
moment (or on a recurring schedule) and runs a prompt scoped to this
writing project. Convenient wrapper around the underlying
`mcp__scheduled-tasks__create_scheduled_task` MCP tool.

Use cases:
- "Revisit this question on 2026-06-15."
- "Every Monday morning, summarize last week's progress."
- "In two weeks, check whether the absence audit is due."

## Arguments

- **`<description>`** (required) — what the scheduled task should do.
  Will be expanded into a full prompt for the scheduled run.
- **`--when=<expression>`** (required) — when to fire. Accepts:
  - Absolute: `2026-06-15T09:00:00-04:00` (ISO 8601 with tz offset).
  - Relative: `tomorrow at 9am`, `in 2 weeks`, `monday 6am`.
  - Recurring: `every weekday at 9am`, `every monday at 8am`.
- **`--task-id=<slug>`** (optional) — kebab-case ID for the scheduled
  task. Default: derive from `<description>` (first 5 words).
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify `mcp__scheduled-tasks__create_scheduled_task` is available.
   If not, abort with `scheduled-tasks MCP not loaded; cannot schedule.`
3. Parse `<expression>` into either a `fireAt` (one-time) or
   `cronExpression` (recurring). If parsing fails, ask user to clarify.

## Execution

1. Expand `<description>` into a full prompt for the scheduled run.
   Include:
   - Project context: "This task runs in the context of <vault-path>."
   - The description as the primary instruction.
   - A note that the scheduled run starts fresh — no chat history.
2. Call `mcp__scheduled-tasks__create_scheduled_task` with:
   - `taskId`: derived or supplied
   - `description`: short one-line summary
   - `prompt`: the expanded prompt from step 1
   - `fireAt` or `cronExpression` per parsed expression

Note that scheduled tasks run only while Cowork is open. If Cowork is
closed when a scheduled task is due, it fires on next Cowork launch.
Include this caveat in the output.

## Output on success

```
Scheduled review created: <task-id>
  Fires: <fireAt or cronExpression>
  Description: <description>
  Project context: <vault>

Note: scheduled tasks run only while Cowork is open. If Cowork is closed
at the scheduled time, the task fires on next launch.
```

## Output on failure

- `scheduled-tasks MCP not loaded; cannot schedule`
- `could not parse --when=<expression>`
- `scheduled task creation failed: <error>`

## Standalone use

Same preconditions. Useful for tying recurring planning rituals
(weekly check-ins, monthly drift audits) into the writing project's
working rhythm.
