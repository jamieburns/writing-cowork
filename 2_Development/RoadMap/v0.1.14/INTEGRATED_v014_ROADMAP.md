# writing-cowork v0.1.14 — Integrated Roadmap
**Baseline:** v1 design + findings from Authority/Epistemology active-project adoption

**Release principle:** Fix operational friction on active projects + ship next architectural piece (Subset 4 Review) + integrate drift as observability substrate.

---

## Part 1: ARCHITECTURE INTEGRATION — Review Skills (Subset 4)

### Context: v1 Design vs. Active-Project Findings

**v1 Design (Subset 4 — Review) proposes 9 skills:**
- `run-agentic-review <scope> [--perspectives=...]` — agentic review execution
- `synthesize-reviews <scope>` — combine agentic reviews
- `run-gap-analysis <scope> --against=<target>` — gap reporting
- `ingest-human-review <feedback-file> [--reviewer-id=...]` — ingest feedback
- `triage-review <review-file>` — classify findings
- `draft-reviewer-response <reviewer-id> [--items=...]` — reply to human reviewers
- `handoff-feedback-for-integration <source-id> --target=...` — send findings to substance/voice
- `update-reviewer-tracking <reviewer-id> --status=...` — track reviewer engagement
- `list-reviewer-status [--status=...]` — show reviewer tracking

**Active-Project Findings (Review chat 2026-05-21) propose a different angle — cycle management:**
- `review-spawn-cycle <artifact> <methodology> <persona>` — set up fresh review context
- `review-log-cycle` — record cycle in log.md + create findings file
- `review-promote-findings <cycle-id>` — send findings to inbox/promotion/
- `review-add-human-reviewer <name> <profile>` — manage reviewer roster
- `review-prep-reader-bundle <cycle-id>` — specify content selection for reader review
- `review-show-queue` / `review-show-log` — cycle visualization

### **INTEGRATION DECISION: Both patterns are needed. They're complementary.**

**Proposed unified Subset 4 (13 skills total):**

#### **Cycle Management Layer (outer loop)**
- `review-spawn-cycle <artifact> <methodology> [--persona=<name>]` — initialize review context (agentic or human)
- `review-log-cycle` — record cycle + auto-create findings file
- `review-show-queue [--status=pending|in-progress|complete]` — upcoming cycles
- `review-show-log [--by=cycle-date|methodology|persona]` — cycle history
- `review-add-human-reviewer <name> <profile-path>` — manage reviewer roster
- `review-prep-reader-bundle <cycle-id>` — Review specifies content selection; returns manifest for PM to package

#### **Feedback Workflow Layer (inner loop per cycle)**
- `run-agentic-review <scope> [--perspectives=friendly,neutral,hostile|custom]` — execute agentically
- `synthesize-reviews <scope>` — combine agentic outputs
- `ingest-human-review <feedback-file>` — struct ingest of human feedback (no normalization)
- `triage-review <review-file>` — classify per project's triage classes
- `draft-reviewer-response <reviewer-id> [--items=...]` — reply to humans
- `handoff-feedback-for-integration <source-id> --target=substance|voice` — promote to substance/voice
- `update-reviewer-tracking <reviewer-id> --status=read|triaged|responded|integrated` — track engagement

#### **Why this structure works:**
- Cycle management (outer) handles "what are we reviewing and when"
- Feedback workflow (inner) handles "how do we process feedback once we're reviewing"
- Mirrors how Authority's Review chat actually works (cycles → agentic → triage → promote)
- Gating checklist from v1 design still applies; findings add cycle-tracking requirements

---

## Part 2: DRIFT AS OBSERVABILITY INFRASTRUCTURE

### New Drift Checks (runtime enhancements to `drift_check.py`)

**Two new checks in `drift_check.yaml` + minor bug fix:**

#### **1. `cross_phase_dependency_change` check**
- **What:** diffs todos.md `depends-on` column since last drift run; flags any new dependency spanning phase boundaries
- **Why:** Epistemology found tasks shifting to later phases silently (e.g., Phase 3 task newly depends on Phase 5)
- **Surfaces:** drift report's Attention block + hub Attention section
- **Config:** threshold settable (default: warn on any cross-phase; could be "warn on backward-phase only")

