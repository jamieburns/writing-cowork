---
name: pm-install-router
description: >
  This skill should be used when the user asks to "install the router",
  "create CLAUDE.md", "set up the project router", "add the Tier-1 router",
  or any variant of placing the writing-cowork `CLAUDE.md` router at the
  vault root. Copies templates/CLAUDE.md into the vault, substituting
  project-specific placeholders. The router is the always-loaded pointer
  file that tells a session where everything lives. Invoked by
  pm-setup-project; also usable standalone for retrofitting onto an
  existing vault.
metadata:
  version: "0.1.0"
  role: pm
  subset: information-architecture
---

# pm-install-router

Copy `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md` from the plugin to
`<vault>/CLAUDE.md` (vault root — required; the router is only loaded when it
sits at the root of the working directory).

The router is **Tier 1** of the three-tier read contract (see the information
architecture spine, §5): it is loaded on every turn, so it carries pointers and
invariants only, never content. Tier 2 is `project_hub.md` (State manifest) and
`process/memory/INDEX.md` (Reference manifest); Tier 3 is the topic files those
manifests point at.

## Managed-block convention

The template ships with ownership markers:

```
<!-- BEGIN WRITING-COWORK MANAGED: <block-name> -->  ... plugin-owned
<!-- END   WRITING-COWORK MANAGED: <block-name> -->
<!-- BEGIN PROJECT-OWNED --> ... <!-- END PROJECT-OWNED -->
```

Two managed blocks ship: `router-orientation` and `router-skills`. Both are
regenerated on sync; the `PROJECT-OWNED` block is never touched by the plugin.

Three properties of this convention matter when editing the template:

1. Block-level HTML comments are **stripped before the file enters model
   context**, so markers cost no runtime tokens on a file that loads every
   turn.
2. Because they are stripped, **the model never sees them.** The template
   therefore also carries one short *visible* line stating the boundary. Do not
   remove it — without it, a session asked to "add something to CLAUDE.md"
   writes into a managed block and loses the edit on the next sync.
3. The convention is **markdown-only**; JSON files cannot carry markers.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title; default
  title-cased `<name>`.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/CLAUDE.md` does NOT already exist. If it does, stop —
   do not merge or append. A pre-existing `CLAUDE.md` is the user's, and
   silently rewriting it is exactly the failure the marker convention exists to
   prevent. Report it and let the user decide.
3. Verify `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md` exists.

## Execution

1. Read `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md` from the plugin.
2. Substitute `{{title}}`, `{{date_iso}}`, and `{{plugin_version}}` (read the
   `version` field from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`).
3. Atomic-write to `<vault-path>/CLAUDE.md` using the Write file tool, not a
   shell heredoc — the template contains backticks and `$` characters.

## Output on success

```
Installed CLAUDE.md router at <vault-path>/CLAUDE.md
```

## Output on failure

- `CLAUDE.md already exists at <vault-path>/CLAUDE.md; review it before installing the router (this skill will not merge)`
- `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md not found in plugin install`
- `permission denied writing to <vault-path>`

## Standalone use

Same preconditions. Retrofitting the router onto an existing vault is the
common standalone case. After installing, check that the paths named in the
`router-orientation` block actually exist in that vault — an older vault may
predate `process/memory/` (run `pm-init-memory`) or use a different roadmap
shape.

## Known constraint

Whether a given runtime loads a root `CLAUDE.md` is **runtime-dependent**.
It is documented behaviour for the Claude Code CLI. If a session does not
appear to be following the router, verify the file is actually being loaded
before assuming the content is wrong.

## Related skills

- `pm-init-memory` — creates the `process/memory/` tree the router points at.
- `pm-install-project-hub` — installs the Tier-2 State manifest.
