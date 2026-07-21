# writing-cowork plugin v1 — design draft

**Status:** DRAFT for writer review.
**Created:** 2026-05-13
**Source enumeration:** Task #18 (PM ~38 verbs / substance 4 verbs / voice ~12 verbs / review ~9 verbs = ~63 total)
**Decision point:** scope cut for v1 + release sequencing + interface contracts + gating checklists.

---

## v1 goal

**Cover all four roles** (PM, substance, voice/tone, review) at minimum-useful skill depth per role. Per-subset gating with checklists; each subset proves in Reconciliation before releasing to Epistemology.

This is broader than a typical "v1" — it's "cover the pattern end-to-end at minimum-useful depth" rather than "ship the smallest viable thing." The reasoning: a partial v1 (e.g., PM-only) doesn't validate the multi-role architecture; you only learn what's wrong when all roles are exercising the substrate together.

## Release sequence

Five subsets after the 1+2 merger. Each subset has its own gating checklist (below). A subset is released to Epistemology only after Reconciliation passes its checklist.

| # | Subset | Skill count | Gates on |
|---|--------|-------------|----------|
| 1 | **MVP — PM (Foundation + Planning)** | 35 | Nothing (first subset) |
| 2 | **PM Cross-role visibility** | 2 | MVP in Reconciliation |
| 3 | **Voice/tone** | 9 | MVP in Reconciliation |
| 4 | **Review** | 9 | MVP in Reconciliation |
| 5 | **Substance** | 3 | MVP in Reconciliation |

**Tracking metric:** skill-count completed + subset-gate sign-offs. No calendar timelines (user-pace varies; calendar estimates would be misleading). If a specific subset needs a budgeting estimate at the time it's being scheduled, one can be produced then.

**Parallelization:** Subsets 2–5 can run in parallel after MVP ships if bandwidth allows. Sequential is simpler; parallel is faster. Default plan: sequential through Subset 2, then parallelize 3/4/5 if desired.

---

## MVP — PM (Foundation + Planning)

**Goal:** Set up new projects, manage daily PM mechanics, migrate Reconciliation off the embedded drift_check, AND provide roadmap/tasks/kanban for ongoing planning visibility. Merged from previous Subsets 1+2 because splitting created a workflow gap where mechanical PM worked but planning didn't.

### Skills

**Setup orchestration:**
- `setup-project <name> [--vault=<path>] [--git=new-github|local|existing|none]` — top-level setup. Invokes the sub-skills below in order, with rollback on failure.

**Setup sub-skills** (each invokable standalone):
- `init-vault <path>` — create folder skeleton with `.gitkeep` markers.
- `init-git [--separate-git-dir]` — git init with optional iCloud-safe layout.
- `init-github <slug> [--private]` — create remote, add origin, push. Uses no-`--source` pattern.
- `install-charter` — place charter.md from plugin template.
- `install-handoff` — place handoff.md.
- `install-for-other-contexts` — place for_other_contexts.md.
- `install-hierarchy-and-ownership` — place file_hierarchy.md + initial file_ownership.md.
- `install-drift-check-config` — place drift_check.yaml from template; prompts for project-specific values.
- `place-lift-decisions <decisions-file>` — copy the pre-lift decisions doc to vault root.
- `init-voice-handoff` — place voice_handoff.md template with project placeholders.
- `init-voice-exceptions` — create empty voice_exceptions.md.
- `init-reader-review-tracking` — create empty tracking file.
- `init-roadmap [--shape=phase|now-next-later]` — create empty roadmap.
- `init-todos` — create empty todos file.

**Registry:**
- `register-project <config-path>` — add project to `~/.config/cowork/registry.yaml`.
- `list-projects` — show registry.
- `enable-project <name>` / `disable-project <name>` — toggle registry flag.

**File ownership:**
- `claim-file <path> <context>` — set Status in ownership table.
- `release-file <path>` — clear claim on commit.
- `show-claims [--owner=...]` — list currently-claimed files.

**Drift:**
- `run-drift-check [--project=<name>|--all] [--dry-run]` — invoke `~/code/cowork-tools/drift_check.py`.