#### **2. `workstream_status_staleness` check**
- **What:** scans `project_hub.md` for `<!-- ROLE-STATUS-START/END -->` blocks; timestamps each; flags blocks not updated > N days
- **Why:** Status blocks can freeze if a chat goes idle; PM needs to know this
- **Surfaces:** drift report's Attention block + hub Attention section
- **Config:** threshold settable (default: 14 days)
- **Prerequisite:** pm-setup-project must scaffold the status blocks per vault-side convention (see below)

#### **3. Minor fix: `.gitkeep` inflation in inbox counts**
- **What:** `drift_check.py` currently counts `.gitkeep` in folder counts (inbox/promotion/, inbox/hub-updates/, etc.)
- **Current behavior:** empty inbox/promotion/ shows as "promotion: 1" instead of "promotion: 0"
- **Fix:** exclude dotfiles from counts (2-line change in count site)

### Why drift is foundational:
- Review cycles produce lots of state changes (queue.md, log.md, findings/)
- PM needs to notice changes across all chats (analysis, review, voice)
- Drift is the only always-running observer; it should surface what matters
- These checks close gaps in observability for active projects

---

## Part 3: SUBSTANCE / ANALYSIS ROLE CLARIFICATION

### **Decision: Doc-only approach (Option B)**

**Reasoning:**
1. Reconciliation's model (substance = conversational + handoff via inbox) is **working**
2. Authority/Epistemology adopted successfully using **same handoff model** (no analysis-* skills needed yet)
3. Root issue was **naming confusion** (plugin terminology collapsed PM and analysis), not missing skills
4. Subset 5 skills (`capture-decision-lock`, `rename-concept`, `lock-phase`) are **genuinely substance-focused**, not analysis-workflow-focused
5. Analysis work IS happening in Authority; it just happens in a separate Analysis chat + hands off via inbox/promotion/

**Implementation:**
- Rename Subset 5 from "**Substance**" to "**Substance** (and Analysis Artifact Integration)"
- Add three documentation sections:

1. **`templates/charter.md` — add § "Substance and Analysis Roles"**
   - PM does project structure and logistics
   - **Substance** does artifact manipulation (lock decisions, rename concepts, close phases) — via dedicated chat
   - **Analysis** does analytical work (claims, arguments, framing) — via dedicated chat
   - Both hand off to PM via `inbox/promotion/` (promotes → PM integrates via `process-inbox-item`)
   - No plugin-side analysis-* skills; analysis is conversational outside plugin

2. **`templates/for_other_contexts.md` — add § "Substance and Analysis Coordination"**
   - Substance pushes back on substance things (claim strength, scope, framing)
   - PM pushes back on process things (askewness, delegation-back, clarity)
   - Analysis hands off findings; PM routes to substance or voice

3. **`skills/pm-*` descriptions — add cross-reference**
   - "The plugin covers PM, Substance, Voice, and Review roles. Analysis work is conversational (outside plugin); analysis handoffs occur via `inbox/promotion/`."

**Result:** Subset 5 ships as-is (3 skills), but context makes clear this is Substance artifacts, not Analysis process. No future confusion.

---

## Part 4: PLANNING ENHANCEMENTS

### **A. `pm-init-todos` schema update**

Current schema: `| ID | Description | Milestone | Status | Added | Notes |`

**Updated schema:** `| ID | Description | Milestone | Assignee | Status | Added | Notes |`

- **New Assignee column:** captures which chat owns each task
- **Default values per project:** auto-populated from project's role-taxonomy (pm, analysis, review, voice, writer, or compounds like pm+writer)
- **Queryable:** allows `--assignee=analysis` filters
- **Epistemology uses this already** (ad-hoc); now templated upstream

**Implementation:**
- Update `pm-init-todos` to generate schema with Assignee column
- Update `pm-add-task` to accept `--assignee=<value>` argument
- Update `pm-update-task` to accept `--assignee` changes
- Update `pm-list-tasks` to support `--assignee` filtering
- Update `pm-show-kanban` + `pm-show-composite-kanban` to render Assignee column + support `--by=assignee` grouping

---

### **B. `pm-init-review-tracking` → `pm-init-review-workflow` (rename + extend)**

**Current:** creates `process/active/reviewer_tracking.md` only

