# Assessment: Drift Enhancements for v0.1.14

## What's on the table

**Current drift_check.py** (running on schedule via launchd) reports:
- Untracked files, uncommitted changes, stale branches
- Inbox folder counts (promotion, hub-updates)
- Recent commits + tags
- File ownership accuracy (claim/release consistency)

**Active-project findings** propose two new checks + one bug fix for drift observability on projects with multiple active chats.

---

## Current Drift Check Coverage

From Reconciliation's use (active since v0.1.0):

```yaml
# drift_check.yaml example
checks:
  - type: git-status           # uncommitted changes
  - type: inbox-counts        # inbox/promotion/, etc.
  - type: file-ownership      # claim/release table accuracy
  - type: recent-commits      # last 10 commits
  - type: drift-threshold     # when to alert (e.g., >3 uncommitted files)
```

**Output format:** console log + hub Attention block update in project_hub.md

**Frequency:** nightly via launchd (configurable)

**Runtime:** Python 3 + PyYAML, reads drift_check.yaml from each project

---

## Findings from Active Projects (Epistemology, 2026-05-20 to 2026-05-22)

### **Finding #1: Cross-phase task dependency changes are silent**

**Observed:**
- Epistemology has phases 1–6 (substance) + process phases (Analysis → Review → Voice)
- Tasks in each milestone can have `depends-on` references to other tasks
- If a Phase 3 task newly depends on a Phase 5 task, **project shape changes** (breaks planning assumptions)
- Currently, `pm-show-status` shows *current* state only; no **change detection**
- PM only notices if they manually inspect todos.md diff (doesn't happen)

**Why it matters:**
- Multi-chat projects have chats updating tasks in their domain
- PM needs *to notice* when cross-phase dependencies form (could indicate blocking issues)
- Rare but project-shape-affecting; warrants observability

**Proposed check:** `cross_phase_dependency_change`

```yaml
  - type: cross-phase-dependency-change
    threshold: warn-on-any              # or: warn-only-backward-phase
    report: hub-attention + drift-log   # surfaces in Attention block
```

**Implementation:**
1. On drift run, diff todos.md since last run
2. Parse `depends-on` column for each task
3. For each new/modified depends-on, check if source + target tasks are in different phases
4. If cross-phase, log as Attention item + include in drift report
5. Config option: warn on any cross-phase, or only warn on backward-phase (Phase 5 task → Phase 3 task = backward)

**Questions for you:**
- **Should this warn on ALL cross-phase dependencies, or only backward-phase (blocking) dependencies?**
  - All: more visibility; noisier (legitimate forward-phase dependencies exist)
  - Backward-only: fewer false alarms; might miss legitimate cross-phase issues
  - My read: warn on any; PM can add exception config if a cross-phase dependency is intentional

---

### **Finding #2: Chat-managed status blocks can go stale without warning**

**Observed (vault-side innovation 2026-05-16):**
- project_hub.md has `<!-- ANALYSIS-STATUS-START/END -->`, `<!-- REVIEW-STATUS-START/END -->`, etc. blocks
- Each chat (Analysis, Review, Voice) owns their block; updates on session entry/exit
- If Analysis chat goes idle for 2+ weeks, their status block freezes
- **No mechanism to surface this.** PM reads stale status block as current ground truth

**Why it matters:**
- Stale status = misrepresented project state
- PM doesn't know whether block is current or 2 weeks old
- Silent staleness is the worst failure mode

**Proposed check:** `workstream_status_staleness`

```yaml
  - type: workstream-status-staleness
    threshold-days: 14
    pattern: <!-- .+-STATUS-START.*-END -->   # regex for status blocks
    report: hub-attention + drift-log
```

**Implementation:**
1. Scan project_hub.md for `<!-- ROLE-STATUS-START -->...<!-- ROLE-STATUS-END -->` blocks
2. Extract timestamp from block header (each block should have one, e.g., "Updated 2026-05-22")
3. Compare to drift run date
4. If > threshold days (default 14), surface as Attention item
5. Config: per-project threshold (default 14); skip specific blocks (e.g., PM-STATUS can be older without warning)

**Questions for you:**
- **Should each status block have an explicit timestamp in the block header?** (Requirement for this check to work)
  - Yes: clean, queryable, PM can scan visually
  - Or embedded in comment: `<!-- ANALYSIS-STATUS-UPDATED-2026-05-22 -->`
- **Should threshold be global or per-role?** (E.g., PM status block tolerate 30d, Analysis tolerate 14d)
  - Global: simpler
  - Per-role: more nuanced

**My read:** Yes to timestamps; global threshold (14d default, override per project in drift_check.yaml)

---

### **Finding #3: `.gitkeep` inflates inbox folder counts**

**Observed:**
- Inbox folders (inbox/promotion/, inbox/hub-updates/, inbox/issues/) have `.gitkeep` to preserve empty directories
- Drift report shows: `promotion: 1` when folder is actually empty
- PM reads drift report, thinks there's an item waiting, has to verify it's just gitkeep
- Recurring friction (drift runs nightly)

**Why it matters:**
- Minor but daily; 2-line fix

**Proposed fix:**
```python
# In drift_check.py count_files():
def count_files(folder_path):
    if not os.path.isdir(folder_path):
        return 0
    files = [f for f in os.listdir(folder_path) if not f.startswith('.')]
    return len(files)
```

**Effect:** empty inboxes report as `promotion: 0`, not `promotion: 1`

**Straightforward:** no config, no decisions needed.

---

## Integration with Review Skills (Subset 4)

**Why drift matters for Review:**

Review cycle work generates lots of state changes:
- queue.md changes (new cycles added)
- log.md changes (completed cycles logged)
- findings/ grows (new findings files)
- reviewer_tracking.md changes (status updates)

**PM needs observability:**
- Drift should notice if a cycle log hasn't been updated in N days
- Drift should surface if new cross-phase dependencies form (might indicate review blocking issues)
- Drift should tell PM "Review queue has 3 pending cycles"

**Proposal:** extend drift checks to include Review-workstream metrics

```yaml
  - type: review-queue-status
    path: process/review/queue.md
    alert-on: pending-cycles-count > 5
    report: hub-attention
```

**For v0.1.14:** basic observability (stale blocks, cross-phase deps). Can add Review-specific metrics later if needed.

---

## Detailed Implementation Plan

### **A. `cross_phase_dependency_change` check**

**File:** ~/code/cowork-tools/drift_check.py (add new check class)

**Inputs:**
- todos.md from vault
- phase definitions from project (roadmap.md structure)
- drift_check.yaml config: `cross-phase-dependency-change: {warn-mode: any|backward-only, threshold: 0}`

**Algorithm:**
1. Load current todos.md
2. Load previous todos.md snapshot (stored by drift check run N-1)
3. For each row, parse milestone (determines phase)
4. For each task, parse `depends-on` column
5. For each new/changed depends-on:
   - Resolve target task's milestone
   - If source phase != target phase AND (warn-mode = any OR target phase < source phase), flag
6. Collect flagged items, append to Attention block

**Output template (hub Attention block):**
```
## Attention

- **Cross-phase dependencies (new):**
  - Task #18 (Phase 3) newly depends on Task #45 (Phase 6)
  - Task #22 (Phase 4) newly depends on Task #51 (Phase 5) — review this for blocking risk
```

**Questions for you:**
- Should we snapshot todos.md after each drift run, or use git log --patch to diff? (Snapshot is simpler; git log is more durable)

---

### **B. `workstream_status_staleness` check**

**File:** ~/code/cowork-tools/drift_check.py (add new check class)

**Inputs:**
- project_hub.md from vault
- drift_check.yaml config: `workstream-status-staleness: {threshold-days: 14, skip-blocks: [PM-STATUS]}`

**Algorithm:**
1. Scan project_hub.md for lines matching `<!-- (\w+)-STATUS-START -->`
2. Find corresponding `<!-- (\w+)-STATUS-END -->` block
3. Extract timestamp from block header (format: `<!-- ROLE-STATUS-UPDATED-YYYY-MM-DD -->`)
4. Calculate days since update: `today - timestamp`
5. If days > threshold AND role not in skip-list, flag

**Output template (hub Attention block):**
```
## Attention

- **Status block staleness:**
  - ANALYSIS-STATUS not updated for 18 days (threshold: 14)
  - REVIEW-STATUS not updated for 3 days (OK)
```

**Prerequisites:**
- pm-setup-project must scaffold status blocks WITH timestamp headers
- Template: `<!-- ANALYSIS-STATUS-UPDATED-YYYY-MM-DD -->` format for extraction

**Questions for you:**
- Should timestamp be in separate comment line or embedded in opening comment?
- Should pm-setup-project auto-update timestamps on vault setup, or is it chat's responsibility?

---

### **C. `.gitkeep` Inflation Fix**

**File:** ~/code/cowork-tools/drift_check.py (modify count_files() function)

**Change:**
```python
# Before:
files = os.listdir(folder_path)
count = len(files)

# After:
files = [f for f in os.listdir(folder_path) if not f.startswith('.')]
count = len(files)
```

**Effect:**
- Empty inbox/promotion/ → `promotion: 0` (was `promotion: 1`)
- No config needed
- Backward-compatible (doesn't break existing drift_check.yaml)

---

## Gating Checklist (for Review's use)

- [ ] `cross_phase_dependency_change` check runs without errors
- [ ] Detects new task dependencies correctly
- [ ] Classifies cross-phase vs same-phase correctly
- [ ] Surfaces findings in hub Attention block
- [ ] Config option (any|backward-only) works
- [ ] `workstream_status_staleness` check runs without errors
- [ ] Extracts timestamps correctly from status blocks
- [ ] Calculates staleness correctly
- [ ] Surfaces in hub Attention block
- [ ] Threshold config (global + skip-list) works
- [ ] `.gitkeep` fix: empty inboxes report as 0, not 1
- [ ] Existing drift checks (git-status, file-ownership, etc.) still work

---

## Your Decisions

**Before solution design, confirm:**

1. **Cross-phase dependency check:**
   - Warn on ANY cross-phase, or backward-only? (My read: any)
   - Snapshot todos.md or git log diff? (My read: snapshot)

2. **Status block staleness check:**
   - Timestamp format embedded in comment, or separate line? (My read: embedded `<!-- ROLE-STATUS-UPDATED-YYYY-MM-DD -->`)
   - pm-setup-project auto-updates timestamps on setup, or chat responsibility? (My read: chat responsible at session entry/exit)
   - Global threshold (14d default) with per-project override in drift_check.yaml? (My read: yes)

3. **`.gitkeep` fix:**
   - Proceed as outlined? (Should be uncontroversial)

4. **Integration:**
   - Are these three checks sufficient for Epistemology/Authority PM observability?
   - Any other drift-side metrics needed for Review workflows?

Once locked, I'll detail implementation for each check.
