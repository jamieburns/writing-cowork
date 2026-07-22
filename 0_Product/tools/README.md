# tools/

Scripts bundled inside the writing-cowork plugin, alongside `skills/` and
`templates/`. Ships as part of `0_Product/`, so `${CLAUDE_PLUGIN_ROOT}/tools/`
resolves correctly for any installed copy of the plugin.

## Contents

- `drift_check.py` — multi-project vault drift check. YAML-driven; one
  shared script handles all registered projects via a registry file plus
  per-project configs. Invoked by the `pm-run-drift-check` skill; see that
  skill's `SKILL.md` for the supported arguments and output locations.

## History

Originally developed and maintained in a separate `cowork-tools` repo
(`~/code/cowork-tools/`), external to the plugin. Incorporated into the
plugin itself (this location) on 2026-07-22, so installing the
writing-cowork plugin is sufficient on its own — no separate repo clone or
per-machine setup step is required to get a working drift check.

The standalone `cowork-tools` repo still exists as of the incorporation
date. Per Jamie's plan: it will be retired as a whole once adoption of the
plugin-bundled copy is confirmed across projects (see
`1_Project/Decisions.md` and the drift-check incorporation planning doc in
`1_Project/Documents/`). Until then, treat `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py`
as authoritative — it is the copy that ships with and is versioned
alongside the plugin.

## Versioning

`drift_check.py` carries its own `DRIFT_CHECK_VERSION` constant,
independent of the plugin's own `plugin.json` version — the two can in
principle be patched on different cadences. Check the running script's
version directly with:

```
python3 "${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py" --version
```

Every drift report's header also stamps the script version that produced
it, so historical reports can be cross-checked against a particular script
version even after the script has since been updated.

## Requirements

- Python 3.8+
- PyYAML — `pip3 install pyyaml --break-system-packages`

## Setup (per machine)

1. Create the per-machine registry at `~/.config/cowork/registry.yaml` if
   it doesn't already exist (a project-setup skill will create/update this
   automatically going forward — see `pm-sync-project-to-plugin`).
2. For each project, a `drift_check.yaml` lives in its
   `process/data_management/` directory (installed by
   `pm-install-drift-check-config` during project setup) and is added to
   the registry.
3. Optionally install a scheduled job (e.g. launchd on macOS) that runs
   `python3 "${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py" --all` on a
   schedule. The plugin does not manage this scheduling itself — it's a
   per-machine, per-user choice.

## Usage

```
# Run all enabled projects in the registry
python3 "${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py" --all

# Run a single project by name (from registry)
python3 "${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py" --project <name>

# Run a single project by config path (bypasses the registry)
python3 "${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py" --config /path/to/project/process/data_management/drift_check.yaml

# Don't write outputs — inspect what would happen
python3 "${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py" --all --dry-run

# Confirm the running script's own version
python3 "${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py" --version
```

Normally invoked through the `pm-run-drift-check` skill rather than called
directly — the skill handles preconditions (PyYAML installed, registry
present, etc.) and surfaces output in a consistent format.

## Architecture

One Python implementation, many project consumers. Per-project state lives
in each project's vault:

- `<vault>/process/data_management/drift_check.yaml` — config for this project.
- `<vault>/project_hub.md` — Attention block written here.
- `<vault>/process/data_management/file_ownership.md` — drift footer written here.
- `<vault>/process/data_management/drift_reports/<date>T<time>.md` — detailed report on drift.
- `<vault>/process/data_management/.drift_flag` — marker file (gitignored).
- `<vault>/.drift_last_run` — early-exit optimization state (gitignored).

Cross-project state lives outside vaults:

- `~/.config/cowork/registry.yaml` — list of registered projects, with `enabled` flag per project.
- `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py` — the shared script (this file).
- Any scheduled-job configuration you set up per machine (e.g. a launchd plist on macOS).
