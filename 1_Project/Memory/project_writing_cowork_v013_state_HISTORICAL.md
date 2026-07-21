---
name: writing-cowork-project-state-at-v0-1-13-2026-05-20
description: "HISTORICAL / STALE — snapshot from 2026-05-20 at v0.1.13. plugin.json is now v0.1.14; see 1_Project/Decisions.md for the current open discrepancy this created."
type: project
originSessionId: 988852c3-1715-4f55-8d1f-6cfeedc2a4a6
---

> **This entry is superseded.** Kept for historical record only. `plugin.json` moved to v0.1.14 sometime after 2026-05-23 (see `2_Development/RoadMap/v0.1.14/`), but `pm-version`'s EXPECTED VERSION marker was never bumped to match, and it's unclear whether v0.1.14 was ever pushed/released. See `1_Project/Decisions.md` → "Open discrepancy found during reorg."

writing-cowork plugin was at **v0.1.13**. Dev workflow, consumer refresh procedure, and durable issue-logging were all established.

**Why this mattered at the time:** v0.1.13 closed the last open meta-gap from the 2026-05-20 cleanup arc — a way for specialist contexts in any vault chat to capture process/plugin observations and route them to a durable place.

**Dev workflow (as of that snapshot) — still accurate, see `1_Project/Process/dev-workflow-and-release.md` for the current version:**
- PLUGIN dev: Claude Code CLI. `claude plugin marketplace update jamie-cowork-plugins` + `claude plugin update writing-cowork@jamie-cowork-plugins` after pushing.
- COWORK runtime updates: marketplace-level uninstall+reinstall procedure (`pm-refresh-cowork-plugin`).
- ISSUES surfaced by specialist contexts: `pm-create-issue-report` (specialist-side), `pm-escalate-issue` (librarian-side).

**Anthropic support thread 215474352137566** — status unknown as of this reorg; was open as of the v0.1.13 snapshot.