**Extended:** scaffolds the **4-file Review workstream disposition** (vault-side innovation 2026-05-21):
- `process/review/queue.md` — upcoming cycles (agentic + human)
- `process/review/log.md` — cumulative cycle log with four-file relationship documented in header
- `process/review/findings/` — per-cycle findings (YYYY-MM-DD_<artifact>_<persona>.md)
- `process/active/reviewer_tracking.md` — per-human-reviewer engagement state (already exists)

**Why:** Authority/Epistemology discovered this layout; it's general. Scaffolding it prevents re-invention.

**Skill rename:** `pm-init-review-tracking` → `pm-init-review-workflow` (better reflects scope; workflow = queue + log + findings + tracking)

---

### **C. Workstream Status Block Scaffolding**

**Vault-side convention (2026-05-16):** active chats maintain `<!-- ROLE-STATUS-START/END -->` blocks in `project_hub.md`

**Plugin integration:**
- `pm-setup-project` detects project's role-taxonomy (from charter + for_other_contexts)
- Auto-generates skeleton blocks: `<!-- PM-STATUS-START/END -->`, `<!-- ANALYSIS-STATUS-START/END -->`, etc.
- Documents convention in `templates/for_other_contexts.md` § Workstream Status Blocks

**Why:** eliminates manual block setup; gives chats a template to fill in

---

## Part 5: ISSUE #2 INTEGRATION — Kanban Rendering (CSS Grid)

**Current:** pm-show-kanban uses dataviewjs with horizontal scroll (v0.1.8+)

**Issue #2 proposal:** rewrite to CSS Grid auto-fit for better responsive layout

