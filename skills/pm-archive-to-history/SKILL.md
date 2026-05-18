---
name: pm-archive-to-history
description: >
  This skill should be used when the user asks to "archive a file",
  "move <file> to history", "close out an active task doc", or any
  variant of moving a file from process/active/ to process/history/.
  Optionally renames the file with a date prefix during the move.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-archive-to-history

Move a file from `<vault>/process/active/` to `<vault>/process/history/`,
optionally adding a date prefix to the filename for chronological sorting.
Update the file's row in `file_ownership.md` to `archived`.

## Arguments

- **`<file>`** (required) — vault-relative path to the file in
  `process/active/` (e.g., `process/active/workstream_3_handoff.md`).
- **`--reason=<text>`** (optional) — appended to the file's Notes column
  in the ownership table.
- **`--date-prefix`** (optional, flag) — prepend today's date to the
  filename: `workstream_3_handoff.md` → `2026-05-17_workstream_3_handoff.md`.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify `<file>` exists under `<vault>/process/active/`.
3. Verify `<vault>/process/history/` exists.
4. Compute the destination path (with date prefix if `--date-prefix`).
5. Verify the destination doesn't already exist.

## Execution

1. Use `git mv` if the project is git-tracked; otherwise filesystem `mv`.
   `git mv` preserves history under `git log --follow`.
2. Update the row in `file_ownership.md`:
   - Update the path (if `--date-prefix` changed the filename).
   - Set Status to `archived`.
   - Append `--reason=<text>` to Notes column if provided.
3. Atomic-write the ownership table.

The skill does NOT commit. The caller (typically the librarian context)
commits with prefix `[data-mgmt]` after batching archive moves.

## Output on success

```
Archived: process/active/<old-name> → process/history/<new-name>
  Status: <prev> → archived
  Notes: <appended-reason>
```

## Output on failure

- `file not found at <vault>/process/active/<file>`
- `process/history/ not found; run pm-init-vault first`
- `destination already exists at <path>; choose a different name or remove the existing file`
- `git mv failed: <error>`
- `file <path> not listed in file_ownership.md; archive proceeds but ownership table is out of sync — add the entry manually`

## Standalone use

Same preconditions. Useful for closing out workstream handoff docs,
archived audit reports, completed coherence action plans, etc.
