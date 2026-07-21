---
name: pm-tag-snapshot
description: >
  This skill should be used when the user asks to "tag a snapshot",
  "mark this point in history", "create a snapshot tag", or any variant
  of creating an annotated git tag in the `snapshot/` namespace.
  Snapshots are boundary-of-state markers without lock or release
  semantics — "here's where I changed gears."
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-tag-snapshot

Create an annotated git tag in the `snapshot/<date>-<name>` namespace,
push it, and log the snapshot in the project's tag history. Snapshots are
navigation aids; they don't imply external release or substantive lock.

## Arguments

- **`<name>`** (required) — short kebab-case name for the snapshot (e.g.,
  `end-of-initial-development`, `pre-restructure`). The skill prepends
  the date.
- **`<message>`** (required) — the annotated tag message. Should describe
  what's true at this snapshot.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.
- **`--no-push`** (optional, flag) — create the tag locally but don't push
  to origin.

## Preconditions

1. Resolve vault root.
2. Verify `<vault>` is a git repo.
3. Verify `<vault>` has a commit (can't tag an unborn branch).
4. Compute today's date in YYYY-MM-DD (local timezone).
5. Verify the tag `snapshot/<date>-<name>` doesn't already exist. If it
   does, abort with `tag snapshot/<date>-<name> already exists; choose a
   different name or delete the existing tag`.

## Execution

Run via host shell:

```bash
cd <vault>
git tag -a snapshot/<date>-<name> -m "<message>"
# Push unless --no-push
if [ -z "$NO_PUSH" ] && git remote get-url origin >/dev/null 2>&1; then
    git push origin snapshot/<date>-<name>
fi
```

Per tagging_conventions.md: always annotated (`-a`), push explicitly per
tag (not `--tags`).

## Output on success (with push)

```
Tagged: snapshot/<date>-<name>
  Message: <message>
  Pushed: snapshot/<date>-<name> → origin
```

## Output on success (no push)

```
Tagged locally: snapshot/<date>-<name>
  Message: <message>
  Push manually with: git push origin snapshot/<date>-<name>
```

## Output on failure

- `<vault> is not a git repo`
- `<vault> has no commits; cannot tag unborn branch`
- `tag snapshot/<date>-<name> already exists; choose a different name`
- `git push failed: <error>`

## Standalone use

Same preconditions. Snapshot tags are cheap and reversible; use
liberally to mark significant points in the project's git history.
