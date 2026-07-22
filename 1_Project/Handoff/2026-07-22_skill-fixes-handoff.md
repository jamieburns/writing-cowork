# Handoff: two skill fixes for writing-cowork, sourced from Reconciliation Hypothesis

**To:** whoever is picking up writing-cowork plugin development next
**From:** Claude (Cowork), cloud session working the Reconciliation Hypothesis vault
**Date:** 2026-07-22
**Status:** Proposed — skill substance drafted below, not yet built/packaged/tested against the real plugin repo

## Where this came from

Two prior-day docs in the Reconciliation Hypothesis vault (`process/history/writing_cowork_skill_problem_report_2026-07-21.md` and `..._usage_signal_2026-07-21.md`) did an evidence-based pass over which writing-cowork skills are actually in use in that vault and what's going wrong with them. Two findings there are concrete, dated, and already-realized process failures rather than hypothetical gaps — those are what this handoff turns into skill substance. A third, smaller filename fix is included since it's cheap to bundle into either.

This handoff is scoped to the **plugin project** (wherever writing-cowork's source lives, e.g. `~/code/cowork-tools/` per the Reconciliation Hypothesis vault's references) — not to the Reconciliation Hypothesis vault itself, which is only the consumer/evidence source here.

**Caveat carried over from the source report:** the analysis behind this handoff was done without read access to the actual plugin source (`~/code/cowork-tools/drift_check.py` and the `pm-*` skill implementations were not reachable from that session — only their effects on the vault's files were visible). Verify against real code before implementing.

---

## Fix 1 — dependency gate on task close (`pm-close-task` / `pm-update-task`)

### Problem, with evidence

Neither skill currently checks a task's declared `Milestone`/`Depends-on` relationship before allowing a transition to `done`. In the Reconciliation Hypothesis vault, tasks **I3.2** (`d64cca0b`, "Lock markers applied to deliverable layer") and **I3.3** (`42917629`, "Hub recent-history lock event entry") were both marked `done` on 2026-05-20, then had to be manually reverted to `planned` the same day after the writer pointed out that voice/tone work should gate Phase 12 lock — a dependency that existed in the data but wasn't checked at close time. An inbox cover-note referencing the (incorrect) closure had already been drafted and had to be pulled before the pm processed it.

Broader signal: of 85 total task rows in that vault's `todos.md`, 13 (~15%) are marked `UNDONE`, `reverted`, `Retired`, or `Re-scoped` — i.e., needed some kind of manual correction after the fact. Not all 13 are dependency-gate failures specifically, but the I3.2/I3.3 pair confirms the failure mode is real, not speculative.

### Proposed skill substance

Add a pre-close check to `pm-close-task` (and the `done`-setting path of `pm-update-task`) that runs **before** writing the status change:

1. Read the task row's `Milestone` and any `Depends-on` field (if the schema doesn't currently have a `Depends-on` column, this fix depends on adding one — see Open Question below).
2. If `Depends-on` references other task IDs: check each referenced task's current status. If any referenced task is not `done`, block the close and surface a warning: `Cannot close <id>: depends on <other-id> ("<title>"), currently <status>.` Require an explicit override flag (e.g. `--force`) to close anyway, and if overridden, write a one-line note into the task's `Notes` field recording the override (`Closed despite open dependency <other-id> — overridden <date>`).
3. If `Milestone` is set but the skill has no visibility into milestone-level gating rules (e.g. "voice/tone work gates lock milestones") — that's a vault-specific convention, not something the skill can hardcode. Proposed approach: let `Depends-on` be the general mechanism, and treat milestone-gating as a specific *use* of it — i.e., the fix for the I3.2/I3.3 case is that closing a lock-milestone task should have had an explicit `Depends-on` reference to the voice-pass task, which the gate would then have caught. This pushes the actual gating logic into task data (where the writer/pm already thinks about it) rather than baking project-specific rules into the skill.

### Open question to resolve before building

