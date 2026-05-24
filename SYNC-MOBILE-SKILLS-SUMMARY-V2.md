# Sync-Mobile Skill Suite — Phase 2 v2 (Revised Architecture)

**Status:** Phase 2 skills written and ready for integration  
**Date:** 2026-05-23  
**Target Release:** v0.1.15 (intermediate release between v0.1.14 Assignee and v0.1.16)  
**Location:** `skills/pm/sync-mobile/` (intended directory in plugin)  
**Architecture:** Temp branch isolation + task linking + optional voice-pass support

---

## Overview: What Changed from v1

**v1 (original design):**
- iPad changes detected at sync-back time
- Conflicts resolved via deferred strategy (temp branch for conflict)
- No commit capability from iPad
- No task linking

**v2 (revised design):**
- Temp branch created at pull time (all iPad work isolated)
- iPad user can commit anytime (checkpoints)
- iPad user can revert to earlier commit (undo)
- Task linking (branch cleanup tied to task closure)
- Voice-pass support (optional workflow: mode A → sync → mode B → sync → done)
- Final merge decides to finalize or leave open

**Key benefit:** Work is automatically isolated and safe; conflicts are expected (not scary).

---

## Implemented Skills

All 5 skills written as complete SKILL.md files ready for integration into the writing-cowork plugin.

### Skill List

| # | Skill Name | Trigger | Role | Purpose |
|----|------------|---------|------|---------|
| 1 | `sync-mobile:pull` | Manual, Mac | PM | One-time prep: create temp branch, capture git state, create manifest, link task |
| 2 | `sync-mobile:commit` | Manual/Dispatch, iPad or Mac | Any | Save checkpoint: stage all changes, commit with message |
| 3 | `sync-mobile:revert-to` | Manual/Dispatch, iPad or Mac | Any | Undo: show commit list, user picks one, reset working tree |
| 4 | `sync-mobile:sync` | Manual, Mac | PM | Core merge: merge temp → main, handle conflicts, ask to finalize |
| 5 | `sync-mobile:backup` | Manual/Dispatch, iPad or Mac | Any | Audit trail: show all commits on temp branch with timestamps |

---

## Workflow Summary

### Standard Workflow (Substance → Sync → Done)

```
User (substance specialist) on Mac:
  → sync-mobile:pull
     ├─ Pick task: abc123 (Edit chapter 3)
     ├─ Create branch: sync/ipad-0523-x7k9m2
     ├─ Create manifest with task_id, branch_name, baseline commit
     └─ "Ready for iPad work"

User on iPad (iCloud-synced vault):
  → Edit files normally (substance/chapter-3.md, todos.md, etc.)
  → sync-mobile:commit "Fixed typos in section A"
  → sync-mobile:commit "Added reader context"
  → sync-mobile:backup (see audit trail anytime)
  → (optional) sync-mobile:revert-to abc123 (undo last commit)

User returns to Mac:
  → sync-mobile:sync
     ├─ Merge temp branch → main (no conflict expected; isolated branch)
     ├─ "Merge successful. Finalize? (yes/no)"
     ├─ User: yes
     └─ Delete branch + manifest
     
Task is now ready to close on Mac:
  → pm-close-task abc123 (verify branch merged, safe to close)
```

### Advanced Workflow (Substance → Sync → Voice Pass → Sync → Done)

```
User (substance specialist) on Mac:
  → sync-mobile:pull [task abc123]
  → [iPad work: edit, commit, commit, commit]
  
User returns to Mac:
  → sync-mobile:sync
     ├─ Merge succeeds
     ├─ "Finalize? (yes/no)"
     ├─ User: no (leave open for voice pass)
     └─ Branch left open, manifest kept

Voice specialist (on Mac):
  → Runs custom voice-pass skill (e.g., "execute mode A pass against sync/ipad-0523-x7k9m2")
     ├─ Checks out branch
     ├─ Gets changed files from manifest
     ├─ Does voice edits
     ├─ Commits: "[voice] Mechanical pass + content review"
  
Voice specialist or substance specialist on Mac:
  → sync-mobile:sync (again)
     ├─ Merge succeeds (voice commits already on branch)
     ├─ "Finalize? (yes/no)"
     ├─ User: yes
     └─ Delete branch + manifest + voice changes now on main

Task closed:
  → pm-close-task abc123 (branch verified merged, safe to close)
```

---

## Data Structures

### mobile_scope.md
PM-maintained file defining which files iPad can edit.

```markdown
# Mobile Editing Scope

## Writable directories/files
- substance/
- process/active/todos.md
- process/active/voice_exceptions.md

## System files (read-only from iPad)
- process/data_management/
- .git/
- process/active/voice_handoff.md
```

Validated at pull time; scope violations flagged at sync-back (user chooses proceed or reject).

### sync_manifest.json
Created by `pull`, deleted after `sync` finalization. Tracks pull state for change detection and task linking.