**Inbox routing:**
- `process-inbox-item <inbox-file>` — reads request (promotion or hub-update), applies, archives cover. Both sides of transfer in one skill.
- `create-promotion-request <artifact-path> [--placement=...] [--notes=...]` — sender-side; produces inbox/promotion/ entry.
- `create-hub-update-request --section=... --change=add|update|remove --content=...` — sender-side hub update.

**Tagging:**
- `tag-snapshot <name> <message>` — annotated snapshot tag + push.
- `tag-lock <date>-<name> <rationale>` — decision-lock with explicit rationale + log.

**Archive:**
- `archive-to-history <file> [--reason=...]` — move from process/active/ to process/history/ with optional rename.

**One-time migration:**
- `migrate-to-shared-tool <project>` — Reconciliation-specific need; migrates a project from embedded drift_check to shared cowork-tools.

**Planning skills (added from former Subset 2):**

**Roadmap:**
- `add-milestone <name> [--phase=...|--bucket=now|next|later] [--depends-on=<other-milestone>[,...]]`
- `update-milestone <name> [--status=planned|in-progress|done] [--depends-on=...]`
- `show-roadmap` — phase-based canonical view.
- `show-status` — Now/Next/Later derived view; highlights blockers explicitly.

**Tasks:**
- `add-task <description> [--milestone=...]`
- `update-task <id> --status=planned|in-progress|done`
- `list-tasks [--milestone=...] [--status=...]`
- `close-task <id> [--notes=...]`

**Kanban:**
- `show-kanban` — per-project kanban view (Dataview-rendered inside Obsidian).
- `show-composite-kanban` — cross-project kanban as Cowork artifact (pulls from registry).

**Scheduling:**
- `schedule-review <description> <when>` — wrapper around mcp__scheduled-tasks__create_scheduled_task.

**Total MVP skills:** 35 (24 Foundation + 11 Planning)

### Gating checklist (Reconciliation passes before releasing to Epistemology)

**Foundation gates:**
- [ ] All 24 Foundation skills install and are discoverable in Cowork.
- [ ] Each Foundation skill invoked at least once in real Reconciliation workflow.
- [ ] `setup-project` invoked on a throwaway test project; produces a clean vault matching the manual data-management lift's output.
- [ ] `resume-setup` recovers cleanly after a simulated mid-flight failure of `setup-project`.
- [ ] `migrate-to-shared-tool` successfully migrates Reconciliation from embedded drift_check to shared cowork-tools.
- [ ] `run-drift-check` produces equivalent output to the existing embedded script.
- [ ] `process-inbox-item` correctly prompts on ambiguous placement; resolves cleanly.
- [ ] `tag-lock` enforces structured message format (Why / Decision / Alternatives considered).
- [ ] No regressions in Reconciliation state (file_ownership accurate, hub Attention block updates, claim/release table consistent).

**Planning gates:**
- [ ] All 11 Planning skills install and are discoverable.
- [ ] Roadmap populated with current Reconciliation phases; `show-roadmap` reads cleanly.
- [ ] Tasks populated with current Reconciliation active work; `list-tasks` and `show-kanban` work.
- [ ] Per-project kanban renders inside Obsidian via Dataview.
- [ ] Composite kanban renders as Cowork artifact pulling from all registered projects.
- [ ] One sample `schedule-review` task fires correctly via scheduled-tasks MCP.

**Overall MVP gate:**
- [ ] PM workflow exercised end-to-end using only skills (no manual scripts) — claim → edit → release → drift-check → tag.
- [ ] Writer subjective sign-off — "this feels at least as good as the manual version, and the planning visibility adds real value."

### Open questions for MVP (locked answers from writer)

1. **`setup-project` rollback behavior on partial failure:** **leave partial state, provide `resume-setup` recovery skill.** Writer-confirmed.
2. **`process-inbox-item` ambiguity resolution:** **ask interactively.** Writer-confirmed.
3. **`tag-lock` message conventions:** **structured format enforced** (Why / Decision / Alternatives considered). Writer-confirmed.

### Open questions still pending writer adjudication

