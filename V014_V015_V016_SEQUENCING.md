# Release Sequencing: v0.1.14 → v0.1.15 → v0.1.16

**Date:** 2026-05-23  
**Status:** Coordination note for parallel development chats

---

## Release Plan

### v0.1.14 (Current, Ship Now)

**Features:**
- Assignee column (role-based task ownership)
- Multi-mode kanban grouping (status / assignee / milestone)
- role_taxonomy.md template

**Skills Updated (5):**
- pm-init-todos (new Assignee column + example tasks)
- pm-add-task (--assignee support)
- pm-update-task (assignee change)
- pm-list-tasks (assignee filtering)
- pm-show-kanban (--by=status|assignee|milestone + --show= columns)

**Status:** Skills written, ready for integration testing  
**Timeline:** Independent of sync-mobile; ship when ready  
**Test Scope:** Assignee workflow + backward compatibility with 6-col schema

---

### v0.1.15 (Intermediate, Sync-Mobile)

**Features:**
- Mobile sync capability (temp branch isolation, commit/revert/backup)
- Task-linked branch cleanup (safety hooks in pm-close-task / pm-update-milestone)
- Git mergetool configuration (Beyond Compare, added to pm-setup-project)
- Phase 3 documentation (user guide, PM guide, voice guide, troubleshooting)

**Skills Added (5):**
- sync-mobile:pull (create temp branch, capture state, create manifest)
- sync-mobile:commit (checkpoint on temp branch)
- sync-mobile:revert-to (undo via git reset --hard)
- sync-mobile:sync (merge temp → main, handle conflicts, finalize or leave open)
- sync-mobile:backup (audit trail of commits)

**Skills Modified (3):**
- pm-setup-project (add git mergetool config to standard setup)
- pm-close-task (add branch verification before task closure)
- pm-update-milestone (add branch verification before phase closure)

**Status:** Skills specs written, Phase 3 in progress  
**Timeline:** After v0.1.14 releases; blocked on Phase 3 completion  
**Test Scope:** 6 sync-mobile scenarios + integration with v0.1.14 features (if both in same build)

---

### v0.1.16 (Deferred, Your Previous v0.1.15)

**Features:**
- Pushes out from v0.1.15 (what was originally scheduled for v0.1.15)

**Status:** Awaiting v0.1.15 to land  
**Timeline:** Start planning after v0.1.15 ships  
**No action needed yet:** Wait for v0.1.15 completion signal

---

## Coordination Notes

### For v0.1.14 Chat
- Ship v0.1.14 assignee work as planned
- No dependencies on sync-mobile (work independently)
- Sync-mobile is coming in v0.1.15, not blocking you
- If you finish before sync-mobile Phase 3 completes: great, v0.1.14 releases
- If you're still testing: both can land in same release cycle without conflict

### For v0.1.15 Chat (Sync-Mobile)
- You're the intermediate build between v0.1.14 and v0.1.16
- Phase 3 (docs + testing) is your gate before release
- Coordinate timing with v0.1.14 ship, but work can happen in parallel
- Note: version is v0.1.15 (not v0.1.16 as originally planned)

### For v0.1.16 Chat
- Your scope is deferred to make room for v0.1.15 (sync-mobile)
- You are NOT blocked; start your planning work anytime
- When v0.1.15 ships, you'll move from "previously v0.1.15" to "now v0.1.16"
- Timeline: Begin integration planning after v0.1.15 ships + Phase 3 docs available

---

## No File Conflicts

- **v0.1.14** updates task-related skills (todos, add-task, update-task, list-tasks, show-kanban)
- **v0.1.15** adds sync-mobile skills (new directory) + modifies pm-setup-project, pm-close-task, pm-update-milestone
- **No overlapping file changes** between the two (different skill families)
- Safe to develop in parallel

---

## Integration Checklist (v0.1.15)

When v0.1.14 is done and v0.1.15 Phase 3 work completes:

- [ ] Copy 5 sync-mobile SKILL.md files to plugin
- [ ] Update plugin.json with 5 new skills
- [ ] Update pm-setup-project: add git mergetool config (one-time, machine-level)
- [ ] Update pm-close-task: add branch verification (check for unmerged branches linked to task)
- [ ] Update pm-update-milestone: add branch verification (check for unmerged branches linked to phase)
- [ ] Update pm-version sentinel: v0.1.14 → v0.1.15
- [ ] Test sync-mobile workflows on Reconciliation Hypothesis (6 scenarios)
- [ ] Verify v0.1.14 features (assignee, kanban) still work with sync-mobile integration
- [ ] Release v0.1.15

---

**Last Updated:** 2026-05-23  
**Status:** Ready for coordination across three parallel chats

