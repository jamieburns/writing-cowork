---
name: pm-sync-project-to-plugin
description: >
  This skill should be used when the user asks to "sync a project to the
  plugin", "set up drift check for this project", "upgrade this project
  to the current plugin version", "refresh this project's plugin state",
  "point this project at the bundled drift_check.py", "fix a project
  whose memory/config got messed up", "migrate an existing project to the
  plugin", "lift this vault into current conventions", "upgrade this
  vault's folder layout", "retrofit the new hierarchy onto this vault",
  or any variant of bringing a vault's plugin-managed state — drift-check
  config, registry entry, and folder layout/naming — into alignment with
  the currently installed writing-cowork plugin. Covers four cases with
  one mechanism: first-time setup for a vault that's never used this
  plugin's drift-check tooling, upgrading a vault from an older plugin
  version's conventions (config or folder layout), refreshing a vault
  whose config has drifted or been corrupted, and migrating a vault's
  folder layout/naming onto current conventions (e.g. `analysis/` ->
  `research_and_analysis/`). One-time per invocation, idempotent — safe
  to re-run.
metadata:
  version: "0.2.0"
  role: pm
  subset: mvp-foundation
  supersedes: pm-migrate-to-shared-tool, pm-migrate-existing-project
---

# pm-sync-project-to-plugin

Bring a project vault's plugin-managed state — drift-check configuration,
registry entry, and folder layout/naming — into alignment with the
currently installed writing-cowork plugin, regardless of the vault's
starting state. Originally replaced the narrower `pm-migrate-to-shared-tool`
(embedded-script -> shared-script migration only); as of v0.2.0 also
absorbs what was briefly a separate `pm-migrate-existing-project` skill,
folding folder-layout migration in as a fifth case rather than
maintaining a sibling skill with its own drifting conventions. One
mechanism covering every case a growing project count is likely to hit:

- **First-time setup** — a vault has no drift-check config at all yet
  (new project, or one that predates this plugin).
- **Config upgrade** — a vault's `drift_check.yaml` or registry entry
  reflects an older plugin version's conventions (e.g. still pointing at
  an external script path from before drift-check incorporation, or
  missing a `checks:` entry a newer plugin version expects).
- **Config refresh** — a vault's plugin-managed config exists but has
  drifted, been hand-edited incorrectly, or otherwise doesn't match what
  a fresh install of the current plugin would produce.
- **Layout migration** — a vault's folder names/layout reflect an older
  plugin convention (e.g. `analysis/` instead of `research_and_analysis/`)
  or the vault predates the plugin's folder conventions entirely.

The point of unifying these: with more than one or two projects, doing
this by hand differently each time — or maintaining several similarly-named
skills each covering one slice of "bring this vault current" — is exactly
how mistakes and inconsistency creep in from project to project. One
skill, run the same way regardless of starting state or which aspect of
the vault has drifted, is what prevents that. **Consistency across
projects is a deliberate design goal of this plugin** — the default for
any vault behind current conventions is to migrate it, not to have the
plugin quietly tolerate multiple naming/config generations indefinitely.
Aliasing/tolerating an old name is the exception, reserved for a specific
named case where migrating is genuinely unreasonable (e.g. a name baked
into an external system the vault must interoperate with) — not a
general fallback for avoiding migration work.

## Arguments

- **`<project>`** (required for config cases) — project slug for the
  registry entry. Optional for a pure `--target=layout` invocation against
  an unregistered vault.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.
- **`--target=auto|config|layout|all`** (optional, default `auto`) —
  `config` runs only the drift-check config sync (setup/upgrade/refresh
  cases, as in v0.1.0). `layout` runs only the folder-layout migration.
  `all` runs both. `auto` detects what's needed and runs it (see
  Detection below).
- **`--mode=auto|setup|upgrade|refresh`** (optional, default `auto`,
  applies to `--target=config`/`all`) — forces a specific config case
  when auto-detection would guess wrong.
- **`--layout-mode=auto|full|folders-only|refs-only`** (optional,
  default `auto`, applies to `--target=layout`/`all`) — `full` runs
  folder moves + reference rewrites together; `folders-only`/`refs-only`
  split the two phases across separate invocations (e.g. move folders
  now, review and apply reference rewrites in a follow-up pass).
