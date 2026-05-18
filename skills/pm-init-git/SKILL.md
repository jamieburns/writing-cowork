---
name: pm-init-git
description: >
  This skill should be used when the user asks to "initialize git for this
  vault", "set up version control on the project", "git init the vault",
  or any variant of starting git tracking on a freshly scaffolded
  writing-cowork project. Initializes a git repo on the main branch in the
  given vault path and makes an initial commit of the scaffold so the repo
  has a base for subsequent pushes. Invoked by pm-setup-project after
  pm-init-vault; skippable when `--git=none` or `--git=existing`.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-init-git

Initialize a git repository on the `main` branch inside the supplied vault
path, then make an initial commit of whatever scaffold pm-init-vault
produced. The initial commit gives pm-init-github something to push, and
gives later install skills a clean parent commit to base their work on.

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
git add -A
git commit -m "[data-mgmt] init vault repo (writing-cowork pm-setup-project)"
```

If `user.email` or `user.name` is not set globally and the local repo lacks
them, the commit will fail. In that case, abort with a clear message asking
the user to set `git config --global user.email` and `git config --global
user.name`, then resume.

Use `git init -b main` not `git init` — older git defaults to `master`,
which we don't want.

The initial commit message uses the `[data-mgmt]` prefix per HANDOFF.md's
commit prefix convention.

## Output on success

```
Initialized git repo at <vault-path>
  Branch: main
  Initial commit: [data-mgmt] init vault repo (writing-cowork pm-setup-project)
  Commit hash: <short hash>
```

## Output on failure

Specific error from git, plus the most likely fix. Examples:

- `git CLI not found on PATH`
- `vault is already a git repo; use --git=existing in pm-setup-project to skip this step`
- `git commit failed: user.email not configured. Run: git config --global user.email "<your email>"`
- `git commit failed: nothing to commit. pm-init-vault must run first to produce a scaffold.`

Do not leave the repo partially initialized. If `git init` succeeded but
`git commit` failed, the repo state is "unborn main" — that's recoverable;
the user just needs to make a commit. Note this in the failure message so
pm-resume-setup can pick up from the commit step.

## Standalone use

When invoked outside the orchestrator, the same preconditions apply. The
scaffold must already exist; this skill never creates files itself. If
the user wants to git-init an existing-content vault, that works too —
`git add -A` will pick up whatever's there.
