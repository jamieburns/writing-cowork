---
name: pm-resume-setup
description: >
  This skill should be used when the user asks to "resume a failed
  pm-setup-project", "continue setup after fixing an issue", "pick up
  setup where it failed", or any variant of resuming a partial
  pm-setup-project run after a sub-skill failure. Reads the state file
  at ~/.config/cowork/writing-cowork/setup_state/<name>_setup_state.json
  and continues from the failed step.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-resume-setup

Continue a partial `pm-setup-project` run after a sub-skill failure.
Reads the state file written by pm-setup-project, identifies the failed
or skipped step, re-runs it (or skips past it if the issue was resolved
out-of-band), then continues forward through the remaining sub-skills.

Implements writing-cowork locked decision #6: leave partial state on
failure, provide pm-resume-setup recovery skill. No rollback.

## Arguments

- **`<name>`** (required) — project name matching the state file at
  `~/.config/cowork/writing-cowork/setup_state/<name>_setup_state.json`.

## Preconditions

1. Verify state file exists at
   `~/.config/cowork/writing-cowork/setup_state/<name>_setup_state.json`.
   If not, abort with `no setup state for <name>; pm-setup-project was
   never started or completed cleanly`.
2. Parse the state file. Verify required fields present: `name`, `vault`,
   `git_mode`, `started_at`, `completed_steps`, `last_attempted_step`,
   `status`.
3. If `status == "complete"`, output `setup for <name> already complete;
   no resume needed` and exit cleanly (no-op).

## Execution

1. **Identify the resume point.** The first sub-skill NOT in
   `completed_steps` AND not skipped per the orchestrator's skip rules
   (e.g., pm-init-github skipped when `git_mode != "new-github"`).
2. **Run the resume point sub-skill.** Invoke via the Skill tool with
   the state-file's stored args (`vault`, `name`, `git_mode`, etc.).
3. **On success:** mark the sub-skill complete in the state file, then
   continue to the next sub-skill in the orchestrator's order. Repeat.
4. **On second failure of the same sub-skill:** abort. The underlying
   problem isn't transient. Update the state file's `last_error` with
   the new error message and exit.
5. **On success of the final step:** set `status: "complete"`. Same as
   a clean pm-setup-project run.

Critical: the user may have manually fixed the underlying issue between
the original failure and the resume invocation. The skill should NOT
assume the failure mode is the same. Re-run the failed sub-skill from
scratch; its own preconditions will catch any remaining issue.

## Output on success

```
Resumed setup for <name> from step <N> (<sub-skill>):
  Completed: <list of newly-completed steps>
  Final status: complete
```

If multiple sub-skills were run during resume, list them. If only one
remained, single-line output.

## Output on failure

- `no setup state for <name>; nothing to resume`
- `setup for <name> already complete; no resume needed` (informational, not error)
- `state file at <path> is corrupted: <parse error>. Inspect the file before retrying.`
- `sub-skill <name> failed again on resume: <verbatim error>. The underlying issue is not transient — fix it before re-invoking pm-resume-setup.`

## Standalone use

This IS the canonical use — resume-setup is only invoked after a
pm-setup-project failure. It's not intended for any other purpose.
