---
name: pm-sync-project-to-plugin
description: >
  This skill should be used when the user asks to "sync a project to the
  plugin", "set up drift check for this project", "upgrade this project
  to the current plugin version", "refresh this project's plugin state",
  "point this project at the bundled drift_check.py", "fix a project
  whose memory/config got messed up", or any variant of bringing a
  vault's plugin-managed files (drift_check.yaml, registry entry, and
  related config) into alignment with the currently installed
  writing-cowork plugin. Covers three cases with one mechanism: first-time
  setup for a vault that's never used this plugin's drift-check tooling,
  upgrading a vault from an older plugin version's conventions, and
  refreshing a vault whose config has drifted or been corrupted. One-time
  per invocation, idempotent — safe to re-run.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
  supersedes: pm-migrate-to-shared-tool
---

# pm-sync-project-to-plugin

Bring a project vault's plugin-managed drift-check configuration into
alignment with the currently installed writing-cowork plugin, regardless
of the vault's starting state. This replaces the narrower
`pm-migrate-to-shared-tool` (which only handled the one-time
embedded-script → shared-external-script migration) with a single
skill covering every case a growing project count is likely to hit:

- **First-time setup** — a vault has no drift-check config at all yet
  (new project, or one that predates this plugin).
- **Version upgrade** — a vault's `drift_check.yaml` or registry entry
  reflects an older plugin version's conventions (e.g. still pointing at
  an external script path from before drift-check incorporation, or
  missing a `checks:` entry a newer plugin version expects).
- **Refresh** — a vault's plugin-managed config exists but has drifted,
  been hand-edited incorrectly, or otherwise doesn't match what a fresh
  install of the current plugin would produce. Also useful when a
  project's own memory/notes about its plugin setup have gotten
  confused and you just want to reconcile against ground truth.

The point of unifying these: with more than one or two projects, doing
this by hand differently each time is exactly how mistakes creep in from
project to project. One skill, run the same way regardless of starting
state, is what prevents that.

## Arguments

- **`<project>`** (required) — project slug for the registry entry.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.
- **`--mode=auto|setup|upgrade|refresh`** (optional, default `auto`) —
  `auto` detects which case applies (see Detection below) and proceeds;
  an explicit mode skips detection and forces that path, useful when
  detection would guess wrong (e.g. a vault with an unusual
  hand-modified config that looks like drift but isn't).
- **`--dry-run`** (optional, flag) — report what would change without
  writing anything.

## Detection (mode=auto)

Resolve vault root, then inspect:

1. **No `process/data_management/drift_check.yaml` and no legacy
   `process/data_management/drift_check.py`** → **setup**. Nothing to
   preserve; scaffold fresh from the current plugin template.
2. **Legacy embedded `process/data_management/drift_check.py` exists**
   (pre-shared-tool pattern) → **upgrade**, extracting config from the
   embedded script the same way `pm-migrate-to-shared-tool` did.
3. **`drift_check.yaml` exists AND references the old external path**
   (`~/code/cowork-tools/drift_check.py`, or any path outside
   `${CLAUDE_PLUGIN_ROOT}`) — note: `drift_check.yaml` itself doesn't
   store an invocation path (that lives in the `pm-run-drift-check`
   skill, not per-project config), so this case is actually detected via
   the **registry entry** or a stale note in the vault referencing the
   old path. → **upgrade**.
4. **`drift_check.yaml` exists, no legacy script, registry entry (if
   any) doesn't reference a stale path, but content doesn't match what
   the current plugin's template would produce** (missing `checks:`
   entries the current template includes by default, outdated marker
   names, etc.) → **refresh**.
5. **Everything matches current template** → report already in sync,
   no-op.

If detection is ambiguous, report what was found and ask the user to
supply an explicit `--mode` rather than guessing.

## Preconditions

1. Resolve vault root.
2. Verify `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py` exists (the
   plugin-bundled script this skill is syncing the project toward).
3. Verify `${CLAUDE_PLUGIN_ROOT}/templates/drift_check.yaml` exists (the
   current template to sync against).

## Execution

### Case: setup

1. Invoke `pm-install-drift-check-config` (or its underlying logic
   directly) to place a fresh `drift_check.yaml` from the current
   template, substituting project-specific values.
2. Invoke `pm-register-project` for `<project>` if not already
   registered.
3. Invoke `pm-enable-project` for `<project>` if the registry entry
   exists but is disabled.
4. Commit with prefix `[data-mgmt]`.

### Case: upgrade (from legacy embedded script)

