---
name: sync-mobile:pull
description: Capture vault state before iPad sync — create temp branch, manifest, and prepare for offline work
type: skill
role: pm
---

# Pull Vault for Mobile Sync

**Purpose:** Prepare vault for iPad work by creating an isolated temp branch and capturing git state.

**Who runs this:** PM or specialist on Mac, before leaving with iPad  
**When:** Before taking iPad to work offline  
**Output:** Temp branch created, manifest saved, vault ready for mobile editing  
**Prerequisite:** `sync-mobile:setup` must have run once (creates mobile_scope.md)

---

## Instructions

---

## PHASE 1: Task Selection

### Step 1: Ask user to pick a task

Query open tasks from `process/active/todos.md`:

```bash
grep "^| " process/active/todos.md | grep -v "status:completed" | head -20
```

Display to user:
```
Which task are you syncing for?

  (1) abc123 - Edit chapter 3 (substance)
  (2) def456 - Review voice edits (voice)
  (3) ghi789 - Fix typos (writer)
  (4) Skip task linking (use --no-task if recurring)

Choose: (1/2/3/4)?
```

**If user picks 1-3:**
- Extract task ID from selection (e.g., `abc123`)
- Store as `$TASK_ID`
- Proceed to Phase 2

**If user picks 4 (or ran with `--no-task`):**
- Set `$TASK_ID = "none"`
- Proceed to Phase 2
- (Branch won't be linked to task; cleanup will be manual)

---

## PHASE 2: Git State Verification

### Step 2: Verify git is clean

```bash
git status
```

**If working tree is clean:**
  - Proceed to Step 3

**If working tree is dirty** (modified files, staged changes):
  ```
  ⚠ Uncommitted changes detected
  
  Modified files:
  [list from git status]
  
  Options:
    (1) Commit changes now
    (2) Stash changes (temporary hide, recover later)
    (3) Abort pull (fix it manually, then retry)
  ```
  
  Ask: "(1/2/3)?"
  
  - If (1): Prompt for commit message, then `git commit -m "<msg>"`
  - If (2): `git stash` (saves changes, reverts working tree)
  - If (3): End with "Abort pull. Fix uncommitted changes, then retry."

### Step 3: Get current git state

Capture the baseline (before iPad work):

```bash
CURRENT_COMMIT=$(git rev-parse HEAD)
COMMIT_TIME=$(git log -1 --format=%ai HEAD)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
TAG=$(git describe --tags --exact-match HEAD 2>/dev/null || echo "none")
```

Show user:
```
Current vault state:
  Commit: $CURRENT_COMMIT (short: ${CURRENT_COMMIT:0:7})
  Time: $COMMIT_TIME
  Branch: $BRANCH
  Tag: $TAG
```

---

## PHASE 3: Create Temp Branch

### Step 4: Create session ID and temp branch

Generate session ID (iPad-friendly format):

```bash
SESSION_ID="ipad-$(date +%m%d)-$(openssl rand -hex 3)"
# Example: ipad-0523-a7k9m2

TIMESTAMP=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
BRANCH_NAME="sync/ipad-${SESSION_ID}"
```

Create and checkout temp branch:

```bash
git checkout -b $BRANCH_NAME
echo "✓ Created branch: $BRANCH_NAME"
```

---

## PHASE 4: Create Manifest

### Step 5: Build manifest with all metadata

Create `process/data_management/sync_manifest.json`:

```json
{
  "created_at": "$TIMESTAMP",
  "session_id": "$SESSION_ID",
  "task_id": "$TASK_ID",
  "branch_name": "$BRANCH_NAME",
  "mac_git_head": {
    "commit": "$CURRENT_COMMIT",
    "short_commit": "${CURRENT_COMMIT:0:7}",
    "timestamp": "$COMMIT_TIME",
    "branch": "$BRANCH",
    "tag": "$TAG"
  },
  "vault_path": "$(pwd)",
  "mobile_scope": [
    "$(grep -A20 '## Writable' process/active/mobile_scope.md | grep '^-' | sed 's/^- //' | tr '\n' ',' | sed 's/,$//')"
  ],
  "icloud_ready": true,
  "notes": ""
}
```

Verify manifest is valid:

```bash
cat process/data_management/sync_manifest.json | python3 -c "import sys, json; json.load(sys.stdin); print('✓ Manifest valid')"
```

---

## PHASE 5: Final Verification

### Step 6: Check iCloud is accessible

Verify iCloud vault directory is mounted and writable:

```bash
test -w "$(pwd)" && echo "✓ iCloud directory writable" || echo "⚠ iCloud not ready"
```

If not writable:
```
⚠ iCloud not accessible or not writable

This usually means:
  - iCloud sync is paused
  - Vault is not in iCloud Drive
  - Permissions issue

Fix iCloud, then retry pull.
```

### Step 7: Summary and next steps

Output completion message:

```
✓ Vault pulled and ready for iPad

Session ID: $SESSION_ID
Task linked: $TASK_ID
Temp branch: $BRANCH_NAME
Baseline commit: ${CURRENT_COMMIT:0:7} at $COMMIT_TIME

Writable scope (on iPad):
$(grep -A20 '## Writable' process/active/mobile_scope.md | grep '^-')

Next:
  1. Take iPad to work location
  2. Open Obsidian vault (same iCloud folder)
  3. Edit files normally (changes sync via iCloud)
  4. Commit edits as needed: sync-mobile:commit "<message>"
  5. Return to Mac and run: sync-mobile:sync

Branch status:
  Manifest: process/data_management/sync_manifest.json
  Temp branch: $BRANCH_NAME (isolated, not on main)
  
If you need to check sync status from iPad:
  sync-mobile:check-sync (see if Mac changed while you worked)
```

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| mobile_scope.md not found | Run sync-mobile:setup first |
| Git not clean (dirty working tree) | Commit or stash changes, retry |
| iCloud not accessible | Fix iCloud sync, retry |
| Manifest creation fails | Check file permissions in process/data_management/ |
| Branch creation fails | Verify branch name not already in use; check git |
| Commit time capture fails | Git may not be configured; check `git config --list` |

---

## Important Notes

- **Manifest is ephemeral** — Created now, deleted after sync-mobile:sync
- **Temp branch is isolated** — All iPad edits go here, main branch untouched
- **Task linking optional** — Use --no-task to skip; cleanup then requires manual branch management
- **iCloud sync prerequisite** — This feature depends on iCloud file sync; won't work with pure git sync
- **Session ID in branch name** — Helps correlate pull/sync cycles and identify specific iPad sessions
- **mobile_scope.md is enforced** — Only files listed there can be edited on iPad; violations flagged at sync-back

---

## Output Examples

### Success (task linked)

```
✓ Vault pulled and ready for iPad

Session ID: ipad-0523-x7k9m2
Task linked: abc123 (Edit chapter 3)
Temp branch: sync/ipad-ipad-0523-x7k9m2
Baseline commit: abc1def at 2026-05-23 14:30

Writable scope (on iPad):
  - substance/
  - process/active/todos.md
  - process/active/voice_exceptions.md

Next:
  1. Take iPad, open vault in Obsidian
  2. Edit files normally
  3. Commit: sync-mobile:commit "Finished chapter 3"
  4. Return to Mac: sync-mobile:sync
```

### Success (no task)

```
✓ Vault pulled and ready for iPad

Session ID: ipad-0523-y8m1p3
Task linked: none (manual cleanup needed)
Temp branch: sync/ipad-ipad-0523-y8m1p3
Baseline commit: def2abc at 2026-05-23 14:30

[Same instructions, but note task cleanup will be manual]
```

### Error: Git dirty

```
⚠ Uncommitted changes detected

Modified files:
  substance/chapter-3.md (modified)
  process/active/todos.md (modified)

Options:
  (1) Commit changes now
  (2) Stash changes
  (3) Abort pull

Choose: (1/2/3)?
```

---

