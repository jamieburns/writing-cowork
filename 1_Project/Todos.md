# Todos — writing-cowork (plugin development)

Created: 2026-07-29

Granular task list for this repo. One row per work item. Distinct from
`2_Development/RoadMap/Roadmap.md`: the roadmap captures version status; this
captures the work inside it. Distinct from `1_Project/Decisions.md`: that
records commitments already made; this records work not yet done.

Task IDs are 8-char short hashes (locked decision #9). Status values:
`planned` → `in-progress` → `done`. Assignee `user` means Jamie does it
outside a session; everything else is agent-executable.

**Schema note.** This uses the plugin's own `pm-init-todos` schema so this repo
dogfoods `pm-add-task` / `pm-update-task` / `pm-list-tasks` / `pm-close-task`.
See task `a4e1c7b2` — `drift_check.py` expects a *different* column set, which
is a real defect surfaced by adopting the schema here.

## Now — blocking the v0.1.17 release

| ID | Description | Milestone | Assignee | Status | Added | Notes |
|----|-------------|-----------|----------|--------|-------|-------|
| 3f8a2d19 | Marketplace catalog description in `cowork-plugins-marketplace` | v0.1.17-release | user | planned | 2026-07-29 | Not a connected folder; deliberately untouched by sessions |
| 7c1b9e04 | Cowork-side marketplace uninstall/reinstall refresh | v0.1.17-release | user | planned | 2026-07-29 | Procedure in `1_Project/Process/dev-workflow-and-release.md` |
| b25d6f37 | Optional `release/v0.1.17-*` tag | v0.1.17-release | user | planned | 2026-07-29 | Matches `release/v0.1.14` |
| e90c4a58 | Run `pm-install-git-hooks` against this repo — first execution ever | v0.1.17-release | pm | planned | 2026-07-29 | Hook has never fired. Verify exec bit, `core.hooksPath`, and that `drift_check.py --dry-run` emits "Session hygiene" lines |
| 14a7b3e6 | Verify memory settings actually gate, in a fresh Cowork session | v0.1.17-release | pm | planned | 2026-07-29 | Cannot be tested from a session that already loaded them. #40495 suggests they may be inert |
| 0d92f4a7 | Install `drift_check.yaml` for this repo — it has none, so `pm-install-git-hooks` precondition 4 fails and the post-commit hook would be inert | v0.1.17-release | pm | planned | 2026-07-29 | Blocks `e90c4a58`. Found 2026-07-29 trying to run the checker here; this repo is not registered with a drift config at all |

## Next — v0.1.18, recovered from the dated handoffs

Verified against source 2026-07-29, not inherited on trust. Provenance:
`1_Project/Handoff/2026-07-2{1,2,3}_*.md` and
`1_Project/Documents/v0.1.15_planning_roadmap_2026-07-22.md`.

| ID | Description | Milestone | Assignee | Status | Added | Notes |
|----|-------------|-----------|----------|--------|-------|-------|
| a4e1c7b2 | Reconcile the todos schema: `drift_check.py:496` expects `id\|title\|status\|priority\|milestone\|depends-on`; `pm-init-todos` writes `ID\|Description\|Milestone\|Assignee\|Status\|Added\|Notes` | v0.1.18 | pm | planned | 2026-07-29 | Found by adopting the schema in this repo. Any checker reading todos rows is operating on a schema no template produces |
| c6d05a91 | Cross-phase dependency check is inert by default — `drift_check.py:536` gates on `cross_phase_config`, populated only from a `checks:` block the shipped `drift_check.yaml` template lacks | v0.1.18 | pm | planned | 2026-07-29 | Shipped-but-dead code. Original finding 2026-07-23, re-verified 2026-07-29 |
| 5b3e8c72 | Dependency gate at task close — `pm-close-task` should refuse or warn when `depends-on` is unmet | v0.1.18 | pm | planned | 2026-07-29 | Blocked by `a4e1c7b2`. Earlier claim that `depends-on` doesn't exist is stale — it exists in the checker, not the template |
| 9e2f471d | `pm-show-composite-kanban` — add `--by=` and filter parity with `pm-show-kanban` | v0.1.18 | pm | planned | 2026-07-29 | Self-documented `v0.1.15 TODO:` at SKILL.md line 23 |
| 8a45c0e3 | `pm-migrate-todos-schema` — legacy checkbox `todos.md` blocks task CRUD | v0.1.18 | pm | planned | 2026-07-29 | Self-documented in `pm-list-tasks`; composite-kanban special-cases it. Affects Reconciliation Hypothesis |
| 2d7f6b18 | Decide: drift exclude-list currency is per-vault config maintenance, or a plugin-level self-diagnosing mode | v0.1.18 | pm | planned | 2026-07-29 | Decision, not build. Outcome goes to `Decisions.md` |
| f13c8d40 | Full Disk Access / launchd + iCloud fragility in `pm-setup-project` (macOS) | v0.1.18 | pm | planned | 2026-07-29 | Silent-fail class; has already caused a real outage per project memory |

## Next — decisions needed from Jamie

| ID | Description | Milestone | Assignee | Status | Added | Notes |
|----|-------------|-----------|----------|--------|-------|-------|
| 6b91e2a5 | Confirm this repo's `priority_prefixes` list — `0_Product` at minimum, plus which parts of `1_Project/` or `2_Development/` join it | v0.1.18 | user | planned | 2026-07-29 | Mechanism confirmed 2026-07-22; the list was never settled. Closeable in a minute |
| d84a0c63 | Disposition the four dated handoffs in `1_Project/Handoff/` — frozen history or delete | v0.1.18 | user | planned | 2026-07-29 | Everything unresolved in them is now on this list, so nothing is lost either way |
| 0c5e93b7 | Confirm `resources/` content policy is a per-vault `charter.md` call and write the closing note | v0.1.18 | user | planned | 2026-07-29 | Already reasoned through 2026-07-22; needs a sentence, not design work |
| 47f2a8d1 | Decide whether the matcher false-positive is worth pursuing at all | v0.1.18 | user | planned | 2026-07-29 | Its sourcing was struck 2026-07-22 (misattributed from Epistemology). Recommend dropping to a theoretical note |

## Later — carried backlog

| ID | Description | Milestone | Assignee | Status | Added | Notes |
|----|-------------|-----------|----------|--------|-------|-------|
| ba6d3f19 | Review Skills — Subset 4, 13 skills | backlog | pm | planned | 2026-07-29 | Locked in `DECISIONS_v014.md`, never shipped. Scope in `2_Development/RoadMap/v0.1.14/ASSESSMENT_REVIEW_SKILLS_v014.md` |
| 71e4c8b0 | Drift Enhancements — verify what actually shipped before rebuilding | backlog | pm | planned | 2026-07-29 | Status-staleness timestamps and `.gitkeep` fix may already be in. Scope in `ASSESSMENT_DRIFT_ENHANCEMENTS_v014.md`. Overlaps `c6d05a91` |
| 3ca70e52 | `#63081` — replace angle brackets in 16 skill `description:` fields (`<vault>` → `[vault]`) | backlog | pm | planned | 2026-07-29 | Cowork's upload validator fails silently on these. Low urgency: the CLI dev workflow doesn't hit it |
| e58b21fc | Citation ledger — design the `last accessed` touch mechanism | backlog | pm | planned | 2026-07-29 | Load-bearing: the 16-day TTL is locked, so an unreliable touch means wrong deletions. Nothing built yet — no template, no skill |
| 96d7c34a | Citation ledger — `last verified` staleness checking | backlog | pm | planned | 2026-07-29 | Manual for now; automatic deferred. Blocked by `e58b21fc` |
| 4e0b9a76 | Missing `analysis-*` and review-tracking skill families | backlog | pm | planned | 2026-07-29 | Causes ad hoc, inconsistent workarounds per the 2026-07-21 problem report |
| c72f5e81 | Batch / preview operations on the claim → promote → process-inbox chain | backlog | pm | planned | 2026-07-29 | Needs usage evidence first: how often are multi-file promotions actually done? |
| 1f6a4d90 | `pm-release-file` — distinguish force-releasing someone else's stale claim from a normal self-release | backlog | pm | planned | 2026-07-29 | Same code path today; an accidental unlock leaves no audit trace |
| 8d3e07c4 | `--all` / registry-wide parity for per-project skills that lack it | backlog | pm | planned | 2026-07-29 | `pm-run-drift-check`, `pm-enable-project`, `pm-disable-project` have it; comparable skills don't |
| 5a91b6e2 | `git log --all` sweep to convert the skill usage-signal doc from signal to ledger | backlog | pm | planned | 2026-07-29 | Would settle the "apparently unused" skills question and the `writer_voice_sample*.md` provenance question |
| 20c8f7d5 | Recheck Anthropic support thread 215474352137566 | backlog | user | planned | 2026-07-29 | Four items, all open as of 2026-07-21. Recheck, don't re-research — record in `history/2026-07-29_roadmap-narrative-archive.md` |
| b47e1a38 | v0.1.19 — production-pipeline tooling | v0.1.19 | pm | planned | 2026-07-29 | Deferred |
| e6c2d509 | v0.2.0 — `pm-sync-project-to-plugin`: drift-check config + vault layout + router migration | v0.2.0 | pm | planned | 2026-07-29 | Deferred. Skill exists at v0.2.0 with the layout case; the sync mechanism is the remaining work |
