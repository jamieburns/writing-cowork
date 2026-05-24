---
name: sync-mobile:sync
description: Merge temp branch back to main — handle conflicts or finalize
type: skill
role: pm
---

# Sync Changes Back to Main

**Purpose:** Merge iPad changes from temp branch back to main. Handle conflicts if needed. Optionally finalize and clean up.

**Who runs this:** PM or specialist on Mac, after returning from iPad  
**When:** Ready to integrate iPad work back into main vault  
**Output:** Branch merged successfully, or conflict summary for resolution  
**Prerequisite:** `sync-mobile:pull` must have run (manifest must exist)

---

## Instructions

You're back on Mac. Time to merge the temp branch work into main.

---

## PHASE 1: Verify State

### Step 1: Check manifest exists

```bash
if [ ! -f process/data_management/sync_manifest.json ]; then
  echo "✗ No manifest found. Run sync-mobile:pull first."
  exit 1
fi
```

### Step 2: Extract branch and task info

```bash
BRANCH_NAME=$(cat process/data_management/sync_manifest.json | grep -oP '"branch_name": "\K[^"]+')
TASK_ID=$(cat process/data_management/sync_manifest.json | grep -oP '"task_id": "\K[^"]+')
BASELINE=$(cat process/data_management/sync_manifest.json | grep -oP '"commit": "\K[^"]+')

echo "Merging: $BRANCH_NAME → main"
[ "$TASK_ID" != "none" ] && echo "Task linked: $TASK_ID"
```

### Step 3: Check working tree is clean

```bash
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠ Uncommitted changes on main. Commit or stash first."
  exit 1
fi
```

Ensure main is clean before merging.

---

## PHASE 2: Attempt Merge

### Step 4: Switch to main and merge

```bash
git checkout main
git merge --no-ff $BRANCH_NAME -m "[writer] Sync iPad changes from $(date +'%Y-%m-%d %H:%M')"
```

---

## PHASE 3: Handle Merge Result

### Step 5a: No Conflict — Merge Succeeded

If merge succeeds:

```bash
MERGE_COMMIT=$(git rev-parse HEAD)
MERGE_SHORT=$(git rev-parse --short HEAD)
```

Show user:
```
✓ Merge successful

Merged: $BRANCH_NAME → main
Commit: $MERGE_SHORT

Changes on temp branch:
$(git diff --stat $BASELINE HEAD)
```

Then proceed to Step 6 (finalize or leave open).

### Step 5b: Conflict — Merge Failed

If merge fails (conflict detected):

```bash
echo "⚠ Conflict detected during merge"

CONFLICTED_FILES=$(git diff --name-only --diff-filter=U)
echo "Conflicted files:"
echo "$CONFLICTED_FILES"
```

Show user:
```
⚠ Merge conflict detected

Files with conflicts:
  substance/chapter-3.md
  process/active/todos.md

Options:
  (1) Launch merge tool (Beyond Compare)
      - Resolve conflicts in UI
      - Save and exit
      - Git will complete merge
  
  (2) Abort merge
      - Undo merge attempt
      - Return branch to safe state
      - Decide what to do next
```

Ask: "(1/2)?"

**If (1) — Launch merge tool:**

```bash
for file in $CONFLICTED_FILES; do
  git mergetool $file
done
```

After user resolves all conflicts:
```bash
git commit -m "[writer] Resolve mobile sync conflict (temp branch $BRANCH_NAME)"
```

Then proceed to Step 6.

**If (2) — Abort merge:**

```bash
git merge --abort
echo "✓ Merge aborted. Branch state restored."
echo "Next: resolve conflicts and retry, or discuss with team."
exit 0
```

---

## PHASE 4: Finalize or Leave Open

### Step 6: Ask user to finalize

After successful merge (with or without conflict resolution):

```
✓ Merge complete

Branch: $BRANCH_NAME
Merged to: main
Commit: $MERGE_SHORT

Would you like to finalize (delete branch + cleanup)?
  (1) Yes, finalize — delete branch and manifest
  (2) No, leave open — keep branch for more work
```

Ask: "(1/2)?"

---

