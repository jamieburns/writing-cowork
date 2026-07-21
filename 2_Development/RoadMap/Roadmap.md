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

**Status (checked 2026-07-21): no reply beyond the initial acknowledgment** — Jamie checked email directly, nothing further came in. Followed up with a web search against current Anthropic docs/changelog/GitHub issues to see if any of the four original items shipped a fix since May 2026. None have:

1. **Update detection / stale plugin cache** — still broken. [GitHub #69020](https://github.com/anthropics/claude-code/issues/69020) is the closest match (Cowork installs stale cached plugin, ignores marketplace updates), still open, cross-references 3 sibling issues with the same pattern. Checked Cowork changelog through June 2026 (v1.11847.5, v1.11187.4) — no marketplace-cache or update-detection fix mentioned. `pm-refresh-cowork-plugin`'s marketplace-uninstall-reinstall workaround is still necessary.
2. **"Save plugin" generic validation error** — root cause now public via [GitHub #56376](https://github.com/anthropics/claude-code/issues/56376): Cowork's client discards the server's detailed `validation_errors[]` array and shows only a generic toast. Still open.
3. **Bonus finding, actionable:** [GitHub #63081](https://github.com/anthropics/claude-code/issues/63081) — Cowork's upload validator silently fails on angle brackets (`<vault>`, `<name>`, etc.) in a `SKILL.md`'s `description:` frontmatter field, even inside backticks. **16 of this plugin's 60 skills have this exact pattern** (e.g. `pm-add-task` references `` `<vault>/process/active/todos.md` `` in its description) — likely explains the original "Save plugin" failure even though `claude plugin validate` passed. Workaround: `<vault>` → `[vault]`. Low urgency since the dev workflow here doesn't use the "Save plugin" button, but a real, cheap cleanup if ever wanted. List of affected skills is in the session record; re-grep with: `awk '/^---$/{c++;next} c==1' skills/*/SKILL.md` scoped to the `description:` block if picking this up.
4. **extraKnownMarketplaces / private catalogs** — Anthropic shipped **organization-level** private marketplaces (support.claude.com confirms private/internal source repos for org marketplaces), which doesn't address a personal/individual setup like this one. The feature that would actually help — [GitHub #66184](https://github.com/anthropics/claude-code/issues/66184), Cowork's Personal tab accepting custom marketplace URLs — is still open, marked "Critical — blocking my work" by another user.

**Net: nothing has shipped that resolves any of the four original items.** No follow-up to Anthropic is warranted right now beyond what's already on file — the honest status is "still broken, still open" across the board. Re-check this section if picking the thread back up, rather than re-researching from scratch.

## Legacy / uncertain work items

- Phase 9 (legacy `todos.md` migration to vault) — no `todos.md` was found in this repo during the reorg; if this refers to something in a different (end-user) vault, track it there instead.