- **`--dry-run`** (optional, flag) — report what would change (config
  diffs, folders to move, references found and their proposed rewrites,
  references flagged for manual review) without writing anything.
- **`--skip-layout-tag`** (optional, flag) — skip the rollback-tag
  precondition for the layout case specifically. **Requires explicit user
  confirmation before use** — this removes the primary safety mechanism
  for folder migration. Only intended for a vault where an equivalent
  recent tag/commit already exists. Has no effect on the config cases,
  which don't move files and don't require a tag.

## Detection (mode=auto / target=auto)

### Config state

1. **No `process/data_management/drift_check.yaml` and no legacy
   `process/data_management/drift_check.py`** → **setup**. Nothing to
   preserve; scaffold fresh from the current plugin template.
2. **Legacy embedded `process/data_management/drift_check.py` exists**
   (pre-shared-tool pattern) → **upgrade**, extracting config from the
   embedded script.
3. **`drift_check.yaml` exists AND the registry entry (or a stale note in
   the vault) references the old external path**
   (`~/code/cowork-tools/drift_check.py`, or any path outside
   `${CLAUDE_PLUGIN_ROOT}`) → **upgrade**.
4. **`drift_check.yaml` exists, no legacy script, no stale path
   reference, but content doesn't match what the current plugin's
   template would produce** (missing `checks:` entries, outdated marker
   names, etc.) → **refresh**.
5. **Everything matches current template** → config already in sync,
   no-op for this target.

### Layout state

Scan the vault root for folders matching known prior names, sourced from
`${CLAUDE_PLUGIN_ROOT}/templates/file_hierarchy.md` rather than
hardcoded here (so the mapping stays in sync as conventions evolve):

| Old name found | Current name | Notes |
|---|---|---|
| `analysis/` | `research_and_analysis/` | |
| ad hoc build/output dir (`BookDeliverables/`, or similar — not pattern-matched, see Execution) | `production/` | Cannot be reliably auto-detected by name alone |
| *(future entries as conventions add more)* | | Keep this table sourced from `file_hierarchy.md`, not hand-maintained here |

If none of the known old names are present and the vault has no
`process/data_management/` at all → this is also the **config setup**
case (greenfield vault, no plugin conventions at all) — the two states
coincide; running `--target=all` handles both in one pass.

If the vault already has current folder names and no known old names →
layout already current, no-op for this target.

If detection is ambiguous for either target, report what was found and
ask the user to supply an explicit `--mode`/`--layout-mode` rather than
guessing.

## Preconditions

1. Resolve vault root.
2. For `--target=config`/`all`: verify
   `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py` and
   `${CLAUDE_PLUGIN_ROOT}/templates/drift_check.yaml` exist.
