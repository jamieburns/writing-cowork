---
name: pm-update-milestone
description: >
  This skill should be used when the user asks to "update a milestone",
  "mark a phase done", "change milestone status", "add a dependency to
  a milestone", or any variant of editing an existing milestone entry in
  the project's roadmap.md. Works with both roadmap shapes.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-planning
---

# pm-update-milestone

Edit an existing milestone in `<vault>/process/active/roadmap.md`.
Common edits: change status, add or remove dependencies, update goal
text, mark gates checked.

## Arguments

- **`<name>`** (required) — milestone name to update.
- **`--status=planned|in-progress|done`** (optional) — set status.
- **`--depends-on=<list>`** (optional) — replace the depends-on list
  with the supplied comma-separated names.
- **`--goal=<text>`** (optional) — update the goal text.
- **`--check-gate=<gate-text>`** (optional) — mark a gate checkbox as
  done. Repeatable. Phase shape only.
- **`--uncheck-gate=<gate-text>`** (optional) — uncheck a gate. Repeatable.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root and verify roadmap.md exists.
2. Locate the milestone entry by name. If not found, abort with
   `milestone <name> not found in roadmap.md`.
3. If `--check-gate=` or `--uncheck-gate=` is provided and the roadmap
   is now-next-later shape (no gates), abort with `gates are phase-shape
   only; this roadmap is now-next-later`.

## Execution

1. Read roadmap.md.
2. Apply the requested edits to the milestone entry:
   - Update `**Status:**` line.
   - Replace or update `**Depends on:**` line.
   - Replace or update `**Goal:**` line.
   - For gate checks: find the `- [ ] <text>` line matching `<gate-text>`
     and change to `- [x] <text>` (or reverse for uncheck).
3. If status is `done` and the roadmap is phase-shape, optionally
   suggest moving the milestone to a "Locked phases (closed)" section.
   Do not auto-move without writer confirmation.
4. Atomic-write the modified roadmap.md.

## Output on success

```
Updated milestone <name>:
  <list of changes applied>
```

## Output on failure

- `roadmap.md not found`
- `milestone <name> not found in roadmap.md`
- `gate not found: <gate-text>`
- `gate operations require phase-shape roadmap`

## Standalone use

Same preconditions. Most common standalone use: marking a milestone done
when its work completes.
