---
name: pm-register-project
description: >
  This skill should be used when the user asks to "register a project",
  "add this project to the cowork registry", "enable drift check for this
  vault", or any variant of adding a project entry to the per-machine
  cowork registry. Appends a new entry to ~/.config/cowork/registry.yaml
  pointing at the project's drift_check.yaml. Invoked by pm-setup-project
  as the final step; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-register-project

Append the project to `~/.config/cowork/registry.yaml`, the per-machine
registry that `~/code/cowork-tools/drift_check.py --all` reads. After
registration, the nightly launchd drift-check job picks the project up
automatically.

The registry is the shared cowork-tools surface — distinct from the
writing-cowork plugin's setup state file. Multiple plugins and tools may
share the registry; only writing-cowork's per-project state lives under
the `writing-cowork/` subdirectory of the cowork config root.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault. Used to
  resolve the config path (`<vault-path>/process/data_management/drift_check.yaml`).
- **`<name>`** (required) — project slug; appears as the `name:` field in
  the registry entry.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/data_management/drift_check.yaml` exists
   (created earlier by `pm-install-drift-check-config`). If absent, abort
   with `drift_check.yaml not found at <expected path>; run
   pm-install-drift-check-config first`.
3. Verify `~/.config/cowork/registry.yaml` exists. If absent, create it
   atomically with the minimal valid content:

   ```yaml
   # Cowork drift-check registry — per-machine.
   # Lives at ~/.config/cowork/registry.yaml.
   projects:
   ```

4. Verify the registry does NOT already contain a `name: <name>` entry.
   If it does, abort with `project <name> is already registered in
   ~/.config/cowork/registry.yaml; remove that entry first or use a
   different name`.

## Execution

1. Read `~/.config/cowork/registry.yaml`.
2. Parse the YAML (PyYAML preferred; the cowork-tools installer ensures
   it's present per cowork-tools README).
3. Append a new entry to the `projects:` list:

   ```yaml
   - name: <name>
     config: "<vault-path>/process/data_management/drift_check.yaml"
     enabled: true
   ```

4. Write the result back to `~/.config/cowork/registry.yaml` atomically
   (write to `registry.yaml.tmp`, then `mv`).

Use YAML round-trip (e.g., `ruamel.yaml`) if available to preserve comments
and ordering; if only stock `yaml` (PyYAML) is available, accept that
comments will be lost on rewrite and surface that in the success output as
a one-line note.

## Output on success

```
Registered project <name> in ~/.config/cowork/registry.yaml
  config: <vault-path>/process/data_management/drift_check.yaml
  enabled: true
```

If comments were stripped during round-trip:

```
Registered project <name> in ~/.config/cowork/registry.yaml
  config: <vault-path>/process/data_management/drift_check.yaml
  enabled: true
  Note: comments stripped (PyYAML round-trip); consider installing ruamel.yaml for comment preservation.
```

## Output on failure

- `drift_check.yaml not found at <expected path>; run pm-install-drift-check-config first`
- `project <name> is already registered in ~/.config/cowork/registry.yaml; remove that entry first or use a different name`
- `~/.config/cowork/registry.yaml is invalid YAML: <parse error>. Inspect the file before retrying.`
- `permission denied writing to ~/.config/cowork/registry.yaml`

## Standalone use

Same preconditions. Useful for registering a project that was set up
before pm-register-project existed, or for re-registering after a manual
registry edit.
