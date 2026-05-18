---
name: pm-init-github
description: >
  This skill should be used when the user asks to "create a GitHub remote",
  "push the project to GitHub", "set up the github repo for this vault",
  or any variant of publishing a freshly initialized writing-cowork project
  to a private GitHub repository. Creates the remote via `gh`, adds it as
  origin over HTTPS, and pushes main. Invoked by pm-setup-project after
  pm-init-git; skipped when `--git` is not `new-github`.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-init-github

Create a private GitHub repository for the project, wire it as the local
repo's `origin`, and push `main`. Uses HTTPS for the remote URL —
`gh auth login` configures git's credential helper to inject the gh token
on HTTPS pushes, so no SSH key is required. Do not substitute an SSH URL
(this was a learning during writing-cowork's own bootstrap; HANDOFF.md
documents the lock).

## Arguments

- **`<name>`** (required) — the GitHub repository slug. Lowercase,
  kebab-case. Matches the project's vault `<name>` arg from pm-setup-project.
- **`<vault-path>`** (required) — absolute path to the local repo. Must
  be an initialized git repo with at least one commit on `main`.
- **`--github-org=<org>`** (optional, default `jamieburns`) — GitHub
  organization or user account.

## Preconditions

1. Verify `gh` is on PATH. If not, abort with `gh CLI not found on PATH`.
2. Verify `git` is on PATH.
3. Verify `gh auth status` reports authenticated for `github.com`. If not,
   abort with `gh is not authenticated. Run: gh auth login`.
4. Verify `<vault-path>` is a git repo on branch `main` with at least one
   commit. If unborn-main or wrong branch, abort with the relevant message.
5. Verify the local repo does not already have an `origin` remote. If it
   does, abort with `local repo already has an origin remote; remove it
   first or use --git=existing`.
6. Verify the remote repo `<org>/<name>` does NOT already exist on GitHub
   (via `gh repo view <org>/<name>` — exit code 0 means it exists). If it
   exists, abort with `GitHub repo <org>/<name> already exists; choose a
   different name or delete the existing repo first`.

## Execution

Run via host shell (osascript path when invoked from sandbox-mode Claude).
The sequence — no `--source` flag, no `--push` flag (per HANDOFF.md's
locked convention):

```bash
cd <vault-path>
gh repo create <org>/<name> --private
git remote add origin https://github.com/<org>/<name>.git
git push -u origin main
```

`gh repo create` without `--source` just creates the empty remote; it does
not touch the local repo. We then manually add the remote with the HTTPS
URL we want, and push. This sequence avoids the `--source` + `--separate-git-dir`
incompatibility that bit the project during the manual phase.

## Output on success

```
Created GitHub remote: <org>/<name>
  URL: https://github.com/<org>/<name>
  origin → https://github.com/<org>/<name>.git (HTTPS)
  Pushed: main → origin/main
```

## Output on failure

Specific error plus the most likely fix. Examples:

- `gh CLI not found on PATH`
- `gh is not authenticated. Run: gh auth login`
- `local repo already has an origin remote; remove with: git remote remove origin`
- `GitHub repo <org>/<name> already exists. Either: (1) choose a different name, (2) delete via gh repo delete <org>/<name> --confirm, or (3) use --git=existing if you want to use the existing repo as-is`
- `git push rejected. If you set the remote to an SSH URL, switch to HTTPS: git remote set-url origin https://github.com/<org>/<name>.git`

On a partial failure (remote created but local push failed), the GitHub
repo exists but is empty. pm-resume-setup can retry the push; do not
auto-delete the remote.

## Standalone use

When invoked outside the orchestrator, the same preconditions apply.
Useful when bolting a remote onto a project that started with `--git=local`
and now wants GitHub.
