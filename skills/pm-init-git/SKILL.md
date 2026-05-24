---
name: pm-init-git
description: >
  This skill should be used when the user asks to "initialize git for this
  vault", "set up version control on the project", "git init the vault",
  or any variant of starting git tracking on a freshly scaffolded
  writing-cowork project. Initializes a git repo on the main branch in the
  given vault path. Does not commit — pm-finalize-scaffold-commit handles
  the single setup-completion commit at the end of pm-setup-project.
  Skippable when `--git=none` or `--git=existing`.
  
  **Lift Procedure Integration:** Invoked during project setup (stage 1).
  See ~/code/cowork-tools/lift/README.md for full lift workflow.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-init-git

Initialize a git repository on the `main` branch inside the supplied vault
path. Pure git-init, no commit. The single setup-completion commit is
deferred to `pm-finalize-scaffold-commit` so the full scaffold (vault
skeleton + all installed top-level docs + voice/planning files) lands as
one logical commit instead of N small ones.

## Arguments

- **`<vault-path>`** (required) — absolute path to a directory that
  pm-init-vault has already populated (or equivalent scaffold from a manual
  setup). Must be a directory; must not already be a git repo.

## Preconditions

1. Verify `git` is on PATH. If not, abort with `git CLI not found on PATH`.
2. Verify `<vault-path>` exists and is a directory.
3. Verify `<vault-path>/.git` does NOT already exist. If it does, abort
   with `vault is already a git repo; use --git=existing in
   pm-setup-project to skip this step`.

## Execution

Run via host shell (osascript path when invoked from sandbox-mode Claude;
direct shell otherwise). The sequence:

```bash
cd <vault-path>
git init -b main
```

Use `git init -b main` not `git init` — older git defaults to `master`,
which we don't want.

No staging, no commit. The vault is left with a fresh `.git/` directory and
an "unborn main" branch. Subsequent install/init sub-skills add files to the
working tree; `pm-finalize-scaffold-commit` performs the single `git add -A`
+ `git commit` + `git push` at the end of setup.

## Output on success

```
Initialized git repo at <vault-path>
  Branch: main (unborn — no commits yet; finalize step will make the first commit)
```

## Output on failure

Specific error from git, plus the most likely fix. Examples:

- `git CLI not found on PATH`
- `vault is already a git repo; use --git=existing in pm-setup-project to skip this step`
- `vault path does not exist: <path>`

Failure modes for `git init -b main` are rare — typically only when the path
is invalid or `git` is missing. The skill does not need to handle commit
failures because it does not commit.

## Standalone use

When invoked outside the orchestrator (e.g., the user wants to git-init a
vault that already has content), the same preconditions apply. The skill
only inits; the user is responsible for any subsequent staging and commit.
