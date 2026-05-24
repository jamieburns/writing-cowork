---
name: sync-mobile:sync-back
description: Sync iPad changes back to Mac — detect conflicts, merge safely, or defer for resolution
type: skill
role: pm
---

# Sync Changes Back

**Purpose:** Detect iPad changes, handle conflicts, and safely integrate them into Mac vault.

**Who runs this:** iPad (via dispatch) or manual on Mac  
**When:** After returning from iPad or when ready to sync offline edits  
**Output:** Changes committed, or conflict deferred to sync_conflict_*.md

---

## Instructions

This is the core sync skill. It detects what changed on iPad, checks for conflicts with Mac, and either merges or defers.

---

## PHASE 1: Wait for iCloud sync

### Step 1: Wait for iCloud to sync iPad changes

iCloud should have synced iPad's file edits by now. But let's be sure. We'll retry up to 3 times:

**Attempt 1:**
- Wait 5 seconds
- Check if files have changed since pull:
  ```bash
  MANIFEST_TIME=$(cat process/data_management/sync_manifest.json | grep created_at | cut -d'"' -f4)
  find . -type f -newermt "$MANIFEST_TIME" -not -path "./.git/*" -not -path "./_scratch/*" | wc -l
  ```
- If count > 0: files have been modified. Proceed to Phase 2.
- If count = 0: no files changed. Go to Attempt 2.

**Attempt 2:**
- Wait 10 seconds
- Repeat check
- If count > 0: proceed to Phase 2
- If count = 0: go to Attempt 3

**Attempt 3:**
- Wait 15 seconds
- Repeat check
- If count > 0: proceed to Phase 2
- If count = 0: go to Step 2

### Step 2: No files changed after 3 attempts

Output warning:

```
⚠ iCloud sync may be delayed

No file changes detected after 30 seconds. Options:
  (1) Retry waiting (another 15 seconds)
  (2) Ignore delay and continue sync anyway
  (3) Abort sync and try again later
```

Ask user: "(1/2/3)?"

