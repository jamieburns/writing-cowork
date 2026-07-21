---
name: pm-enable-project
description: >
  This skill should be used when the user asks to "enable a cowork project",
  "turn on drift checks for <project>", "activate <project> in the
  registry", or any variant of flipping a registered project's `enabled`
  flag to true. Edits ~/.config/cowork/registry.yaml in place. Pairs with
  pm-disable-project.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-enable-project

Set a registered project's `enabled` flag to `true` in
`~/.config/cowork/registry.yaml`. The shared drift_check launchd job will
include this project on its next run.

## Arguments

- **`<name>`** (required) — project slug as it appears in the registry's
  `name:` field (e.g., `epistemology`, `reconciliation`).

## Preconditions

1. Verify `~/.config/cowork/registry.yaml` exists. If not, abort with
   `no registry; cannot enable a project that isn't registered`.
2. Verify the project `<name>` exists in the registry. If not, abort with
   `project <name> not in registry; run pm-register-project first or
   pm-list-projects to see what's registered`.

## Execution

Use the YAML round-trip approach with `ruamel.yaml` if available (preserves
comments). If only PyYAML is available, accept comment stripping and
proceed; surface that in success output.

```python
import yaml  # or ruamel.yaml
data = yaml.safe_load(open("~/.config/cowork/registry.yaml"))
for p in data["projects"]:
    if p["name"] == "<name>":
        p["enabled"] = True
        break
# atomic write: .tmp then mv
```

Alternative if comment preservation matters more than dependency-free:
edit the file as text via regex, locating the line `name: <name>` and
flipping the next `enabled:` line. More fragile; pick whichever the
project's Python environment supports cleanly.

## Output on success

```
Enabled project <name> in ~/.config/cowork/registry.yaml
  Previous: enabled: <prev-value>
  Current: enabled: true
```

If comments were stripped by round-trip: append one line `Note: comments
in registry.yaml may have been stripped (install ruamel.yaml to
preserve).`

## Output on failure

- `no registry; cannot enable a project that isn't registered`
- `project <name> not in registry; run pm-register-project first`
- `~/.config/cowork/registry.yaml is invalid YAML: <parse error>`
- `permission denied writing to ~/.config/cowork/registry.yaml`

## Standalone use

Same preconditions. Useful for re-enabling a project that was paused via
pm-disable-project.