1. **Extract config from the embedded script.** The embedded
   `drift_check.py` typically has its config hardcoded at the top
   (the original Reconciliation Hypothesis pattern). Parse it to
   extract: project_name, vault path, exclude_prefixes, exclude_patterns,
   build config, xref_targets, inbox buckets/overdue_days, markers.

   If the embedded script is significantly customized and parsing isn't
   feasible, prompt the user to confirm or hand-author the
   `drift_check.yaml` from the current template.
2. **Write `drift_check.yaml`** at
   `<vault>/process/data_management/drift_check.yaml` with the extracted
   values, merged against the current template's defaults (so the
   upgraded project also picks up any `checks:` entries — cross-phase
   dependency detection, workstream status staleness — that didn't exist
   when the embedded script was first written).
3. **Verify the plugin-bundled script works against the new config.**
   Run a dry-run:
   `python3 "${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py" --config <vault>/process/data_management/drift_check.yaml --dry-run`.
   Compare output structure to what the embedded script produced. If
   meaningful divergence, abort and report — manual reconciliation
   needed.
4. **Remove the embedded script.**
5. **Update any per-project scheduled job** (e.g. launchd plist) that
   invoked the embedded script directly — repoint it at
   `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py`, or note that a
   shared/plugin-wide scheduled job now covers this project if one
   exists.
6. Invoke `pm-register-project` / `pm-enable-project` as in setup.
7. Commit with prefix `[data-mgmt]`.

### Case: upgrade (from stale external-path reference)

1. Confirm no config values need to change beyond the invocation path
   itself — `drift_check.yaml`'s own content is invocation-path-agnostic
   (the path lives in the `pm-run-drift-check` skill / any scheduled job
   command line, not in the per-project YAML).
2. If a scheduled job on this machine references the old
   `~/code/cowork-tools/drift_check.py` path for this project
   specifically, flag it for the user to update (or update it directly
   if the skill has been granted the necessary host access) — point it
   at `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py`.
3. No commit needed if `drift_check.yaml` itself didn't change; report
   what was (or needs to be) updated.

### Case: refresh

1. Read the existing `drift_check.yaml`.
2. Diff its structure against the current `${CLAUDE_PLUGIN_ROOT}/templates/drift_check.yaml`
   — report which keys are missing, which look stale (e.g. an
   `exclude_prefixes` list that hasn't kept pace with the vault's actual
   folder structure — do NOT auto-add project-specific excludes the
   template wouldn't know about; only flag structural/schema gaps, not
   content judgment calls).
3. Merge forward: add any missing top-level keys the template defines
   (e.g. a `checks:` section that didn't exist in an older template
   version) while preserving all existing project-specific values
   (vault path, exclude lists, xref targets, etc.) — never overwrite a
   value the project has already customized.
4. Write the merged `drift_check.yaml`.
5. Verify via dry-run, same as the upgrade case.
6. Commit with prefix `[data-mgmt]`.

## Output on success

```
Synced <project> to writing-cowork v<plugin-version> (mode: <setup|upgrade|refresh>):
  drift_check.yaml: <written | merged | unchanged>
  Registered: in ~/.config/cowork/registry.yaml
  Verified: plugin-bundled script produces expected output (dry-run)
  Committed: [data-mgmt] sync to plugin v<version> (<project>)

Next drift check run will use ${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py.
```

## Output on failure

- `plugin-bundled drift_check.py not found at ${CLAUDE_PLUGIN_ROOT}/tools/ — plugin install may be incomplete`
- `no drift_check setup found and --mode=upgrade|refresh was forced; nothing to upgrade/refresh — use --mode=setup or omit --mode for auto-detection`
- `embedded script config could not be parsed automatically; supply --manual-config flag or hand-author the drift_check.yaml first`
- `dry-run output diverges from prior config — manual reconciliation needed before proceeding`
- `detection ambiguous: found <description of conflicting signals> — supply an explicit --mode`

## Standalone use

Use this any time a project's plugin-managed state needs to be brought
current — not just once per project's lifetime. As project count grows,
this is the single mechanism for: onboarding a new vault, catching a
vault up after a plugin version bump, or repairing a vault whose config
drifted or was hand-edited incorrectly. Running it with no changes needed
is a safe, cheap no-op — encourage using it liberally rather than trying
to remember whether a given vault "needs" syncing.

## Related

- `pm-install-drift-check-config` — the underlying single-file installer
  this skill wraps for the setup case.
- `pm-register-project` / `pm-enable-project` — registry mechanics this
  skill invokes as needed.
- `pm-run-drift-check` — actually runs the check once a project is synced.