## PHASE 5: Cleanup (if finalizing)

### Step 7a: Delete Branch and Manifest

If user chooses finalize (1):

```bash
# Delete temp branch
git branch -d $BRANCH_NAME
echo "✓ Branch deleted: $BRANCH_NAME"

# Delete manifest
rm process/data_management/sync_manifest.json
echo "✓ Manifest deleted"
```

Output:
```
✓ Finalized

Branch deleted: $BRANCH_NAME
Manifest deleted
Vault back to normal state (on main)

Status:
  All iPad work integrated into main
  Ready for next operations
```

### Step 7b: Leave Open (if not finalizing)

If user chooses to leave open (2):

```bash
echo "✓ Branch left open for additional work"
echo "Manifest still in place: process/data_management/sync_manifest.json"
echo ""
echo "Next steps:"
echo "  - More editing/work on temp branch"
echo "  - sync-mobile:commit to save new work"
echo "  - sync-mobile:sync again when ready to finalize"
```

---

## PHASE 6: Update Task (if linked)

### Step 8: Inform user about task status

If task was linked:

```bash
echo "ℹ Task linked: $TASK_ID"
echo "Task status remains as-is (you manage updates)"
echo "When task is complete, close it via: pm-close-task $TASK_ID"
echo ""
echo "Note: Closing the task will verify branch is merged."
```

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No manifest found | Run sync-mobile:pull first |
| Main has uncommitted changes | Commit or stash on main, retry |
| Merge conflict on critical files | User resolves with merge tool; may need discussion |
| Merge tool not configured | Run sync-mobile:setup to configure Beyond Compare |
| Branch doesn't exist | Branch may have been deleted; check git branch -a |
| Merge commit fails | Rare; check `git status`, resolve and commit manually |

---

## Important Notes

- **Merge uses --no-ff** — Creates a merge commit even if fast-forward possible (clean history)
- **Conflict handling is interactive** — User resolves via merge tool, not auto-merge
- **Finalize is optional** — Can leave branch open if more work needed (voice pass, etc.)
- **Task status is manual** — Sync doesn't auto-update task; user manages via pm-update-task/pm-close-task
- **Manifest deleted on finalize** — Can't recover task link after deletion (but git history has the branch)

---

## Output Examples

### Success (No Conflict)

```
✓ Merge successful

Merged: sync/ipad-0523-x7k9m2 → main
Commit: abc1234

Changes integrated:
  substance/chapter-3.md  | 50 ++++++++
  process/active/todos.md | 10 ++
  2 files changed, 60 insertions(+)

Would you like to finalize (delete branch + cleanup)?
  (1) Yes, finalize
  (2) No, leave open

Choose: (1/2)?
[User: 1]

✓ Finalized

Branch deleted: sync/ipad-0523-x7k9m2
Manifest deleted
Vault back to normal state (on main)

Status:
  All iPad work integrated into main
  Task abc123 (Edit chapter 3) — close when ready
```

### Conflict — Resolved

```
⚠ Merge conflict detected

Conflicted files:
  substance/chapter-3.md
  process/active/todos.md

Options:
  (1) Launch merge tool (Beyond Compare)
  (2) Abort merge

Choose: (1/2)?
[User: 1]

[User resolves conflicts in Beyond Compare UI for each file]

✓ Merge complete

Branch: sync/ipad-0523-x7k9m2
Merged to: main
Commit: def5678

Would you like to finalize?
  (1) Yes, finalize
  (2) No, leave open

Choose: (1/2)?
[User: 1]

✓ Finalized — all resolved and cleaned up
```

### Leave Open for Voice Pass

```
✓ Merge successful

Merged: sync/ipad-0523-x7k9m2 → main
Commit: abc1234

Would you like to finalize?
  (1) Yes, finalize
  (2) No, leave open

Choose: (1/2)?
[User: 2]

✓ Branch left open for additional work

Manifest in place: process/data_management/sync_manifest.json
Branch: sync/ipad-0523-x7k9m2 (ready for voice pass)

Next:
  - Voice specialist can do mode B pass
  - When complete: sync-mobile:sync again
  - Then finalize
```

---
