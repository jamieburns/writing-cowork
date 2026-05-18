---
name: pm-migrate-to-shared-tool
description: >
  This skill should be used when the user asks to "migrate a project to
  shared cowork-tools", "switch from embedded drift_check to the shared
  script", "remove the per-project drift_check.py", or any variant of the
  one-time migration from an embedded drift_check.py to the shared
  ~/code/cowork-tools/drift_check.py. One-time, idempotent.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-migrate-to-shared-tool

Migrate a project from an embedded `process/data_management/drift_check.py`
to the shared `~/code/cowork-tools/drift_check.py`. Generates the project's
`drift_check.yaml` from its existing embedded config, removes the embedded
script, registers the project in the cowork registry.

This is a one-time migration per project. Idempotent: re-running detects
the migration is complete and exits cleanly.

## Arguments

- **`<project>`** (required) — project slug for the registry entry.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify the shared tool exists: `~/code/cowork-tools/drift_check.py`.
3. Verify `<vault>/process/data_management/drift_check.py` exists (the
   thing being migrated). If absent, check whether
   `<vault>/process/data_management/drift_check.yaml` already exists — if
   yes, abort with `migration already complete; <vault> uses the shared
   tool`. If neither, abort with `no drift_check setup found at
   <vault>/process/data_management/; run pm-install-drift-check-config
   first`.
4. Verify the project isn't already in the registry (if it is, just
   confirm and report — migration target reached).

## Execution

1. **Extract config from embedded script.** The embedded
   `drift_check.py` typically has its config hardcoded at the top
   (Reconciliation pattern). Parse it to extract: project_name, vault
   path, exclude_prefixes, exclude_patterns, build config, xref_targets,
   inbox buckets/overdue_days, markers.

   If the embedded script is significantly customized and parsing isn't
   feasible, prompt the user to confirm or hand-author the
   drift_check.yaml from the plugin template.

2. **Write drift_check.yaml.** Place at
   `<vault>/process/data_management/drift_check.yaml` with the extracted
   values. Use the same template as pm-install-drift-check-config but
   pre-filled.

3. **Verify shared tool works against the new config.** Run a dry-run:
   `python3 ~/code/cowork-tools/drift_check.py --config <vault>/process/data_management/drift_check.yaml --dry-run`.
   Compare output structure to what the embedded script produced. If
   meaningful divergence, abort and report — manual reconciliation needed.

4. **Remove the embedded script.** Delete
   `<vault>/process/data_management/drift_check.py`.

5. **Update launchd job (if any).** If the project has its own per-project
   launchd plist for drift checks, disable/remove it. The shared launchd
   job (`com.cowork.driftcheck.plist`) runs the shared script against all
   registered projects.

6. **Register the project.** Invoke pm-register-project for `<project>`
   if not already registered.

7. **Commit the changes** with prefix `[data-mgmt]`.

## Output on success

```
Migrated <project> to shared cowork-tools:
  Wrote: process/data_management/drift_check.yaml
  Removed: process/data_management/drift_check.py
  Registered: in ~/.config/cowork/registry.yaml
  Verified: shared script produces equivalent output (dry-run)
  Committed: [data-mgmt] migrate to shared cowork-tools (<project>)

Next nightly drift check will use the shared script.
```

## Output on failure

- `shared cowork-tools not installed at ~/code/cowork-tools/drift_check.py`
- `no drift_check setup found at <vault>/process/data_management/`
- `migration already complete; <vault> uses the shared tool`
- `embedded script config could not be parsed automatically; supply
  --manual-config flag or hand-author the drift_check.yaml first`
- `dry-run output diverges from embedded script — manual reconciliation
  needed before removing the embedded script`

## Standalone use

This is the canonical use. Reconciliation Hypothesis is the first
project that needs this migration (per HANDOFF.md: it runs its own
embedded drift_check.py during canary; will migrate after Epistemology
runs cleanly for 1-2 weeks on the shared script).
