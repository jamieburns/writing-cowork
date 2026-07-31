# Activity Log

The single **shared, append-only** activity log for this repo — the semantic layer over git's mechanical layer. One entry per durable change: what, why, from what inputs, and the commit that carried it.

**Kind:** Log (append-only; never overwrite an entry). **Schema** and rationale: `1_Project/Documents/information_architecture_spine_2026-07-24.md` §4.

**Conventions**
- **Append-only, newest-last.** Sessions orient by reading the *tail*.
- **Author-stamped** — the role or `user` responsible for the change.
- **Index-first** — terse and scannable; the primary reader is the next session reloading state cheaply, not a prose reader.
- Rolls to `1_Project/History/` at phase/version close so this live file stays bounded.

> **Bootstrap note (2026-07-26):** this file was created ahead of its formal v0.16 build (the Log was a decided-form / deferred-mechanics organ per the spine). The location `1_Project/Log.md` and the newest-last convention are provisional — the v0.16 `pm-close-session` work may confirm or revise them.

---

## Entry schema

```
- <YYYY-MM-DD> · <author: role|user> · <action>
  why: <one line>
  inputs: <files / decisions read>
  changed: <files written>  · commit: <hash | uncommitted>
```

---

## Entries

- 2026-07-26 · user → claude · Established validate-before-commit as a hard release gate.
  why: `claude plugin validate .` must always run before committing a version bump — user-directed standing rule, not an optional step.
  inputs: `1_Project/Process/dev-workflow-and-release.md`; spine §4 (log schema)
  changed: `1_Project/Process/dev-workflow-and-release.md` (release-checklist gate); `1_Project/Log.md` (this log created)  · commit: 831608c

- 2026-07-29 · claude · Closed out the information-architecture / memory workstream; v0.1.17 content complete.
  why: memory management moved from an open problem to a shipped model, and the enforcement mechanism changed twice as evidence arrived — hooks do not run in Cowork, so enforcement moved to a git post-commit hook that fires where consent actually happens.
  inputs: spine §5/§6/§8; `Decisions.md`; GitHub #40495/#47993/#63360; `drift_check.py`
  changed: `Roadmap.md` (stale narrative sections corrected); `drift_check.py` (v0.3.1 — log_unlanded no longer flags the schema example)  · commit: 417c755
- 2026-07-29 · claude · Roadmap reduced to status-only; created Todos.md; swept the dated handoffs into it.
  why: status files were accreting history, so the roadmap had stopped being readable at a glance, and the only record of unresolved work lived in four ephemeral dated handoffs that the architecture says are never sources of truth.
  inputs: `1_Project/Handoff/2026-07-2{1,2,3}_*.md`; `1_Project/Documents/v0.1.15_planning_roadmap_2026-07-22.md`; `drift_check.py`; `pm-init-todos`, `pm-show-composite-kanban`, `pm-list-tasks` SKILL.md
  changed: `2_Development/RoadMap/Roadmap.md` (82 -> 45 lines); `2_Development/RoadMap/history/2026-07-29_roadmap-narrative-archive.md` (new); `1_Project/Todos.md` (new, 29 items); `1_Project/Decisions.md` (3 sections); `CLAUDE.md` (orient list)  · commit: edcbd9b

- 2026-07-30 · claude · v0.1.17 enforcement made fail-loud; pm-install-git-hooks executed for the first time.
  why: the first real host run showed the post-commit hook was inert — `command -v python3` resolves to Homebrew's python3, which lacked PyYAML, so drift_check exited 2 onto a stderr the hook discarded while ignoring the exit code. A broken checker was indistinguishable from a clean repo, in the one component v0.1.17 exists to ship.
  inputs: `0_Product/skills/pm-install-git-hooks/SKILL.md`; `templates/hooks/post-commit`; `drift_check.py:60-64,701-716`; `Decisions.md` (status-file rule, process/-tree prohibition)
  changed: `templates/hooks/post-commit` (4 silent exits now report); `drift_check.py` (0.3.2 — unconfigured session_hygiene is a finding); `pm-install-git-hooks/SKILL.md` (precondition 6, step 7); `1_Project/Process/drift_check.yaml` (new, hand-authored for this layout); `1_Project/Process/git-hooks/post-commit` (installed; core.hooksPath set); `Decisions.md` (2 sections); `Todos.md` (+c3f80b6e, +7e4b1a93, 6b91e2a5 reclassified)  · commit: e210d0b

