---
name: pm-install-project-hub
description: >
  This skill should be used when the user asks to "install the project hub",
  "create project_hub.md", "set up the where-am-I doc", or any variant of
  placing the writing-cowork project hub at the vault root. Copies
  templates/project_hub.md into the vault root, substituting project-specific
  placeholders. Invoked by pm-setup-project; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-install-project-hub

Copy `${CLAUDE_PLUGIN_ROOT}/templates/project_hub.md` from the plugin to `<vault>/project_hub.md`
(vault root — this is the exception to the "minimum at root" rule because
the hub is the navigation entry point and `drift_check.yaml`'s `hub:` field
points at it).

The hub contains a tool-managed `## Attention` block written by drift-check
on each run, plus librarian-edited sections for project paragraph,
navigation table, current work threads, recently completed, and see-also.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title; default
  title-cased `<name>`.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/project_hub.md` does NOT already exist.
3. Verify the plugin's `${CLAUDE_PLUGIN_ROOT}/templates/project_hub.md` exists.

## Execution

1. Read `${CLAUDE_PLUGIN_ROOT}/templates/project_hub.md` from the plugin.
2. Substitute `{{name}}`, `{{title}}`, `{{date_iso}}`, `{{vault_path}}`.
3. Atomic-write to `<vault-path>/project_hub.md`.

The template includes the `<!-- DRIFT-ATTENTION-START -->` / `<!-- DRIFT-ATTENTION-END -->`
marker pair in the Attention section, pre-populated with a benign "no drift
yet" placeholder. The drift-check skill rewrites this block on each run.

## Output on success

```
Installed project_hub.md at <vault-path>/project_hub.md
```

## Output on failure

- `project_hub.md already exists at <vault-path>/project_hub.md; remove it first or skip this step`
- `${CLAUDE_PLUGIN_ROOT}/templates/project_hub.md not found in plugin install`
- `permission denied writing to <vault-path>`

## Standalone use

Same preconditions. The hub is required by drift-check, so installing it is
not optional for active projects. Useful for retrofitting onto an existing
project.
