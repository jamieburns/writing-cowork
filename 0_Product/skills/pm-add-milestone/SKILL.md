---
name: pm-add-milestone
description: >
  This skill should be used when the user asks to "add a milestone",
  "add a phase", "add to the roadmap", "create a milestone in the
  now/next/later", or any variant of appending a new milestone entry to
  `<vault>/process/active/roadmap.md`. Works with both roadmap shapes
  (phase-based and now-next-later).
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-planning
---

# pm-add-milestone

Append a new milestone entry to the project's roadmap.md. The skill
detects the roadmap shape (phase or now-next-later) by parsing the
file's header and places the entry in the appropriate section.

## Arguments

- **`<name>`** (required) — short milestone name. For phase shape:
  passed verbatim. For now-next-later: same.
- **`--phase=<n>`** (optional, phase shape only) — explicit phase number.
  If omitted, append to the highest phase number + 1.
- **`--bucket=now|next|later`** (optional, now-next-later shape only) —
  which bucket to add to. Required for now-next-later; ignored for phase.
- **`--depends-on=<other-milestone>[,<another>]`** (optional) — comma-
  separated milestone names this one depends on. Surfaced in the
  milestone's notes.
- **`--goal=<text>`** (optional) — one-sentence goal statement. If
  omitted, leave a placeholder for the writer to fill in.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify `<vault>/process/active/roadmap.md` exists.
3. Parse the roadmap to detect shape (phase or now-next-later).
4. If shape is phase and `--bucket` is provided, abort with `roadmap is
   phase-shaped; use --phase=<n> instead of --bucket=`.
5. If shape is now-next-later and `--phase` is provided, abort with
   the symmetric error.
6. If `--depends-on` is provided, verify the referenced milestones exist
   in the roadmap. If not, warn but proceed (writer may be adding them
   later).

## Execution

Compose the milestone entry. For phase shape:

```markdown
### Phase <n> — <name>

**Goal:** <goal-or-placeholder>

**Gates:**

<!-- gates to be defined; replace this comment with - [ ] checkbox items as gates are decided -->

**Status:** planned

**Depends on:** <list-if-supplied>
```

For now-next-later shape: append a bullet to the appropriate bucket
section:

```markdown
- **<name>** — <goal-or-placeholder>. Depends on: <list-if-supplied>.
```

Atomic-write the modified roadmap.md.

The gates placeholder is intentionally a markdown comment, not a
checkbox. This way `pm-show-roadmap`'s gate counter shows "0 of 0
checked" (an absence) rather than "0 of 1 checked" (which would
mis-represent the placeholder as an unmet gate). Once real gates are
added, the comment line is replaced with `- [ ] <gate-text>` lines.

## Output on success

```
Added milestone <name> to roadmap.md
  Shape: <phase|now-next-later>
  Position: <phase-N | bucket-name>
  Goal: <goal-or-"placeholder">
```

## Output on failure

- `roadmap.md not found at <vault>/process/active/`
- `roadmap shape conflict: --<flag> doesn't match the roadmap's shape`
- `phase number <n> already exists; choose a different number or omit --phase`

## Standalone use

Same preconditions. Useful for ad-hoc planning sessions.
