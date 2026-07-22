# Review Phase — Planning Roadmap (Deferred)

**Status:** Planning only, deferred to its own future version release. Nothing below is scheduled against the current update pass. This document exists so review-related items have a landing place separate from `v0.1.15_planning_roadmap_2026-07-22.md`, per your instruction not to reopen anything review-related in the current process.

**Date:** 2026-07-22
**Author:** Claude (Cowork), cloud session

---

## Why this is split out

The current update pass is scoped to: (1) verifying what's actually shipped vs. locked-but-unbuilt across the plugin, and (2) incorporating `drift_check.py` into the plugin itself. Review Skills (Subset 4) is a large, separately-locked workstream (13 skills) that deserves its own dedicated version and its own dedicated planning pass when you're ready — not a subsection competing for attention inside a smaller, more mechanical update. Everything below is carried over verbatim in substance from the prior roadmap draft and the source handoffs; nothing has been re-litigated or re-decided.

---

## 1. Review Skills Subset 4 — locked, unshipped (13 skills)

Locked in `2_Development/RoadMap/v0.1.14/DECISIONS_v014.md` and detailed in `ASSESSMENT_REVIEW_SKILLS_v014.md`. Confirmed **not shipped**: no `review-*` skill exists anywhere in the current 60-skill list (verified again this pass — skill directory listing shows no `review-*` prefix).

**Locked decisions (Option A on all three, per the assessment doc's "RESPONSE" lines):**

1. Integrate both the v1-design feedback-workflow skills (9) and the findings-proposal cycle-management skills (7, with `run-agentic-review` overlap resolved) into 13 total skills — not picking one set over the other.
2. Extend `pm-init-reader-review-tracking` to scaffold the full 4-file disposition (`process/review/queue.md`, `log.md`, `findings/`, plus `reviewer_tracking.md`), rather than a separate init skill.
3. Add `review-prep-reader-bundle` (Review-side manifest); defer PM-side packaging (`pm-package-reader-bundle`) to a later version.

**The 13 skills as locked:**

Cycle management (7): `review-spawn-cycle`, `review-log-cycle`, `review-show-queue`, `review-show-log`, `review-add-human-reviewer`, `review-prep-reader-bundle`, (possibly `review-remove-human-reviewer`).

Feedback workflow (9, cycle-aware refinements of v1 design): `run-agentic-review`, `synthesize-reviews`, `run-gap-analysis`, `ingest-human-review`, `triage-review`, `draft-reviewer-response`, `handoff-feedback-for-integration`, `update-reviewer-tracking`, `list-reviewer-status`.

**When this is picked back up:** confirm whether two more months of evidence (through this update pass) changes anything about the locked decisions before building — but per your instruction here, do NOT re-open that discussion now. Just carry the locked decisions forward intact.

---

## 2. Consumer-vault `review/` folder — shares design with the hierarchy work

From the prior roadmap's §2 (new file hierarchy for consumer vaults): the `review/` folder proposal is **the same folder** the locked Review Skills work already defines (`process/review/{queue.md,log.md,findings/}`). When the hierarchy redesign is eventually picked up, sequence it after or alongside Review Skills so the folder isn't designed twice or drifts apart from the skill work that populates it.

---

## 3. Task dependency gate — additive, not a Review-skill dependency, but related enough to flag

Not part of Review Skills proper, but related in spirit: the "close-time gate" proposal from the handoffs (block `pm-close-task`/`pm-update-task` from closing a task whose dependency isn't satisfied) is **separate from and additive to** the drift-check's cross-phase dependency detection (confirmed shipped in `drift_check.py` — see the sibling drift-check-incorporation doc). This item does not require Review Skills to ship first, and isn't inherently a "review" item — flagging it here only because the original assessment lumped dependency-tracking language near review-cycle language. Recommend treating it as its own independent workstream whenever picked up, not bundled with Review Skills.

**Reminder from the prior pass:** `Depends-on` does not exist as a column in `todos.md`'s real schema (confirmed against `pm-add-task`/`pm-init-todos` SKILL.md). Building the close-time gate is schema-migration-sized work, not a small patch — budget accordingly whenever it's scheduled.

---

## 4. Smaller review-adjacent gaps (from the handoffs, still deferred)

- **`pm-show-composite-kanban`** has a self-documented `v0.1.15 TODO:` to match `pm-show-kanban`'s `--by=`/filter options. Small, but it's a Review/PM-facing display gap — deferring alongside the rest per your instruction, even though it's cheap enough it could be picked up independently later without waiting for the full Review Skills build.
- **`pm-release-file`** force-release-of-someone-else's-claim not distinguished from self-release. Adjacent to Review's multi-actor claim patterns; deferring with the rest.
- **Legacy checkbox-format vaults blocking task CRUD** (`pm-migrate-todos-schema` gap) — not review-specific, but was raised in the same handoff batch; if it turns out to gate Review Skills adoption in a legacy vault (Reconciliation is on this legacy schema), it may need to move up in priority when Review Skills work actually starts. Flagging the dependency risk now so it isn't missed later, not scheduling it.

---

## Summary

Nothing in this document is scheduled. It exists purely so that when you're ready to open a Review-phase version, the full scope — locked decisions, the shared `review/` folder design, and the smaller adjacent gaps — is in one place instead of scattered across handoffs and a prior roadmap draft.
