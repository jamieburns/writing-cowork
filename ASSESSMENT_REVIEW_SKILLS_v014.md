# Assessment: Review Skills (Subset 4) for v0.1.14

## What's on the table

**v1 design Subset 4** specifies 9 Review skills. **Active-project findings** propose a different skill set oriented toward cycle management. This assessment compares both and asks: should we integrate them, choose one, or iterate?

---

## v1 Design: Feedback Workflow Orientation (9 skills)

From `writing_cowork_plugin_v1_design.md` § Subset 4:

```
run-agentic-review <scope> [--perspectives=friendly,neutral,hostile|custom-list]
synthesize-reviews <scope>
run-gap-analysis <scope> --against=<target>
ingest-human-review <feedback-file> [--reviewer-id=...]
triage-review <review-file>
draft-reviewer-response <reviewer-id> [--items=...]
handoff-feedback-for-integration <source-id> --target=substance|voice
update-reviewer-tracking <reviewer-id> --status=read|triaged|responded|integrated
list-reviewer-status [--status=...]
```

**Design intent:** Wrap agentic review execution, human feedback ingest, triage classification, and response drafting. Tracks per-reviewer engagement state.

**Gating checklist (from v1 design):**
- All 9 install + discoverable
- run-agentic-review produces 3 review files per perspective
- synthesize-reviews produces skeleton
- run-gap-analysis against hypothesis produces findings
- triage-review classifies per project's triage classes
- ingest-human-review produces structured ingest report
- Reviewer tracking maintained across full round
- end-to-end workflow via skills only

---

## Findings from Active-Project Use (Authority Review chat, 2026-05-21)

From `/tmp/plugin_findings_for_writing_cowork.md`:

### What Review chat observed:

**"The plugin has `pm-*`, `voice-*`, and (planned) `review-*` skills, but no `review-*` skills. The Review role is push-driven and cycle-shaped, with predictable operations."**

**Proposed skills (mirroring voice-* and pm-* patterns):**

```
review-spawn-cycle <artifact> <methodology> <persona-or-reviewer>
review-log-cycle
review-promote-findings <cycle-id>
review-add-human-reviewer <name> <profile>
review-prep-reader-bundle <cycle-id>
review-show-queue
review-show-log
```

**Why this matters:**
- Authority's review workflow is **cycle-driven** — each cycle is a unit (agentic OR human)
- Cycles spawn, log, promote as bundles
- Current gaps: no way to spawn a review context, log its completion, promote findings atomically
- Reader-bundle generation has **PM/Review role split** (Review picks content, PM packages)

### Vault-side pattern (4-file disposition, 2026-05-21):

```
process/review/queue.md          — upcoming cycles
process/review/log.md             — completed cycles (agentic + human)
process/review/findings/          — per-cycle detail files (YYYY-MM-DD_<artifact>_<persona>.md)
process/active/reviewer_tracking.md — per-human-reviewer engagement state
```

**Why:** A multi-pass review framework needs to distinguish:
- **Cycle** — a unit of review work (one artifact, one methodology, one persona/reviewer)
- **Findings** — the output of that cycle
- **Reviewer** — the human doing the reviewing (across cycles)

---

## Integration Analysis

### Do they conflict?

**No.** They operate at different levels:

| Aspect | v1 Design | Findings Proposal |
|--------|-----------|-------------------|
| **Level** | Feedback workflow (per cycle) | Cycle management (outer container) |
| **Scope** | Run review → triage → respond | Track cycles, log, promote |
| **Orientation** | Feedback processing (verbs: run, synthesize, ingest, triage, draft, handoff) | Cycle lifecycle (verbs: spawn, log, promote, track) |
| **Time horizon** | During a cycle | Across multiple cycles |

### Can they work together?

**Yes.** Natural pairing:

1. **Cycle Setup** (findings): `review-spawn-cycle <artifact> --methodology=agentic --persona=friendly`
   - Creates review context, preps skeleton files, loads persona/method docs
2. **In-Cycle Feedback Processing** (v1 design): `run-agentic-review <scope>` → `triage-review` → `draft-reviewer-response`
   - Executes review, processes output, tracks reviewer engagement
3. **Cycle Completion** (findings): `review-log-cycle` → `review-promote-findings <cycle-id>`
   - Records cycle, packs findings for inbox/promotion/ → Analysis/Voice

