# Decisions — Current State

This file holds the **current resting state** of decisions only — the latest answer, not the history of how we got there. Full rationale and dated lockdown records live in `2_Development/RoadMap/v0.1.14/DECISIONS_v014.md` and future version-specific decision files.

When a decision changes, update the row here; don't append a new one. The old value's rationale stays in the versioned RoadMap detail file where it was originally locked.

---

## Repo structure & housekeeping

| Topic | Current decision |
|---|---|
| Sync capability | Not delivered, never will be from this plugin. Discipline is Obsidian + iCloud across Mac/phone/tablet, managed outside Cowork. See `1_Project/Memory/feedback_no_sync_capability.md`. |
| `0_Product` folder | Pointer/README only — cannot physically contain `skills/`, `.claude-plugin/`, etc. (Claude Code plugin-loader constraint: those must stay at repo root). |
| Reorg scope | This dev repo only. Does NOT change what `pm-init-vault`/`pm-setup-project` scaffold for new end-user writing projects. |
| Memory management | All memories live as visible files in `1_Project/Memory/`, not in hidden session-managed storage. No new memory files outside this location without explicit user consent. |

## Plugin development (carried over from `DECISIONS_v014.md`)

**v0.1.14 status (confirmed by Jamie, 2026-07-21): released, in successful daily use for 2 months.** Only the Assignee Column workstream actually shipped — confirmed by skill listing, no `review-*`/`cycle-*` skills exist. Review Skills and Drift Enhancements were locked decisions but are open work, not urgent, see `2_Development/RoadMap/Roadmap.md`.

| Topic | Current decision |
|---|---|
| Review Skills (Subset 4) | Locked: integrate 13 skills (cycle management + in-cycle feedback workflow), unified delivery. **Not yet shipped.** |
| Review setup mechanism | Extend `pm-init-reader-review-tracking` rather than creating a parallel skill |
| Reader-bundle pattern | Add `review-prep-reader-bundle`; PM-side packaging deferred to v0.1.15+ |
| Cross-phase dependency detection | Warn on ANY cross-phase dependency by default; per-project override in `drift_check.yaml`. **Ship status unverified** — may be embedded in existing `pm-run-drift-check`/`drift_check.py` code rather than a new skill name. |
| Status staleness format | `<!-- ROLE-STATUS-UPDATED-YYYY-MM-DD -->`, embedded comment. Ship status unverified, same caveat as above. |
| Staleness threshold | Global 14-day default, per-project override. Ship status unverified. |
| Assignee sourcing | Read role taxonomy from `charter.md`. **Shipped in v0.1.14.** |
| Assignee kanban grouping | `--by=assignee` as an alternative mode, not always-on column. **Shipped in v0.1.14.** |

## Resolved during reorg (2026-07-21)

`plugin.json` was at v0.1.14 while the `pm-version` skill's EXPECTED VERSION marker still said v0.1.13 — a release-checklist gap (marker wasn't bumped when v0.1.14 shipped). Fixed: marker, "Expected for" block, and skill-count sentinel (58→60) all updated in `skills/pm-version/SKILL.md`.

**Still open, not resolved here:** Anthropic support thread 215474352137566's current status — filed via support.claude.com, no connector/API access to check it. Needs Jamie to check directly. Subset 5 (Substance) — user is handling separately.
