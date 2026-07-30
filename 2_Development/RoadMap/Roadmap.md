# writing-cowork Roadmap

**Status only — no history.** This file answers "where is each version, right
now." It does not record how we got here.

- **Work items** → `1_Project/Todos.md` (the task list; one row per work item)
- **Why a thing was decided** → `1_Project/Decisions.md`
- **Superseded roadmap narrative** → `2_Development/RoadMap/history/`
- **Per-version detail** → the version's own folder under `2_Development/RoadMap/`

| Version | Status | Scope |
|---|---|---|
| v0.1.1 – v0.1.9 | Shipped | Foundation, Planning (Subset 2), Voice/tone (Subset 3), refresh-workaround skill, MVP validated |
| v0.1.10 – v0.1.11 | Shipped | Dev-workflow hardening; `pm-refresh` as a documented consumer-side workaround |
| v0.1.12 – v0.1.13 | Shipped | `inbox/README.md` scaffold; `inbox/issues/` + `pm-create-issue-report` + `pm-escalate-issue` |
| v0.1.14 | Shipped, released, in daily use | Assignee column (6 skills + `role_taxonomy` template) |
| v0.1.15 | Shipped to Claude Code CLI; **not refreshed in Cowork** | `0_Product/` consolidation via `git-subdir` marketplace source; `research_and_analysis/` + `production/` folder naming |
| **v0.1.16** | **Content complete** — folded into the v0.1.17 release, never released standalone | Information architecture spine: Tier-1 router, ownership markers, visible memory, memory settings, activity log, provenance registry, `pm-install-router` / `pm-init-memory` / `pm-init-log` / `pm-close-session`, `drift_check` session-hygiene checks |
| **v0.1.17** | **Content complete; release outstanding** | Claude Code hooks dropped. Enforcement is a git `post-commit` session-hygiene hook (`pm-install-git-hooks`) — host-side, every runtime, fires at commit, never blocks |
| v0.1.18 | Open, unscheduled | Recovered backlog: drift-check schema and config gaps, dependency gate, kanban parity. See `Todos.md` |
| v0.1.19 | Deferred | Production-pipeline tooling |
| v0.2.0 | Deferred | `pm-sync-project-to-plugin` — drift-check config + vault layout + router migration in one mechanism |

**Version shorthand.** Elsewhere in this repo these appear as v0.16, v0.17,
v0.19 — dropping the leading `1.`. They mean v0.1.16, v0.1.17, v0.1.19. v0.2.0
is genuinely the next minor and comes after v0.1.19.

## Blocking the v0.1.17 release

Three steps, all Jamie's — tracked as rows in `Todos.md`:
marketplace catalog description in `cowork-plugins-marketplace`, the Cowork-side
uninstall/reinstall refresh, and an optional `release/v0.1.17-*` tag.

**Known risk carried into the release:** `pm-install-git-hooks` has never been
executed and the `post-commit` hook has never fired. Its underlying checks are
tested; the installer is not. This repo is the first test. The memory settings
are likewise unverified in Cowork — the hook deliberately does not depend on
them.

## Not on the roadmap

- Subset 5 (Substance, 3 skills) — Jamie is handling separately.
- Anthropic support thread 215474352137566 — four items, all still open, nothing
  shipped that resolves any of them. Recheck rather than re-research; the record
  is in `history/2026-07-29_roadmap-narrative-archive.md`.
