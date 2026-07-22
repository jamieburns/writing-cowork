---
name: pm-run-drift-check
description: >
  This skill should be used when the user asks to "run the drift check",
  "check for vault drift", "run drift_check on this project", or any
  variant of invoking the plugin-bundled drift_check.py against one
  or more projects. Wraps the bundled script; no per-project script
  duplication.
metadata:
  version: "0.2.0"
  role: pm
  subset: mvp-foundation
---

# pm-run-drift-check

Invoke `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py` against a specific
project, the current project, or all registered projects. Writes output
per the project's `drift_check.yaml` config (Attention block in
project_hub, footer in file_ownership, per-run drift report on drift).

**Incorporated into the plugin 2026-07-22.** Previously this skill
invoked an external script at `~/code/cowork-tools/drift_check.py`,
requiring a separate one-time repo clone per machine. The script now
ships inside the plugin itself (`0_Product/tools/drift_check.py`), so
`${CLAUDE_PLUGIN_ROOT}` resolves it automatically for any installed copy
— no separate setup step needed beyond installing the plugin. See
`tools/README.md` for the incorporation history and the standalone
`cowork-tools` repo's retirement plan.

## What the script actually checks

Eight checks, run per project on each invocation (unless skipped by the
early-exit optimization below):

1. **File inventory drift** — vault files not listed in
   `file_ownership.md`; ownership entries with no corresponding file on
   disk.
2. **Cross-reference validation** — markdown links/image refs in
   `xref_targets` that don't resolve.
3. **Build freshness** — source markdown vs. last-built deliverable
   mtimes (skipped entirely if the project's `drift_check.yaml` has
   `build.enabled: false`).
4. **Gitignored items present** — surfaces scratch/build outputs that
   exist in the vault, informationally (not flagged as drift).
5. **Inbox surface** — counts items in configured inbox buckets; flags
   items older than `inbox.overdue_days` as overdue. `.gitkeep` and other
   dotfiles are excluded from these counts, so an empty inbox bucket
   correctly reports 0, not 1.
6. **Cross-phase dependency change detection** — warns on NEW
   dependencies (in `todos.md`'s `depends-on` column) that cross phase
   boundaries, compared against the previous git-committed version of
   `todos.md`. Enabled per-project via a `checks:` entry of type
   `cross-phase-dependency-change` in `drift_check.yaml`; supports an
   `exceptions` list of task IDs to exempt. Requires the vault to be a
   git repo with at least one prior commit — silently produces no
   findings otherwise (not an error).
7. **Workstream status block staleness** — scans `project_hub.md` for
   `<!-- ROLE-STATUS-START/END -->` blocks containing an `Updated:
   YYYY-MM-DD` line; flags blocks older than a configurable threshold
   (default 14 days). Enabled per-project via a `checks:` entry of type
   `workstream-status-staleness`; supports `threshold-days` and a
   `skip-blocks` list of role names to exempt (e.g. a PM block that's
   allowed to go stale longer).
8. **Early-exit optimization** — if a `.drift_last_run` marker exists and
   the vault's latest git commit is no newer than that marker, the full
   check is skipped for this run (the run time is still recorded). This
   means drift checks are effectively free on unchanged vaults; it also
   means a manual `pm-run-drift-check` invocation right after committing
   a change will always run the full check (the commit is newer than any
   prior marker).

**Report filenames include time-of-day** (`YYYY-MM-DDTHHMM.md`), fixed
2026-07-22 — same-day reruns no longer silently overwrite each other's
report. Every report's header also stamps the script's own version
(`drift_check v<X.Y.Z>`), independent of the plugin's version — check
`${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py --version` to confirm which
script version a project is actually running.

## Arguments

- **`--project=<name>`** (optional) — run against a specific registered
  project (looked up by name in `~/.config/cowork/registry.yaml`).
- **`--all`** (optional, flag) — run against all enabled projects in the
  registry.
- **`--config=<path>`** (optional) — explicit path to a drift_check.yaml
  (bypasses the registry). Useful for one-off checks against unregistered
  projects (e.g. a throwaway test vault).
- **`--dry-run`** (optional, flag) — don't write outputs; print what would
  be checked.

Exactly one of `--project`, `--all`, or `--config` must be supplied. If
none and the current directory contains a `process/data_management/drift_check.yaml`,
use it as `--config=<vault>/process/data_management/drift_check.yaml`.

## Preconditions

1. Verify `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py` exists (it ships
   with the plugin; absence indicates a broken/incomplete plugin
   install, not a missing external dependency).
2. Verify `python3` is on PATH.
3. Verify PyYAML is installed (`python3 -c "import yaml"`). If not, abort
   with `PyYAML not installed; run: pip3 install pyyaml --break-system-packages`.
4. If `--project=<name>` or `--all`, verify `~/.config/cowork/registry.yaml`
   exists.
5. If `--config=<path>`, verify the path exists.

## Execution

Invoke the bundled script via osascript (host shell) — drift_check.py
needs host filesystem access, not sandbox:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py" \
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
  Report: <vault>/process/data_management/drift_reports/<date>T<time>.md
  Attention block updated: <vault>/project_hub.md
```

For `--all`, summary per project plus aggregate count.

## Output on failure

- `drift_check.py not found at ${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py — plugin install may be incomplete or corrupted; try reinstalling writing-cowork`
- `PyYAML not installed; run: pip3 install pyyaml --break-system-packages`
- `project <name> not in registry; run pm-list-projects to see what's registered`
- `drift_check.yaml not found at <path>`

## Standalone use

Run ad-hoc when you want a fresh drift report mid-session, rather than
waiting for a scheduled job. The script is idempotent; running it N times
in a row with no intervening changes produces the same result (and after
the first run, subsequent runs short-circuit via the early-exit
optimization until the vault's next commit).

## Related

- `tools/README.md` (plugin-bundled) — incorporation history, versioning,
  per-machine setup, and the standalone `cowork-tools` repo's retirement
  plan.
- `pm-sync-project-to-plugin` — sets up, upgrades, or refreshes a
  project's drift-check config (and other plugin-managed files) to match
  the current plugin version; the skill to use when a project's registry
  entry or `drift_check.yaml` needs to be pointed at the plugin-bundled
  script for the first time.