- 2026-07-30 · claude · Corrected the lane invariant: `git status` is not a safe read from the sandbox mount.
  why: the session's first commit attempt failed on a stale `.git/index.lock` that a sandbox-side `git status` had created and been unable to unlink. `Decisions.md` recorded this cleanup as done on 2026-07-23; it recurred because the invariant blames mutations, and the actual trigger is any index-refreshing read.
  inputs: observed EPERM on `git status` from the mount; `feedback_sandbox_host_lanes.md`; `CLAUDE.md` invariants
  changed: `1_Project/Memory/feedback_git_status_creates_index_lock.md` (new); `1_Project/Memory/INDEX.md`; `1_Project/Todos.md` (+d51c9a27)  · commit: 2e7f0b3

- 2026-07-31 · claude · drift_check 0.4.0: config preflight; `_trashcan/` untracked.
  why: the 2026-07-30 fix made the *hook* fail loudly, but the checker it calls still reported "clean" whenever it could not read its inputs or was handed a key it does not implement — the general form of a4e1c7b2 / c6d05a91 / 7e4b1a93 / 6b91e2a5.
  inputs: `Decisions.md` ("Hygiene checks fail loudly"); `drift_check.py` ProjectConfig + check_inventory; 2026-07-30 session findings
  changed: `drift_check.py` (0.4.0 — check_config_preflight, unknown-key detection, inventory early-return); `plugin.json` (description); `.gitignore` (+_trashcan/); `Decisions.md` (2 sections); `Todos.md` (7e4b1a93 annotated); `_trashcan/` (13 files untracked, kept on disk)  · commit: d431f75
\n

- 2026-07-31 · claude · Cleared 5 pre-release bugs; drift_check 0.5.1.
  why: Jamie is feature complete and wants defects down before releasing v0.1.17. Three of the five were a single code path — the todos/roadmap reading in drift_check — and two more defects surfaced only once that code was actually executed against real data.
  inputs: `Todos.md`; `drift_check.py` load_todos/parse_roadmap_phases/check_cross_phase_dependency; `pm-init-todos`; both roadmap templates; `templates/CLAUDE.md` vs this repo's `CLAUDE.md`
  changed: `drift_check.py` (0.5.1 — header-driven columns, configurable todos/roadmap, milestone-derived phases, unescaped-pipe split); `templates/drift_check.yaml` (+todos/roadmap keys, +checks block); `pm-init-todos` (+Depends-On); 16 skill descriptions; `CLAUDE.md`; `templates/CLAUDE.md`; `Decisions.md`; `Todos.md` (5 closed, +9c14be7f)  · commit: 0e15efc
\n

- 2026-07-31 · claude · Cleared the last two in-scope pre-release bugs.
  why: both were cases of the tooling documenting a capability it lacked — a migration warning naming no runnable skill, and a release command that could not tell bookkeeping from a break-in.
  inputs: `pm-list-tasks` legacy-schema branch; `pm-show-composite-kanban`; `pm-release-file`; `Todos.md`
  changed: `pm-migrate-todos-schema/SKILL.md` (new); `pm-release-file/SKILL.md` (0.2.0); `pm-list-tasks/SKILL.md` (warning names the skill); `plugin.json` (description); `Decisions.md`; `Todos.md` (2 closed)  · commit: 0cb98e8
\n