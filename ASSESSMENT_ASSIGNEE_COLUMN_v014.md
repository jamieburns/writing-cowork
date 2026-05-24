# Assessment: Assignee Column for v0.1.14

## What's on the table

**Current todos.md schema:** `| ID | Description | Milestone | Status | Added | Notes |`

**Findings proposal:** add **Assignee column** (between Milestone and Status) to track which chat owns each task, making task ownership queryable across multi-chat projects.

**Active-project finding:** Epistemology project discovered this need ad-hoc and implemented it locally; now templating upstream.

---

## Current State

### Today's todos.md Schema

```
| ID | Description | Milestone | Status | Added | Notes |
```

**Current use:** tracks task description, which phase/milestone it belongs to, completion state, when added, and miscellaneous notes.

**Missing:** no explicit ownership/assignment tracking. In multi-chat projects (PM, Analysis, Review, Voice), tasks scatter across chats and nobody has authoritative view of "who owns what."

**Current workaround (Authority/Epistemology):** tasks use the Notes column informally, e.g., "assigned to voice chat" — not machine-queryable.

---

## Findings Proposal: Assignee Column

### Proposed Schema

```
| ID | Description | Milestone | Assignee | Status | Added | Notes |
```

**New column position:** between Milestone and Status (logically: "what phase" → "who does it" → "how far along")

**Values:** drawn from project's **role-taxonomy** (defined in charter + for_other_contexts.md)
- Examples: `pm`, `analysis`, `review`, `voice`, `writer`, or compounds like `pm+writer`, `analysis+voice`
- Default values: auto-populated per-project from role-taxonomy on project setup
- Can be empty/unassigned if task isn't yet claimed by a role

**Queryability:** enable filters like `pm-list-tasks --assignee=analysis` to show all analysis-owned tasks

**Rendering:** kanban board should display Assignee column and support `--by=assignee` grouping option

---

## Findings from Active Projects (Authority, 2026-05-21)

### **Observation: Task ownership is invisible in multi-chat projects**

**Current situation:**
- Epistemology PM creates tasks in todos.md; chats work them
- Analysis chat owns some tasks; Review owns others; Voice owns others
- PM has no query to answer "what does Analysis chat own right now?"
- PM has to manually read todos.md and infer from task description ("draft analysis of chapter X" = probably Analysis)

**Discovery:**
- Epistemology added ad-hoc Assignee column locally and found it valuable
- They populate it manually on task creation: `pm-add-task "analyze X" --milestone=phase-2 --assignee=analysis`
- Allows PM to say: "show me what's on Analysis's plate" without reading every task

**Why it matters:**
- Multi-chat workload visibility — PM can load-balance or see who's blocked
- Handoff clarity — when Analysis finishes and hands off to Voice, both can see the explicit ownership change
- Queryability — enables Kanban filtering and roll-up reporting

---

## Impact Analysis

### Skills Affected

#### **1. `pm-init-todos` (current schema generation)**

**Today:** generates 6-column schema

**Change:** 
- Generate 7-column schema with Assignee between Milestone and Status
- Read project's role-taxonomy from charter + for_other_contexts.md
- Auto-populate example rows with one task per role (labeled accordingly) so users see the pattern

**Example output:**
```
| fk9d2c | Decide on framing approach | phase-1 | analysis | pending | 2026-05-20 | |
| g2k4e1 | Draft structure outline | phase-2 | pm | pending | 2026-05-20 | |
| h3l5f2 | Voice-tone calibration pass | phase-5 | voice | pending | 2026-05-20 | |
```

#### **2. `pm-add-task` (task creation)**

**Today:** accepts `description`, `milestone`, optional `status`, optional `notes`

**Change:** accept `--assignee=<value>` argument (optional; defaults to empty/unassigned)

**Example:**
```
pm-add-task "review chapter 3 for consistency" --milestone=phase-4 --assignee=review
```

#### **3. `pm-update-task` (task modification)**

**Today:** accepts `task-id` and can change `status`, `milestone`, `notes`

**Change:** accept `--assignee=<new-assignee>` to reassign tasks

**Example:**
```
pm-update-task fk9d2c --assignee=voice
```

#### **4. `pm-list-tasks` (task querying)**

**Today:** accepts optional filters like `--status=pending`

**Change:** support `--assignee=<value>` filtering and combined filters

**Examples:**
```
pm-list-tasks --assignee=analysis
pm-list-tasks --status=in-progress --assignee=voice
pm-list-tasks --milestone=phase-3
```

#### **5. `pm-show-kanban` (per-project visualization)**

**Today:** renders todos.md as Dataview kanban with columns for Status (pending, in-progress, done) + shows ID, Description, Milestone

**Change:** 
- Include Assignee column in rendered output
- Support `--by=assignee` grouping option to render kanban columns as Assignee roles (instead of Status)
- Keep `--by=status` as default; allow user to switch grouping

