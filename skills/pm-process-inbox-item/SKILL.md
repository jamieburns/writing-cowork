---
name: pm-process-inbox-item
description: >
  This skill should be used when the user asks to "process the inbox",
  "handle an inbox item", "route a promotion request", or any variant of
  reading and applying a request in inbox/promotion/ or inbox/hub-updates/.
  Reads the request, applies its placement or hub-update instructions,
  archives the cover-note to process/history/.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-process-inbox-item

Read an inbox cover-note (promotion request or hub-update request), apply
its instructions (move artifact to canonical path, or edit hub), and
archive the cover-note to `process/history/`. Both sides of the inbox
transfer in one skill.

## Arguments

- **`<inbox-file>`** (required) — path (absolute or vault-relative) to
  the cover-note in `inbox/promotion/` or `inbox/hub-updates/`.
- **`--vault=<path>`** (optional) — vault root. Default: inferred from
  `<inbox-file>` path.

## Preconditions

1. Verify `<inbox-file>` exists and is a markdown file.
2. Parse the cover-note to determine request type:
   - Header "Promotion request" → artifact placement
   - Header "Hub update request" → hub edit
3. For promotion requests: verify the referenced artifact files also
   exist in the same inbox directory.
4. For hub-update requests: verify `<vault>/project_hub.md` exists.

## Execution — promotion request

1. Read the cover-note's `Proposed placement` field.
2. If placement is ambiguous (e.g., user says "decide for me"), prompt the
   user interactively for a target path. Do not silently choose.
3. Move the artifact file(s) from `inbox/promotion/` to the resolved
   target path. Use `git mv` if the project is git-tracked, otherwise
   filesystem `mv`. Preserves file history.
4. Add an entry to `<vault>/process/data_management/file_ownership.md`
   for the placed file (Status: working, Owner: data-mgmt).
5. Move the cover-note itself to `<vault>/process/history/<date>_promotion_<source>.md`
   (date in YYYY-MM-DD format, source from the cover-note's `From:` field).
6. Commit the changes with prefix `[promotion]` per HANDOFF.md conventions.

## Execution — hub update request

1. Parse the cover-note's sections ("Add to Recently completed",
   "Update in Current work threads", "Remove from Current work threads").
2. Apply each section's edits to `<vault>/project_hub.md`. Use atomic
   writes.
3. Move the cover-note to `<vault>/process/history/<date>_hub-update_<source>.md`.
4. Commit with prefix `[data-mgmt]`.

## Output on success — promotion

```
Processed promotion request from <source>:
  Moved: inbox/promotion/<file> → <target-path>
  Updated: process/data_management/file_ownership.md (added entry)
  Archived: process/history/<date>_promotion_<source>.md
  Committed: [promotion] <terse message>
```

## Output on success — hub update

```
Processed hub-update request from <source>:
  Updated project_hub.md sections: <list>
  Archived: process/history/<date>_hub-update_<source>.md
  Committed: [data-mgmt] <terse message>
```

## Output on failure

- `inbox file not found at <path>`
- `cover-note format unrecognized: expected 'Promotion request' or 'Hub update request' header`
- `placement ambiguous and writer not reachable; held in inbox`
- `referenced artifact <file> not found in inbox/promotion/`
- `git mv failed: <error>`
- `permission denied writing to <target>`

## Standalone use

Same preconditions. Useful when you have a stack of inbox items and want
to process them one at a time.
