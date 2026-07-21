---
name: pm-list-projects
description: >
  This skill should be used when the user asks to "list cowork projects",
  "show registered projects", "what projects are in the registry", or any
  variant of querying the per-machine cowork registry. Reads
  ~/.config/cowork/registry.yaml and prints each registered project with
  its name, drift_check.yaml path, and enabled status.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-list-projects

Read `~/.config/cowork/registry.yaml` and print each registered project
in a scannable table.

## Arguments

- **`--enabled-only`** (optional, flag) — show only projects with
  `enabled: true`. Default: show all.
- **`--format=table|yaml`** (optional, default `table`) — output format.

## Preconditions

1. Verify `~/.config/cowork/registry.yaml` exists. If absent, output
   `no registry; no projects registered yet` and exit cleanly (not an
   error — it's a valid empty state).

## Execution

1. Read `~/.config/cowork/registry.yaml`.
2. Parse with PyYAML (`python3 -c "import yaml; ..."`).
3. For each project entry in `projects:`, extract `name`, `config`, `enabled`.
4. Apply `--enabled-only` filter if set.
5. Render per `--format`:
   - `table`: one row per project, columns `name`, `enabled`, `config`
   - `yaml`: dump the filtered list as YAML

## Output on success (table)

```
Projects registered in ~/.config/cowork/registry.yaml:

  name              enabled   config
  ----------------  --------  ----------------------------------------
  reconciliation    true      /Users/.../Reconciliation Hypothesis/process/data_management/drift_check.yaml
  epistemology      true      /Users/.../Epistemology/process/data_management/drift_check.yaml

2 project(s) registered, 2 enabled.
```

## Output on failure

- `~/.config/cowork/registry.yaml is invalid YAML: <parse error>. Inspect the file before retrying.`
- `permission denied reading ~/.config/cowork/registry.yaml`

## Standalone use

Pure read operation. Same preconditions, same output. Safe to run anytime.
