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

| Topic | Current decision |
|---|---|
| Review Skills (Subset 4) | Integrate 13 skills (cycle management + in-cycle feedback workflow), unified delivery |
| Review setup mechanism | Extend `pm-init-reader-review-tracking` rather than creating a parallel skill |
| Reader-bundle pattern | Add `review-prep-reader-bundle`; PM-side packaging deferred to v0.1.15+ |
| Cross-phase dependency detection | Warn on ANY cross-phase dependency by default; per-project override in `drift_check.yaml` |
| Status staleness format | `<!-- ROLE-STATUS-UPDATED-YYYY-MM-DD -->`, embedded comment |
| Staleness threshold | Global 14-day default, per-project override |
| Assignee sourcing | Read role taxonomy from `charter.md` |
| Assignee kanban grouping | `--by=assignee` as an alternative mode, not always-on column |

## ⚠️ Open discrepancy found during reorg (2026-07-21)

`plugin.json` is at **v0.1.14**, but the `pm-version` skill's EXPECTED VERSION marker still says **v0.1.13** — this violates your own release checklist (`plugin.json`, `pm-version` marker, and description text must all move together). Also unclear whether v0.1.14 was ever pushed/released via the marketplace workflow, or is still mid-flight — the latest commit (`c6fbc9e`) covers only the Assignee Column piece of the locked v0.1.14 decisions, not Review Skills or Drift Enhancements. **Not resolved here — flagging for your next dev session.**
