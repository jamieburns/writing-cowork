# Memory Index

Visible, user-manageable memory for the writing-cowork dev project. Replaces hidden session-managed memory as of 2026-07-21 — see `feedback_visible_memory_only.md` for the rule.

- [No sync capability](feedback_no_sync_capability.md) — this plugin does not and will not deliver device-sync; that's handled manually via Obsidian + iCloud across Mac/phone/tablet.
- [Visible memory only](feedback_visible_memory_only.md) — the management rule: no new memory files outside `1_Project/Memory/` without explicit consent.
- [Sandbox vs. host lane discipline](feedback_sandbox_host_lanes.md) — file tools/inspection use sandbox or device_bash; git, gh, and any host CLI go through osascript on the real filesystem. Confirmed again 2026-07-21: device_bash hit the same stale `.git/index.lock` EPERM pattern as the original cloud-sandbox case.
- [Verify agent-supplied citations](feedback_verify_agent_citations.md) — research subagents can generate plausible-looking but wrong identifiers; verify before quoting.
- [Self-contained scripts when Cowork must be quit](feedback_self_contained_quit_scripts.md) — package the full workflow into one Terminal-runnable script before the user quits.
- [When workarounds pile up, check the docs](feedback_workarounds_warrant_doc_check.md) — stop and read canonical docs before adding a 3rd/4th workaround for the same problem.
- [writing-cowork project state (stale, historical)](project_writing_cowork_v013_state_HISTORICAL.md) — snapshot from 2026-05-20 at v0.1.13. Superseded — plugin.json is now v0.1.14 but pm-version's marker wasn't bumped to match. See `1_Project/Decisions.md` for the current open discrepancy.
- [Personal plugin marketplace mechanics](reference_personal_plugin_marketplace.md) — raw reference notes on the two-client (Claude Code / Cowork) plugin distribution setup. Polished into a runnable procedure at `1_Project/Process/dev-workflow-and-release.md`.
