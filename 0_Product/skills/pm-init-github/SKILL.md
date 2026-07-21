---
name: pm-init-github
description: >
  This skill should be used when the user asks to "create a GitHub remote",
  "set up the github repo for this vault", or any variant of publishing a
  freshly initialized writing-cowork project to a private GitHub repository.
  Creates the remote via `gh` and adds it as origin over HTTPS. Does not
  push — pm-finalize-scaffold-commit handles the single setup-completion
  commit and push at the end. Invoked by pm-setup-project after pm-init-git;
  skipped when `--git` is not `new-github`.
  
  **Lift Procedure Integration:** Invoked during project setup (stage 1).
  See ~/code/cowork-tools/lift/README.md for full lift workflow.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-init-github

Create a private GitHub repository for the project and wire it as the local
repo's `origin`. Does not push — the local repo has no commits at this point
in the orchestrator sequence, so any push would fail anyway. The single
setup-completion push is deferred to `pm-finalize-scaffold-commit` after
all install/init sub-skills have written their files.

Uses HTTPS for the remote URL — `gh auth login` configures git's credential
helper to inject the gh token on HTTPS pushes, so no SSH key is required.
Do not substitute an SSH URL (this was a learning during writing-cowork's
own bootstrap; HANDOFF.md documents the lock).

## Arguments

- **`<name>`** (required) — the GitHub repository slug. Lowercase,
  kebab-case. Matches the project's vault `<name>` arg from pm-setup-project.
- **`<vault-path>`** (required) — absolute path to the local repo. Must
  be an initialized git repo.
- **`--github-org=<org>`** (optional, default `jamieburns`) — GitHub
  organization or user account.

## Preconditions

1. Verify `gh` is on PATH. If not, abort with `gh CLI not found on PATH`.
2. Verify `git` is on PATH.
3. Verify `gh auth status` reports authenticated for `github.com`. If not,
   abort with `gh is not authenticated. Run: gh auth login`.
4. Verify `<vault-path>` is a git repo (presence of `.git/` directory).
   No requirement on commits or branch state — push is deferred.
5. Verify the local repo does not already have an `origin` remote. If it
   does, abort with `local repo already has an origin remote; remove it
   first or use --git=existing`.
6. Verify the remote repo `<org>/<name>` does NOT already exist on GitHub
   (via `gh repo view <org>/<name>` — exit code 0 means it exists). If it
   exists, abort with `GitHub repo <org>/<name> already exists; choose a
   different name or delete the existing repo first`.

## Execution

Run via host shell (osascript path when invoked from sandbox-mode Claude).
The sequence — no `--source` flag, no push (per HANDOFF.md's locked
convention and the deferred-finalize design):

```bash
cd <vault-path>
gh repo create <org>/<name> --private
git remote add origin https://github.com/<org>/<name>.git
```

`gh repo create` without `--source` just creates the empty remote; it does
not touch the local repo. We then manually add the remote with the HTTPS
URL we want. Push happens later in `pm-finalize-scaffold-commit`.

## Output on success

```
Created GitHub remote: <org>/<name>
  URL: https://github.com/<org>/<name>
  origin → https://github.com/<org>/<name>.git (HTTPS)
  Push deferred to pm-finalize-scaffold-commit.
```

## Output on failure

Specific error plus the most likely fix. Examples:

- `gh CLI not found on PATH`
- `gh is not authenticated. Run: gh auth login`
- `local repo already has an origin remote; remove with: git remote remove origin`
- `GitHub repo <org>/<name> already exists. Either: (1) choose a different name, (2) delete via gh repo delete <org>/<name> --confirm, or (3) use --git=existing if you want to use the existing repo as-is`

On a partial failure (remote created but `git remote add origin` failed),
the GitHub repo exists but the local repo doesn't know about it.
pm-resume-setup can retry; do not auto-delete the remote.

## Standalone use

When invoked outside the orchestrator, the same preconditions apply.
Useful when bolting a remote onto a project that started with `--git=local`
and now wants GitHub. After this skill, the user runs `git push -u origin
main` themselves (or invokes `pm-finalize-scaffold-commit` if there are
uncommitted scaffold files).
