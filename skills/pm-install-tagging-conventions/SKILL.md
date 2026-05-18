---
name: pm-install-tagging-conventions
description: >
  This skill should be used when the user asks to "install the tagging
  conventions", "create tagging_conventions.md", "set up the git tag
  conventions doc", or any variant of placing the writing-cowork git tag
  reference doc. Copies templates/tagging_conventions.md into the vault's
  process/data_management/ directory. Pure reference doc — only project name
  is substituted. Invoked by pm-setup-project; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-install-tagging-conventions

Copy `templates/tagging_conventions.md` from the plugin to
`<vault>/process/data_management/tagging_conventions.md`. The doc defines
the three writing-cowork git tag namespaces (`release/`, `lock/`,
`snapshot/`) and the workflows for each. Reference doc — only the project
name is substituted; the conventions themselves are project-invariant.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/data_management/` exists.
3. Verify `<vault-path>/process/data_management/tagging_conventions.md`
   does NOT already exist.
4. Verify the plugin's `templates/tagging_conventions.md` exists.

## Execution

1. Read template, substitute `{{name}}`, `{{title}}`, `{{date_iso}}`.
2. Atomic-write to
   `<vault-path>/process/data_management/tagging_conventions.md`.

## Output on success

```
Installed tagging_conventions.md at <vault-path>/process/data_management/tagging_conventions.md
```

## Output on failure

- `data_management directory missing; run pm-init-vault first`
- `tagging_conventions.md already exists at <path>; remove it first or skip this step`
- `templates/tagging_conventions.md not found in plugin install`

## Standalone use

Same preconditions.
