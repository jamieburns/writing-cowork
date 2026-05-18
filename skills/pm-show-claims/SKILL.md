---
name: pm-show-claims
description: >
  This skill should be used when the user asks "what's currently claimed",
  "show me file claims", "who's editing what", or any variant of querying
  the current claim state across the project. Reads file_ownership.md and
  lists rows where Status starts with `claimed:`.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-show-claims

Scan `<vault>/process/data_management/file_ownership.md` for rows with
`Status: claimed:<context>` and print them in a scannable table.

## Arguments

- **`--owner=<context>`** (optional) — filter to only claims by a specific
  context (e.g., `--owner=substance` shows only substance's claims).
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify ownership table exists. If not, output `no ownership table; no
   claims to show` and exit cleanly.

## Execution

1. Read `file_ownership.md`.
2. Parse the table rows. For each row, check if Status starts with `claimed:`.
3. Apply `--owner=` filter if set.
4. Format as a scannable table: `File | Claimed by | Notes`.

## Output on success

```
Currently claimed files (in <vault>/process/data_management/file_ownership.md):

  File                              Claimed by      Notes
  --------------------------------  --------------  ------------------
  part1_draft.md                    substance       mid-edit on §3.5
  process/active/voice_handoff.md   voice           preface-scaffold pass

2 file(s) currently claimed.
```

If no claims exist:

```
No files currently claimed in <vault>/process/data_management/file_ownership.md.
```

## Output on failure

- `file_ownership.md not found at <vault>/process/data_management/`
- `permission denied reading file_ownership.md`

## Standalone use

Pure read operation. Safe to run at any time. Useful when picking up a
project: see what other contexts are mid-edit before claiming anything
yourself.
