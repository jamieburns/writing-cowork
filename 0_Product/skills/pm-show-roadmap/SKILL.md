---
name: pm-show-roadmap
description: >
  This skill should be used when the user asks to "show the roadmap",
  "display the project roadmap", "what's the phase plan", or any variant
  of rendering `<vault>/process/active/roadmap.md` in a scannable view.
  Returns the canonical view (whatever shape the roadmap was set up with).
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-planning
---

# pm-show-roadmap

Render the project's roadmap.md in its canonical shape — phase-based
view if the roadmap was set up that way, now-next-later view otherwise.
For the alternative derived view, use `pm-show-status`.

## Arguments

- **`--vault=<path>`** (optional) — vault root. Default: cwd.
- **`--format=text|markdown`** (optional, default `markdown`) — output
  format.

## Preconditions

1. Resolve vault root.
2. Verify roadmap.md exists. If not, output `no roadmap found; run
   pm-init-roadmap to create one` and exit cleanly.

## Execution

1. Read roadmap.md.
2. Parse milestones into a structured form.
3. Render per `--format`:
   - `markdown`: pass through the file's markdown structure with a
     summary header (total milestones, count by status).
   - `text`: render as a flat table — name, status, depends-on,
     short-goal.

## Output on success (phase shape, markdown)

```
Roadmap for <project> (phase shape)

  Phases: 4
  Status counts: planned=2, in-progress=1, done=1

  Phase 1 — Foundation [done]
    Goal: ...
  Phase 2 — Core build [in-progress]
    Goal: ...
  Phase 3 — Integration [planned]
    Goal: ...
  Phase 4 — Release [planned]
    Goal: ...
```

## Output on failure

- `no roadmap found at <vault>/process/active/roadmap.md`
- `roadmap.md is malformed; could not parse milestones`

## Standalone use

Pure read operation. Safe anytime.
