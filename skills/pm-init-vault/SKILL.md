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
metadata:
  version: "0.1.0"
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

1. The path's parent directory exists and is writable.
2. If the path exists, it is a directory and is empty (ignoring `.DS_Store`).
   If not empty, abort with: `vault path exists and is non-empty; pm-init-vault
   is for new vaults only`.

## Directory skeleton

Create the following structure, creating parent directories as needed:

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
    ├── promotion/.gitkeep
    └── hub-updates/.gitkeep
```

Use the file tools (Write) for each file, not shell heredocs — Write produces
clean file state and avoids encoding surprises.

`.gitkeep` files are empty. They exist solely to make git track otherwise
empty directories.

## .gitignore content

The standard writing-cowork ignores:

```
# Scratch / unsync conventions
_scratch/
**/scratch/
_*
!_admin_*.log
!_admin_*.sh
*.scratch.md

# macOS
.DS_Store

# Editor / OS
*.swp
*~
```

The `!_admin_*.log` and `!_admin_*.sh` exceptions allow Reconciliation-style
admin logs at vault root. Genericize when porting if those filename
conventions change.

## Output on success

Plain confirmation listing what was created. Example:

```
Vault skeleton created at /Users/jburns/.../Epistemology
  process/active/
  process/history/
  process/data_management/
  process/data_management/drift_reports/
  inbox/promotion/
  inbox/hub-updates/
  .gitignore
```

## Output on failure

Specific, actionable error. Examples:

- `vault path exists and is non-empty; pm-init-vault is for new vaults only`
- `parent directory does not exist: <path>`
- `permission denied writing to <path>`

Do not partial-create. If any mkdir or write fails partway, leave the
filesystem as it stands and return the error. The orchestrator's
`pm-resume-setup` will retry the whole step.

## Standalone use

When invoked outside the orchestrator (e.g., the user wants the skeleton
bolted onto an already-existing repo), the same rules apply — empty target,
filesystem-only work. The user is responsible for any subsequent `git add` /
commit.
