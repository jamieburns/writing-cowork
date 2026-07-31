---
name: pm-install-git-hooks
description: >
  This skill should be used when the user asks to "install the git hooks",
  "set up the post-commit check", "add session-hygiene enforcement", "wire
  up commit-time checks", or any variant of installing writing-cowork's git
  hooks into a vault. Installs a tracked hooks directory and points
  core.hooksPath at it, so a post-commit session-hygiene check runs on every
  commit. Git hooks are unrelated to Claude Code hooks and run in every
  runtime. Invoked by pm-setup-project; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: information-architecture
---

# pm-install-git-hooks

Install `process/data_management/git-hooks/post-commit` and point
`core.hooksPath` at that directory, so the session-hygiene checks run at commit
time.

## Why this exists

**Claude Code hooks do not run in Cowork.** Verified 2026-07-27 — see
`Decisions.md` → "Hooks in Cowork". SessionStart, Stop, `PreToolUse`, and
`UserPromptSubmit` never fire there, and `/hooks` does not exist. Since consumer
vaults run in Cowork, agent-runtime hooks cannot enforce anything for them.

**Git hooks are a different mechanism entirely.** They run wherever `git` runs —
on the host, under the user's own shell — and no agent runtime is involved. That
makes them the only enforcement available in *every* runtime, which is the
constraint recorded as spine §6d.

**Why commit-time is the right moment.** The project's control model is that
**git is the consent mechanism**: an unreviewed change shows up as an
uncommitted diff, and committing is the act of accepting it. Session-close was
always a proxy for "before this work becomes permanent." The commit *is* that
moment, so checking there is better aligned than checking at session end — and
unlike session close, it cannot be forgotten.

## Why `post-commit`, and why it does not block

`post-commit` runs after the commit lands and cannot fail it. That is
deliberate:

- A blocking `pre-commit` check gets `--no-verify`'d the first time someone is
  in a hurry, and a check that is routinely bypassed is worse than one that
  always reports.
- The hygiene findings are **not** reasons to reject a commit. "You have
  uncommitted durable content elsewhere" and "a log entry has no hash yet" are
  things to notice, not things to prevent.
- Committing must stay reliable. A hook that can wedge the commit path is a
  liability in a writing tool.

## Compute at install, don't template

The hook needs absolute paths to the Python interpreter, `drift_check.py`, and
the vault's `drift_check.yaml`. A shipped template cannot carry machine-specific
absolute paths — the same reasoning as `autoMemoryDirectory`. This skill
resolves them at install time and substitutes them into the hook.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`--hooks-dir=<rel>`** (optional) — default `process/data_management/git-hooks`.
- **`--force`** (optional) — overwrite an existing `post-commit`, after backing it up.

## Preconditions

1. `<vault-path>` exists and is a git repository (`.git` present). If not, stop —
   this skill has nothing to attach to.
2. `${CLAUDE_PLUGIN_ROOT}/templates/hooks/post-commit` exists.
3. `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py` exists.
4. `<vault-path>/process/data_management/drift_check.yaml` exists — install the
   drift-check config first, or the hook is inert.
5. If `core.hooksPath` is **already set to something else**, stop and report it.
   Silently repointing it would disable hooks the user set up deliberately.
6. **The resolved interpreter can import PyYAML.** Check with
   `<python> -c 'import yaml'`. `drift_check.py` exits 2 on a missing PyYAML, and
   before 2026-07-30 the hook discarded that and printed nothing — a broken
   checker looked exactly like a clean repo (task `c3f80b6e`). The hook now
   reports the failure, but an installer that knowingly wires up a checker that
   cannot run is still the wrong default. If the import fails, stop and report:
   `pip3 install pyyaml --break-system-packages` against **that** interpreter.
   Note the interpreter is machine-specific: `command -v python3` resolved to
   Homebrew's `/opt/homebrew/bin/python3` on the dev machine, not `/usr/bin/python3`,
   and only one of the two had PyYAML.

## Execution

1. `mkdir -p <vault>/<hooks-dir>`.
2. Read `${CLAUDE_PLUGIN_ROOT}/templates/hooks/post-commit`.
3. Substitute:
   - `{{python_path}}` — resolved interpreter (`command -v python3`), absolute.
   - `{{drift_check_path}}` — absolute path to the bundled `drift_check.py`.
   - `{{config_path}}` — absolute path to the vault's `drift_check.yaml`.
4. Write it, then `chmod +x`. **A hook that is not executable fails silently** —
   verify the bit is set rather than assuming.
5. `git -C <vault> config core.hooksPath <hooks-dir>` (repo-local, not global).
6. Verify: `git -C <vault> config --get core.hooksPath` returns the expected value.
7. **Smoke-test the checker before declaring success**, do not just verify the
   wiring: run
   `<python> <drift_check> --config <config> --dry-run` and confirm it exits 0
   and emits at least one line. An installer that reports success while the
   thing it installed cannot run is the failure this step exists to prevent.
   An exit of 2 means PyYAML (precondition 6); a `session_hygiene — NOT
   CONFIGURED` line means the vault's `drift_check.yaml` has no
   `session_hygiene:` block and the hook would have nothing to say.

The hooks directory is **tracked**, unlike `.git/hooks/`, so the hook travels
with a clone. Each machine still needs `core.hooksPath` set once — that is what
makes this skill worth re-running after a fresh clone.

## Output on success

```
Installed git hooks at <vault>/<hooks-dir>
  post-commit    → session-hygiene check (warns, never blocks)
  core.hooksPath → <hooks-dir>
Resolved: python3 <path>, drift_check.py <path>, config <path>
```

## Output on failure

- `<vault-path> is not a git repository; nothing to attach hooks to`
- `core.hooksPath is already set to <other>; refusing to repoint it — remove or merge manually`
- `post-commit already exists at <path>; pass --force to overwrite (a backup will be written)`
- `drift_check.yaml not found; run pm-install-drift-check-config first or the hook will be inert`
- `<python> cannot import PyYAML; drift_check.py will exit 2 and the hook will report itself unavailable on every commit`
- `smoke test failed: drift_check.py exited <rc> — refusing to report a successful install`

## Verifying it works

Make a trivial commit in a vault that has something durable uncommitted. The
hook should print a session-hygiene block to stderr. If nothing prints, check in
order: the executable bit, `core.hooksPath`, and whether `drift_check.py --config
<path> --dry-run` produces "Session hygiene" lines at all.

## Escape hatch

`WRITING_COWORK_SKIP_HYGIENE=1 git commit ...` silences the hook for scripted or
batch commits. Worth knowing before it becomes a habit — routine use means the
check is too noisy and should be tuned rather than muted.

## Related skills

- `pm-close-session` — the fuller ritual; this hook catches what a missed close leaves behind.
- `pm-run-drift-check` — the same checks, run deliberately.
- `pm-schedule-review` — schedule a periodic drift check; the third layer alongside the hook and the close skill.
