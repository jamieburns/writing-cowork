---
name: pm-init-reader-review-tracking
description: >
  This skill should be used when the user asks to "initialize reader review
  tracking", "create reviewer_tracking.md", "set up the reviewer tracking
  file", or any variant of creating the reader/reviewer status tracking
  document. Creates an empty (header-only) reviewer_tracking.md in the
  vault's process/active/ directory. Invoked by pm-setup-project;
  also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-init-reader-review-tracking

Create an initially-empty `process/active/reviewer_tracking.md` with a
minimal header. This file tracks per-reviewer status — who has been sent
what, what stage their feedback is in, and whether their input has been
integrated. Used by review skills in Subset 4 (`ingest-human-review`,
`triage-review`, `update-reviewer-tracking`, `list-reviewer-status`).

The file starts empty (header only). Reviewer rows are appended as
reviewers are added.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug; used in the header line.
- **`--title=<title>`** (optional) — human-readable title.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/active/` exists.
3. Verify `<vault-path>/process/active/reviewer_tracking.md` does NOT
   already exist.

## Execution

Atomic-write the following content to
`<vault-path>/process/active/reviewer_tracking.md`:

```markdown
# Reviewer tracking — <title>

Created: <date_iso>

Tracked here: reader/reviewer engagements. One row per reviewer.
Status values: `pending` (not yet sent) → `sent` (package out) →
`read` (reviewer confirmed receipt) → `triaged` (feedback classified) →
`responded` (writer reply sent) → `integrated` (changes landed).

| Reviewer ID | Name | Package sent | Status | Last updated | Notes |
|-------------|------|--------------|--------|--------------|-------|
```

## Output on success

```
Initialized reviewer_tracking.md at <vault-path>/process/active/reviewer_tracking.md
```

## Output on failure

- `process/active directory missing; run pm-init-vault first`
- `reviewer_tracking.md already exists at <path>; remove it first or skip this step`

## Standalone use

Same preconditions.