**Modes:**
```
pm-show-kanban                              # default: Status columns (pending, in-progress, done)
pm-show-kanban --by=assignee                # Assignee columns (pm, analysis, review, voice, etc.)
pm-show-kanban --by=status --filter-assignee=analysis  # filter to only analysis-owned tasks
```

#### **6. `pm-show-composite-kanban` (cross-project visualization)**

**Today:** aggregates todos.md from all registered projects; renders kanban by Status

**Change:** same as pm-show-kanban — support Assignee column display + `--by=assignee` grouping

---

## Implementation Considerations

### **A. Role-Taxonomy Sourcing**

**Where does Assignee get its allowed values?**

Option 1: Hardcoded list (pm, analysis, review, voice, substance, writer, librarian + combinations)
- Pros: simple, predictable
- Cons: inflexible if project invents new roles

Option 2: Read from charter.md (charter lists the roles participating in this project)
- Pros: project-specific, flexible
- Cons: requires parsing charter; charter format must be stable

Option 3: Read from for_other_contexts.md (lists coordination model + role definitions)
- Pros: same as Option 2
- Cons: same as Option 2

**Recommendation:** Option 2 or 3. Charter already lists roles in the "Roles" section. pm-init-todos can read that section + default example Assignee values accordingly.

---

### **B. Default Values at Setup Time**

**Should `pm-init-todos` auto-populate Assignee column with example values?**

Option 1: All rows blank (user fills in manually)
- Pros: no assumptions
- Cons: user has to fill in; might be slow

Option 2: Auto-populate one example per detected role (e.g., one pm task, one analysis task, one voice task)
- Pros: shows the pattern; users can copy/paste structure
- Cons: adds example rows user has to clean up

**Recommendation:** Option 2. Show one task per detected role as a template, with a comment like "Delete these examples and add your own tasks."

---

### **C. Kanban Rendering: Status vs. Assignee Grouping**

**Current kanban groups by Status (pending, in-progress, done) — should Assignee be an alternative grouping or an additional column?**

Option 1: Additional column (always show Assignee alongside Status grouping)
- Pros: no breaking change; Status remains primary grouping
- Cons: more cluttered; two dimensions at once

Option 2: Alternative grouping (--by=assignee switches from Status columns to Assignee columns)
- Pros: cleaner; users choose what they want to see
- Cons: different view mode; needs docs/examples

**Recommendation:** Option 2. `--by=status` (default) groups by Status; `--by=assignee` groups by Assignee. Users can switch based on what they need to see.

---

### **D. Composite Kanban: Cross-Project Aggregation**

**`pm-show-composite-kanban` pulls todos.md from multiple projects. Should filtering/grouping work across projects?**

Example:
```
pm-show-composite-kanban --by=assignee
# Shows all tasks from all projects grouped by assignee
# (might reveal "analysis" has 20 tasks across Authority + Reconciliation projects)
```

**Recommendation:** Yes. Composite kanban should support `--by=assignee` grouping and `--filter-assignee` filtering. Reveals load distribution across projects.

---

## Integration with Draft Assignee Tracking

**Note:** Assignee column is **task-level** ownership (which chat owns this task). It's separate from:
- **Reviewer tracking** (`reviewer_tracking.md`) — tracks individual human reviewers across review cycles
- **Claim/release tracking** (`file_ownership.md`) — tracks which context claims a file during edits

These three are complementary: who owns the task (Assignee) vs. who claims the file to edit it (file_ownership) vs. who's reviewing (reviewer_tracking).

---

## Decision Points for You

**Before implementation, confirm:**

1. **Role-taxonomy sourcing:** Read from charter (Option 2/3), or hardcoded list (Option 1)?

2. **Auto-populate examples at setup time?** (Option 1: blank, Option 2: examples per role)

3. **Kanban grouping strategy:** `--by=assignee` alternative mode (Option 2), or always-visible Assignee column (Option 1)?

4. **Composite kanban support:** Should `pm-show-composite-kanban` support `--by=assignee` and cross-project aggregation? (Likely yes, but confirm)

5. **Any other Assignee-column use cases** Authority/Epistemology have observed that aren't covered above?

Once locked, I'll detail implementation specs for each skill.

---

## Gating Checklist (for later)

- [ ] Todos.md schema includes Assignee column (between Milestone and Status)
- [ ] `pm-init-todos` generates schema with example tasks per detected role
- [ ] `pm-add-task --assignee=<value>` works; defaults to blank
- [ ] `pm-update-task --assignee=<value>` works; changes ownership
- [ ] `pm-list-tasks --assignee=<value>` filters correctly
- [ ] `pm-list-tasks --assignee=analysis --status=pending` supports combined filters
- [ ] `pm-show-kanban --by=status` groups by Status (default)
- [ ] `pm-show-kanban --by=assignee` groups by Assignee
- [ ] Kanban renders Assignee column in both views
- [ ] `pm-show-composite-kanban` supports same grouping/filtering
- [ ] Cross-project Assignee aggregation works (PM can see all analysis tasks across projects)
- [ ] Existing status-based kanban queries still work (backward compatible)
