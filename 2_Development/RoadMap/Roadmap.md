# writing-cowork Roadmap

High-level phase/version summary. Full detail for each version lives in its own folder under `2_Development/RoadMap/`.

| Version | Status | Summary |
|---|---|---|
| v0.1.1 – v0.1.9 | Shipped | Foundation, Planning (Subset 2), Voice/tone (Subset 3), refresh-workaround skill, MVP validated |
| v0.1.10 – v0.1.11 | Shipped | Dev-workflow hardening (Claude Code CLI as the dev environment), pm-refresh rewritten as a documented consumer-side workaround |
| v0.1.12 – v0.1.13 | Shipped | `inbox/README.md` scaffold, `inbox/issues/` convention + `pm-create-issue-report` + `pm-escalate-issue` (GitHub routing) |
| **v0.1.14** | **Shipped, released, in successful daily use for 2 months (confirmed 2026-07-21)** | Assignee column (6 skills + role_taxonomy template). `pm-version`'s marker was stale at v0.1.13 pointing to this exact version — fixed 2026-07-21. |
| v0.1.15+ | Not started | See "Carried-over decisions" below |

## Carried-over decisions from `DECISIONS_v014.md` — not yet shipped

`DECISIONS_v014.md` locked three workstreams for v0.1.14: Assignee Column, Review Skills (Subset 4, 13 skills), and Drift Enhancements. Only Assignee Column shipped — confirmed by skill listing: no `review-*` or `cycle-*` skills exist anywhere in the current 60 skills (only the pre-existing `pm-init-reader-review-tracking` and `pm-schedule-review`). Drift Enhancements' status wasn't independently re-verified in this pass (they may be embedded as code changes to `pm-run-drift-check`/`drift_check.py` rather than new skill names, which wouldn't show up in a skill-name check).

These are open, not urgent — pick up whenever you're ready to resume feature work:

- Review Skills (Subset 4, 13 skills per the locked decision) — full scope in `2_Development/RoadMap/v0.1.14/ASSESSMENT_REVIEW_SKILLS_v014.md`
- Drift Enhancements (cross-phase dependency detection, status-staleness timestamps, `.gitkeep` inflation fix) — full scope in `2_Development/RoadMap/v0.1.14/ASSESSMENT_DRIFT_ENHANCEMENTS_v014.md`. Worth a quick check of `pm-run-drift-check`/`drift_check.py` before assuming this is unshipped.

## Deferred, being handled separately (per user, 2026-07-21)

- Subset 5 (Substance, 3 skills) — user will clean this up separately, not part of this housekeeping pass.

## Anthropic support thread 215474352137566

Filed via support.claude.com's contact form (private, account-tied — no MCP/API access to check status). **Needs Jamie to check directly** — no automated way to verify whether it's been answered. Full original correspondence: `1_Project/History/_anthropic_feedback_2026-05-18.md` and `_anthropic_reply_2026-05-18.md`.

## Legacy / uncertain work items

- Phase 9 (legacy `todos.md` migration to vault) — no `todos.md` was found in this repo during the reorg; if this refers to something in a different (end-user) vault, track it there instead.
