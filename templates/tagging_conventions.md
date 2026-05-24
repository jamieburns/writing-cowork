# Tagging conventions — {{title}}

Git tags in this repo follow a three-namespace convention. Pattern source: writing-cowork plugin v0.1 (lifted from Reconciliation Hypothesis).

**Established:** {{date_iso}}

## Namespaces

### `release/<v>-<purpose>` — external distributions

Distribution boundaries. Paired with GitHub Releases that hold the built deliverables (PDF / DOCX / EPUB / etc., per the project's deliverable format).

Examples: `release/v1.0-reviewer-r1`, `release/v1.0-reviewer-r2`, `release/v1.0-final`, `release/v2.0-reviewer-r1`.

### `lock/<date>-<name>` — decision-locks

Substantive commitments treated as settled. Revising a lock requires an explicit decision-log entry (typically in `project_hub.md` or a dedicated decision log).

Examples: `lock/<YYYY-MM-DD>-phase1-foundational-decisions`, `lock/<YYYY-MM-DD>-terminology-finalization`.

### `snapshot/<date>-<name>` — historical markers

Boundary-of-state markers without lock or release semantics. Navigation aids — "here's where I changed gears."

Examples: `snapshot/<YYYY-MM-DD>-end-of-initial-development`, `snapshot/<YYYY-MM-DD>-pre-restructure`.

## Conventions

- **Always annotated.** Use `git tag -a <name> -m "<message>"`. Lightweight tags lack metadata and aren't used.
- **Push explicitly.** `git push origin <tag>` — not `git push --tags`. Keeps intent visible.
- **Date format YYYY-MM-DD** for `lock/` and `snapshot/`.
- **Hyphens, no spaces** in tag names.
- **Filter by namespace** with `git tag -l 'release/*'`, `git tag -l 'lock/*'`, `git tag -l 'snapshot/*'`.

## Release workflow

For external distributions:

1. Build the deliverables per the project's build process.
2. Tag the commit: `git tag -a release/v1.0-reviewer-r1 -m "Reviewer round 1 distribution"`.
3. Push the tag: `git push origin release/v1.0-reviewer-r1`.
4. Create the GitHub Release with artifacts attached:

```bash
gh release create release/v1.0-reviewer-r1 \
  <path/to/deliverable-1> \
  <path/to/deliverable-2> \
  --title "<title> — Reviewer Round 1" \
  --notes "<release notes>"
```

Reviewers download artifacts from the GitHub Release page or via direct URLs.

## Lock workflow

For substantive decision-locks:

1. Update the affected artifacts (`project_hub.md`, decision logs).
2. Commit those updates with `[data-mgmt]` or `[substance]` prefix as appropriate.
3. Tag: `git tag -a lock/<date>-<name> -m "Why / Decision / Alternatives considered"`.
4. Push the tag: `git push origin lock/<date>-<name>`.

The tag message should capture *why* the lock was made, *what* was decided, and *what alternatives were considered* (per writing-cowork locked decision #8 on tag-lock message format). Future-you needs to judge whether the lock should hold under new evidence.

## When to snapshot-tag

Snapshot tags mark state transitions and operational boundaries. Use them to create clear historical checkpoints without locking decisions.

**Create a snapshot tag when:**

- **Phase complete:** You've finished a substantive phase (e.g., Phase 1 outline is done, Phase 3 revision is complete).
- **Mode shift:** You're changing how the project operates (e.g., "now entering review cycle", "shifting from distributed outline to centralized draft").
- **Before major refactor:** You're about to restructure content, reorganize the vault, or make breaking changes. The snapshot is a baseline for comparing before/after.
- **Role handoff:** You're handing the artifact off between contexts or roles (e.g., "substance → review handoff point").
- **Natural checkpoint:** You've reached a logical moment to mark progress (end of week, before taking on new scope, after a major decision).

**Do not snapshot-tag for:** everyday commits, minor edits, incremental progress. Those are regular commits.

**Example timeline:**

```
2026-05-15  snapshot/phase-1-outline-complete     (Phase 1 outline done)
2026-05-16  lock/2026-05-16-terminology-locked    (key terms locked: "system", "agent", etc.)
2026-05-17  snapshot/phase-2-research-baseline    (baseline before Phase 2 research begins)
2026-05-22  snapshot/review-phase-entry           (entering review cycle)
2026-05-23  lock/2026-05-23-chapter-3-framing     (PM + substance decided on chapter 3 framing)
```

**Tag message for snapshots:** Describe the state you're marking ("Phase 1 outline complete and ready for review") or the transition happening ("Entering review cycle — substance complete").

Snapshots are navigation aids. They help you jump to specific historical states when exploring evolution of the draft.

## Listing and inspection

```bash
git tag -l 'release/*'                         # all release tags
git tag -l 'lock/*' --sort=-creatordate        # locks, newest first
git show release/v1.0-reviewer-r1              # tag message + diff from prior
git log --decorate --oneline                   # commits with their tags
```
