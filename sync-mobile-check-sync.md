---
name: sync-mobile:check-sync
description: From iPad, check if your vault is current (no changes on Mac since pull)
type: skill
role: any
---

# Check Sync Status

**Purpose:** Verify that vault is current; alert if Mac has changed since pull.

**Who runs this:** iPad user (via dispatch)  
**When:** Before syncing back, to anticipate conflicts  
**Output:** Status report (current vs behind)

---

## Instructions

This skill runs on Mac (triggered from iPad via dispatch). It checks if Mac has changed since you pulled.

### Step 1: Check for manifest

Look for sync manifest:

```bash
ls -la process/data_management/sync_manifest.json
```

If NOT found:
- Output: "No manifest found. Run sync-mobile:pull first."
- End

If found: continue

### Step 2: Read manifest

Parse `process/data_management/sync_manifest.json`:

```bash
cat process/data_management/sync_manifest.json
```

Extract:
- `mac_git_head.commit`: The commit that was pulled (e.g., `abc1def`)
- `created_at`: When it was pulled (e.g., `2026-05-23T14:30:22Z`)

### Step 3: Get current Mac git HEAD

Get the current commit on Mac:

```bash
CURRENT_COMMIT=$(git rev-parse HEAD)
echo "Current: $CURRENT_COMMIT"
```

### Step 4: Compare

If `CURRENT_COMMIT == manifest.commit`:
  - **CURRENT:** Vault unchanged on Mac since pull
  
If `CURRENT_COMMIT != manifest.commit`:
  - **BEHIND:** Mac has new commits since pull
  - Count commits: `git log manifest.commit..HEAD --oneline | wc -l`
  - Show the commits: `git log manifest.commit..HEAD --oneline`

### Step 5: Output status

**If CURRENT:**

```
✓ Your vault is current

Last pull: 2026-05-23 14:30
Mac state: unchanged since pull
  Commit pulled: abc1def
  Commit now: abc1def

Ready to sync changes on return. No conflicts expected.
```

**If BEHIND:**

```
⚠ Mac has changed since pull

3 new commits on Mac since 2026-05-23 14:30:

  xyz9abc - [writer] Edited chapter 2
  def1234 - [voice] Mechanical pass
  ghi5678 - [substance] Added notes

You may encounter conflicts when syncing back.
Tip: On return, review what changed before resolving conflicts.
```

---

## Error handling

| Error | Resolution |
|-------|-----------|
| No manifest | "Run sync-mobile:pull first" and end |
| Manifest corrupted | Error: "Manifest corrupted. Delete and re-pull." |
| Git command fails | Verify git repo is clean and accessible |

---

## Notes

- This is a **read-only check**. No files are modified.
- If vault is current: no action needed, ready to sync back anytime.
- If vault is behind: good information to have before resolving conflicts.

---

## Output

Current:
```
✓ Your vault is current
  No changes on Mac since pull
  Ready to sync
```

Behind:
```
⚠ Mac has 3 new commits since pull
  Review before syncing back
```