Does `todos.md`'s current row schema have a `Depends-on` (or equivalent) column at all? The usage-signal doc doesn't confirm one exists. If not, this is two changes, not one: (a) add the column and a convention for how it's populated (manually by whoever creates the task, most likely), (b) add the close-time check that reads it. Worth confirming against the actual `todos.md` template/schema in the plugin repo before scoping the work.

---

## Fix 2 — drift-check exclude list vs. false-positive rate (`pm-run-drift-check` / `drift_check.yaml`)

### Problem, with evidence

Reports from the Reconciliation Hypothesis vault's `drift_reports/`: 153 "unaccounted" files flagged on 2026-07-11, 348 on 2026-07-18, 94 on 2026-07-20 (the drop reflects a manual `file_ownership.md` reconciliation pass, not a config fix). Nearly all the noise across all three runs is the same handful of large, clearly-intentional groups that the exclude list hasn't kept pace with: the `bible_reference/` and `resources/Bibles/BSB/` reference corpora (~80 files each run), and on 07-18 specifically the entire `handoffs/*` and `recommendations/*` working trees.

By contrast, the build-staleness check in the same reports is working correctly and consistently — all three runs correctly flag the same 4 stale build outputs (889–1082 hours stale). The problem is specific to the inventory/exclude-list mechanism, not the whole skill.

Practical cost: when a report's real signal (4 genuine issues) is buried under hundreds of expected non-issues, that's the exact condition under which nobody reads the report carefully anymore — which defeats the point of running it nightly.

### Proposed skill substance

This is less "new skill" and more "the existing skill needs an exclude-list maintenance step it doesn't currently have":

1. Add `bible_reference/`, `resources/Bibles/`, `handoffs/`, and `recommendations/` to `drift_check.yaml`'s `exclude_prefixes` for the Reconciliation Hypothesis vault specifically (this part is a config edit in that vault's own `drift_check.yaml`, not a plugin-repo change — flagging here for completeness, but it's not blocked on this handoff).
2. At the plugin level, consider whether `pm-run-drift-check` should have a **self-diagnosing mode**: if the same set of paths appears as "unaccounted" in N consecutive runs (configurable, default maybe 3) without being acted on, treat that as a signal the exclude list is stale rather than a signal the writer is ignoring real problems, and surface a distinct "these look like config gaps, not real drift" summary section separate from the "these are new/changed" section. This turns a recurring silent failure mode into something the skill catches on its own instead of requiring a human to notice the pattern across multiple dated reports (which is exactly what didn't happen for 9+ days per the source report's finding 1c: the same ~24-entry `inventory_missing` list appeared verbatim in the 07-11, 07-18, and 07-20 reports).
3. Smaller, bundle-in-for-free fix: report filenames are currently `YYYY-MM-DD.md` even though the report header already contains a full timestamp (`2026-07-11T10:22:40`). Two runs on the same day silently overwrite each other with no trace the earlier run happened. Rename convention to `YYYY-MM-DDTHHMM.md` (or similar) — low-risk, but worth confirming against the real `drift_check.py` source before editing since this was inferred from output files, not the script itself.

### Open question to resolve before building

Is the exclude-list staleness a per-project config maintenance problem only (i.e., every writing-cowork vault will eventually hit this and the fix is "remember to update `drift_check.yaml` as the vault grows"), or is it worth the plugin-level self-diagnosing addition in 2 above? The former is a one-line vault-specific fix with no plugin change needed; the latter is real feature work. Recommend scoping 1 (vault config) as an immediate fix regardless, and treating 2 as a separate decision about whether it's worth plugin-level investment.

---

## Not included here

The problem report also flagged an audit-trail/content-separation issue and noted several skills with no filesystem-trace evidence of ever firing (`pm-create-issue-report`, `pm-escalate-issue`, `pm-schedule-review`, most `voice-*` skills beyond one exception row). Those aren't included as skill substance here because: the audit-trail issue is a vault-side process convention already being remediated directly in that vault (not a plugin defect), and the "apparently unused" skills need more evidence before concluding anything about them (several are read-only/display skills with no trace by design, and git history — the strongest usage signal — was unreachable from that session).