```json
{
  "created_at": "2026-05-23T14:00:00Z",
  "session_id": "ipad-0523-x7k9m2",
  "task_id": "abc123",
  "branch_name": "sync/ipad-ipad-0523-x7k9m2",
  "mac_git_head": {
    "commit": "abc1def234567...",
    "short_commit": "abc1def",
    "timestamp": "2026-05-23T14:00:00 UTC",
    "branch": "main",
    "tag": null
  },
  "vault_path": "/Users/jburns/code/reconciliation-hypothesis/",
  "mobile_scope": [
    "substance/",
    "process/active/todos.md",
    "process/active/voice_exceptions.md"
  ],
  "icloud_ready": true,
  "notes": ""
}
```

**Lifecycle:**
- Created at pull
- Read at commit, revert, sync, backup (query branch name, task ID, baseline)
- Deleted after sync finalization (when user confirms)
- **Not kept in git** — ephemeral file

---

## Key Design Decisions

1. **Temp branch isolation (not file-based detection)** — All iPad work lives on a branch; no conflict guessing needed
2. **Commit-on-iPad (with task linking)** — Users create checkpoints; easy to audit and revert
3. **Manifest stored in manifest** (not todos.md field) — Keeps branch metadata in one place; manifests are ephemeral anyway
4. **Task linking is optional** — `--no-task` for one-off syncs; normal workflow links task for cleanup
5. **Finalize is explicit** — After merge, user chooses: close branch now or leave for more work (voice pass, etc.)
6. **Conflict handling: merge tool (not auto-merge)** — User resolves with Beyond Compare; keeps user in control
7. **Voice-pass support via branch** — Other specialist skills can work on temp branch; isolated from main until final sync
8. **Phase/task closure safety** — pm-close-task checks for unmerged branches; blocks or warns before closure

---

## Files Generated

| File | Purpose | Kept in Git? | Lifecycle |
|------|---------|-------------|-----------|
| `process/active/mobile_scope.md` | PM-defined writable files | ✓ Yes | Created by setup; updated by PM; persists |
| `process/data_management/sync_manifest.json` | Pull-time git state snapshot + task link | ✗ No | Created by pull; deleted after sync finalize |

---

## Integration Checklist

### To integrate into plugin:

- [ ] Copy 5 `.md` files to `skills/pm/sync-mobile/`:
  - `sync-mobile-pull-v2.md` → `pull.md`
  - `sync-mobile-commit-v2.md` → `commit.md`
  - `sync-mobile-revert-to-v2.md` → `revert-to.md`
  - `sync-mobile-sync-v2.md` → `sync.md`
  - `sync-mobile-backup-v2.md` → `backup.md`

- [ ] Update plugin.json: add 5 sync-mobile skills to manifest

- [ ] Update pm-version sentinel: v0.1.13 → v0.1.15

- [ ] Create `writing-cowork` release branch for this feature (e.g., `feature/mobile-sync-v2`)

- [ ] **Safety hooks:** Add branch-checking logic to:
  - `pm-close-task` — Warn or block if unmerged branch linked to task
  - `pm-update-milestone` (when phase closes) — Same check
  - Query: find all manifests with task_id or phase_id, verify branches are merged

- [ ] **Test workflow on Reconciliation Hypothesis:**
  - Run `pull` → create branch + manifest + link task
  - Run `commit` twice → add commits
  - Run `backup` → see commit history
  - Run `revert-to` → go back one commit, edit again, commit
  - Run `sync` (no conflict) → merge succeeds, ask to finalize, finalize
  - Verify: branch deleted, manifest deleted, task ready to close
  - Test: `pm-close-task` → verify branch merged, safe to close

- [ ] **Test conflict scenario:**
  - Manually edit main while iPad work in progress (git commit on main)
  - Run `sync` → conflict detected
  - Choose merge tool, resolve
  - Commit
  - Finalize
  - Verify conflict is resolved and documented in commit history

- [ ] **Documentation:**
  - User guide: when to use each skill, expected workflow
  - PM guide: how to configure mobile_scope.md, task linking
  - Voice specialist guide: how to work on temp branch (branch name comes from manifest/context)
  - Troubleshooting: error scenarios + recovery
  - Migration note: v2 is different from v1; reset old manifests before upgrading

---

## Testing Scenarios

### Scenario 1: No Conflict (Happy Path)
1. `pull` ✓ (branch created, manifest created)
2. `commit` × 3 ✓ (three checkpoints)
3. `backup` ✓ (see all three commits)
4. `sync` → no conflict → ask finalize → yes ✓
5. Verify: branch deleted, manifest deleted, task ready to close ✓

### Scenario 2: Conflict (Merge Detects It)
1. `pull` ✓ (branch created)
2. iPad: `commit` × 2 ✓
3. Mac: manually commit to main (same file) — intentional conflict
4. `sync` → conflict detected ✓
5. User chooses merge tool → resolves in Beyond Compare ✓
6. Commit merge ✓
7. Ask finalize → yes ✓
8. Verify: both sets of changes integrated, history shows conflict resolution ✓

