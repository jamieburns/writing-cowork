---
name: pm-tag-lock
description: >
  This skill should be used when the user asks to "tag a lock", "lock in
  a decision", "create a decision-lock tag", or any variant of creating
  an annotated git tag in the `lock/` namespace. Locks mark substantive
  commitments treated as settled; revising a lock requires an explicit
  decision-log entry. Tag message format enforced per writing-cowork
  locked decision #8.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-tag-lock

Create an annotated git tag in the `lock/<date>-<name>` namespace, with
a structured rationale message, push it, and log the lock. The message
format is enforced per writing-cowork's locked decision #8 (Why /
Decision / Alternatives considered).

## Arguments

- **`<name>`** (required) — kebab-case name for the lock (e.g.,
  `phase1-foundational-decisions`, `terminology-finalization`). The skill
  prepends the date.
- **`<why>`** (required) — one or two sentences: why this decision was
  made. Captures the context for future-you.
- **`<decision>`** (required) — what was decided. Concrete and specific.
- **`<alternatives>`** (required) — one sentence listing alternatives
  considered and rejected. If none considered, write "none considered"
  honestly — but the writer should reflect on whether this lock is
  actually a settled decision or just a default.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.
- **`--no-push`** (optional, flag) — create locally only.

## Preconditions

1. Resolve vault root.
2. Verify `<vault>` is a git repo with at least one commit.
3. Compute today's date YYYY-MM-DD (local timezone).
4. Verify the tag `lock/<date>-<name>` doesn't already exist.

## Execution

Construct the annotated tag message in the structured format:

```
Why: <why>

Decision: <decision>

Alternatives considered: <alternatives>
```

Run via host shell:

```bash
cd <vault>
git tag -a lock/<date>-<name> -F - <<EOF
Why: <why>

Decision: <decision>

Alternatives considered: <alternatives>
EOF
if [ -z "$NO_PUSH" ] && git remote get-url origin >/dev/null 2>&1; then
    git push origin lock/<date>-<name>
fi
```

Use `-F -` (read message from stdin) rather than `-m` to handle multi-line
messages correctly.

## Output on success (with push)

```
Locked: lock/<date>-<name>
  Why: <why-truncated-to-one-line>
  Decision: <decision-truncated-to-one-line>
  Alternatives: <alternatives-truncated>
  Pushed: lock/<date>-<name> → origin
```

## Output on failure

- `<vault> is not a git repo`
- `tag lock/<date>-<name> already exists; choose a different name`
- `missing required field <name|why|decision|alternatives>; all three
  rationale fields are mandatory per writing-cowork locked decision #8`

## Standalone use

Same preconditions. Locks are heavyweight — use only for substantive
commitments. Snapshot tags (pm-tag-snapshot) are the appropriate tool
for lighter "boundary of state" markers.
