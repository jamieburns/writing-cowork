---
name: pm-process-inbox-item
description: >
  This skill should be used when the user asks to "process the inbox",
  "handle an inbox item", "route a promotion request", "review an issue
  report", or any variant of reading and applying a request in
  inbox/promotion/, inbox/hub-updates/, or inbox/issues/. Reads the
  cover-note, applies the right action (placement, hub edit, or issue
  triage), and archives the cover-note to process/history/.
metadata:
  version: "0.1.1"
  role: pm
  subset: mvp-foundation
---

# pm-process-inbox-item

Read an inbox cover-note (promotion request, hub-update request, or
issue report), apply the appropriate action, and archive the cover-note
to `process/history/`. Both sides of the inbox transfer in one skill.

## Arguments

- **`<inbox-file>`** (required) — path (absolute or vault-relative) to
  the cover-note in `inbox/promotion/`, `inbox/hub-updates/`, or
  `inbox/issues/`.
- **`--vault=<path>`** (optional) — vault root. Default: inferred from
  `<inbox-file>` path.

## Preconditions

1. Verify `<inbox-file>` exists and is a markdown file.
2. Parse the cover-note to determine request type:
   - Header "Promotion request" → artifact placement
   - Header "Hub update request" → hub edit
   - Header "Issue report" → issue triage
3. For promotion requests: verify the referenced artifact files also
   exist in the same inbox directory.
4. For hub-update requests: verify `<vault>/project_hub.md` exists.
5. For issue reports: no extra precondition; the librarian reads and
   decides.

## Execution — promotion request

1. Read the cover-note's `Proposed placement` field.
2. If placement is ambiguous (e.g., user says "decide for me"), prompt the
   user interactively for a target path. Do not silently choose.
3. Move the artifact file(s) from `inbox/promotion/` to the resolved
   target path. Detect whether the **source file** is git-tracked via
   `git ls-files --error-unmatch <source>` (exit 0 if tracked, non-zero
   if untracked). If tracked, use `git mv` to preserve history. If
   untracked (common — inbox files are usually transient and never
   committed), use plain `mv` + `git add <target>` on the destination.
   Document which path was taken in the output. Do not let `git mv` fail
   silently when the source is untracked; that's the bug from MVP gating.
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

## Execution — issue report

Issues are triage items, not auto-actionable. The librarian decides
disposition per-issue.

1. Read the cover-note's title, description, severity, scope, and
   plugin-version fields.
2. Summarize the issue to the user (writer or invoking context) and
   ask for disposition:
   - **Escalate to GitHub** — invoke `pm-escalate-issue` against this
     cover-note. The skill creates a GitHub Issue, appends the URL to
     the cover-note, and archives the cover-note to
     `process/history/`. Best for plugin-level observations.
   - **Handle locally** — apply whatever vault-side fix is appropriate
     (edit a doc, adjust a config, etc.), then archive the cover-note
     to `<vault>/process/history/<date>_issue_<slug>_local.md` with a
     short disposition note appended. Best for vault-specific issues.
   - **Close (no action)** — archive to
     `<vault>/process/history/<date>_issue_<slug>_closed.md` with a
     short reason. Best for issues that turn out to be expected
     behavior, duplicates, or resolved before processing.

3. Commit the archive (and any local fixes) with prefix
   `[data-mgmt]` per HANDOFF.md conventions.

## Output on success — issue report (escalated)

```
Processed issue report from <source>:
  Disposition: escalated
  GitHub URL: <url>
  Archived: process/history/<date>_issue_<slug>_escalated.md
  Committed: [data-mgmt] <terse message>
```

## Output on success — issue report (handled locally)

```
Processed issue report from <source>:
  Disposition: handled locally
  Local fix: <one-line summary>
  Archived: process/history/<date>_issue_<slug>_local.md
  Committed: [data-mgmt] <terse message>
```

## Output on success — issue report (closed)

```
Processed issue report from <source>:
  Disposition: closed (no action)
  Reason: <one-line reason>
  Archived: process/history/<date>_issue_<slug>_closed.md
```

## Output on failure

- `inbox file not found at <path>`
- `cover-note format unrecognized: expected 'Promotion request' or 'Hub update request' header`
- `placement ambiguous and writer not reachable; held in inbox`
- `referenced artifact <file> not found in inbox/promotion/`
- `git mv failed: <error>` (only when source was tracked; untracked sources should fall back to `mv + git add` automatically)
- `permission denied writing to <target>`

## Standalone use

Same preconditions. Useful when you have a stack of inbox items and want
to process them one at a time.