**Example workflow (Authority's actual pattern):**
```
review-spawn-cycle epistemology-chapter-3 agentic friendly
run-agentic-review epistemology-chapter-3 --perspectives=friendly,neutral,hostile
synthesize-reviews epistemology-chapter-3
triage-review findings/*.md
review-log-cycle                    # record in log.md, create findings file
review-promote-findings cycle-003   # send to inbox/promotion/ for Analysis
```

---

## Decision Points for You

### **1. Should we integrate both sets (13 skills total) or pick one?**

**Option A: Integrate both (13 skills)**
- Cycle management outer loop (7 findings skills) + feedback workflow inner loop (9 v1 skills minus overlap)
- Strength: covers Authority's actual workflow end-to-end
- Trade-off: larger Subset 4 (13 vs. 9 skills); more complex gating checklist

**Option B: v1 design as-is (9 skills)**
- Ignore findings proposal; ship v1 design unchanged
- Strength: simpler, less scope creep
- Trade-off: Authority will build cycle management ad-hoc outside plugin (like they did for workstream blocks); loses standardization

**Option C: Findings proposal only (7 skills, no v1 feedback workflow)**
- Cycle management only; no in-cycle feedback processing
- Strength: focused, lighter
- Trade-off: loses agentic-review execution; Authority has to call agentic review outside plugin

**My read:** Option A (integrate). Here's why:
- Authority has proven they need cycle management (vault-side innovation)
- They also need in-cycle processing (agentic reviews, triage, responses)
- 13 skills for full-coverage is proportionate to PM (35) + Voice (9)
- Gating checklist can be updated to include cycle requirements

RESPONSE: Option A
### **2. What about the 4-file disposition for Review workstream?**

**Current:** `pm-init-reader-review-tracking` creates reviewer_tracking.md only

**Findings:** should scaffold queue.md, log.md, findings/ + reviewer_tracking.md (4 files total)

**Should we:**
- **Option A:** Extend pm-init-reader-review-tracking to scaffold all 4 files
- **Option B:** Leave pm-init-reader-review-tracking as-is; let Review chats create queue/log/findings manually
- **Option C:** Create a separate `pm-init-review-workflow` skill that scaffolds all 4

**My read:** Option A or C. The 4-file disposition is general-purpose (any multi-cycle project needs it); shouldn't be manual.

**If Option C:** rename pm-init-reader-review-tracking → pm-init-review-tracking (shorter, matches pattern), keep existing behavior, then add `pm-init-review-workflow` to scaffold full workstream.

RESPONSE: Option A
### **3. Reader-bundle generation responsibility split**

**Findings note:** "For human-review cycles, packaging the reader bundle (PDF/Word/cover note) is PM-side operational work, but choosing what goes into the bundle is Review-side cycle judgment."

**Pattern:** Review provides manifest (content selection + framing notes); PM executes packaging via some future skill like `pm-package-reader-bundle`.

**For v0.1.14:** should we:
- **Option A:** Add `review-prep-reader-bundle <cycle-id>` skill (Review specifies what goes in; returns manifest), and document the expectation that PM will package it (future skill)
- **Option B:** Skip reader-bundle skills for now; document the pattern in for_other_contexts.md
- **Option C:** Add both review-prep and pm-package (larger scope)

**My read:** Option A. Review needs to specify bundle content; PM packaging is downstream (v0.1.15 or later when we build general artifact-packaging infrastructure).

RESPONSE: A

---

## Recommended Path (for your confirmation)

**Ship Subset 4 as 13 integrated skills:**

**Cycle Management (7 skills from findings):**
- `review-spawn-cycle <artifact> --methodology=<agentic|human> [--persona=<name>]`
- `review-log-cycle [--findings-location=<path>]` — records cycle + auto-creates findings file
- `review-show-queue [--status=pending|in-progress|done]`
- `review-show-log [--by=cycle-date|methodology]`
- `review-add-human-reviewer <name> <profile-path>`
- `review-prep-reader-bundle <cycle-id>` — outputs manifest
- *[Possibly: `review-remove-human-reviewer <name>`]*

**Feedback Workflow (9 skills from v1, refined for cycles):**
- `run-agentic-review <scope> [--cycle=<id>] [--perspectives=...]` — ties review to cycle
- `synthesize-reviews <scope>`
- `run-gap-analysis <scope> --against=<target>`
- `ingest-human-review <feedback-file> [--cycle=<id>] [--reviewer-id=...]`
- `triage-review <review-file>` — classifies findings per project's triage classes
- `draft-reviewer-response <reviewer-id> [--cycle=<id>] [--items=...]`
- `handoff-feedback-for-integration <source-id> --target=substance|voice [--cycle=<id>]`
- `update-reviewer-tracking <reviewer-id> --status=read|triaged|responded|integrated`
- `list-reviewer-status [--status=...]`

**Infrastructure:**
- Extend `pm-init-reader-review-tracking` to scaffold 4-file disposition (or create separate `pm-init-review-workflow`)
- Document PM/Review reader-bundle split in for_other_contexts.md

---

## Your Call

**Before we move to solution design, confirm or modify:**

1. **Integrate both (13 skills) or pick single approach?** A/B/C?
2. **4-file disposition scaffolding:** extend pm-init-reader-review-tracking (Option A) or separate skill (Option C)?
3. **Reader-bundle pattern:** document in for_other_contexts.md + add review-prep-reader-bundle (Option A)?
4. **Any skills missing or redundant?** Any adjustments?

Once locked, I'll create the detailed skill specs for each of the 13.