3. For `--target=layout`/`all`: verify `<vault>` is a git repo, and that
   the working tree is clean (no uncommitted changes). If either check
   fails, abort the layout portion specifically — per the consistency
   design principle above, layout migration will not run against a vault
   with no rollback mechanism or an unclean starting point. (The config
   portion has no such requirement and may still proceed if only
   `--target=all` was requested and layout preconditions fail — report
   clearly which portion ran and which didn't.)
4. For `--target=layout`/`all`: verify
   `${CLAUDE_PLUGIN_ROOT}/templates/file_hierarchy.md` exists (source of
   the old→new folder mapping).

## Execution

### Case: setup (config)

1. Invoke `pm-install-drift-check-config` (or its underlying logic
   directly) to place a fresh `drift_check.yaml` from the current
   template, substituting project-specific values.
2. Invoke `pm-register-project` for `<project>` if not already
   registered.
3. Invoke `pm-enable-project` for `<project>` if the registry entry
   exists but is disabled.
4. Commit with prefix `[data-mgmt]`.

### Case: upgrade (config, from legacy embedded script)

1. **Extract config from the embedded script.** Parse hardcoded values:
   project_name, vault path, exclude_prefixes, exclude_patterns, build
   config, xref_targets, inbox buckets/overdue_days, markers. If the
   embedded script is significantly customized and parsing isn't
   feasible, prompt the user to confirm or hand-author the
   `drift_check.yaml` from the current template.
2. **Write `drift_check.yaml`**, merged against the current template's
   defaults (so the upgraded project also picks up any `checks:` entries
   that didn't exist when the embedded script was first written).
3. **Verify** via `python3 "${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py"
   --config <vault>/process/data_management/drift_check.yaml --dry-run`.
   Compare output structure to what the embedded script produced. If
   meaningful divergence, abort and report — manual reconciliation
   needed.
4. **Remove the embedded script.**
5. **Update any per-project scheduled job** that invoked the embedded
   script directly — repoint it at
   `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py`.
6. Invoke `pm-register-project` / `pm-enable-project` as in setup.
7. Commit with prefix `[data-mgmt]`.

### Case: upgrade (config, from stale external-path reference)

1. Confirm no config values need to change beyond the invocation path
   itself.
2. If a scheduled job on this machine references the old
   `~/code/cowork-tools/drift_check.py` path for this project
   specifically, flag it for the user to update (or update it directly
   if granted host access) — point it at
   `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py`.
3. No commit needed if `drift_check.yaml` itself didn't change; report
   what was (or needs to be) updated.

### Case: refresh (config)

1. Read the existing `drift_check.yaml`.
2. Diff its structure against the current
   `${CLAUDE_PLUGIN_ROOT}/templates/drift_check.yaml` — report which keys
   are missing, which look stale. Do NOT auto-add project-specific
   excludes the template wouldn't know about; only flag structural/schema
   gaps, not content judgment calls.
3. Merge forward: add any missing top-level keys while preserving all
   existing project-specific values — never overwrite a value the
   project has already customized.
4. Write the merged `drift_check.yaml`.
5. Verify via dry-run, same as the upgrade case.
6. Commit with prefix `[data-mgmt]`.

### Case: layout migration

1. **Tag the rollback point.** Unless `--skip-layout-tag` was passed with
   explicit confirmation, invoke `pm-tag-snapshot` with name
   `pre-migrate-<date>` and a message identifying what's about to change
   (e.g. "before folder-layout migration: analysis/ -> research_and_analysis/").
   Hard precondition — if tagging fails for any reason, abort the layout
   portion before touching any files. A failed *push* of the tag is not
   itself fatal (the local tag still allows rollback) but must be
   reported clearly.

2. **Confirm the folder mapping with the vault owner.** Present the
   detected mapping (old name → new name) for confirmation before moving
   anything. `analysis/` → `research_and_analysis/` is unambiguous.
   `production/` requires listing top-level folders that look like
   build/output directories (heuristic: contains generated file types —
   `.docx`, `.epub`, `.pdf` — or was named in `file_hierarchy.md`'s
   "Project-specific build/output directories" line) and asking the
   writer to confirm which map to `production/`, or confirm none apply.
   **This is the vault-owner-concurrent checkpoint** — do not proceed
   past it without explicit confirmation, even with `--dry-run` off.
   `--dry-run` shows what *would* happen; this step gates whether it
   actually happens.

3. **Move folders.** For each confirmed mapping, `git mv <old> <new>`
   (preserves history better than filesystem move + add/rm). If the
   destination already exists, abort that folder's move and flag it for
   manual reconciliation rather than merging or overwriting silently.

4. **Scan for and rewrite internal cross-references.** Grep the vault
   (excluding `.git/`, gitignored paths, scratch-convention paths) for
   the old folder name as a path-shaped token — markdown links, YAML
   values (`drift_check.yaml`'s `exclude_prefixes`/`exclude_patterns`/
   `xref_targets`/`build.sources`/`build.outputs`), documented
   skill-scope arguments (e.g. `voice-run-mechanical-pass`'s `<scope>`
   usage), and mentions in `file_hierarchy.md`, `file_ownership.md`,
   `project_hub.md`, `handoff.md`, `charter.md`.

   **Be conservative — this is a grep-and-propose pass, not a blind
   find/replace.** A bare mention of the word in prose (no trailing
   slash, no file-extension pattern, not inside a path) is not a rewrite
   candidate. For every match:
   - **High-confidence** (unambiguous path-shaped reference) → rewrite
     automatically, log file/line/before/after.
   - **Low-confidence** (ambiguous path-shape, or inside a code block /
     quoted historical text) → do NOT rewrite. Add to a flagged-for-review
     list with file/line/context; leave untouched.

   Atomic-write each modified file. Never touch anything on the flagged
   list.

5. **Update plugin-managed config referencing moved folders.** If
   `drift_check.yaml`'s exclude/build paths reference an old folder name,
   rewrite those specifically (structured YAML values — always
   high-confidence). Re-run `pm-run-drift-check --dry-run` afterward to
   confirm the config still parses and produces sane output; if it
   errors, report clearly rather than committing a broken config.

6. **Commit.** One commit for folder moves + high-confidence reference
   rewrites, prefixed `[data-mgmt]`, summarizing what moved. Do NOT
   describe flagged-for-review items as resolved in the commit message —
   they're explicitly still open.

## Output on success (config)

```
Synced <project> to writing-cowork v<plugin-version> (mode: <setup|upgrade|refresh>):
  drift_check.yaml: <written | merged | unchanged>
  Registered: in ~/.config/cowork/registry.yaml
  Verified: plugin-bundled script produces expected output (dry-run)
  Committed: [data-mgmt] sync to plugin v<version> (<project>)

Next drift check run will use ${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py.
```

## Output on success (layout)

```
Migrated <vault> to current writing-cowork layout:
  Rollback tag: snapshot/<date>-pre-migrate-<date>
  Folders moved:
    analysis/ -> research_and_analysis/ (24 files)
  References rewritten (high-confidence, N total):
    process/data_management/file_hierarchy.md:45
    process/data_management/file_ownership.md:112
    ... (full list in commit message)
  Flagged for manual review (M total, NOT changed):
    process/history/some_old_note.md:8 — "analysis" appears in prose,
      ambiguous whether it refers to the folder
  drift_check.yaml: updated, dry-run verified clean
  Committed: [data-mgmt] migrate layout (<vault>)

Review the flagged list above before considering this migration fully
complete. Rollback available via: git checkout snapshot/<date>-pre-migrate-<date>
```

With `--target=all`, both blocks are reported together.

## Output on failure

- `plugin-bundled drift_check.py not found at ${CLAUDE_PLUGIN_ROOT}/tools/ — plugin install may be incomplete`
- `no drift_check setup found and --mode=upgrade|refresh was forced; nothing to upgrade/refresh — use --mode=setup or omit --mode for auto-detection`
- `embedded script config could not be parsed automatically; supply --manual-config flag or hand-author the drift_check.yaml first`
- `dry-run output diverges from prior config — manual reconciliation needed before proceeding`
- `detection ambiguous: found <description of conflicting signals> — supply an explicit --mode/--layout-mode`
- `<vault> is not a git repo; run pm-init-git first — layout migration requires a rollback mechanism and will not run without one`
- `<vault> has uncommitted changes: <list> — commit or stash before migrating layout`
- `rollback tag already exists at snapshot/<date>-pre-migrate-<date>; a layout migration may already be in progress or was previously attempted — investigate before re-running`
- `git mv failed for <old> -> <new>: destination already exists — manual reconciliation needed`
- `drift_check.yaml dry-run failed after layout rewrite: <error> — folders were moved and tagged for rollback, but config needs manual fixing before the vault's drift check will run cleanly again`

## Standalone use

Use this any time a project's plugin-managed state needs to be brought
current — not just once per project's lifetime, and not just for config.
As project count grows, this is the single mechanism for: onboarding a
new vault, catching a vault up after a plugin version bump (config or
layout), or repairing a vault whose config or folder naming drifted.
Running it with no changes needed is a safe, cheap no-op — encourage
using it liberally rather than trying to remember whether a given vault
"needs" syncing, and rather than remembering which of several
similarly-scoped skills covers which aspect of "bringing a vault current."

## Related

- `pm-install-drift-check-config` — the underlying single-file installer
  the config cases wrap.
- `pm-register-project` / `pm-enable-project` — registry mechanics the
  config cases invoke as needed.
- `pm-run-drift-check` — actually runs the check once a project is
  synced; also used to verify config sanity after a layout rewrite.
- `pm-tag-snapshot` — used for the layout case's mandatory rollback point.
- `templates/file_hierarchy.md` — source of truth for current folder
  naming conventions; the layout case reads from it rather than
  hardcoding the old-to-new mapping.
