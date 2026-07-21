---
name: sync-mobile:resolve-conflict
description: Resolve deferred conflicts from mobile sync — merge with Beyond Compare or choose strategy
type: skill
role: any
---

# Resolve Mobile Sync Conflict

**Purpose:** Guide user through resolving deferred mobile sync conflicts.

**Who runs this:** User on Mac, when sync_conflict_*.md exists  
**When:** After returning from iPad with conflict detected  
**Output:** Conflicts resolved, changes committed, vault in normal state

---

## Instructions

You have a deferred conflict from mobile sync. This skill guides you through resolution.

---

## PHASE 1: Load conflict summary

### Step 1: Find conflict summary file

List conflict summaries:

```bash
ls -la process/active/sync_conflict_*.md
```

If NO files found:
- Output: "No conflicts to resolve. Sync likely succeeded without conflict."
- End

If ONE file found:
- Read it
- Proceed to Step 2

If MULTIPLE files found:
- Ask user: "Multiple conflicts found. Resolve all now? (all/one-at-time)"
- If all: process each one, looping back for next
- If one-at-time: ask which one to resolve first

### Step 2: Parse conflict summary

Read the file (e.g., `process/active/sync_conflict_20260523T143022.md`):

```bash
cat process/active/sync_conflict_20260523T143022.md
```

Extract:
- `Temp branch:` → `$TEMP_BRANCH` (e.g., `sync/conflict-20260523T143022-abc1def`)
- `Conflicted files:` → `$CONFLICTED_FILES` (list)
- `Resolution strategy:` → check which box is ticked (if any)

Show user the summary:

```
Conflict Summary:
  Temp branch: $TEMP_BRANCH
  Conflicted files: [list from summary]
  
What was last edited:
  [show timestamps and commits from summary]
```

---

## PHASE 2: Choose resolution strategy

### Step 3: Ask for resolution strategy (if not already chosen)

Check conflict summary: is a resolution strategy already chosen (box ticked)?

If YES (user deferred with a choice):
- Use that choice (iPad wins / Mac wins / manual merge)
- Skip to Step 4

If NO (user needs to decide now):

```
Choose how to resolve conflicts:
  (1) iPad wins — Keep iPad versions, discard Mac changes
  (2) Mac wins — Keep Mac versions, discard iPad changes
  (3) Manual 3-way merge — Use Beyond Compare to resolve line-by-line
```

Ask: "(1/2/3)?"

---

## PHASE 3: Execute resolution

### Step 4a: iPad wins

For each conflicted file, keep iPad version:

```bash
git checkout --theirs [file] [file] [file]
```

Commit:

```bash
git commit -m "[writer] Resolve mobile sync conflict — iPad wins"
```

Output:

```
✓ Resolution: iPad wins
  Files updated: [list]
  Committed at [time]
```

### Step 4b: Mac wins

For each conflicted file, keep Mac version:

```bash
git checkout --ours [file] [file] [file]
```

Commit:

```bash
git commit -m "[writer] Resolve mobile sync conflict — Mac wins"
```

Output:

```
✓ Resolution: Mac wins
  Files updated: [list]
  Committed at [time]
```

### Step 4c: Manual 3-way merge

For each conflicted file, launch Beyond Compare:

```bash
git mergetool [file]
```

This will:
1. Open Beyond Compare
2. Show three panes: BASE (original), LOCAL (Mac), REMOTE (iPad)
3. You resolve conflicts in the UI
4. Save and close
5. Git stages the resolved file
6. Repeat for next conflicted file

After all files resolved:

```bash
git commit -m "[writer] Resolve mobile sync conflict — manual merge"
```

Output:

```
✓ Resolution: Manual 3-way merge
  Files resolved: [N]
  Committed at [time]
  
Tips for Beyond Compare:
  - Left pane (LOCAL): Mac version
  - Right pane (REMOTE): iPad version
  - Center pane (output): Your merged result
  - Use buttons to accept left/right/both or manually edit
```

---

## PHASE 4: Cleanup

### Step 5: Verify merge completed

Check git status:

```bash
git status
```

Should show:
```
On branch main
nothing to commit, working tree clean
```

If NOT clean:
- Output: "Merge incomplete. Unresolved files remain. Run `git status` to see."
- End (user needs to investigate)

If clean: proceed

### Step 6: Delete conflict summary and temp branch

Delete conflict summary:

```bash
rm process/active/sync_conflict_20260523T143022.md
```

Delete temp branch:

```bash
git branch -d sync/conflict-20260523T143022-abc1def
```

(If branch has unmerged commits, git will prevent deletion as safety measure.)

Output:

```
✓ Conflict resolved and cleaned up

Conflict summary: deleted
Temp branch: deleted
Vault: normal state

Ready for next sync or other operations.
```

### Step 7: If multiple conflicts, loop back

If user chose "one-at-time" earlier:
- Check for remaining sync_conflict_*.md files
- If more exist: ask "Resolve next conflict? (yes/no)"
- If yes: go back to Step 1 for next file

---

## Error handling

| Error | Resolution |
|-------|-----------|
| No conflict summary found | "No conflicts. Sync likely succeeded." |
| Multiple conflicts, user chose one-at-a-time | Loop after each resolution |
| Beyond Compare not found | "Beyond Compare not configured. Run sync-mobile:setup." |
| Merge tool fails | "Merge tool error. Retry or resolve manually with git." |
| Branch deletion fails | "Branch has unmerged content. Check git status." |
| Temp branch not found | "Branch may have been deleted manually. Check git branch -a." |
| Conflict summary deletion fails | Permission error; try manual deletion |

---

## Important notes

- **Git mergetool is safe.** If you change your mind during merge, close Beyond Compare without saving. Git will keep the conflict markers.
- **Each file can have different strategy.** You can use iPad wins for some files and manual merge for others.
- **After commit:** Vault is back in normal state. No special post-sync behavior.
- **Next sync:** Run sync-mobile:pull → work on iPad → sync-mobile:sync-back again.

---

## Output

iPad wins:
```
✓ Conflict resolved — iPad wins
  substance/chapter-3.md: updated
  process/active/todos.md: updated
  Committed
  
Vault ready for normal operations
```

Mac wins:
```
✓ Conflict resolved — Mac wins
  substance/chapter-3.md: updated
  process/active/todos.md: updated
  Committed
```

Manual merge:
```
✓ Conflicts resolved — manual merge
  substance/chapter-3.md: merged via Beyond Compare
  process/active/todos.md: merged via Beyond Compare
  Committed
  
All conflicts resolved. Vault is clean.
```

