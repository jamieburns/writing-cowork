---
name: pm-install-charter
description: >
  This skill should be used when the user asks to "install the charter",
  "create the project charter", "add a charter file to the vault", or any
  variant of placing the writing-cowork charter template at the vault root.
  Copies templates/charter.md into the vault, substituting project-specific
  placeholders. Invoked by pm-setup-project; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-install-charter

Copy `templates/charter.md` from the plugin to
`<vault>/process/data_management/charter.md`, substituting standard
placeholders. Placement is `process/data_management/` (not vault root) to
keep substantive writing artifacts visible at the root and group all
process/PM documents together.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — the project's slug; substituted for `{{name}}`
  in the template.
- **`--title=<title>`** (optional) — human-readable project title;
  substituted for `{{title}}`. Default: title-cased `<name>` with hyphens
  replaced by spaces (e.g., `morning-letters` → `Morning Letters`).

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/data_management/` exists (pm-init-vault
   created it). If absent, abort with `data_management directory missing;
   run pm-init-vault first`.
3. Verify `<vault-path>/process/data_management/charter.md` does NOT
   already exist. If it does, abort with `charter.md already exists at
   <expected path>; remove it first or skip this step`.
4. Verify the plugin's `templates/charter.md` exists and is readable.

## Execution

1. Read `templates/charter.md` from the plugin's templates directory.
2. Substitute these placeholders in the content:
   - `{{name}}` → `<name>` arg
   - `{{title}}` → resolved title
   - `{{date_iso}}` → today's date in YYYY-MM-DD format (UTC)
   - `{{vault_path}}` → absolute `<vault-path>`
3. Write the result to `<vault-path>/process/data_management/charter.md`
   atomically: write to `charter.md.tmp` in the same directory, then `mv`
   to `charter.md`.

## Output on success

```
Installed charter.md at <vault-path>/process/data_management/charter.md
  Substituted: {{name}}={{name-value}}, {{title}}={{title-value}}, {{date_iso}}={{today}}
```

## Output on failure

Specific error plus the most likely fix. Examples:

- `data_management directory missing; run pm-init-vault first`
- `charter.md already exists at <vault>/process/data_management/charter.md; remove it first or skip this step`
- `templates/charter.md not found in plugin install (plugin may be corrupted; reinstall)`
- `permission denied writing to <vault-path>/process/data_management/`

Do not partial-write. If the atomic-write `mv` fails, the `.tmp` file is left
in place; subsequent runs of this skill will detect it and abort with a
specific error so the user can investigate.

## Standalone use

When invoked outside the orchestrator, the same preconditions apply. The
vault must exist; charter.md must not. Useful for retrofitting a charter
onto an existing project that was set up before this skill existed.
