# v0.1.14 Decision Lockdown

**Date:** 2026-05-23 | **Status:** Locked | **Author:** Autonomous review

---

## Assessment 1: Review Skills (Subset 4)

### Decision 1.1: Integration Approach

**LOCKED: Option A — Integrate both sets (13 skills total)**

**Rationale:**
- Authority (active project) has validated need for cycle management (queue/log/promote pattern)
- They also need in-cycle feedback processing (agentic review, triage, response)
- Both layers are complementary: outer loop (cycle lifecycle) + inner loop (feedback workflow)
- Size (13 skills) is proportionate to PM (35) + Voice (9); Subset 4 becomes ~25% of full plugin
- Full end-to-end coverage justifies scope expansion

**Implementation:** Deliver as unified Subset 4 with 13 integrated skills, updated gating checklist

---

### Decision 1.2: 4-File Review Workstream Disposition

**LOCKED: Option A — Extend `pm-init-reader-review-tracking`**

**Rationale:**
- The 4-file disposition (queue.md, log.md, findings/, reviewer_tracking.md) is general-purpose
- Should not be manual scaffolding
- Extending existing skill is simpler than creating parallel `pm-init-review-workflow`
- Keeps pm-side setup mechanics in one place

**Implementation:** 
- Rename parameter/docs for clarity, but keep skill name `pm-init-reader-review-tracking`
- Scaffold all 4 files on invocation
- Preserve backward compatibility (if called without Review context, still creates reviewer_tracking.md only)

---

### Decision 1.3: Reader-Bundle Pattern

**LOCKED: Option A — Add `review-prep-reader-bundle`, document split in `for_other_contexts.md`**

**Rationale:**
- Review role specifies bundle content (manifest)
- PM role packages it (future skill, v0.1.15+)
- Document this split so both roles understand responsibility boundary

**Implementation:**
- Include `review-prep-reader-bundle <cycle-id>` in final 13-skill list
- Add section to `for_other_contexts.md`: "Review-PM Reader-Bundle Workflow"
- No pm-package skill yet; document as forward pointer

---

## Assessment 2: Drift Enhancements

### Decision 2.1: Cross-Phase Dependency Detection

**LOCKED: Warn on ANY cross-phase dependency (not backward-only)**

**Rationale:**
- More visibility is better for multi-chat project observability
- PM can add exceptions in drift_check.yaml if a dependency is intentional
- False-alarm cost (one config line) < missed-blocker cost (project planning breaks silently)
- Conservative default (warn-on-any) with config valve (per-project threshold)

**Implementation:**
- Add `cross-phase-dependency-change` check class to drift_check.py
- Config: `warn-mode: any` (default) or `warn-mode: backward-only` (opt-in)
- Surface in hub Attention block with both source + target phase labels
- Diff todos.md via git log (durable; avoids snapshot artifacts)

---

### Decision 2.2: Status Block Staleness Timestamp Format

**LOCKED: Embedded in comment, format `<!-- ROLE-STATUS-UPDATED-YYYY-MM-DD -->`**

**Rationale:**
- Single-line format is clean, regex-queryable, PM-readable by eye
- No separate metadata files needed
- Format is unambiguous (ISO date, no parsing ambiguity)

**Implementation:**
- Template (installed by pm-setup-project): `<!-- ANALYSIS-STATUS-UPDATED-2026-05-23 -->`
- Add to all role status block headers
- Drift check scans for this pattern, extracts date, calculates staleness
- No auto-update by pm-setup-project; chat responsibility at session entry/exit

---

### Decision 2.3: Threshold (Global vs. Per-Role)

**LOCKED: Global threshold (14d default) with per-project override in `drift_check.yaml`**

**Rationale:**
- Simpler default behavior
- Per-project config allows customization without per-role complexity
- Example: Epistemology can set `threshold-days: 21` if their Review cycle is naturally longer

**Implementation:**
- drift_check.yaml config: `workstream-status-staleness: { threshold-days: 14, skip-blocks: [PM-STATUS] }`
- Can skip specific blocks if they're intentionally long-lived (e.g., PM status can be older without warning)

---

### Decision 2.4: `.gitkeep` Inflation Fix

**LOCKED: Proceed as outlined (2-line code change)**

**Rationale:**
- Straightforward, no friction
- Empty inbox folders report as 0, not 1
- No config needed; backward-compatible

