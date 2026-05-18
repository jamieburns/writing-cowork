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

Use **text-append**, not YAML round-trip. The registry has a stable shape
(a single top-level `projects:` list of dicts) where adding a new entry is
purely additive — we never need to mutate existing entries or other top-level
keys. Text-append preserves all comments (which YAML round-trip via PyYAML
would strip) and avoids needing `ruamel.yaml` as a runtime dependency.

1. Read `~/.config/cowork/registry.yaml` (existing content).
2. Build the new entry text:

   ```yaml

     - name: <name>
       config: "<vault-path>/process/data_management/drift_check.yaml"
       enabled: true
   ```

   Note: leading blank line for readability; two-space indent matches the
   convention used by the existing entries.

3. Write `<existing-content> + <new-entry-text>` to
   `~/.config/cowork/registry.yaml.tmp`.
4. **Validate the result** by parsing it with PyYAML before committing the
   write: `python3 -c "import yaml; yaml.safe_load(open('<tmp-path>'))"`.
   If parsing fails, abort with the parse error — do NOT overwrite the
   original file. The user inspects what went wrong before retrying.
5. On valid parse, `mv registry.yaml.tmp registry.yaml`.

This approach preserves comments, the `enabled: false` flag on individual
entries with their inline comments, and any other writer-edited content.

## Output on success

```
Registered project <name> in ~/.config/cowork/registry.yaml
  config: <vault-path>/process/data_management/drift_check.yaml
  enabled: true
```

(Comments and existing entries are preserved by the text-append approach;
no caveats needed in the success output.)

## Output on failure

- `drift_check.yaml not found at <expected path>; run pm-install-drift-check-config first`
- `project <name> is already registered in ~/.config/cowork/registry.yaml; remove that entry first or use a different name`
- `~/.config/cowork/registry.yaml is invalid YAML before append: <parse error>. Fix the existing file before retrying.`
- `~/.config/cowork/registry.yaml.tmp would be invalid YAML after append: <parse error>. Aborted; original registry untouched.`
- `permission denied writing to ~/.config/cowork/registry.yaml`

## Standalone use

Same preconditions. Useful for registering a project that was set up
before pm-register-project existed, or for re-registering after a manual
registry edit.
