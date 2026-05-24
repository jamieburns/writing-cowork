---
name: sync-mobile:backup
description: List commits on temp branch — audit trail and recovery reference
type: skill
role: any
---

# Backup / Commit History

**Purpose:** Show audit trail of all commits on temp branch. Useful for understanding what changed and when.

**Who runs this:** iPad user (via dispatch) or Mac user  
**When:** Want to see what's been committed, or prepare to revert  
**Output:** List of commits with timestamps and messages  
**Prerequisite:** `sync-mobile:pull` must have run (manifest must exist)

---

## Instructions

Shows you a readable list of everything committed on the temp branch since you pulled.

---

## PHASE 1: Verify State

### Step 1: Check manifest exists

```bash
if [ ! -f process/data_management/sync_manifest.json ]; then
  echo "✗ No manifest found. Run sync-mobile:pull first."
  exit 1
fi
```

### Step 2: Extract baseline and branch info

```bash
BRANCH_NAME=$(cat process/data_management/sync_manifest.json | grep -oP '"branch_name": "\K[^"]+')
BASELINE=$(cat process/data_management/sync_manifest.json | grep -oP '"commit": "\K[^"]+')
PULL_TIME=$(cat process/data_management/sync_manifest.json | grep -oP '"created_at": "\K[^"]+')
```

---

## PHASE 2: Generate Commit List

### Step 3: Get all commits on temp branch

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]; then
  git checkout $BRANCH_NAME
fi
```

Get commit list with details:

```bash
git log $BASELINE..HEAD --format="%h|%ai|%an|%s" > /tmp/commits.txt
```

---

## PHASE 3: Format and Display

### Step 4: Show backup/audit trail

Display header:

```
iPad Session Backup / Audit Trail
==================================

Session ID: [extract from manifest]
Pull time: $PULL_TIME
Branch: $BRANCH_NAME
Baseline (before work): $BASELINE (short: ${BASELINE:0:7})

Commits on temp branch (newest first):
```

Format and display commits:

```bash
nl -nln -w3 -s ') ' /tmp/commits.txt | while IFS='|' read -r num hash time author msg; do
  printf "%s %s at %s by %s\n  %s\n\n" "$num" "$hash" "$time" "$author" "$msg"
done
```

Example output:
```
1) abc1234 at 2026-05-23 14:35:00 UTC by iPad
  Fixed chapter 3 typos and added reader notes

2) def5678 at 2026-05-23 14:20:00 UTC by iPad
  Added more context to chapter 2

3) ghi9101 at 2026-05-23 14:10:00 UTC by iPad
  Started chapter 3 edits

Total: 3 commits since pull at 2026-05-23 14:00
```

---

## PHASE 4: Usage Guidance

### Step 5: Show what you can do with this info

Display next steps:

```
What you can do with this backup:

(1) Remember what you did
    - See the timeline of your work
    - Review commit messages

(2) Prepare to revert (if needed)
    - Use sync-mobile:revert-to to go back to any commit
    - Example: revert-to def5678 (commit 2)

(3) Share for review
    - Show this to others before syncing back
    - Or let voice specialist review changes

(4) Sync back to main
    - When ready: sync-mobile:sync
    - Merges all commits to main

(5) Just keep working
    - Continue editing and committing as normal
    - Check this backup anytime
```

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No manifest found | Run sync-mobile:pull first |
| No commits to list | You haven't committed yet; make edits and sync-mobile:commit |
| Branch doesn't exist | Branch may have been deleted; run pull again |
| Can't read manifest | File may be corrupted; delete and re-pull |

---

## Important Notes

- **Audit trail is permanent** — All commits stay in git history (even after revert)
- **Timestamps are UTC** — For consistency across time zones
- **Author field** — Will show system user or "iPad" if editing on mobile
- **Messages are key** — Good commit messages make this backup useful
- **Non-destructive** — Viewing backup doesn't change anything; safe to call anytime

---

## Output Examples

### Success (With Commits)

```
iPad Session Backup / Audit Trail
==================================

Session ID: ipad-0523-x7k9m2
Pull time: 2026-05-23T14:00:00Z
Branch: sync/ipad-ipad-0523-x7k9m2
Baseline: abc1234 (before work)

Commits on temp branch (newest first):

1) xyz9abc at 2026-05-23 14:35:00 UTC by iPad
  Fixed chapter 3 typos and added reader notes

2) def5678 at 2026-05-23 14:20:00 UTC by iPad
  Added more context to chapter 2

3) ghi9101 at 2026-05-23 14:10:00 UTC by iPad
  Started chapter 3 edits

Total: 3 commits since pull at 2026-05-23 14:00

What you can do:
  - Revert to any commit (sync-mobile:revert-to)
  - Review before syncing back
  - Share with team
  - Sync back when ready (sync-mobile:sync)
```

### No Commits Yet

```
iPad Session Backup / Audit Trail
==================================

Session ID: ipad-0523-x7k9m2
Pull time: 2026-05-23T14:00:00Z
Branch: sync/ipad-ipad-0523-x7k9m2
Baseline: abc1234 (before work)

No commits yet on temp branch.

You've pulled but haven't committed any changes yet.
Make edits, then: sync-mobile:commit "<message>"
```

---
