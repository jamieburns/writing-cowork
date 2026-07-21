---
name: sync-mobile:verify-pull
description: Safety check — did you remember to pull the vault before leaving for iPad?
type: skill
role: any
---

# Verify Mobile Pull

**Purpose:** Check if vault was pulled for mobile sync; offer to pull if not.

**Who runs this:** Anyone, anytime (especially from iPad as safety check)  
**When:** Before relying on iPad edits, or as a reminder  
**Output:** Confirmation of pull status; optionally performs pull if missing

---

## Instructions

This is a quick sanity check to ensure the vault is ready for mobile sync. It takes 10 seconds.

### Step 1: Check for manifest

Look for the sync manifest:

```bash
ls -la process/data_management/sync_manifest.json
```

### Step 2a: If manifest EXISTS

Read it:

```bash
cat process/data_management/sync_manifest.json
```

Extract and show user:
- `created_at`: When the pull happened
- `ipad_session_id`: Unique session ID
- `mac_git_head.commit`: Commit that was pulled
- `mac_git_head.timestamp`: When that commit was made
- `writable_scope`: List of editable files

Output:

```
✓ Vault is ready for mobile

Last pull: 2026-05-23 14:30 (session: ipad-0523-x7k9m2)
Mac state: commit abc1def at 2026-05-23 14:30

Writable files on iPad:
  - substance/
  - process/active/todos.md
  - process/active/voice_exceptions.md

Status: Ready for iPad work. Changes will sync via iCloud.
```

End.

### Step 2b: If manifest DOES NOT exist

Output warning:

```
⚠ Vault not pulled

No sync manifest found. This means:
  - sync-mobile:pull has not been run, OR
  - Pull was run but manifest was deleted

Options:
  (1) Pull now before relying on iPad edits
  (2) Acknowledge the risk and continue anyway
  (3) Abort
```

Ask user: "(1/2/3)?"

If user chooses (1) — Pull now:
- Invoke sync-mobile:pull skill (full pull process)
- After pull completes: show "✓ Vault is now ready for mobile"

If user chooses (2) — Continue anyway:
- Warn: "⚠ iPad changes may not sync safely without a pull manifest."
- End with: "If this was unintentional, run sync-mobile:pull and try again."

If user chooses (3) — Abort:
- End with: "Aborted. Run sync-mobile:pull when ready."

---

## Error handling

| Error | Resolution |
|-------|-----------|
| manifest.json is corrupted/unreadable | Error: "Manifest corrupted. Delete it and run sync-mobile:pull again." |
| Permission denied reading manifest | Check vault permissions; try `chmod` |
| Manifest exists but is empty | Treat as "not pulled"; offer to re-pull |

---

## Output

Already pulled:
```
✓ Vault is ready for mobile
  Last pull: 2026-05-23 14:30
  Ready for iPad work
```

Not pulled, user chooses to pull:
```
No manifest found. Pulling now...
[runs sync-mobile:pull]
✓ Vault is now ready for mobile
```

Not pulled, user continues anyway:
```
⚠ Vault not pulled
  Changes on iPad may not sync safely
  Run sync-mobile:pull if this was unintentional
```

