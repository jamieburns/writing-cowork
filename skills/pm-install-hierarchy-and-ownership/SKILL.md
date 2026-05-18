---
name: pm-install-hierarchy-and-ownership
description: >
  This skill should be used when the user asks to "install file hierarchy",
  "set up the ownership table", "scaffold data-management docs",
  "install file_hierarchy.md and file_ownership.md", or any variant of
  placing the two core data-management documents into a new vault.
  Copies templates/file_hierarchy.md and templates/file_ownership.md into
  the vault's process/data_management/ directory. Invoked by pm-setup-project;
  also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-install-hierarchy-and-ownership

Place the two foundational data-management documents into a new vault:

- `process/data_management/file_hierarchy.md` — conceptual layout of vault
  contents; describes which folders hold what kind of content.
- `process/data_management/file_ownership.md` — the claim/release table
  used by `pm-claim-file` / `pm-release-file` / `pm-show-claims` and read
  by drift_check.py.

Both files start as templates with a generic baseline; writers fill in
project-specific entries over time.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title; default
  title-cased `<name>`.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/data_management/` exists (pm-init-vault
   created it). If absent, abort with `data_management directory missing;
   run pm-init-vault first`.
3. Verify neither `file_hierarchy.md` nor `file_ownership.md` already
   exists in `process/data_management/`. If either does, abort with a
   specific message identifying which.
4. Verify the plugin's `templates/file_hierarchy.md` and
   `templates/file_ownership.md` both exist.

## Execution

For each of the two templates:

1. Read the template from the plugin.
2. Substitute `{{name}}`, `{{title}}`, `{{date_iso}}`, `{{vault_path}}`.
3. Atomic-write to the target path in `process/data_management/`.

Both writes must complete successfully. If `file_hierarchy.md` writes
cleanly but `file_ownership.md` fails, leave `file_hierarchy.md` in place
and return the failure for `file_ownership.md` — pm-resume-setup will
re-run the whole skill; the precondition check will then catch
`file_hierarchy.md` already existing and report.

This is a deliberate trade-off — atomicity at the two-file level would
require a more elaborate rollback than the manual-phase convention
supports. Two files is a small enough scope that the resume-then-clean
flow is acceptable.

## Output on success

```
Installed data-management scaffolding at <vault-path>/process/data_management/
  file_hierarchy.md
  file_ownership.md
```

## Output on failure

- `data_management directory missing; run pm-init-vault first`
- `file_hierarchy.md already exists at <path>; remove it first or skip this step`
- `file_ownership.md already exists at <path>; remove it first or skip this step`
- `templates/file_hierarchy.md not found in plugin install`
- `templates/file_ownership.md not found in plugin install`

## Standalone use

Same preconditions. Useful for retrofitting the data-management baseline
onto an existing project that was set up before this skill existed.
