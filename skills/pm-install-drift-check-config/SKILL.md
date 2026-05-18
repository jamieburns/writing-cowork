---
name: pm-install-drift-check-config
description: >
  This skill should be used when the user asks to "install the drift check
  config", "set up drift_check.yaml", "configure drift detection for this
  vault", or any variant of placing the project-specific drift_check
  configuration. Copies templates/drift_check.yaml into the vault's
  process/data_management/ directory, substituting project-specific values.
  Invoked by pm-setup-project; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-install-drift-check-config

Install `process/data_management/drift_check.yaml` from the plugin's
template, substituting project-specific values. Once placed and registered,
this is the config that `~/code/cowork-tools/drift_check.py` reads for
this project.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault. Used directly
  as the `vault:` field in the YAML.
- **`<name>`** (required) — project slug; used for log greppability.
- **`--title=<title>`** (optional) — human-readable title; substituted for
  `project_name:` in the YAML. Default: title-cased `<name>`.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/data_management/` exists.
3. Verify `<vault-path>/process/data_management/drift_check.yaml` does NOT
   already exist.
4. Verify the plugin's `templates/drift_check.yaml` exists.

## Execution

1. Read `templates/drift_check.yaml` from the plugin.
2. Substitute placeholders:
   - `{{name}}` → `<name>` arg
   - `{{title}}` → resolved title (used as `project_name:` value)
   - `{{vault_path}}` → absolute `<vault-path>` (used as `vault:` value)
   - `{{date_iso}}` → today's date YYYY-MM-DD
3. Atomic-write to `<vault-path>/process/data_management/drift_check.yaml`.

The template ships with sensible defaults for `exclude_prefixes`,
`exclude_patterns`, `markers`, `inbox.buckets`, etc., matching the
Reconciliation pattern. Project-specific overrides (e.g., build pipeline
configuration, custom xref_targets beyond `project_hub.md`) are added by
the writer in follow-up edits.

## Output on success

```
Installed drift_check.yaml at <vault-path>/process/data_management/drift_check.yaml
  project_name: <title>
  vault: <vault-path>
```

## Output on failure

- `drift_check.yaml already exists at <path>; remove it first or skip this step`
- `data_management directory missing; run pm-init-vault first`
- `templates/drift_check.yaml not found in plugin install`

## Standalone use

Same preconditions. The drift_check.yaml is the bridge between a project
and cowork-tools — without it, the project can't be registered via
pm-register-project, and drift_check.py has nothing to read.