**Implementation:**
- Modify `count_files()` in drift_check.py: filter out dot-files
- Effect: `os.listdir()` → filter `not f.startswith('.')`

---

## Assessment 3: Assignee Column

### Decision 3.1: Role-Taxonomy Sourcing

**LOCKED: Option 2 — Read from `charter.md`**

**Rationale:**
- Charter already lists participating roles in structured format
- Project-specific, flexible (supports custom roles)
- Easier to maintain than hardcoding
- `pm-init-todos` can parse charter's "Roles" section and auto-populate examples

**Implementation:**
- `pm-init-todos` reads charter.md, extracts role list from "Roles" section
- Uses detected roles as valid Assignee values for this project
- Fallback to sensible defaults if charter parsing fails (pm, analysis, review, voice, writer)

---

### Decision 3.2: Auto-Populate Examples at Setup

**LOCKED: Option 2 — Auto-populate one example per detected role**

**Rationale:**
- Shows pattern immediately (users can see structure)
- Reduces friction (copy-paste template vs. inventing from scratch)
- User can delete examples before first real use

**Implementation:**
- `pm-init-todos` generates one template task per detected role
- Example: `| abc123 | [Example Analysis Task] | phase-1 | analysis | pending | 2026-05-23 | Delete this and add your real tasks |`
- Include a comment row or note explaining deletion

---

### Decision 3.3: Kanban Grouping Strategy

**LOCKED: Option 2 — Alternative grouping with `--by=assignee`**

**Rationale:**
- Cleaner than always-visible column (less clutter)
- Users choose grouping based on what they need to see:
  - `--by=status` (default): "where are things in completion?"
  - `--by=assignee`: "who has what on their plate?"
- Both views render the Assignee data; just different grouping

**Implementation:**
- `pm-show-kanban --by=status` (default): group columns by Status, include Assignee in card
- `pm-show-kanban --by=assignee`: group columns by Assignee, include Status in card
- Support `--filter-assignee=analysis` to slice to one role
- Keep Status view as default for backward compatibility

---

### Decision 3.4: Composite Kanban Support

**LOCKED: Yes — Support `--by=assignee` and cross-project aggregation**

**Rationale:**
- Reveals load distribution across projects
- Example: "Show me all tasks owned by Analysis chat across all projects" = workload visibility
- Same mechanics as single-project kanban; scales to multiple projects
- Enables PM to load-balance across concurrent projects

**Implementation:**
- `pm-show-composite-kanban --by=status` (default)
- `pm-show-composite-kanban --by=assignee`: aggregates + groups by role across all projects
- `pm-show-composite-kanban --by=assignee --filter-assignee=voice`: show all voice tasks across projects

---

## Summary of Locked Decisions

| Topic | Decision | Rationale |
|-------|----------|-----------|
| **Review Skills** | Integrate 13 (cycle mgmt + feedback workflow) | Both layers proven + complementary |
| **Review Setup** | Extend `pm-init-reader-review-tracking` | Simpler than parallel skill; general-purpose |
| **Reader-Bundle** | `review-prep-reader-bundle` + doc split | Review specifies, PM packages (v0.1.15+) |
| **Cross-Phase Deps** | Warn on ANY | More visibility; PM can config exceptions |
| **Status Staleness** | Embedded timestamp `<!-- ROLE-UPDATED-YYYY-MM-DD -->` | Clean, queryable, PM-readable |
| **Staleness Threshold** | Global (14d) + per-project override | Simpler default; flexible config |
| **`.gitkeep` Fix** | Proceed (2-line filter) | Uncontroversial; solves daily friction |
| **Assignee Sourcing** | Read from charter.md | Project-specific, flexible, maintained |
| **Assignee Examples** | Auto-populate per role | Shows pattern; reduces setup friction |
| **Kanban Grouping** | `--by=assignee` alternative mode | Users choose; cleaner than always-visible |
| **Composite Kanban** | Support `--by=assignee` cross-project | Reveals workload distribution |

---

## Next Steps: Implementation Unblocked

These decisions unblock the **v0.1.14 sprint task breakdown** showing:
- Parallel execution of Review (Subset 4), Drift (enhancements A+B+C), and Assignee (column + skills) work
- Dependencies between skills (e.g., pm-init-todos changes enable pm-add-task/pm-update-task changes)
- Gating checklists for each workstream
- Estimated effort and implementation order
