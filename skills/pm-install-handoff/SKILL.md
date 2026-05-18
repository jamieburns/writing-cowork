---
name: pm-install-handoff
description: >
  This skill should be used when the user asks to "install the handoff doc",
  "create the project handoff file", "add a handoff.md to the vault", or any
  variant of placing the writing-cowork handoff template at the vault root.
  Copies templates/handoff.md into the vault, substituting project-specific
  placeholders. Invoked by pm-setup-project; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-install-handoff

Copy `templates/handoff.md` from the plugin to `<vault>/handoff.md`,
substituting standard placeholders.

The handoff doc is the routing document for any new Claude chat picking up
work on the project — it tells new context what's built, what's outstanding,
and what conventions to follow. The template is a generic skeleton; writers
fill in project specifics over time.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug, substituted for `{{name}}`.
- **`--title=<title>`** (optional) — human-readable title; substituted for
  `{{title}}`. Default: title-cased `<name>`.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/handoff.md` does NOT already exist.
3. Verify the plugin's `templates/handoff.md` exists.

## Execution

1. Read `templates/handoff.md` from the plugin's templates directory.
2. Substitute `{{name}}`, `{{title}}`, `{{date_iso}}`, `{{vault_path}}`.
3. Atomic-write to `<vault-path>/handoff.md`.

## Output on success

```
Installed handoff.md at <vault-path>/handoff.md
```

## Output on failure

- `handoff.md already exists at vault root; remove it first or skip this step`
- `templates/handoff.md not found in plugin install`
- `permission denied writing to <vault-path>`

## Standalone use

Same preconditions. Useful for retrofitting a handoff onto an existing
project.
