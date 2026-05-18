# writing-cowork — development handoff

**Created:** 2026-05-13
**Purpose:** First-message context for any new Claude chat picking up writing-cowork plugin development. Self-contained — no need to read the chat history that produced this handoff.

---

## What writing-cowork is

A Cowork plugin that wraps a multi-role cowork pattern (PM, substance, voice/tone, review) for long-form writing projects. The plugin provides skills (verbs) invokable from any chat in a writing project's vault; a "main project chat" orchestrates by invoking skills and spawning specialist chats for sustained dialog work.

The pattern was developed and validated through manual implementation in two pilot projects: **Reconciliation Hypothesis** (the canary; most-developed) and **Epistemology** (lifted from Reconciliation 2026-05-13). Plugin formalizes what was manually scripted across those projects.

## What's already built (don't redo)

- **`~/code/cowork-tools/`** — separate runtime repo. Contains `drift_check.py` (multi-project YAML-driven vault drift check) and `lift/` (procedure docs for manual process lifts). The plugin will INVOKE cowork-tools scripts via its skills; cowork-tools is a runtime dependency, not part of the plugin.
- **Reconciliation Hypothesis** vault at `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Reconciliation Hypothesis/` — the source pattern. Has charter, handoff, ownership table, drift_check.yaml (after migration), full data-management scaffold, voice/tone workstream, substance/analytical work.
- **Epistemology** vault at `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Epistemology/` — lifted derivative. Has same scaffold, project_hub.md authored fresh, drift_check active via shared cowork-tools.
- **`~/.config/cowork/registry.yaml`** — per-machine registry of projects the shared drift_check operates over.
- **`~/Library/LaunchAgents/com.cowork.driftcheck.plist`** — nightly drift check launchd job running shared script.

## The design

**Primary reference:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Reconciliation Hypothesis/_scratch/writing_cowork_plugin_v1_design.md`

Read it first. Contains:

- Five release subsets (MVP + Cross-role visibility + Voice/tone + Review + Substance).
- 58 v1 skills enumerated with brief interface contracts.
- Per-subset gating checklists (criteria for "Reconciliation passes, release to Epistemology").
- 12 locked design decisions (substrate, repo, scope, metric, parallelization, plus 7 question-locks).

**This handoff is a routing doc; the design doc is the authoritative spec.**

## Immediate next actions

1. **Create the plugin repo.** `~/code/writing-cowork/` with git init (not separate-git-dir; this is NOT iCloud-synced). Then `gh repo create jamieburns/writing-cowork --private` (use the no-`--source` pattern per phase1 recovery learning — see design doc § MVP).

2. **Scaffold the plugin directory structure:**
   ```
   writing-cowork/
   ├── README.md             (user-facing description; defer until skills exist)
   ├── HANDOFF.md            (this file, moved into repo at creation)
   ├── plugin.yaml           (or whatever Cowork plugin manifest format requires)
   ├── skills/
   │   ├── pm/               (Subset 1 + 2 skills)
   │   ├── voice/            (Subset 3 skills)
   │   ├── review/           (Subset 4 skills)
   │   └── substance/        (Subset 5 skills)
   ├── templates/            (markdown templates installed into projects by setup skills)
   └── docs/
       ├── drift_remediation_guide.md
       ├── triage_classes_default.md
       └── agentic_perspectives/
   ```
   Verify against Cowork's plugin layout spec — the structure above is a sketch.

3. **Write the first skill: `setup-project`.** It's the orchestrator that invokes all setup sub-skills, so its contract locks the contract for everything beneath it. Start here even though it depends on sub-skills not yet written — sketching `setup-project`'s interface forces the right sub-skill interfaces.

4. **Implement setup sub-skills** in dependency order: `init-vault`, `init-git`, `init-github`, `install-charter`, `install-handoff`, etc. Each is a separate skill folder under `skills/pm/`.

5. **Continue through Subset 1 (MVP Foundation) skills**, then Subset 2 (MVP Planning) skills. Together = MVP. 35 skills total.

6. **Migrate Reconciliation** to use the MVP skills (using `migrate-to-shared-tool` skill once written) — Reconciliation is the canary. Apply gating checklist from design doc § MVP.

7. **Release MVP to Epistemology** after Reconciliation passes gating.

## Outstanding items from the prior chat

- **Task #17 — voice/tone lift to Epistemology.** Apply script ready at `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Reconciliation Hypothesis/_scratch/epistemology_voice_lift_apply.sh`. Writer said "run it." Not blocking plugin work — can run any time. If skipped, Subset 3 (Voice/tone skills) will handle Epistemology's voice setup when that subset ships.

- **Reconciliation drift_check migration** to shared cowork-tools. Memo in Reconciliation's `inbox/promotion/from_epistemology_lift_2026-05-13.md` describes the target. Plugin's `migrate-to-shared-tool` skill (in MVP) handles this. Target: roughly 2026-06-03 (after canary). If MVP ships before then, do via the skill. If not, do manually per the memo's instructions.

- **Absence audit for Epistemology** triggers at first substantive commit OR 2026-07-08, whichever first. Plugin's `run-absence-audit` skill (Subset 2 Cross-role visibility) handles this. If that subset is shipped by trigger time, run it via the skill; otherwise manual per Epistemology's `variations_from_reconciliation.md` § Checkpoint #2.

- **Voice/tone Mode A/B/C terminology** in Epistemology's voice_handoff.md still uses old "Mode A/B/C" names. When Voice/tone skills land (Subset 3), update the handoff to use descriptive skill names (`run-mechanical-pass`, `audit-terminology`, `shift-terminology`).

## Conventions inherited from manual phase

- **Atomic file writes.** Skills that modify tracked files write to `<file>.tmp`, then `mv` to `<file>`. Avoids torn reads from concurrent operations (e.g., kanban view + skill update).
- **Commit prefixes.** `[data-mgmt]` for librarian/PM mechanical work; `[lift]` for lift-sequence commits; `[voice]`, `[substance]`, `[reader-review]` for specialist context work; `[writer]` / `[obsidian]` for writer's direct edits; `[promotion]` for inbox arrivals.
- **Scratch convention.** `_scratch/`, folders named `scratch/` at any depth, files prefixed `_`, files with `.scratch.md` extension — all gitignored.
- **No-`--source` flag for `gh repo create`; use HTTPS remote.** Use `gh repo create <slug> --private` then `git remote add origin https://github.com/<owner>/<slug>.git` then `git push -u origin main`. The `--source=.` flag is incompatible with `--separate-git-dir` (phase 1 learning). HTTPS remote (not SSH) is correct for this machine — `gh auth login` configures git's credential helper to inject the gh token on HTTPS pushes; no SSH key is set up by default. Do not substitute `git@github.com:<owner>/<slug>.git` (writing-cowork repo creation learning, 2026-05-17).