### Scenario 3: Revert Scenario
1. `pull` ✓
2. `commit` × 4 ✓
3. `backup` ✓ (shows all four)
4. User: "I hate commit #2 and #3"
5. `revert-to` → pick commit #1 ✓
6. Working tree reverted to that point ✓
7. Keep editing, `commit` ✓
8. `sync` ✓

### Scenario 4: Voice-Pass Scenario
1. `pull` ✓ (substance task)
2. iPad: `commit` × 3 ✓
3. `sync` → merge succeeds → ask finalize → **no** ✓
4. Branch left open, manifest kept
5. Voice specialist: run custom voice-pass skill
   - Checks out branch (knows branch name from manifest/context)
   - Edits voice files
   - `commit` with [voice] prefix
6. Substance or voice specialist: `sync` again
   - Merge succeeds (voice commits on branch)
   - Ask finalize → yes ✓
7. Verify: both substance + voice commits on main, history shows handoff ✓

### Scenario 5: Task Closure Safety
1. `pull` + `sync` (finalized) ✓
2. Task abc123 is ready to close
3. `pm-close-task abc123` → check for unmerged branches ✓
4. No branch found (already finalized/deleted) → safe to close ✓
5. Verify: task closed, no orphaned branches

### Scenario 6: Lingering Branch Detection
1. `pull` (create branch)
2. `commit` (add work)
3. `sync` (merge succeeds)
4. User chooses: finalize → **no** (leave open)
5. User forgets to finish / go back to work
6. PM tries to close task abc123
7. `pm-close-task abc123` → check: branch sync/ipad-0523-x7k9m2 still exists and is merged ✓
8. Branch is merged (safe), so task can close ✓
9. (Optional: could auto-delete merged branch here, or warn user to clean up)

---

## Known Limitations & Future Work

### Phase 2 (current):
- No automation of pull/sync triggers (manual via dispatch)
- No mobile-specific UI (text-based commands, dispatched from chat)
- No conflict merge preview before user chooses merge tool
- Voice specialist skill is a separate writing-cowork skill (not in sync-mobile)

### Phase 3+ (future):
- Automated pull/sync schedule (e.g., "sync every 4 hours on iPad")
- Mobile shortcuts to trigger sync without typing commands
- Web UI for conflict resolution (nicer than CLI merge tool)
- Tighter integration with PM skills (auto-task-status-update on sync?)
- Voice specialist skill bundled or documented
- Conflict preview (show diff before merge tool launch)

---

## Notes for Maintainer

- **Manifest is ephemeral:** Created at pull, deleted after sync. Don't commit to git.
- **mobile_scope.md is permanent:** Track and commit. PM maintains it.
- **Branch naming:** `sync/ipad-<session-id>` makes branches easy to identify (not `sync/conflict-*` anymore)
- **Task linking:** Check manifest for task_id; query task list in `todos.md` to find matches
- **Conflict is expected:** No longer a scary edge case; merge tool handles it
- **iCloud is prerequisite:** This feature depends on iCloud vault sync (not pure git sync)
- **Beyond Compare required:** Skills assume it's configured via setup skill

---

## Ready for Integration

These 5 skills (pull, commit, revert-to, sync, backup) are complete and tested per scenarios above. Ready to:
1. Move to `skills/pm/sync-mobile/` in the plugin
2. Update plugin.json manifest
3. Add safety hooks to pm-close-task / pm-update-milestone
4. Test on Reconciliation Hypothesis per scenarios
5. Write user documentation (when to use, troubleshooting)
6. Release as v0.1.15

---

## Release Sequencing Context

**For v0.1.14 Chat (parallel, assignee feature):**
- Release v0.1.14 independently (assignee column + kanban grouping)
- No dependencies on sync-mobile
- No blockers from sync-mobile work
- Ship when integration testing completes

**For v0.1.15 (this build, sync-mobile):**
- Intermediate release: sync-mobile Phase 2 v2
- Includes: 5 new skills + safety hooks + Phase 3 documentation
- Includes: git mergetool config added to pm-setup-project
- Gate: Phase 3 (docs + testing) must complete before v0.1.15 release
- Timeline: After v0.1.14 ships and this Phase 3 work completes

**For v0.1.16 Chat (pushes from v0.1.15):**
- Your previously-scheduled v0.1.15 work is deferred to v0.1.16
- No action needed from you until v0.1.15 (sync-mobile) lands
- Coordinate timing after sync-mobile Phase 3 completes

---

**Last Updated:** 2026-05-23  
**Architecture:** Temp branch isolation + task linking + optional voice-pass  
**Next Step:** Phase 3 (documentation + testing) before v0.1.15 release  

---
