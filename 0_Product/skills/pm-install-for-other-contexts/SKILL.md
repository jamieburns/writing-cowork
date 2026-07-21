---
name: pm-install-for-other-contexts
description: >
  This skill should be used when the user asks to "install the for-other-contexts
  doc", "create the cross-context briefing file", "add for_other_contexts.md
  to the vault", or any variant of placing the writing-cowork
  for-other-contexts template at the vault root. Copies
  templates/for_other_contexts.md into the vault, substituting
  project-specific placeholders. Invoked by pm-setup-project;
  also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-install-for-other-contexts

Copy `${CLAUDE_PLUGIN_ROOT}/templates/for_other_contexts.md` from the plugin to
`<vault>/process/data_management/for_other_contexts.md`, substituting
standard placeholders. Placement is `process/data_management/` (not vault
root) per the convention.

The for-other-contexts doc is the briefing surface for specialist chats
(voice, substance, review) joining a project mid-stream. Distinct from
handoff.md, which is for the main PM chat: this one is short and oriented
toward what a specialist needs to know to be useful on their first
invocation.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title; default
  title-cased `<name>`.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/data_management/` exists.
3. Verify `<vault-path>/process/data_management/for_other_contexts.md`
   does NOT already exist.
4. Verify the plugin's `${CLAUDE_PLUGIN_ROOT}/templates/for_other_contexts.md` exists.

## Execution

1. Read template, substitute `{{name}}`, `{{title}}`, `{{date_iso}}`,
   `{{vault_path}}`.
2. Atomic-write to
   `<vault-path>/process/data_management/for_other_contexts.md`.

## Output on success

```
Installed for_other_contexts.md at <vault-path>/process/data_management/for_other_contexts.md
```

## Output on failure

- `data_management directory missing; run pm-init-vault first`
- `for_other_contexts.md already exists at <vault>/process/data_management/for_other_contexts.md; remove it first or skip this step`
- `${CLAUDE_PLUGIN_ROOT}/templates/for_other_contexts.md not found in plugin install`

## Standalone use

Same preconditions.
