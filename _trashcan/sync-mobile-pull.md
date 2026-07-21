---
name: sync-mobile:pull
description: Create sync manifest and prepare vault for iPad sync before leaving Mac
type: skill
role: pm
---

# Pull Vault for Mobile

**Purpose:** Capture current git state and prepare vault for iPad sync.

**Who runs this:** User (any role) before leaving Mac with iPad  
**When:** Right before taking iPad to work offline  
**Output:** sync_manifest.json created; vault ready for mobile sync via iCloud

---

## Instructions

You're about to leave Mac for iPad work. This skill captures the current state of the vault so we can safely sync changes back later.

### Step 1: Verify setup

Check if `process/active/mobile_scope.md` exists:

```bash
ls -la process/active/mobile_scope.md
```

If NOT found:
- Output: "Mobile scope not configured. Run sync-mobile:setup first."
- End here

If found: continue

### Step 2: Check git is clean

Verify no uncommitted changes:

```bash
git status --porcelain
```

If there are changes (anything in output):
- List the uncommitted changes
- Ask user: "Uncommitted changes exist. Before pulling for mobile:
  - Commit these changes? (yes)
  - Stash them? (stash)
  - Abort pull? (abort)"
  
If yes: User commits (guide them with: `git commit -m "[writer] Pre-mobile-sync commit"`)  
If stash: `git stash`  
If abort: End here with "Pull aborted. Address changes and retry."

After handling: re-run `git status --porcelain` to verify clean

### Step 3: Capture git HEAD state

Get current git information:

```bash
# Current commit hash (full)
COMMIT=$(git rev-parse HEAD)
echo "Commit: $COMMIT"

# Commit timestamp (ISO 8601)
TIMESTAMP=$(git log -1 --format=%ai HEAD)
echo "Timestamp: $TIMESTAMP"

# Current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Branch: $BRANCH"

# Tag (if any; suppress error if none)
TAG=$(git describe --tags --exact-match HEAD 2>/dev/null || echo "")
echo "Tag: $TAG"
```

Show user what you've captured.

### Step 4: Read mobile scope

Read `process/active/mobile_scope.md`:

Extract the "Writable directories/files" section. Parse it into a JSON array:

```json
[
  "substance/",
  "process/active/todos.md",
  "process/active/voice_exceptions.md",
  "process/active/voice_handoff.md"
]
```

Show this to user: "Writable files on iPad: [list]"

### Step 5: Create sync manifest

Create file: `process/data_management/sync_manifest.json`

Contents (use values from Steps 3-4):

```json
{
  "created_at": "[ISO 8601 current timestamp, e.g., 2026-05-23T14:30:22Z]",
  "ipad_session_id": "ipad-[MMDD]-[random 6-char alphanumeric]",
  "mac_git_head": {
    "commit": "[COMMIT from Step 3]",
    "timestamp": "[TIMESTAMP from Step 3]",
    "tag": "[TAG from Step 3, or null]",
    "branch": "[BRANCH from Step 3]"
  },
  "writable_scope": [array from Step 4],
  "vault_path": "[user's vault path, e.g., /Users/jburns/Library/Mobile Documents/iCloud~md~obsidian/Documents/ReconciliationHypothesis]",
  "notes": ""
}
```

Note: `ipad_session_id` should be auto-generated as `ipad-MMDD-` followed by 6 random alphanumeric characters (e.g., `ipad-0523-x7k9m2`)

Verify file was created:

```bash
cat process/data_management/sync_manifest.json
```

### Step 6: Prompt for optional notes

Ask user: "Add notes to the manifest? (e.g., 'editing chapters 3-4', 'voice pass', etc.) Leave blank to skip."

If user provides notes: edit the `notes` field in sync_manifest.json  
If blank: leave `notes: ""`

### Step 7: Show summary and next steps

Output:

```
✓ Vault pulled and ready for mobile

Manifest created: process/data_management/sync_manifest.json
  Session: [ipad_session_id]
  Mac state: commit [short commit hash] at [timestamp]
  Branch: [branch]
  Tag: [tag or none]
  Writable files: [list]

Ready to work on iPad. Changes will sync automatically via iCloud.

When returning to Mac:
  → Run sync-mobile:sync-back to commit your changes
```

---

## Error handling

| Error | Resolution |
|-------|-----------|
| mobile_scope.md not found | "Run sync-mobile:setup first" and end |
| Git has uncommitted changes | Prompt: commit/stash/abort |
| manifest.json creation fails | Permission error on process/data_management/; check folder permissions |
| Git commands fail | Verify git repo is initialized; check for repo corruption |

---

## Important notes

- **No git commits are made by this skill.** It only captures state and creates the manifest.
- **Vault files are NOT modified.** Only sync_manifest.json is created.
- **Session ID is auto-generated** to track this pull/sync cycle. Keep it for reference.
- **On return:** Do NOT manually edit manifest. Run sync-mobile:sync-back; it will delete manifest after syncing.

---

## Output

Success:
```
✓ Vault pulled and ready for mobile
  Session: ipad-0523-x7k9m2
  Mac state: abc1def at 2026-05-23 14:30
  Writable files: [list]
  
Take your iPad. See you when you return.
```

With notes:
```
✓ Vault pulled and ready for mobile
  Session: ipad-0523-x7k9m2
  Notes: editing chapters 3-4, voice pass
```

