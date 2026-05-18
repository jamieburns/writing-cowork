---
name: pm-finalize-scaffold-commit
description: >
  This skill should be used when the user asks to "finalize the scaffold",
  "commit the initial scaffold", "wrap up project setup", or "make the
  setup-completion commit". Captures the entire writing-cowork vault
  scaffold — directories, top-level docs, data-management files, voice
  scaffold, planning files — as a single git commit, then pushes if origin
  is configured. Invoked by pm-setup-project as the penultimate step
  (before pm-register-project); skipped when `--git=none`.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-finalize-scaffold-commit

Commit the full vault scaffold in a single `[data-mgmt]` commit, then push
if origin is configured. This is the "one commit per logical operation"
pivot — the install/init sub-skills are pure file writers; this skill turns
their collective output into one git commit with a coherent message.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault (must be an
  initialized git repo).
- **`<name>`** (required) — the project's slug; appears in the commit
  message for log greppability.

## Preconditions

1. Verify `git` is on PATH.
2. Verify `<vault-path>/.git/` exists (vault is git-initialized).
3. Verify there is something to commit: `git status --porcelain` returns
   non-empty output. If empty, abort with `nothing to commit; scaffold
   sub-skills must run first`.

## Execution

Run via host shell (osascript path when invoked from sandbox-mode Claude).
The sequence:

```bash
cd <vault-path>
git add -A
git commit -m "[data-mgmt] initial vault scaffold (writing-cowork pm-setup-project for <name>)"
# Conditional push
if git remote get-url origin >/dev/null 2>&1; then
    git push -u origin main
fi
```

The commit message is long-form per HANDOFF.md's commit-message convention.
The push is conditional: `--git=local` projects have no remote, so the
push step is silently skipped (not an error).

If `user.email` or `user.name` is not set globally, the commit will fail.
In that case, abort with `git commit failed: user.email not configured.
Run: git config --global user.email "<your email>" && git config --global
user.name "<your name>"`.

## Output on success (with push)

```
Finalized vault scaffold at <vault-path>
  Commit: [data-mgmt] initial vault scaffold (writing-cowork pm-setup-project for <name>)
  Commit hash: <short hash>
  Pushed: main → origin/main
```

## Output on success (no push, local-only mode)

```
Finalized vault scaffold at <vault-path>
  Commit: [data-mgmt] initial vault scaffold (writing-cowork pm-setup-project for <name>)
  Commit hash: <short hash>
  Push skipped (no origin remote configured).
```

## Output on failure

Specific error plus the most likely fix. Examples:

- `nothing to commit; scaffold sub-skills must run first`
- `git commit failed: user.email not configured. Run: git config --global user.email "<your email>"`
- `git push rejected. Check origin URL: git remote get-url origin. If SSH, switch to HTTPS: git remote set-url origin https://github.com/<org>/<name>.git`

On a partial failure (commit succeeded but push failed), the commit is
preserved. pm-resume-setup can retry just the push — re-running this skill
will hit the "nothing to commit" guard on the second attempt; the resume
logic should `git push` directly in that case.

## Standalone use

When invoked outside the orchestrator (e.g., after manually scaffolding a
vault), the same preconditions apply. The skill captures whatever is in
the working tree as one commit. If you want finer-grained commits, don't
use this skill — make the commits yourself.
