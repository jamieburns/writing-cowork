---
name: pm-init-project-cowork-settings
description: >
  This skill should be used when the user asks to "enable writing-cowork in
  this project", "set up Cowork project settings", "scope writing-cowork to
  this vault", "configure project memory settings", or any variant of writing
  the per-project Cowork settings file. Writes `[vault]/.claude/settings.json`
  with `enabledPlugins` so writing-cowork loads only in this project, and
  points auto memory at the vault's visible `process/memory/` directory so
  memory writes land in git-tracked files rather than a hidden store. Invoked
  by pm-setup-project as part of the initial scaffold; also usable standalone
  for retrofitting onto an existing vault.

  **Lift Procedure Integration:** Invoked during project setup (stage 1).
  See ~/code/cowork-tools/lift/README.md for full lift workflow.
metadata:
  version: "0.2.0"
  role: pm
  subset: mvp-foundation
---

# pm-init-project-cowork-settings

Write `<vault>/.claude/settings.json` with two things: the `enabledPlugins`
entry that scopes writing-cowork to this project, and the memory settings that
redirect auto memory into the vault.

## Why the memory settings are here

Memory is the **Reference** layer and should live in files the writer can see,
diff, and delete. Auto memory defaults to a hidden, machine-local store outside
the vault and outside git. In practice the two diverge silently — content
written to one is invisible to the other, and stale entries keep being served to
new sessions as though current.

Pointing `autoMemoryDirectory` at `process/memory/` collapses that to **one
store**, inside the repo. `git status` then becomes the review surface: an
unreviewed memory write shows up as an uncommitted change before it is
committed.

## The path must be computed, never templated

`autoMemoryDirectory` requires an **absolute path** (or one starting with `~/`);
relative paths are not supported. A hardcoded path in a shipped template would
be wrong on every machine but the author's, so this skill **resolves the path at
install time** from `<vault-path>`.

Because `.claude/settings.json` is normally git-tracked, the resolved path
travels with the repo. If the vault is later cloned to a different location, the
stored path no longer matches — see "Path drift" below.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault directory.
- **`<name>`** (required) — project slug; used in informational output.
- **`--memory=redirect|disable|none`** (optional, default `redirect`):
  - `redirect` — **Option B, the default.** Set `autoMemoryDirectory` to the
    vault's `process/memory/`. One store, auto-loaded, git-visible.
  - `disable` — **Option A, the fallback.** Set `autoMemoryEnabled: false` and
    omit the directory. Use when redirect misbehaves — memory then lives in
    `process/memory/` by discipline and the router, with nothing auto-loading it.
  - `none` — write only `enabledPlugins`, no memory keys. For vaults where
    memory is managed some other way.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/.claude/settings.json` does NOT already exist. If it
   does, abort — do not overwrite a file the user may have customized. Report
   the keys that would have been added so they can merge by hand.
3. If `--memory=redirect`, verify `<vault-path>/process/memory/` exists or will
   exist (`pm-init-memory` creates it). A directory that never appears means
   memory writes land somewhere unexpected.

## Execution

1. Create `<vault-path>/.claude/` if absent (`mkdir -p`).
2. Resolve the memory path: `<vault-path>/process/memory`, absolute, with no
   trailing slash. If `<vault-path>` sits under the user's home directory,
   prefer the `~/`-relative form — it survives a differing macOS username.
3. Build the settings object:

   ```json
   {
     "enabledPlugins": {
       "writing-cowork@jamie-cowork-plugins": true
     },
     "autoMemoryDirectory": "<resolved path>"
   }
   ```

   For `--memory=disable`, replace `autoMemoryDirectory` with
   `"autoMemoryEnabled": false`. For `--memory=none`, omit both.
4. Write to `.tmp`, parse it to confirm valid JSON, then `mv` into place.

## Provenance — this file cannot carry markers

JSON has no comment syntax, so `.claude/settings.json` cannot carry the
plugin's `BEGIN/END WRITING-COWORK MANAGED` markers. Do **not** try to smuggle
provenance in via a `"_comment"` key: unknown-key tolerance is unverified, and
if a strict reader rejects the file the failure mode is *the plugin stops
loading* — the worst place to take an unverified risk.

Instead, record this file in `process/data_management/file_ownership.md` with
owner `plugin:writing-cowork`. That table is the authoritative registry of what
the plugin owns, and it is format-agnostic.

## Path drift

The stored `autoMemoryDirectory` is absolute and therefore machine- and
location-specific. It goes stale if the vault is moved, cloned elsewhere, or
opened under a different username.

Symptom: memory silently stops appearing in `process/memory/`. Because nothing
errors, this is easy to miss — which is the same class of failure the whole
visible-memory design exists to prevent.

Detection: `pm-run-drift-check` should verify that the configured path resolves
**inside this vault**, and raise an Attention flag when it does not. Fix by
re-running this skill after removing the stale `settings.json`, or by editing
the one key by hand.

## Known constraint — writes to `.claude/` may be blocked

Some Cowork tool paths refuse to write anything under `.claude/`
("Writing to .claude is not permitted via remote tools"). If this skill fails
that way, it is an environment restriction, not a bug in the vault. Fall back to
running the write from the Claude Code CLI or a host shell. **Verify this before
relying on the skill in an unattended Cowork setup run.**

## Runtime caveat

`autoMemoryEnabled` and `autoMemoryDirectory` are documented for the Claude Code
CLI. Whether a given runtime honours them is **not guaranteed** — if memory
still appears from a hidden store after this runs, the setting is not binding in
that runtime and the vault is relying on the router plus discipline instead.
Report it rather than assuming the redirect worked.

## Output on success

```
Initialized Cowork settings at <vault-path>/.claude/settings.json
  enabledPlugins:      writing-cowork@jamie-cowork-plugins = true
  autoMemoryDirectory: <resolved path>            (--memory=redirect)
  autoMemoryEnabled:   false                      (--memory=disable)
```

## Output on failure

- `settings.json already exists at <path>; merge these keys manually or remove the file first: <keys>`
- `permission denied writing to <vault-path>/.claude/ (some Cowork tool paths block .claude/ writes — try the Claude Code CLI)`
- `<vault-path>/process/memory/ not found; run pm-init-memory first or pass --memory=none`

## Standalone use

Retrofitting an existing vault is the common standalone case — including vaults
that predate the memory model. On such a vault, expect an existing hidden store
with accumulated content: review it and promote anything worth keeping into
`process/memory/` **before** redirecting, or that content becomes unreachable
without knowing where to look.

## Related skills

- `pm-init-memory` — creates the `process/memory/` directory this points at.
- `pm-run-drift-check` — should flag a stale `autoMemoryDirectory`.
