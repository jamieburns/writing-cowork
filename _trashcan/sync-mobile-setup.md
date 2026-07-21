---
name: sync-mobile:setup
description: Initialize mobile sync capability — configure mobile_scope.md and Beyond Compare mergetool
type: skill
role: pm
---

# Setup Mobile Sync

**Purpose:** One-time initialization of mobile sync for this project.

**Who runs this:** PM role, or user before first mobile sync  
**Prerequisites:** Project vault exists, git repo initialized  
**Output:** mobile_scope.md configured, Beyond Compare registered as git mergetool

---

## Instructions

You're setting up mobile sync for this project. This is a one-time operation that:
1. Creates a writable-files manifest (mobile_scope.md)
2. Configures Beyond Compare as the merge tool for conflicts
3. Verifies git is ready for mobile workflow

### Step 1: Check existing mobile scope

Read the project: `process/active/mobile_scope.md`

If it exists and is NOT empty:
- Ask user: "Mobile scope already configured. Overwrite with fresh template? (yes/no)"
- If no: show current scope and end
- If yes: continue

### Step 2: Create mobile_scope.md

Create file at `process/active/mobile_scope.md` with this template:

```markdown
# Mobile Editing Scope

**Last updated:** [TODAY'S DATE]
**Managed by:** PM role

## Writable directories/files
- ./substance/ (all files)
- ./process/active/todos.md
- ./process/active/voice_exceptions.md
- ./process/active/voice_handoff.md (voice role only)

## Read-only (sync receives but iPad cannot edit)
- ./process/data_management/ (ownership, hierarchy, drift config)
- ./process/active/reader_tracking.md
- .git/
- _scratch/
- Any file not listed above

## Notes
- **Rationale:** Prevent accidental edits to system files during offline iPad work
- **Edit this list:** When adding new content directories that should be writable on iPad
- **Don't include:** Anything in process/data_management or .git

---
*Initialized by sync-mobile:setup on [DATE]*
```

Save it. Show user what's been created.

### Step 3: Prompt for customization

Ask user: "Would you like to customize the writable scope now, or keep the default?"
- If customize: have user edit the file manually, then continue
- If keep default: continue

### Step 4: Verify Beyond Compare installation

Check if Beyond Compare is installed on this Mac:

```bash
which bcomp
# or
which bcompare
```

If found:
- Continue to Step 5
- Note the path (typically `/usr/local/bin/bcomp` or `/Applications/Beyond Compare.app/Contents/MacOS/bcomp`)

If NOT found:
- Inform user: "Beyond Compare not installed. Download from: https://www.scootersoftware.com/download.php"
- Provide macOS download link
- Ask: "Install now or continue without it? (install-link/continue)"
- If continue without: warn "Merge conflicts will need manual resolution without Beyond Compare"

### Step 5: Configure git mergetool

Configure git to use Beyond Compare for merge conflicts:

```bash
cd /Users/jburns/code/writing-cowork  # or the actual vault path
git config merge.tool bcompare
git config mergetool.bcompare.cmd 'bcomp "$BASE" "$LOCAL" "$REMOTE" "$MERGED"'
```

Verify the configuration:

```bash
git config merge.tool
# Should output: bcompare
```

If this succeeds: continue  
If this fails (permission or path issue): show user the commands and suggest they run manually

### Step 6: Create template manifest (reference only)

Create `process/data_management/sync_manifest.json.template` to show the user what a manifest looks like:

```json
{
  "created_at": "2026-05-23T14:30:22Z",
  "ipad_session_id": "ipad-0523-abc123",
  "mac_git_head": {
    "commit": "abc1def1234567890abcdef1234567890abcdef",
    "timestamp": "2026-05-23T14:30:00+0000",
    "tag": null,
    "branch": "main"
  },
  "writable_scope": [
    "substance/",
    "process/active/todos.md",
    "process/active/voice_exceptions.md"
  ],
  "vault_path": "/Users/jburns/Library/Mobile Documents/iCloud~md~obsidian/Documents/ReconciliationHypothesis",
  "notes": ""
}
```

Note: This is a template. The actual manifest is created by `sync-mobile:pull` when user is ready to sync.

### Step 7: Summary and next steps

Output:

```
✓ Setup complete

Files created:
  - process/active/mobile_scope.md (edit this to customize writable scope)
  - process/data_management/sync_manifest.json.template (reference only)

Merge tool:
  - Beyond Compare configured as git mergetool
  
Next steps:
  1. Review mobile_scope.md and customize if needed
  2. When ready to work on iPad: run sync-mobile:pull
  3. After returning from iPad: run sync-mobile:sync-back
```

---

## Error handling

| Error | Resolution |
|-------|-----------|
| mobile_scope.md exists and won't overwrite | Ask user if they want to reset; if no, show current scope and end |
| Beyond Compare not found | Provide download link; offer to continue without it |
| Git config fails | Show the commands; suggest user run them manually |
| Permission denied on file creation | Suggest `chmod` or check vault write permissions |

---

## Output

Success:
```
✓ Setup complete
  Mobile scope: process/active/mobile_scope.md
  Merge tool: Beyond Compare configured
  Ready to pull and sync
```

If no customization: same output  
If deferred (user wants to edit scope later): note "You can edit mobile_scope.md anytime before pulling"

