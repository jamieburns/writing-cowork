---
name: sync-mobile:revert-to
description: Undo changes by reverting to an earlier commit on temp branch
type: skill
role: any
---

# Revert to Earlier Commit

**Purpose:** Go back to an earlier checkpoint if you've made changes you want to discard.

**Who runs this:** iPad user (via dispatch) or Mac user  
**When:** You've committed changes you don't want to keep; want to revert  
**Output:** Working directory reverted to chosen commit, changes discarded  
**Prerequisite:** `sync-mobile:pull` must have run; commits must exist to revert to

---

## Instructions

You've made commits and now want to go back to an earlier point. This skill shows you the commit history and lets you pick one to revert to.

---

## PHASE 1: List Commits

### Step 1: Verify manifest and branch exist

```bash
if [ ! -f process/data_management/sync_manifest.json ]; then
  echo "✗ No manifest. Run sync-mobile:pull first."
  exit 1
fi

BRANCH_NAME=$(cat process/data_management/sync_manifest.json | grep -oP '"branch_name": "\K[^"]+')
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]; then
  echo "Checking out $BRANCH_NAME"
  git checkout $BRANCH_NAME
fi
```

### Step 2: Get commit history on temp branch

Get the baseline commit (from pull time):

```bash
BASELINE=$(cat process/data_management/sync_manifest.json | grep -oP '"commit": "\K[^"]+')
```

Show commits since baseline:

```bash
git log $BASELINE..HEAD --format="%h|%ai|%s" | nl -nln -w2 -s') '
```

Example output:
```
1) abc1234|2026-05-23 14:35:00 UTC|Fixed chapter 3 typos
2) def5678|2026-05-23 14:20:00 UTC|Added reader notes  
3) ghi9101|2026-05-23 14:10:00 UTC|Started chapter 3 edits
```

Also show the baseline:
```
Baseline (before iPad work):
  jkl2345|2026-05-23 14:00:00 UTC|Last commit on Mac before pull
```

### Step 3: Ask user which commit to revert to

Display formatted menu:

```
Your commits (newest first):

1) abc1234 at 2026-05-23 14:35 — Fixed chapter 3 typos
2) def5678 at 2026-05-23 14:20 — Added reader notes
3) ghi9101 at 2026-05-23 14:10 — Started chapter 3 edits

Baseline (before iPad work):
  jkl2345 at 2026-05-23 14:00 — Last commit on Mac

Which commit to revert to? (1/2/3/baseline)?
```

---

## PHASE 2: Revert

### Step 4: Confirm revert action

Revert is destructive—confirm with user:

```
⚠ Revert is permanent

Reverting to abc1234 will:
  - Discard all changes after that commit
  - Reset files to that point
  - Keep discarded commits in history (can't recover without git expertise)

Confirm revert to abc1234? (yes/no)
```

### Step 5: Perform revert

If user confirms:

```bash
TARGET_COMMIT=$(user_selection)
git reset --hard $TARGET_COMMIT
```

Output:
```
✓ Reverted to $TARGET_COMMIT

Working directory now matches:
  Commit: $TARGET_COMMIT
  Time: [extract from git log]
  Message: [extract commit message]

Files reverted to that state.
```

If user cancels:
```
Revert cancelled. No changes made.
```

---

## PHASE 3: Recovery Path

### Step 6: Show next steps

After revert, user can:

```
Next steps:

(1) Keep working from here
    - Edit files again
    - sync-mobile:commit "<new message>" to save

(2) Check what you lost (if you change your mind)
    git log --oneline -10

(3) Eventually sync back to Mac
    When done: sync-mobile:sync
```

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No manifest found | Run sync-mobile:pull first |
| Not on temp branch | Skill auto-checks out correct branch |
| No commits to revert | You're already at baseline; nothing to undo |
| Git reset fails | Check `git status`, ensure no merge in progress |
| Can't find target commit | Commit may have been rebased; show current history |

---

## Important Notes

- **Revert is permanent** — Discarded commits are gone (unless you know git well enough to recover)
- **Working tree is updated** — Files on iPad will change to match the earlier commit
- **History is preserved** — Discarded commits stay in `git log` for audit; only working tree resets
- **You can keep working** — After revert, edit and commit as normal
- **Safe to use repeatedly** — Revert, edit, commit, revert again if needed

---

## Output Examples

### Success

```
Your commits (newest first):

1) abc1234 at 2026-05-23 14:35 — Fixed chapter 3 typos
2) def5678 at 2026-05-23 14:20 — Added reader notes
3) ghi9101 at 2026-05-23 14:10 — Started chapter 3 edits

Baseline (before iPad work):
  jkl2345 at 2026-05-23 14:00 — Last commit on Mac

Which commit to revert to? (1/2/3/baseline)?
[User selects: 2]

⚠ Revert is permanent

Reverting to def5678 will discard:
  - abc1234: Fixed chapter 3 typos

Confirm? (yes/no)
[User: yes]

✓ Reverted to def5678

Working directory reset to:
  Commit: def5678
  Time: 2026-05-23 14:20:00 UTC
  Message: Added reader notes

Files now match that state. Discarded changes are gone.

Next:
  - Continue editing from here
  - sync-mobile:commit "<message>" to save new work
  - Or: revert again if needed
```

### No Commits

```
No commits to revert to. You're at baseline.

(Already at the state from sync-mobile:pull.)
```

### Cancelled

```
Revert cancelled. No changes made.

Working directory unchanged.
```

---