1. **Task ID generation.** Auto-incrementing integers, UUIDs, or short hashes? My read: short hashes (8 chars) — unique across projects, easy to type.
2. **Dataview query templates.** Skill installs the Dataview query file once at setup; if the writer customizes it, do future skill updates overwrite? My read: install once, never overwrite — writer customizations persist.
3. **Composite kanban refresh frequency.** Always re-pull on view, or cache for N minutes? My read: always re-pull (artifact view is opened on demand; performance is not a concern at the project counts we're discussing).

---

## Subset 2 — PM Cross-role visibility

**Goal:** Project-level digest for the PM chat's "what's happening" awareness.

### Skills

- `show-project-status [--project=...]` — composite per-project view: active milestones, open tasks, in-flight reviewer engagements, recent commits, recent locks, drift status.
- `run-absence-audit <project>` — checkpoint #2 procedure.

**Total Subset 2 skills:** 2

### Gating checklist

- [ ] `show-project-status` for Reconciliation produces a useful digest (writer agrees).
- [ ] `run-absence-audit` runs against Epistemology and produces a structured findings doc.

### Open questions for Subset 2

1. **show-project-status output format.** Markdown digest, Cowork artifact, or both? My read: markdown to stdout primarily; optional `--render=artifact` flag for visual view.

---

## Subset 3 — Voice/tone

**Goal:** Wrap voice/tone mechanics as skills, supporting both Reconciliation's substance-mature voice work and Epistemology's early-stage voice setup.

### Skills

**Mechanical:**
- `run-mechanical-pass <scope> [--ignore-exceptions]` — spelling/punctuation/grammar/typos/citation format/capitalization. Inline summary + accept-prompt protocol.
- `audit-terminology <scope> [--ignore-exceptions]` — detect-and-report only; produces report at `process/active/terminology_scan_YYYY-MM-DD.md`.
- `shift-terminology <old> <new> [<scope>]` — zone-aware X→Y; feedback-first about breakage; auto-apply in current+not-yet zones; lookback list for completed.

**Sample lifecycle:**
- `capture-voice-sample` — elicit fresh sample from writer; place at process/active/writer_voice_sample.md.
- `confirm-voice-sample` — for lifted samples; present + ask confirm-or-refresh.

**Recommendations:**
- `recommend-wording <paragraph> [--variants=N] [--voice-target=...]` — one-shot N alternatives with explicit voice-target framing.

**Exceptions:**
- `add-voice-exception <term> [--scope=project|file|section] [--in=<file or file:section>] [--reason=...]`
- `list-voice-exceptions [--scope=...] [--in=...]`
- `remove-voice-exception <term> [--scope=...] [--in=...]`

**Total Subset 3 skills:** 9

### Gating checklist

- [ ] All 9 skills install.
- [ ] `run-mechanical-pass` correctly handles: blockquotes, `::: passthrough` fenced divs, `<!-- exception -->` inline markers, project/file/section-scoped exceptions.
- [ ] `audit-terminology` produces a report Reconciliation's writer agrees is useful (vs. noise).
- [ ] `shift-terminology` zone-detection correctly distinguishes voice-edited vs. not-yet-edited sections.
- [ ] `confirm-voice-sample` on Epistemology's lifted sample produces appropriate either-confirm-or-refresh dialog.
- [ ] Writer signs off after one voice pass in Reconciliation using only skills.

### Open questions for Subset 3

1. **`shift-terminology` zone detection.** How does the skill determine which sections are voice-edited? Options: explicit marker file, commit prefix scan, file-level frontmatter, manual writer declaration per shift. My read: combination of commit prefix scan (`[voice]` prefix) + writer override per shift.
2. **Inline marker syntax.** `<!-- exception -->` per the earlier discussion. Confirm no change.
3. **Mechanical-pass scope creep.** Should the skill catch capitalization-after-period that isn't paragraph-start? Hyphenation-consistency drift? My read: yes to both; capture in `voice_exceptions.md` if they're intentional.

---

## Subset 4 — Review

**Goal:** Wrap review mechanics. Covers agentic reviews (fully) and human review ingest+triage (synthesis deferred to v2).

### Skills

**Agentic:**
- `run-agentic-review <scope> [--perspectives=friendly,neutral,hostile|custom-list]` — produces N review files.
- `synthesize-reviews <scope>` — mechanical combining of agentic reviews; v2 adds human normalization.

**Gap analysis:**
- `run-gap-analysis <scope> --against=<target>` — gap report.

**Human reviewer:**
- `ingest-human-review <feedback-file> [--reviewer-id=...]` — structured ingest report; no normalization.
- `triage-review <review-file>` — classify items per project's triage classes; works on agentic or human input.
- `draft-reviewer-response <reviewer-id> [--items=...]` — for replying to humans.
- `handoff-feedback-for-integration <source-id> --target=substance|voice --topic=...`

**Tracking:**
- `update-reviewer-tracking <reviewer-id> --status=read|triaged|responded|integrated`
- `list-reviewer-status [--status=...]`

**Total Subset 4 skills:** 9

### Gating checklist

- [ ] All 9 skills install.
- [ ] `run-agentic-review` produces three review files matching the friendly/neutral/hostile pattern Reconciliation used.
- [ ] `synthesize-reviews` produces synthesis skeleton; chat fills in verdict.
- [ ] `run-gap-analysis` against Reconciliation's hypothesis statement produces useful findings.
- [ ] `triage-review` correctly classifies items per Reconciliation's existing triage classes (substance / voice / fairness / source / marker / etc.).
- [ ] `ingest-human-review` on a sample human feedback file produces a structured ingest report.
- [ ] Tracking file maintained across at least one full review round.

### Open questions for Subset 4

1. **Triage classes — project config or skill default?** Reconciliation has detailed triage classes including theological-dissent / fairness / falsifier-layer. Generic projects have simpler classes (substance / voice / typo / suggestion). My read: skill reads `process/active/triage_classes.md` from the project; provides a sensible default if absent.
2. **`run-agentic-review` perspective definitions.** Where do the agentic reviewer prompts live? Plugin defaults (friendly / neutral / hostile) + per-project overrides at `process/active/agentic_perspectives/<name>.md`? My read: yes — plugin provides defaults; project can add or override.

---

## Subset 5 — Substance

**Goal:** Wrap substance mechanics. Smallest set (substance is mostly conversational).

### Skills

- `capture-decision-lock <name> <rationale>` — formalize substance decision (tag + log + hub update via inbox/promotion).
- `rename-concept <old> <new> [<scope>]` — substance equivalent of `shift-terminology`; zone-aware X→Y for substance terms (e.g., Reconciliation's "Cluster" → "Reflection Pattern" rename).
- `lock-phase <phase> <summary>` — close a phase: snapshot tag + hub update + checkbox flips in roadmap.

**Total Subset 5 skills:** 3 (with `check-claim-trace` deferred to v2).

### Gating checklist

- [ ] All 3 skills install.
- [ ] `capture-decision-lock` produces appropriate lock-tag + log entry on a test decision in Reconciliation.
- [ ] `rename-concept` correctly handles zone-awareness same as `shift-terminology`.
- [ ] `lock-phase` closes Phase 8 in Reconciliation (when Phase 8 closes) with correct artifacts.

### Open questions for Subset 5

1. **`rename-concept` vs. `shift-terminology` overlap.** Both are zone-aware X→Y. One difference: voice cares about voice-edited zones; substance cares about lock-status zones. Same skill with `--type=terminology|concept` flag, or two skills? My read: two skills; the zone semantics differ enough that one skill with branches obscures the difference.

---

## v2 / later (out of v1 scope)

- **PM:** `lift-process`, `tag-release`, packaging skills (depends on build-template workstream).
- **PM:** Memory management skills (TBD per writer).
- **PM:** Composite show-project-status (TBD per writer).
- **PM:** Snapshot folder management (dropped; tag skills suffice).
- **Voice:** drift/baseline comparison (`extract-voice-changes`), voice pass reporting, hub attention posting.
- **Review:** Human review synthesis (normalization layer), `generate-reviewer-package` (depends on packaging).
- **Substance:** `check-claim-trace`, analytical templates.

## Cowork-tools vs. plugin

Clean split:

**`~/code/cowork-tools/` holds:**
- `drift_check.py` — runtime, called by `run-drift-check` skill.
- `lift/` — procedure documentation (not skill-related; reference docs).
- Future: `build-template/` when packaging workstream begins.
- Future: any other shared runtime tooling.

**`writing-cowork` plugin holds:**
- Skill definitions (each skill is a folder with `SKILL.md` + supporting files).
- `templates/` — markdown templates installed into projects by setup skills.
- `docs/drift_remediation_guide.md` — the guidance doc referenced from plugin.
- `docs/triage_classes_default.md` — default project triage classes.
- `docs/agentic_perspectives/` — default perspective definitions for run-agentic-review.

**Per-project vault holds:**
- All project-specific config and state (drift_check.yaml, roadmap, todos, reviewer tracking, voice exceptions, etc.).

**Per-machine config holds:**
- `~/.config/cowork/registry.yaml` — registered projects.

The plugin INVOKES cowork-tools scripts. The plugin reads project-specific config to parameterize skill behavior. The registry is per-machine state. Clean layering.

## Plugin manifest sketch

```yaml
# writing-cowork plugin
name: writing-cowork
version: 1.0.0
description: |
  Pattern + tooling for multi-role cowork in long-form writing projects.
  Covers project management, substance, voice/tone, and review roles.

requires:
  - cowork-tools at ~/code/cowork-tools (with drift_check.py available)
  - python3 with PyYAML
  - gh (GitHub CLI) authenticated
  - git
  - launchd (macOS only currently)

skills:
  setup-project: ./skills/pm/setup-project/
  init-vault: ./skills/pm/init-vault/
  # ... (all skills enumerated)

mcp_tools:
  - mcp__scheduled-tasks__create_scheduled_task
  - mcp__Control_your_Mac__osascript

resources:
  templates: ./templates/
  docs: ./docs/
```

## Top-level decisions (writer-confirmed)

1. **Plugin substrate:** Cowork plugin. Locked.
2. **Plugin repo:** New repo `github.com/jamieburns/writing-cowork`, separate from cowork-tools. Locked.
3. **v1 scope:** all five subsets in (after 1+2 merger). Locked.
4. **Tracking metric:** skill-count + subset-gates. No calendar timelines. Locked.
5. **Parallelization:** sequential through Subset 2; subsets 3/4/5 may parallelize after MVP. Decide at the time.

## Locked decisions (full set)

1. **Plugin substrate:** Cowork plugin.
2. **Plugin repo:** New repo `github.com/jamieburns/writing-cowork`, separate from cowork-tools.
3. **v1 scope:** all five subsets in (MVP + Cross-role + Voice + Review + Substance).
4. **Tracking metric:** skill-count + subset-gates. No calendar timelines.
5. **Parallelization:** sequential through Subset 2; subsets 3/4/5 may parallelize after MVP. Decide at the time.
6. **setup-project rollback:** leave partial state; provide `resume-setup` recovery skill.
7. **process-inbox-item ambiguity:** ask interactively.
8. **tag-lock messages:** structured format enforced (Why / Decision / Alternatives considered).
9. **Task IDs:** short hash (8 chars).
10. **Dataview template overwrite policy:** install once, never overwrite — writer customizations persist.
11. **Composite kanban refresh:** always re-pull on view. Atomic file writes (`.tmp` then `mv`) in skills mitigate race conditions.
12. **"Release to Epistemology" operational definition:** plugin install + minimum doc update (handoff docs point at skills); deeper doc revisions happen organically.

## Deferred to skill-implementation time

- **Skill description text.** Cowork's skill matcher needs sharp descriptions that match natural-language phrasings. Reviewed per skill as it's implemented.

---

## Status

Design **locked**. Ready for MVP development to begin.

Next concrete step: create `~/code/writing-cowork/` repo + GitHub remote, write the first skill (`setup-project` is the orchestrator — locks the contract for all sub-skills).
