---
name: pm-release-file
description: >
  This skill should be used when the user (or a specialist context) asks
  to "release a file", "unlock a file", "clear the claim on <path>", or
  any variant of returning a claimed file's Status in file_ownership.md to
  its working canonical value. Pairs with pm-claim-file. Typically runs
  on commit.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-release-file

Clear the `claimed:<context>` Status in
`<vault>/process/data_management/file_ownership.md` and return the file's
Status to its working canonical value. Typically invoked on commit.

## Arguments

- **`<file-path>`** (required) — vault-relative path.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.
- **`--status=<value>`** (optional) — explicit new Status. Default: infer
  from context — `canonical` for load-bearing files, `working` for
  in-development files. The skill picks a sensible default from the file's
  prior Notes or row context; user can override with `--status=`.

## Preconditions

1. Resolve vault root.
2. Verify ownership table exists.
3. Verify the file has a row in the table.
4. Verify the current Status is `claimed:<something>`. If it's already
   `canonical` or `working`, abort with `file <path> is not currently
   claimed; release is a no-op`.

## Execution

Edit the ownership table:

1. Read `file_ownership.md`.
2. Locate the row for `<file-path>`.
3. Update Status to the resolved new value.
4. Atomic-write.

## Output on success

```
Released claim on <file-path>
  Status: claimed:<context> → <new-status>
```

## Output on failure

- `file_ownership.md not found at <vault>/process/data_management/`
- `file <path> not listed in file_ownership.md`
- `file <path> is not currently claimed; release is a no-op`

## Standalone use

Specialist contexts invoke this on commit. Can also be invoked manually
to clear a stale claim (e.g., a chat ended mid-claim and never released).
