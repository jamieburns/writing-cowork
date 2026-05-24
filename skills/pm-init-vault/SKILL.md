---
name: pm-init-vault
description: >
  This skill should be used when the user asks to "initialize a vault",
  "create the vault skeleton", "scaffold the directory structure for a writing
  project", or "set up the process folders". Creates the standard
  writing-cowork directory skeleton at a given path, including the process/,
  inbox/, and gitignored-scratch conventions. Invoked by pm-setup-project
  as the first step; also usable standalone for bolting the structure onto
  an existing vault.
  
  **Lift Procedure Integration:** Invoked during project setup (stage 1).
  See ~/code/cowork-tools/lift/README.md for full lift workflow.
metadata:
  version: "0.1.2"
  role: pm
  subset: mvp-foundation
---

# pm-init-vault

Create the standard writing-cowork directory skeleton at the supplied vault
path. Pure filesystem work — no git, no network. The skeleton is process
infrastructure only; substantive folders (`analysis/`, `graphics/`,
`subprojects/`, etc.) are created organically by the writer later and are
not part of the skeleton.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault directory.
  May or may not exist. Must be empty if it exists.

## Preconditions

Before doing anything, verify:

1. The path's grandparent (or an ancestor directory) exists. The path's
   immediate parent may or may not exist — pm-init-vault creates it with
   `mkdir -p $(dirname <vault-path>)` as part of execution.
2. If the path exists, it is a directory and is empty (ignoring `.DS_Store`).
   If not empty, abort with: `vault path exists and is non-empty; pm-init-vault
   is for new vaults only`.

## Directory skeleton

First ensure the vault's immediate parent directory exists:

```bash
mkdir -p "$(dirname <vault-path>)"
```

Then create the following structure, creating intermediate directories as needed:

```
<vault-path>/
├── .gitignore                         # standard writing-cowork ignores
├── process/
│   ├── active/.gitkeep
│   ├── history/.gitkeep
│   └── data_management/
│       ├── .gitkeep
│       └── drift_reports/.gitkeep
└── inbox/
    ├── README.md                      # copied from templates/inbox_README.md
    ├── promotion/.gitkeep
    ├── hub-updates/.gitkeep
    └── issues/.gitkeep
```

Use the file tools (Write) for each file, not shell heredocs — Write produces
clean file state and avoids encoding surprises.

`.gitkeep` files are empty. They exist solely to make git track otherwise
empty directories. The `inbox/README.md` (copied verbatim from
`${CLAUDE_PLUGIN_ROOT}/templates/inbox_README.md`) documents the two
shipped subdirectories so specialists reading the directory know the
conventions.

## .gitignore content

The standard writing-cowork ignores. Generic baseline — covers every writing
project. Project-specific outputs (build artifacts, deliverables) are NOT
included here; writers add them per-project.

```
# Scratch / unsync conventions
_*
_scratch/
**/_scratch/
scratch/
**/scratch/
*.scratch.md

# macOS
.DS_Store
.AppleDouble
.LSOverride
Icon?
._*

# iCloud Drive sentinels (vaults often live in iCloud)
*.icloud

# Editor / OS
*~
*.swp
*.swo

# Python (for any scripts that may live in process/data_management/)
__pycache__/
*.pyc
.venv/
venv/

# Obsidian — transient workspace state
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/workspace.json.bak

# Drift check artifacts (regenerable per-run)
process/data_management/.drift_flag
process/data_management/drift_reports/
```

Note `_*` is broad — it ignores any file or directory whose name starts with
underscore. Writers who want exceptions (e.g., `_admin_*.log` for tracked
admin scripts) add `!_admin_*.log` style negations to their project's
`.gitignore` per their own convention.

## Output on success

Plain confirmation listing what was created. Example:

```
Vault skeleton created at /Users/jburns/.../Epistemology
  process/active/
  process/history/
  process/data_management/
  process/data_management/drift_reports/
  inbox/
  inbox/README.md
  inbox/promotion/
  inbox/hub-updates/
  inbox/issues/
  .gitignore
```

## Output on failure

Specific, actionable error. Examples:

- `vault path exists and is non-empty; pm-init-vault is for new vaults only`
- `cannot create parent directory <path>: <reason>` (e.g., the path's ancestor is unwritable)
- `permission denied writing to <path>`

Do not partial-create. If any mkdir or write fails partway, leave the
filesystem as it stands and return the error. The orchestrator's
`pm-resume-setup` will retry the whole step.

## Standalone use

When invoked outside the orchestrator (e.g., the user wants the skeleton
bolted onto an already-existing repo), the same rules apply — empty target,
filesystem-only work. The user is responsible for any subsequent `git add` /
commit.