If (1): Attempt 4 — wait 15s more, then proceed or loop back  
If (2): Continue to Phase 2 (vault may be unchanged, we'll flag it)  
If (3): End with "Sync aborted. Ensure iCloud is syncing and retry."

---

## PHASE 2: Detect iPad changes

### Step 3: Detect what changed on iPad

Read manifest to find the baseline commit:

```bash
BASELINE=$(cat process/data_management/sync_manifest.json | grep -A1 '"commit"' | head -2 | tail -1 | cut -d'"' -f4)
echo "Baseline commit: $BASELINE"
```

Now see what iPad changed:

```bash
git diff --name-only $BASELINE HEAD -- . | grep -v "^.git/" | grep -v "^_scratch/"
```

This gives us the list of files iPad edited. Call this `IPAD_FILES`.

If `IPAD_FILES` is empty:
  - **No changes detected.** Go to Step 4 (flag it).

If `IPAD_FILES` is not empty:
  - Show user: "iPad changes detected in: [list]"
  - Proceed to Step 5 (conflict check)

### Step 4: Flag missing iPad changes (if no changes detected)

Output warning:

```
⚠ No iPad changes detected

Expected files (from mobile_scope.md):
  - substance/
  - process/active/todos.md
  - process/active/voice_exceptions.md

But iCloud sync shows no changes. Options:
  (1) Debug: Show me what files have changed since pull (if any)
  (2) Proceed anyway (skip iPad sync, consider it a no-op)
  (3) Abort and retry later
```

Ask user: "(1/2/3)?"

If (1) — Debug:
  ```bash
  git diff --name-only $BASELINE HEAD
  find . -type f -newermt "$(date -d '30 minutes ago')" | head -20
  ```
  Show output. Ask again: "Proceed or abort? (proceed/abort)"

If (2) — Proceed:
  - Note: No changes to sync. Delete manifest and end.
  - Output: "No changes synced. Vault remains in current state."

If (3) — Abort:
  - End with: "Sync aborted. Check iPad edits and retry."

---

## PHASE 3: Detect Mac changes

### Step 5: Detect what changed on Mac since pull

Check if Mac made commits after the baseline:

```bash
git log $BASELINE..HEAD --oneline
```

If no output: Mac has NOT changed since pull. Go to Step 6 (no conflict possible).

If output: Mac HAS changed. Get the list of files:

```bash
git diff --name-only $BASELINE..HEAD
```

Call this `MAC_FILES`.

Show user: "Mac has [N] new commits; changed files: [list]"

### Step 6: Check for overlapping changes (conflict detection)

Find files changed by BOTH iPad and Mac:

```bash
# iPad files
IPAD_FILES=$(git diff --name-only $BASELINE HEAD -- .)

# Mac files  
MAC_FILES=$(git diff --name-only $BASELINE..HEAD)

# Intersection
comm -12 <(echo "$IPAD_FILES" | sort) <(echo "$MAC_FILES" | sort)
```

If intersection is empty:
  - **No conflict.** Go to Step 8 (merge).

If intersection is not empty:
  - **Conflict detected.** Go to Step 7 (create temp branch and defer).

---

## PHASE 4: Validate writable scope

### Step 7a: Check mobile_scope violations

For each file in `IPAD_FILES`, verify it's in the writable scope from `process/active/mobile_scope.md`:

```bash
WRITABLE=$(grep -A10 "## Writable" process/active/mobile_scope.md | grep "^-" | sed 's/^- //' | tr -d '/(.*)')
echo "Writable scope: $WRITABLE"

# Check each iPad file
VIOLATIONS=""
for file in $IPAD_FILES; do
  in_scope=false
  for pattern in $WRITABLE; do
    if [[ $file == $pattern* ]]; then
      in_scope=true
      break
    fi
  done
  if [ "$in_scope" = false ]; then
    VIOLATIONS="$VIOLATIONS\n  - $file"
  fi
done
```

If `VIOLATIONS` is empty:
  - All files are writable. Proceed.

If `VIOLATIONS` is not empty:
  - Output warning:
  ```
  ⚠ Scope violation detected
  
  These files were edited on iPad but are NOT in the writable scope:
  [list]
  
  Options:
    (1) Sync anyway (includes these files)
    (2) Reject sync (abort and fix scope or edits)
  ```
  
  Ask: "(1/2)?"
  
  If (1): Proceed (note violation in commit message)  
  If (2): End with "Sync rejected. Fix scope or edits and retry."

---

## PHASE 5: Merge or defer based on conflict

### Step 8: NO CONFLICT — Merge safely

If no conflict and no violations (or user allowed violations):

```bash
# Show what we're about to merge
git diff $BASELINE HEAD --stat

# Perform merge
git merge --no-ff HEAD -m "[writer] Sync iPad changes from $(date +'%Y-%m-%d %H:%M')"
```

If merge succeeds:
  - Delete manifest: `rm process/data_management/sync_manifest.json`
  - Output:
  ```
  ✓ Synced successfully
  
  iPad changes: [N] files modified
  Conflicts: None
  Committed: [commit-hash]
  
  Your iPad edits are now committed to Mac. Vault is in normal state.
  ```
  - End

If merge fails (unexpected error):
  - Output: "Merge error. Run `git status` to see state. May need manual resolution."
  - Don't delete manifest (manual recovery needed)

### Step 9: CONFLICT DETECTED — Defer to temp branch

If conflict detected:

```bash
# Create temp branch from current HEAD (iPad HEAD)
IPAD_COMMIT=$(git rev-parse HEAD)
SHORT_HASH=$(echo $IPAD_COMMIT | cut -c1-7)
TIMESTAMP=$(date +'%Y%m%dT%H%M%S')
BRANCH_NAME="sync/conflict-${TIMESTAMP}-${SHORT_HASH}"

git checkout -b $BRANCH_NAME
```

Collect conflict info:

```bash
MAC_COMMIT=$(git log $BASELINE..HEAD --oneline | head -1 | cut -d' ' -f1)
CONFLICTED_FILES=$(comm -12 <(echo "$IPAD_FILES" | sort) <(echo "$MAC_FILES" | sort))
```

Create conflict summary at `process/active/sync_conflict_${TIMESTAMP}.md`:

```markdown
# Sync Conflict — $(date +'%Y-%m-%d %H:%M')

**Detected:** $(date -u +'%Y-%m-%dT%H:%M:%SZ')
**Status:** Awaiting resolution on Mac
**Temp branch:** $BRANCH_NAME

## iPad state (when synced back)
**Commit:** $IPAD_COMMIT  
**Timestamp:** $(git log -1 --format=%ai HEAD)  
**Tag:** $(git describe --tags --exact-match HEAD 2>/dev/null || echo "none")

## Mac state (at sync-back time)
**Commit:** $BASELINE  
**New commits since pull:** $(git log $BASELINE..HEAD --oneline | wc -l)  

## Files modified by iPad
$(echo "$IPAD_FILES" | sed 's/^/- /')

## Files modified by Mac
$(echo "$MAC_FILES" | sed 's/^/- /')

## Conflicted files
$(for f in $CONFLICTED_FILES; do echo "- $f"; done)

## Resolution strategy
- [ ] iPad wins (keep iPad version, discard Mac)
- [ ] Mac wins (keep Mac version, discard iPad)
- [ ] Manual 3-way merge (use Beyond Compare)

## How to resolve
1. When ready: run sync-mobile:resolve-conflict
2. Choose your strategy above
3. Follow the merge tool UI
4. Commit and clean up

---
*Generated by sync-mobile:sync-back at $(date -u +'%Y-%m-%dT%H:%M:%SZ')*
```

Output to user:

```
⚠ Conflict detected

Files with conflicts: [list]
iPad changes: $BRANCH_NAME
Conflict summary: process/active/sync_conflict_${TIMESTAMP}.md

Changes are staged on temp branch. Return to Mac to resolve.
When ready: run sync-mobile:resolve-conflict
```

---

## Summary

| Case | Action |
|------|--------|
| No iPad changes | Flag + ask debug/proceed/abort |
| iPad changes, no Mac changes, no violations | Merge immediately, commit, delete manifest |
| iPad changes, no Mac changes, violations | Prompt: sync anyway or reject |
| iPad changes, Mac changes, no overlapping files, no violations | Merge immediately, commit, delete manifest |
| iPad changes, Mac changes, overlapping files | Create temp branch, generate conflict summary, defer |
| iCloud sync incomplete | Retry 3x, then warn and pause |

---

## Error handling

| Error | Resolution |
|-------|-----------|
| No manifest | "Run sync-mobile:pull first" |
| Git merge fails | "Merge error. Check git status. Manual recovery needed." |
| Conflict summary creation fails | Permission error; check process/active permissions |
| Manifest deletion fails | Warn user; manual cleanup needed |

---

## Output

Success (no conflict):
```
✓ Synced successfully
  iPad files: [N] modified
  Conflicts: None
  Committed at [time]
```

Conflict:
```
⚠ Conflict detected
  Temp branch: sync/conflict-20260523T143022-abc1def
  Conflicted files: [list]
  
Return to Mac and run sync-mobile:resolve-conflict
```

No changes:
```
⚠ No iPad changes detected
  Vault unchanged
```