**Implementation plan (per Issue #2 body):**
1. Rewrite Dataview query template to CSS Grid auto-fit columns
2. Ship new `templates/kanban-fullwidth.css` snippet (escapes Obsidian's line-length limit when needed)
3. Add `cssclasses: kanban-fullwidth` frontmatter option to kanban view
4. Apply same treatment to `pm-show-composite-kanban`

**Effort:** 3-4 hours. **Gating:** needs Obsidian testing on actual projects.

**Timing in v0.1.14:** Yes, pair with Assignee column work (both touch kanban rendering).

---

## Part 6: DOCUMENTATION UPDATES

### **Template Updates (existing files)**

**1. `templates/charter.md`**
   - § "Librarian == PM" clarification (older Reconciliation charters separated these roles)
   - § "Substance and Analysis Roles" (see Part 3)
   - § "Mode Boundary Enforcement" — PM actively pushes back on askewness, delegation-back, clarity
   - § "Substance vs. Process Pushback" — substance chats pushback on substance; PM on process

**2. `templates/for_other_contexts.md`**
   - § "Substance and Analysis Coordination" (see Part 3)
   - § "Chat-Managed Workstream Status Blocks" — convention + template
   - § "Reader-Bundle Generation Split" — Review selects content; PM packages artifact
   - § "Two-Axis Phase Model" — guidance for projects needing both substance phases + process phases
   - § "Memory-File Refresh at Role-Shift" — filename stable, frontmatter slug changes, HTML comments explain
   - § "Cross-Context Workflows" — inbox/promotion/ protocol for hand-offs

**3. `templates/tagging_conventions.md`**
   - § "When to Snapshot-Tag" — examples: lift completion, baseline-end trigger, pre-mass-edit, structural reorganization, operational-mode shift

**4. Create `templates/process_data_management/workstream_status_block_convention.md`**
   - OR weave directly into for_other_contexts § Workstream Status Blocks
   - Document: block per role, updated on session entry/exit, format for PM to auto-scaffold

### **Skill Description Updates (cross-references)**

Each `pm-init-*` skill description adds:
- "Maps to lift procedure stage X" (links back to `~/code/cowork-tools/lift/README.md`)

Optional: one top-level doc in plugin enumerating the full lift → plugin mapping.

### **Charter Template Addition: Review & Substance**

- Charter gets pre-populated section for Review workflow (agentic + human cycles, reader review)
- Charter mentions Substance + Analysis coordination model

---

## Part 7: GATING CHECKLIST FOR v0.1.14

### **Subset 4 (Review) — from v1 design**
- [ ] All 13 Review skills install and discoverable
- [ ] `review-spawn-cycle` + `review-log-cycle` work on test cycle (agentic)
- [ ] Cycle log renders cleanly in Obsidian
- [ ] `review-prep-reader-bundle` generates manifest; PM can package from it
- [ ] `run-agentic-review` produces 3 review files (friendly/neutral/hostile)
- [ ] `triage-review` classifies correctly per project's triage classes
- [ ] `handoff-feedback-for-integration` promotes findings to inbox/promotion/
- [ ] Reviewer tracking maintained across full cycle
- [ ] PM workflow exercise: spawn → run → triage → promote → integrate (using only skills)

### **Drift infrastructure**
- [ ] `cross_phase_dependency_change` check runs; detects cross-phase new dependencies
- [ ] `workstream_status_staleness` check runs; flags stale blocks
- [ ] Inbox folder counts exclude `.gitkeep`; empty inboxes show "0"
- [ ] Drift report surfaces Attention items cleanly

### **Planning enhancements**
- [ ] Todos.md with Assignee column renders correctly
- [ ] `pm-add-task --assignee=analysis` works
- [ ] Kanban renders Assignee column
- [ ] Kanban CSS Grid layout responsive (Issue #2)
- [ ] Workstream status blocks auto-scaffold on setup

### **Substance/Analysis clarification**
- [ ] Charter + for_other_contexts document the coordination model
- [ ] Authority/Epistemology PM can point to docs when onboarding Analysis chat
- [ ] No confusion about whether Analysis needs plugin skills

### **Documentation**
- [ ] All six template sections readable and coherent
- [ ] Lift procedure ↔ plugin cross-reference complete
- [ ] No orphaned references to old role terminology

### **Integration**
- [ ] Authority/Epistemology PM can read "here's how Review skills work with your cycle process"
- [ ] Authority/Epistemology PM can read "here's how drift now alerts you to stale status blocks"
- [ ] Reconciliation PM sees no regressions in existing workflows

---

## **SUMMARY: v0.1.14 Scope**

| Category | Items | Effort | Notes |
|----------|-------|--------|-------|
| **Review Skills (Subset 4)** | 13 skills (cycle mgmt + feedback workflow) | 10-12 hrs | Gating checklist from v1 + cycle requirements |
| **Drift Infrastructure** | 2 new checks + gitkeep fix | 4-5 hrs | observability for active projects |
| **Planning Enhancements** | Assignee column + review-workflow init + workstream blocks + Issue #2 | 6-8 hrs | Active-project friction relief |
| **Substance/Analysis Doc** | Charter § update + for_other_contexts § additions | 3-4 hrs | Role clarity |
| **Template Updates** | 6 sections across 4 templates | 4-5 hrs | Cross-referenced, consistent |
| **Skill Description Updates** | Lift procedure cross-reference | 1-2 hrs | Upstream linkage |

**Total v0.1.14 effort: 28-36 hours**

**Parallelization opportunity:** Review skills (10-12 hrs) can run in parallel with Drift (4-5 hrs) + Planning (6-8 hrs) while Docs (7-9 hrs) happen in parallel.

---

## **NEXT: DECIDE BREAKDOWN & PRIORITY**

Questions for you:

1. **Does this integration (Review + drift + planning + substance-docs) feel complete?** Any gaps?

2. **Which pieces are most urgent for Authority/Epistemology?**
   - Review skills (they need these now)
   - Drift enhancements (operational observability)
   - Assignee column (task queryability)
   - Substance/Analysis docs (onboarding clarity)

3. **Rhythm:** Would you prefer:
   - **Option A (one chunky 28-36 hr release)** — wait for everything, release all at once
   - **Option B (two releases)** — e.g., Review + Drift (14-17 hrs) in v0.1.14a, then Planning + Docs in v0.1.14b
   - **Option C (three slices)** — e.g., Review (10-12), then Drift + Planning (10-13), then Docs (7-9)

4. **v0.1.15 — what goes there?**
   - Setup-time issues (FDA, PyYAML, iCloud, migrate-existing-project) — 8-10 hrs
   - Nice-to-have (checkpoint, stand-up-brief) — 4-5 hrs
   -pm-version self-referential staleness — 1-2 hrs

Once you answer #1-4, I'll break down into detailed sprint tasks.
