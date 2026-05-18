---
name: pm-run-drift-check
description: >
  This skill should be used when the user asks to "run the drift check",
  "check for vault drift", "run drift_check on this project", or any
  variant of invoking the shared cowork-tools drift_check.py against one
  or more projects. Wraps the shared script; no per-project script
  duplication.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-run-drift-check

Invoke `~/code/cowork-tools/drift_check.py` against a specific project,
the current project, or all registered projects. Writes output per the
project's `drift_check.yaml` config (Attention block in project_hub,
footer in file_ownership, per-day drift report on drift).

## Arguments

- **`--project=<name>`** (optional) — run against a specific registered
  project (looked up by name in `~/.config/cowork/registry.yaml`).
- **`--all`** (optional, flag) — run against all enabled projects in the
  registry.
- **`--config=<path>`** (optional) — explicit path to a drift_check.yaml
  (bypasses the registry). Useful for one-off checks against unregistered
  projects.
- **`--dry-run`** (optional, flag) — don't write outputs; print what would
  be checked.

Exactly one of `--project`, `--all`, or `--config` must be supplied. If
none and the current directory contains a `process/data_management/drift_check.yaml`,
use it as `--config=<vault>/process/data_management/drift_check.yaml`.

## Preconditions

1. Verify `~/code/cowork-tools/drift_check.py` exists and is executable.
2. Verify `python3` is on PATH.
3. Verify PyYAML is installed (`python3 -c "import yaml"`). If not, abort
   with `PyYAML not installed; run: pip3 install pyyaml --break-system-packages`.
4. If `--project=<name>` or `--all`, verify `~/.config/cowork/registry.yaml`
   exists.
5. If `--config=<path>`, verify the path exists.

## Execution

Invoke the shared script via osascript (host shell) — drift_check.py needs
host filesystem access, not sandbox:

```bash
python3 ~/code/cowork-tools/drift_check.py \
    [--project <name> | --all | --config <path>] \
    [--dry-run]
```

Capture stdout/stderr. Surface the script's exit code: non-zero indicates
drift detected (not a skill failure — drift is expected output).

## Output on success (no drift)

```
Drift check: clean — no drift detected.
  Project: <name>
  Last check time written to: <vault>/project_hub.md (Attention block)
                              <vault>/process/data_management/file_ownership.md (footer)
```

## Output on drift detected

```
Drift check: DRIFT DETECTED for <name>.
  Report: <vault>/process/data_management/drift_reports/<date>.md
  Attention block updated: <vault>/project_hub.md
```

For `--all`, summary per project plus aggregate count.

## Output on failure

- `cowork-tools not installed at ~/code/cowork-tools/drift_check.py — install per https://github.com/jamieburns/cowork-tools README`
- `PyYAML not installed; run: pip3 install pyyaml --break-system-packages`
- `project <name> not in registry; run pm-list-projects to see what's registered`
- `drift_check.yaml not found at <path>`

## Standalone use

Run ad-hoc when you want a fresh drift report mid-session, rather than
waiting for the nightly launchd job. The script is idempotent; running it
N times in a row produces the same result.
