---
name: sync-mobile:commit
description: Commit changes on temp branch (dispatch from iPad or Mac)
type: skill
role: any
---

# Commit Mobile Edits

**Purpose:** Save a checkpoint of changes on the temp branch.

**Who runs this:** iPad user (via dispatch) or Mac user  
**When:** After editing on iPad, when you want to save progress  
**Output:** Commit created on temp branch with provided message  
**Prerequisite:** `sync-mobile:pull` must have run (manifest must exist)

---

## Instructions

You've made edits on iPad (or Mac). Time to commit them as a checkpoint.

---

## PHASE 1: Find Manifest & Branch

### Step 1: Verify manifest exists

```bash
if [ ! -f process/data_management/sync_manifest.json ]; then
  echo "✗ No manifest found. Run sync-mobile:pull first."
  exit 1
fi
```

### Step 2: Extract branch name and get current status

```bash
BRANCH_NAME=$(cat process/data_management/sync_manifest.json | grep -oP '"branch_name": "\K[^"]+')
echo "Temp branch: $BRANCH_NAME"

# Verify we're on the temp branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]; then
  echo "⚠ Not on temp branch. Checking out $BRANCH_NAME"
  git checkout $BRANCH_NAME
fi
```

---

## PHASE 2: Stage Changes

### Step 3: Show user what will be committed

```bash
git status
```

Display output to user so they can see what's about to be committed.

If nothing to commit (working tree clean):
```
✓ Working tree clean. Nothing to commit.
```
End skill.

If changes exist, show:
```
On branch sync/ipad-0523-x7k9m2

Modified files:
  substance/chapter-3.md
  process/active/todos.md

Untracked files:
  .obsidian/cache.json (will be ignored)
```

### Step 4: Stage all changes

```bash
git add -A
```

This stages all modified and new files (respecting .gitignore).

---

## PHASE 3: Commit

### Step 5: Get commit message from user

```
Commit message: 
```

Prompt user to type commit message. Accept multi-line if they paste.

Store as `$MESSAGE`.

### Step 6: Perform commit

```bash
git commit -m "$MESSAGE"
```

If commit succeeds:

```bash
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_SHORT=$(git rev-parse --short HEAD)
COMMIT_TIME=$(git log -1 --format=%ai HEAD)
```

Output:
```
✓ Committed: $COMMIT_SHORT
  Branch: $BRANCH_NAME
  Message: $MESSAGE
  Time: $COMMIT_TIME

Checkpoint saved. Keep editing or sync back when ready.
```

If commit fails (unexpected error):
```
✗ Commit failed. Check git status:
  git status
```

---

## PHASE 4: Confirm Checkpoint

### Step 7: Show commit in history

```bash
git log --oneline -3
```

Display last 3 commits so user can see their checkpoint in context:

```
abc1234 Fixed chapter 3 typos
def5678 Added more notes
ghi9101 Started iPad edits
```

Output:
```
✓ Checkpoint saved to temp branch

Next:
  - Continue editing on iPad
  - sync-mobile:commit again when ready
  - When done: return to Mac and run sync-mobile:sync
  - Or: check status with sync-mobile:check-sync (from iPad)
```

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No manifest found | Run sync-mobile:pull first |
| Not on temp branch | Skill auto-checks out correct branch |
| Nothing to commit | No changes to save; keep editing |
| Commit fails | Check `git status`, resolve conflicts, retry |
| Branch doesn't exist | Branch may have been deleted; run pull again |

---

## Important Notes

- **Auto-stages all changes** — Uses `git add -A`, includes new files and deletions
- **Commit is permanent** — Creates a savepoint you can revert to later via sync-mobile:revert-to
- **Message is audit trail** — Describe what you changed so you can find it later
- **Working tree stays dirty** — Commit doesn't reset working tree; you keep editing
- **Safe to call repeatedly** — Commit anytime, as many times as you want

---

## Output Examples

### Success

```
✓ Committed: abc1234
  Branch: sync/ipad-0523-x7k9m2
  Message: Fixed chapter 3 typos and added reader notes
  Time: 2026-05-23 14:35:00 UTC

Checkpoint saved. Keep editing or sync back when ready.

Recent commits:
abc1234 Fixed chapter 3 typos and added reader notes
def5678 Started chapter 3 edits
ghi9101 Work started

Next:
  - Continue editing on iPad
  - sync-mobile:commit again when ready
```

### Nothing to Commit

```
✓ Working tree clean. Nothing to commit.

(No changes since last commit.)
```

### Error: No Manifest

```
✗ No manifest found. Run sync-mobile:pull first.
```

---