## Recommended next step

Before building either fix, get read access to the real plugin source (`~/code/cowork-tools/` was not reachable from the originating session — only names were visible) so the schema assumptions above (does `todos.md` have a `Depends-on` field already? what does `pm-run-drift-check`'s actual exclude-list matching logic look like?) can be checked against code instead of inferred from output files.

---
---

## Addendum (2026-07-22, same day, follow-up session) — verified against real plugin source

**Status of this addendum:** the session that wrote this addendum had direct read access to the actual plugin source at `/root/.claude/plugins/synced/writing-cowork/` (a synced copy of the same plugin the handoff above is about). This is the read access the "Recommended next step" above asked for. Everything below is grounded in real `SKILL.md` files and templates, not inference from vault output. Nothing above this line has been changed — this section only adds to it, and corrects two assumptions the original handoff explicitly flagged as unverified.

### Correction to Fix 1's open question — `Milestone` already exists, `Depends-on` does not

The original handoff's open question ("does `todos.md` have a `Depends-on` column?") is now answered directly: **no**. The real schema, confirmed in `skills/pm-add-task/SKILL.md` and `skills/pm-init-todos/SKILL.md`, is:

`| ID | Description | Milestone | Assignee | Status | Added | Notes |`

So `Milestone` is already a first-class column (has been since at least pm-add-task v0.1.4) — the handoff didn't need to ask about that part, it's there and populated. But there is no `Depends-on` column anywhere, and no dependency-checking logic exists today. Checking `pm-close-task/SKILL.md`, its only preconditions are: todos.md exists, the task ID is found, and a warn-but-proceed if the task is already done — no gate of any kind. `pm-update-task/SKILL.md` is the same: preconditions are just "todos.md exists" and "task found by ID"; setting `--status=done` is unconditional, and the skill merely *suggests* the user separately run `pm-close-task` afterward.

Net effect: Fix 1 as scoped in the original handoff is correct in shape, but it is **net-new feature work, not a small patch**. It requires (a) a schema change to `pm-init-todos` and `pm-add-task` (a breaking change for existing vaults, needing a migration convention for populating `Depends-on` on already-created tasks), and (b) new precondition logic added to both `pm-close-task` and `pm-update-task`. Recommend scoping this explicitly as a schema migration + two skill changes, not a single-skill patch, when it's picked up.

### Correction to Fix 2 — `drift_check.py` is confirmed external; exclude-list mechanism is more capable than the false-positive rate suggests

Confirmed: there are zero `.py` files or `scripts/` directories anywhere under `skills/` in the plugin. `pm-run-drift-check/SKILL.md` shells out directly to `python3 ~/code/cowork-tools/drift_check.py ...`, with its own documented failure message for when that external path is missing. The plugin itself ships only the **config template**, at `templates/drift_check.yaml`, installed per-project by `pm-install-drift-check-config`. So the original handoff's instinct — that the false-positive fix is mostly a config problem, not a plugin-code problem — holds up.

One thing worth correcting: the exclude mechanism itself is not naive. The template supports both `exclude_prefixes` (literal top-level path prefixes) and `exclude_patterns` (real regexes, e.g. `"(^|/)_"`, `"/scratch/"`, `"__pycache__"`). If Fix 2 gets built as "make the exclude list smarter," that capability already exists — the actual gap is purely that nobody has kept the *list* current as the vault grew, which supports treating this as a maintenance-process problem (or the self-diagnosing "stale exclude list" mode proposed in the original Fix 2 §2) rather than an exclude-matching engine rewrite.

The filename-collision claim in Fix 2 §3 is **confirmed accurate** from the template and skill's own documented example output: `reports_dir: process/data_management/drift_reports` combined with a report path of `<vault>/process/data_management/drift_reports/<date>.md` — plain `YYYY-MM-DD.md`, no time component, despite the report body itself containing a full timestamp. The skill's own "Standalone use" section documents running the check on demand as a supported, idempotent operation, which makes same-day double-runs a real and easy-to-hit scenario, not an edge case. This part of Fix 2 can be built with confidence.

### Additional efficiency opportunities found during this pass (new material, not in the original handoff)

These came out of a broad skim of every `SKILL.md` in the plugin, looking specifically for places a skill could save the user (Jamie) trouble — repeated manual invocation chains, self-documented gaps, or missing convenience operations. None of these were visible to the original handoff's session since it couldn't read the source at all.

1. **No gap in initial setup — confirm and move on.** `pm-setup-project` already fully orchestrates all ~20 `pm-init-*`/`pm-install-*`/`pm-finalize-scaffold-commit`/`pm-register-project` sub-skills as one invocation, with a resumable state file (`pm-resume-setup` picks up after a failed step). There's no missing "orchestrator" skill here — this part of the plugin is already efficient, contrary to what one might assume from the sheer number of `pm-init-*`/`pm-install-*` skills listed individually.

2. **`pm-show-composite-kanban` has a self-documented, unresolved feature gap.** Its own `SKILL.md` contains a literal `v0.1.15 TODO:` note saying it needs to support the same `--by=` and filter options that `pm-show-kanban` (the single-project version) already has. It also has a special case carved out for "non-schema todos.md (e.g., Reconciliation legacy checkbox format)" — meaning the two kanban skills have already drifted apart in capability, and at least one vault (Reconciliation Hypothesis, coincidentally the same vault this handoff originated from) is running on a legacy format the composite view has to special-case.

3. **Legacy checkbox format silently blocks task CRUD.** `pm-list-tasks`'s own output includes a documented note: when `todos.md` is in legacy checkbox format, full task CRUD via `pm-add-task`/`pm-update-task` "not available." This is a real, self-acknowledged rough edge for any vault (including, again, Reconciliation Hypothesis) that predates the current schema — worth a migration skill (`pm-migrate-todos-schema` or similar) rather than leaving legacy vaults permanently read-only for task edits.

4. **The claim → work → release → promote → process-inbox chain has no bulk or preview operations.** The standard flow (`pm-claim-file` → edit → `pm-release-file` → `pm-create-promotion-request` → librarian's `pm-process-inbox-item`) is entirely one-item-at-a-time across at least four separate skill invocations, with no batch variant for any of them and no "preview the diff of what a promotion request would change" step before `pm-process-inbox-item` applies it. For a vault with frequent multi-file promotions, a `pm-batch-promote` (accepting a list of files/cover-notes) or a `--dry-run` preview flag on `pm-process-inbox-item` would cut a lot of repeated invocations.

5. **Force-releasing someone else's stale claim isn't distinguished from releasing your own.** `pm-release-file`'s documented "chat ended mid-claim and never released" scenario uses the exact same code path as a normal self-release, with no extra confirmation or audit note for the "this wasn't my claim" case — a plausible source of an accidental unlock going unnoticed, worth a distinct flag/warning path.

6. **Inconsistent `--all`/registry-wide support across otherwise-parallel skills.** `pm-run-drift-check`, `pm-enable-project`, and `pm-disable-project` all support acting across every registered project at once, but `pm-migrate-to-shared-tool` (a comparable one-time, per-project operation) does not — a `--all` mode there would match the pattern already established elsewhere in the plugin and save a manual loop over every registered vault when the plugin gets its next embedded-to-shared migration.

### Recommendation on how to use this addendum

Given the verification above, Fix 1 and Fix 2 as originally scoped are both still worth building, with the corrections noted (Fix 1 is schema-migration-sized work, not a small patch; Fix 2's exclude mechanism doesn't need a rewrite, just currency and the self-diagnosing mode already proposed). Of the six new items, #2 and #3 are the strongest near-term candidates since they're self-documented gaps already acknowledged in the plugin's own `SKILL.md` files (not speculative), and both directly affect the Reconciliation Hypothesis vault specifically since it's on the legacy schema. #4 is the highest-leverage new idea if promotions/claims happen often in daily use, but would need usage evidence (how often are multi-file promotions actually done?) before committing engineering time, the same evidentiary bar the original handoff applied to its own two fixes.
