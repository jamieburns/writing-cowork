# Memory Index

Visible, user-manageable memory for the writing-cowork dev project. **Authoritative** — replaces hidden session-managed memory as of 2026-07-21; see `feedback_visible_memory_only.md` for the rule.

Reached from the repo-root `CLAUDE.md` router. Pull topic files on demand; don't read them all.

- [No sync capability](feedback_no_sync_capability.md) — this plugin does not and will not deliver device-sync; that's handled manually via Obsidian + iCloud across Mac/phone/tablet.
- [Visible memory only](feedback_visible_memory_only.md) — the management rule: no new memory files outside `1_Project/Memory/` without explicit consent.
- [Sandbox vs. host lane discipline](feedback_sandbox_host_lanes.md) — file tools/inspection use sandbox or device_bash; git, gh, and any host CLI go through osascript on the real filesystem. Confirmed again 2026-07-21: device_bash hit the same stale `.git/index.lock` EPERM pattern as the original cloud-sandbox case.
- [`git status` from the sandbox view is a WRITE](feedback_git_status_creates_index_lock.md) — corrects the "read-only inspection is fine anywhere" clause in the CLAUDE.md invariant: `git status` creates `.git/index.lock`, fails to unlink it from the mount, and the orphan blocks the next host-side commit.
- [Verify agent-supplied citations](feedback_verify_agent_citations.md) — research subagents can generate plausible-looking but wrong identifiers; verify before quoting.
- [Self-contained scripts when Cowork must be quit](feedback_self_contained_quit_scripts.md) — package the full workflow into one Terminal-runnable script before the user quits.
- [When workarounds pile up, check the docs](feedback_workarounds_warrant_doc_check.md) — stop and read canonical docs before adding a 3rd/4th workaround for the same problem.
- [Release checklist — version in description](feedback_release_includes_version_in_description.md) — every version bump touches three places so Cowork's UI shows the version without opening files. Polished into `1_Project/Process/dev-workflow-and-release.md`.
- [Re-staged files can be stale](feedback_restaged_files_can_be_stale.md) — `device_stage_files` may serve a cached copy on re-stage while reporting the new size; verify content, or edit on the host.
- [Personal plugin marketplace mechanics](reference_personal_plugin_marketplace.md) — raw reference notes on the two-client (Claude Code / Cowork) plugin distribution setup. Polished into a runnable procedure at `1_Project/Process/dev-workflow-and-release.md`.
- [writing-cowork project state (stale, historical)](project_writing_cowork_v013_state_HISTORICAL.md) — snapshot from 2026-05-20 at v0.1.13. **Superseded** — current state is v0.1.15; read `1_Project/Decisions.md` instead. Kept as a historical record only.

---

## Hidden store retired — 2026-07-26

The platform memory store is **empty and retired**. All 8 entries were reviewed individually and dispositioned: unique content promoted (notably the one-time per-machine setup steps, which existed nowhere else — now in `1_Project/Process/dev-workflow-and-release.md`), duplicates and stale entries discarded. Its `MEMORY.md` is a 3-line pointer back here. Full record in `1_Project/Decisions.md` → "Platform memory store — retirement record".

**This directory is now the only project memory.** Note: `project_memory_write` has no delete affordance — entries there could be blanked but not removed, so the filenames persist even though the content is gone.

## Reconciliation note — 2026-07-25

This index and the hidden platform store had **silently diverged**. Found during the memory-management prototype pass:

- `feedback_release_includes_version_in_description.md` existed only in the platform store — promoted here.
- The platform store's project-state file still claimed v0.1.13 and misinformed a live session — corrected to a tombstone pointing here.
- `feedback_visible_memory_only.md` (the rule governing memory) and `feedback_no_sync_capability.md` existed only here, so the platform store never loaded the rule meant to govern it. Fixed by the repo-root `CLAUDE.md` router plus a pointer in the platform index.

Full analysis: `1_Project/Documents/memory_management_recommendation_2026-07-25.md`. A gating experiment is in flight — see `1_Project/Documents/memory_gating_test_2026-07-25.md` before changing memory settings.
