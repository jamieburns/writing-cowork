---
name: pm-setup-project
description: >
  This skill should be used when the user asks to "set up a new writing project",
  "scaffold a writing-cowork project", "initialize a cowork vault",
  "create a new writing project with the cowork pattern",
  or any variant of starting a fresh project that should run the writing-cowork
  multi-role pattern (PM, substance, voice/tone, review). Orchestrates the full
  setup sequence — vault skeleton, git, GitHub remote, charter, handoff,
  ownership table, drift-check config, voice scaffold, roadmap, todos —
  and registers the project with the per-machine cowork registry.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-setup-project

Orchestrate the full setup of a new writing-cowork project. Invoke the setup
sub-skills in dependency order, persist progress to a state file after each
step, and on any sub-skill failure stop immediately and instruct the user how
to resume with `pm-resume-setup`. Do not roll back partial state — locked
decision #6 in the v1 design.

## Arguments

Parse from the user's invocation language; ask interactively only when an
ambiguity cannot be resolved.

- **`<name>`** (required) — the project's short slug. Lowercase, kebab-case,
  matches the GitHub repo name and the registry key. Example: `epistemology`,
  `reconciliation-hypothesis`, `morning-letters`.
- **`--vault=<path>`** (optional) — absolute path to the vault directory.
  Default: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/<name>`
  (titlecased). If the path exists and is non-empty, abort with a clear error;
  setup is for new projects only.
- **`--git=new-github|local|existing|none`** (optional, default `new-github`):
  - `new-github` — git init + create remote on GitHub + push.
  - `local` — git init only, no remote.
  - `existing` — vault is already a git repo; skip init, verify clean.
  - `none` — no git at all (uncommon; mainly for throwaway test vaults).
- **`--decisions=<file>`** (optional) — path to a pre-lift decisions doc to
  install at vault root via `pm-place-lift-decisions`. If absent, that step is
  skipped silently.
- **`--github-org=<org>`** (optional, default `jamieburns`) — GitHub
  organization or user account for the new remote. Only consulted when
  `--git=new-github`.

## Sub-skill invocation order

Invoke each sub-skill via the Skill tool, in this exact order. After each
successful step, append a record to the state file (see "State file" below).
On any failure, do not call subsequent steps; do not undo prior steps;
return the failure message plus the resume instruction.

| # | Sub-skill | Purpose | Skipped when |
|---|-----------|---------|--------------|
| 1 | `pm-init-vault` | Create folder skeleton with `.gitkeep` markers at the specified path | — |
| 2 | `pm-init-git` | `git init -b main` inside the vault | `--git=none` or `--git=existing` |
| 3 | `pm-init-github` | `gh repo create <org>/<name> --private`, add origin, push | `--git` is not `new-github` |
| 4 | `pm-install-charter` | Place `charter.md` from `templates/charter.md` | — |
| 5 | `pm-install-handoff` | Place `handoff.md` from `templates/handoff.md` | — |
| 6 | `pm-install-for-other-contexts` | Place `for_other_contexts.md` from template | — |
| 7 | `pm-install-hierarchy-and-ownership` | Place `process/data_management/file_hierarchy.md` + initial `file_ownership.md` | — |
| 8 | `pm-install-drift-check-config` | Place `process/data_management/drift_check.yaml` from template, substituting project-specific values | — |
| 9 | `pm-place-lift-decisions` | Copy the supplied decisions doc to vault root | `--decisions` not provided |
| 10 | `pm-init-voice-handoff` | Place `process/active/voice_handoff.md` with placeholders | — |
| 11 | `pm-init-voice-exceptions` | Create empty `process/active/voice_exceptions.md` | — |
| 12 | `pm-init-reader-review-tracking` | Create empty `process/active/reviewer_tracking.md` | — |
| 13 | `pm-init-roadmap` | Create empty `process/active/roadmap.md` | — |
| 14 | `pm-init-todos` | Create empty `process/active/todos.md` | — |
| 15 | `pm-register-project` | Add entry to `~/.config/cowork/registry.yaml` | — |

Skip rules apply at the orchestrator level. Each sub-skill is independently
invokable from chat for ad-hoc use; the orchestrator simply chains them.

## State file

Persist progress at `~/.config/cowork/setup_state/<name>.json`. Create the
parent dir if absent. The state file lives outside the vault so it survives
any failure mode — including a partial `pm-init-vault`.

Format:

```json
{
  "name": "<name>",
  "vault": "<absolute path>",
  "git_mode": "<new-github|local|existing|none>",
  "github_org": "<org or null>",
  "decisions_file": "<path or null>",
  "started_at": "<ISO 8601 UTC timestamp>",
  "completed_steps": [
    {"step": "pm-init-vault", "completed_at": "<ISO 8601 UTC timestamp>"}
  ],
  "last_attempted_step": "<sub-skill name>",
  "last_error": "<error message or null>",
  "status": "in-progress|complete|failed"
}
```

Update the file atomically — write to `<name>.json.tmp`, then `mv` to
`<name>.json`. The atomic-write convention is inherited from the manual phase;
the registry and other long-lived files use it to avoid torn reads.

On success of the final step (`pm-register-project`), set `status: "complete"`.
Keep the file — `pm-resume-setup` checks status before doing anything; a
completed file is a no-op signal, not stale state.

## Output

While running, narrate progress in plain language (suitable for the user
chat): one short line per step, indicating start and end. Example:

```
Setting up project: epistemology
Vault path: ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Epistemology
Git mode: new-github

[1/15] Initialize vault skeleton… done
[2/15] Initialize git repo… done
[3/15] Create GitHub remote jamieburns/epistemology… done
...
[15/15] Register project in cowork registry… done

Setup complete. Next: open the vault in Obsidian and read charter.md.
```

On failure, emit the failing step number, the error message from the
sub-skill, and the resume instruction:

```
[7/15] Install file hierarchy and ownership… FAILED
Error: <verbatim sub-skill error>

State file at: ~/.config/cowork/setup_state/<name>.json
To resume after fixing the cause: invoke pm-resume-setup with name=<name>.
```

## Inputs that require interactive prompting

The orchestrator must resolve these before invoking sub-skills. Ask the user
only what cannot be inferred from arguments or from sensible defaults:

- If `<name>` is missing — ask.
- If the resolved `--vault` path already exists and is non-empty — abort with
  the error message, do not ask. Setup is new-project only.
- If `--git=new-github` and `gh auth status` reports unauthenticated — abort
  with the error message and ask the user to run `gh auth login`. Do not
  prompt for credentials.

## Validation before starting

Before invoking step 1, verify:

1. The `gh` CLI is available on PATH if `--git=new-github`.
2. The `git` CLI is available on PATH if `--git` is anything other than `none`.
3. The plugin's `templates/` directory exists (it ships with the plugin).
4. The registry directory `~/.config/cowork/` exists; create if absent.

If any check fails, report what's missing and abort. Do not write a state file
for a pre-flight abort; state file only tracks runs that began step 1.

## Failure semantics summary

- Stop on first sub-skill error.
- Do not unwind prior steps.
- Write the failure into the state file (status: "failed", last_error filled).
- Tell the user how to resume.

`pm-resume-setup` (separate skill) reads the state file and continues from
`last_attempted_step` — re-running the failed step, then continuing forward.

## Related skills

- `pm-resume-setup` — recovery skill for partial setups.
- `pm-init-vault` through `pm-register-project` — the 15 sub-skills enumerated
  above. Each is independently invokable.
- `pm-list-projects` — list registered projects.
- `pm-enable-project` / `pm-disable-project` — toggle a project's registry
  flag (e.g., to pause drift checks).
