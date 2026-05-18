---
name: pm-show-status
description: >
  This skill should be used when the user asks to "show project status",
  "show me what's going on", "what's now and next", or any variant of
  rendering a Now/Next/Later derived view of the project roadmap.
  Highlights blockers explicitly (unmet dependencies on in-progress or
  planned milestones).
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-planning
---

# pm-show-status

Render the roadmap as a Now/Next/Later derived view, regardless of the
roadmap's underlying shape. For phase-shape roadmaps, in-progress phases
become Now; next-scheduled planned phases become Next; the rest become
Later. For now-next-later roadmaps, the view is direct.

Surfaces blockers: any milestone whose `depends-on` references a
milestone that isn't `done`.

## Arguments

- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify roadmap.md exists.

## Execution

1. Parse roadmap.md into structured milestones.
2. Derive Now/Next/Later bucketing:
   - **Now:** milestones with `status: in-progress`.
   - **Next:** milestones with `status: planned` AND whose dependencies
     are all `done` (or have no dependencies).
   - **Later:** milestones with `status: planned` AND at least one
     unmet dependency.
3. For each milestone, check if it has unmet dependencies. Annotate
   blocked milestones with `(blocked by: <list>)`.
4. Count Done separately (won't appear in Now/Next/Later).

## Output on success

```
Project status for <project> (Now/Next/Later derived view)

  Now (in-progress, 2 milestones):
    - Phase 2 — Core build
    - Voice pass on §A

  Next (planned + unblocked, 1 milestone):
    - Phase 3 — Integration

  Later (planned + blocked, 2 milestones):
    - Phase 4 — Release  (blocked by: Phase 3)
    - Reader-review round 1  (blocked by: Phase 3, Voice pass on §A)

  Done (5 milestones):
    - Phase 1 — Foundation
    - ...
```

If the roadmap is empty (no milestones yet):

```
No milestones in roadmap.md yet. Use pm-add-milestone to start populating.
```

## Output on failure

- `roadmap.md not found`
- `roadmap.md is malformed; could not parse milestones`

## Standalone use

Pure read. Useful as a "where am I" command at session start.
