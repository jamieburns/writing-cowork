---
name: pm-install-router
description: >
  This skill should be used when the user asks to "install the router",
  "create CLAUDE.md", "set up the project router", "add the Tier-1 router",
  "update the router", or any variant of placing or refreshing the
  writing-cowork `CLAUDE.md` router at the vault root. Installs the router
  from template on a clean vault, and on a vault that already has a
  `CLAUDE.md` it merges — adopting existing content into the PROJECT-OWNED
  block or regenerating managed blocks in place — always with a diff, a
  backup, and a documented recovery path. Invoked by pm-setup-project; also
  usable standalone for retrofitting or upgrading.
metadata:
  version: "0.2.0"
  role: pm
  subset: information-architecture
---

# pm-install-router

Place or refresh `<vault>/CLAUDE.md` from `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md`.
Vault root is required — the router is only loaded when it sits at the root of
the working directory.

The router is **Tier 1** of the three-tier read contract (information
architecture spine, §5): loaded every turn, so it carries pointers and
invariants only, never content. Tier 2 is `project_hub.md` (State manifest) and
`process/memory/INDEX.md` (Reference manifest); Tier 3 is the topic files those
manifests point at.

## Managed-block convention

```
<!-- BEGIN WRITING-COWORK MANAGED: <block-name> -->  ... plugin-owned
<!-- END   WRITING-COWORK MANAGED: <block-name> -->
<!-- BEGIN PROJECT-OWNED --> ... <!-- END PROJECT-OWNED -->
```

Two managed blocks ship: `router-orientation` and `router-skills`. Both are
regenerated on every run. `PROJECT-OWNED` is **never** modified by this skill.

Three properties of the convention shape the merge logic below:

1. Block-level HTML comments are **stripped before the file enters model
   context**, so markers cost no runtime tokens.
2. Because they are stripped, **the model never sees them** — so the template
   also carries one short *visible* line stating the boundary. Do not remove it.
3. The convention is **markdown-only**; JSON cannot carry markers.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title; default title-cased `<name>`.
- **`--dry-run`** (optional) — print the diff and the chosen mode, write nothing.
- **`--yes`** (optional) — skip the confirmation prompt. Intended for
  orchestrated runs on a clean vault; see "Orchestrated mode" below.

## Modes — determined by what is already at `<vault>/CLAUDE.md`

Detect the mode **before** doing anything, and report which mode was chosen.

| Situation | Mode | Behaviour |
|---|---|---|
| No `CLAUDE.md` | **install** | Render the template and write it. No prompt needed. |
| `CLAUDE.md` exists **with** our `BEGIN WRITING-COWORK MANAGED` markers | **refresh** | Regenerate each managed block from the current template. Copy the existing `PROJECT-OWNED` block through **byte-for-byte**. Prompt with a diff. |
| `CLAUDE.md` exists **without** our markers | **adopt** | The file is the user's. Render the template, then move the user's **entire existing content** verbatim into the `PROJECT-OWNED` block, under a `## Adopted from previous CLAUDE.md ({{date_iso}})` heading. Nothing is discarded. Prompt with a diff. |
| `CLAUDE.md` exists with markers that are **malformed** (unbalanced BEGIN/END, or a BEGIN with no matching END) | **abort** | Do not guess boundaries — a bad guess silently destroys content. Report the line numbers of the unbalanced markers and stop. |

In **adopt** mode, prefer keeping the user's content whole over trying to
classify it. Sorting their prose into the right managed block is a judgement
call the skill will sometimes get wrong, and being wrong means losing their
words. Adopting wholesale is always recoverable; the user can move pieces up
into the managed structure themselves afterwards.

## Backup and recovery

Before **any** write to an existing `CLAUDE.md`:

1. Copy it to `<vault>/CLAUDE.md.bak-<YYYYMMDD-HHMMSS>`. Never overwrite an
   existing `.bak-*`; the timestamp makes collisions unlikely, but if one
   occurs, append a counter rather than clobbering.
2. If the vault is a git repo and `CLAUDE.md` is tracked, say so in the output —
   `git diff CLAUDE.md` and `git checkout -- CLAUDE.md` are the better recovery
   path, and the user should know it is available.

Report the backup path in the output. Do not delete backups automatically —
they are cheap, and the user decides when they are no longer wanted.

## Execution

1. Read `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md`.
2. Substitute `{{title}}`, `{{date_iso}}`, and `{{plugin_version}}` (the
   `version` field from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`).
3. Determine the mode from the table above.
4. Build the proposed file content in memory.
5. Produce a unified diff (existing → proposed). In **install** mode there is
   nothing to diff; say so rather than printing the whole file.
6. If `--dry-run`: print the mode and diff, stop. Write nothing.
7. Otherwise show the mode, the diff, and the backup path that will be used,
   and **ask for confirmation** unless `--yes` was passed.
8. On confirmation: write the backup, then atomic-write the new content with the
   Write file tool (not a shell heredoc — the template contains backticks and
   `$` characters).

## Orchestrated mode

`pm-setup-project` runs this on a freshly scaffolded vault, so the mode is
always **install** and no prompt appears. If the orchestrator ever encounters
**adopt** or **refresh**, that means the vault was not clean — surface it as a
failure rather than merging silently during an unattended setup run. `--yes` is
for the clean-install case only; it does not authorize an unreviewed adopt.

## Output on success

```
Router: <mode> at <vault-path>/CLAUDE.md
Backup: <vault-path>/CLAUDE.md.bak-20260726-141133   (omitted in install mode)
Managed blocks regenerated: router-orientation, router-skills
PROJECT-OWNED block: preserved (<n> lines)            (refresh mode)
Adopted <n> lines of prior content into PROJECT-OWNED  (adopt mode)
```

## Output on failure

- `malformed managed markers in <vault-path>/CLAUDE.md — unbalanced BEGIN/END at lines <a>, <b>; not modifying the file`
- `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md not found in plugin install`
- `permission denied writing to <vault-path>`
- `refusing to write backup: <vault-path>/CLAUDE.md.bak-<ts> already exists`

## Standalone use

Retrofitting onto an existing vault (**adopt**) and picking up template changes
after a plugin upgrade (**refresh**) are the two common standalone cases. After
either, check that the paths named in `router-orientation` actually exist in
that vault — an older vault may predate `process/memory/` (run `pm-init-memory`)
or use a different roadmap shape.

## Known constraint

Whether a given runtime loads a root `CLAUDE.md` is **runtime-dependent**. It is
documented behaviour for the Claude Code CLI. If a session does not appear to be
following the router, verify the file is actually being loaded before concluding
the content is wrong.

## Related skills

- `pm-init-memory` — creates the `process/memory/` tree the router points at.
- `pm-install-project-hub` — installs the Tier-2 State manifest.
