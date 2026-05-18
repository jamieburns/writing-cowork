---
name: pm-disable-project
description: >
  This skill should be used when the user asks to "disable a cowork
  project", "pause drift checks for <project>", "deactivate <project> in
  the registry", or any variant of flipping a registered project's
  `enabled` flag to false. Edits ~/.config/cowork/registry.yaml in place.
  Pairs with pm-enable-project. Common use: temporarily pause drift checks
  during major restructuring.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-disable-project

Set a registered project's `enabled` flag to `false` in
`~/.config/cowork/registry.yaml`. The shared drift_check launchd job will
skip this project on subsequent runs until re-enabled.

## Arguments

- **`<name>`** (required) — project slug as it appears in the registry.

## Preconditions

1. Verify `~/.config/cowork/registry.yaml` exists.
2. Verify the project `<name>` exists in the registry.

## Execution

Same approach as pm-enable-project — YAML round-trip with comment
preservation when possible. Set the named project's `enabled` to `false`.
Atomic-write the result.

## Output on success

```
Disabled project <name> in ~/.config/cowork/registry.yaml
  Previous: enabled: <prev-value>
  Current: enabled: false
```

## Output on failure

- `no registry; cannot disable a project that isn't registered`
- `project <name> not in registry`
- `~/.config/cowork/registry.yaml is invalid YAML: <parse error>`

## Standalone use

Same preconditions. Useful for pausing drift on a project during
restructuring (when known drift is expected and would create noise).
Remember to re-enable once the restructuring settles.