## Cowork-tools relationship

The plugin INVOKES cowork-tools scripts; cowork-tools doesn't depend on the plugin. Specifically:

- `run-drift-check` skill → invokes `~/code/cowork-tools/drift_check.py`.
- Eventual `package-deliverable` skill (v2/v3) → will invoke a future `~/code/cowork-tools/build-template/` (separate workstream).
- Lift procedure at `~/code/cowork-tools/lift/` is documentation, not invoked by skills.

cowork-tools is the staging area for new capabilities. New runtime tooling sketched there manually; mature implementations get wrapped as skills in the plugin.

## Writer context (memory-resident; restated here for self-containment)

- Writer is methodical, technical, direct. Match that register.
- Prose discipline: state position + substantiate; don't pad with hedges or reviewer-invitation language.
- Writer welcomes claim-strength challenge (overstates strength at substance level; gentle pushback welcomed).
- Voice has three modes (Connect / Convince / Convey); voice register varies per mode.
- Word-economy compression (dropping prepositions, partial words) is residue to eliminate, not voice feature.
- Drift framing: categorize drift (intentional / incidental / lost-way / linguistic-style / substance) for writer adjudication; don't prevent. Substance drift is the boundary.

## Project portfolio context

Writer has at least four writing projects similar to Reconciliation that will eventually consume this plugin, plus one HW/SW project in early stages and one SW project that may or may not adopt the pattern. The plugin is built for the writing projects first; HW/SW projects revisited later. This is why the plugin is named `writing-cowork` rather than generic `cowork`.

## How to start

1. Read this handoff fully.
2. Read the design doc (`writing_cowork_plugin_v1_design.md` — path above).
3. Confirm understanding with writer; surface any questions about the design before starting development.
4. Begin Action #1 above (create the plugin repo).
5. Open a Cowork session with `~/code/writing-cowork/` as workspace once the repo exists; do development from there.

## Open items at handoff

- Cowork plugin layout spec — verify the directory structure sketched above matches what Cowork expects. If different, adapt.
- "Release to Epistemology" — locked as plugin install + minimum doc update (handoff docs point at skills, deeper revisions organic). Confirm understanding.
- Three deferred-to-implementation items: skill description text (per-skill review at implementation time), MVP open questions all locked, Subset gating checklists all defined in design doc.

Welcome to the build. The design's done; the architecture's clear; the gating is concrete. Now it's making it work.
