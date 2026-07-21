---
name: pm-create-hub-update-request
description: >
  This skill should be used when a specialist context asks to "request a
  hub update", "ask the librarian to update the project hub", or any
  variant of producing an inbox/hub-updates/ cover-note describing
  desired changes to project_hub.md. The librarian processes the request
  via pm-process-inbox-item.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-create-hub-update-request

Drops a hub-update-request cover-note into `<vault>/inbox/hub-updates/`
(or `inbox/promotion/` if the project uses only the single inbox
convention). Describes changes the requesting context wants made to
`project_hub.md`. The librarian integrates on its next pass.

## Arguments

- **`--section=<section-name>`** (required, repeatable) — which hub
  section to edit (e.g., `Recently completed`, `Current work threads`,
  `Project paragraph`).
- **`--change=add|update|remove`** (required, paired with `--section=`) —
  the kind of change.
- **`--content=<text>`** (required, paired) — the text to add, the
  replacement text for an update, or the bullet to remove.
- **`--from=<context>`** (optional, default `substance`) — the requesting
  context.
- **`--vault=<path>`** (optional) — vault root.

For multiple sections, pass multiple sets of `--section/--change/--content`.

## Preconditions

1. Resolve vault root.
2. Verify the project has an inbox directory for hub updates:
   prefer `<vault>/inbox/hub-updates/`; fall back to
   `<vault>/inbox/promotion/`. Abort if neither exists.
3. Verify the cover-note destination is unique (timestamp suffix if
   collision).

## Execution

Write the cover-note at
`<vault>/inbox/<inbox-subdir>/<YYYY-MM-DD>_<from>_hub-update.md`:

```markdown
# Hub update request

**From:** <from>
**Date:** YYYY-MM-DD

## <change> <section-name>
<content>

## <next change if multiple sections>
...
```

Atomic-write.

## Output on success

```
Created hub-update request at <vault>/inbox/<subdir>/<date>_<from>_hub-update.md:
  Sections: <list>
  From: <from>

Librarian will integrate via pm-process-inbox-item on next pass.
```

## Output on failure

- `inbox directory not found at <vault>/inbox/; run pm-init-vault first`
- `cover-note destination collision; consider passing a unique --from value`
- `permission denied writing to inbox/`

## Standalone use

Specialist contexts call this directly. Useful when the specialist
finishes work and wants the project hub to reflect their progress (e.g.,
adding to "Recently completed" or updating "Current work threads").
