---
name: pm-claim-file
description: >
  This skill should be used when the user (or a specialist context like
  substance/voice/reader-review) asks to "claim a file", "lock a file for
  editing", "mark <path> as claimed by <context>", or any variant of
  setting a file's Status in file_ownership.md to claimed:<context>.
  Pairs with pm-release-file. Implements the claim/release protocol from
  the data-management charter.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-claim-file

Set a file's `Status` column in `<vault>/process/data_management/file_ownership.md`
to `claimed:<context>`. This prevents other contexts from inadvertently
overwriting work in progress (per the claim-dispute protocol).

## Arguments

- **`<file-path>`** (required) — vault-relative path to the file, as it
  appears in the ownership table (e.g., `part1_draft.md`,
  `process/active/todos.md`).
- **`<context>`** (required) — the context claiming the file. Standard
  values: `data-mgmt`, `substance`, `voice`, `reader-review`, `writer`.
- **`--vault=<path>`** (optional) — vault root. Default: current directory.
- **`--notes=<text>`** (optional) — append a brief note to the file's
  `Notes` column (e.g., `--notes="mid-edit on §3.5"`).

## Preconditions

1. Resolve vault root (default: cwd; or `--vault=`).
2. Verify `<vault>/process/data_management/file_ownership.md` exists.
3. Verify `<file-path>` has a row in the ownership table. If not, abort
   with `file <path> not listed in file_ownership.md; either the file is
   new (and needs an ownership-table entry first) or the path is wrong`.
4. Check current Status. If already `claimed:<other>`, abort with
   `file already claimed by <other>; consult claim_dispute_protocol.md
   for resolution paths (A/B/C)`. Do not overwrite an existing claim
   silently.

## Execution

Edit the ownership table in place via atomic write:

1. Read `file_ownership.md`.
2. Locate the row for `<file-path>` (the row whose first table column
   matches the path or filename).
3. Update the `Status` column to `claimed:<context>`.
4. If `--notes=<text>`, append to or replace the `Notes` column.
5. Write to `file_ownership.md.tmp`, then `mv` to `file_ownership.md`.

Preserve all other rows and formatting verbatim.

## Output on success

```
Claimed file_ownership.md row for <file-path>
  Status: <previous> → claimed:<context>
  Notes: <updated notes if --notes was supplied>
```

## Output on failure

- `file_ownership.md not found at <vault>/process/data_management/`
- `file <path> not listed in file_ownership.md`
- `file already claimed by <other>; consult claim_dispute_protocol.md`
- `permission denied writing to file_ownership.md`

## Standalone use

Same preconditions. Specialist contexts (voice, substance, reader-review)
invoke this directly when claiming a file before editing. The librarian
context (data-mgmt) also uses it for its own claims before mechanical work.
