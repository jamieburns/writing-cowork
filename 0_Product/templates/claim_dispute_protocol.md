# Claim-dispute protocol — {{title}}

When two or more contexts (chats, automated tasks) want to edit the same file concurrently, this protocol determines how the conflict resolves.

**Established:** {{date_iso}} (pattern source: writing-cowork plugin v0.1, lifted from Reconciliation Hypothesis).

---

## Setup

- Each file's current claimant is tracked in `file_ownership.md` `Status` column.
- Format: `claimed:<context>` (e.g., `claimed:substance`, `claimed:data-mgmt`).
- A context claims a file by setting Status before edits begin.
- Release on commit: Status returns to the file's working canonical value.
- If a context attempts to edit and sees Status `claimed:<other>`, the dispute protocol below applies.

---

## Resolution options

The requesting context picks one of three options when it encounters an active claim:

### Option A — Proceed in scratch, merge later

- Make edits in a `_scratch/` location, or `<file>.scratch.md` alongside the canonical file.
- Notify writer when the claimant context completes its work.
- Writer reviews and merges scratch contents into the canonical file on release.
- **Best when** changes are independent of the claimant's edits and a merge will likely be clean.

### Option B — Block

- Wait for the claimant context to release before editing.
- **Best when** changes overlap substantively with the claimant's edits and parallel work would cause merge conflicts.

### Option C — Alternative per context

- Pursue a different approach in the requesting context that doesn't require editing the claimed file.
- Surface the alternative for writer review.
- **Best when** the requesting context's goal can be reframed (e.g., draft a new file instead of editing an existing one).

---

## Default behavior

If the requesting context cannot reach the writer for guidance, default to **Option A** (proceed in scratch). This unblocks work while preserving the claimant's exclusive write.

Writer can override at any time:

- Instruct the requesting context to block (Option B).
- Instruct the claimant to release the claim early.
- Approve a parallel-edit (both contexts proceed; the writer manages the merge manually).

---

## Out-of-band writer edits

If the writer edits a claimed file directly via Obsidian (Mac / iPad / iPhone) while a context holds the claim:

- **Writer's edit takes precedence.**
- The claimant context surfaces a drift report at next operation, identifying which sections changed.
- The writer chooses:
  - Accept the claimant's pending changes, reapplied on top of writer edits.
  - Reject the claimant's pending changes.
  - Request a hybrid merge — writer specifies which portions of the claimant's work to integrate.

This out-of-band case is expected (Obsidian editing is a first-class workflow on mobile during travel); it's not an error.

---

## Recording

- Disputes resolved via Option A or Option C, **or** any resolution requiring writer adjudication, are noted briefly in the affected file's row in `file_ownership.md` (Notes column).
- Trivial parallel work — two contexts editing independent sections of a large document with no foreseeable merge issue — does not require recording.
- Use judgment; the goal is a useful trail of which decisions required active resolution, not a noise log of every parallel operation.

---

## Examples

**Example 1 — Parallel edits, scratch route.**
Substance context is mid-edit on `<main-draft>.md` §3.5 (claimed:substance). Voice context wants to soften phrasing in §2 of the same file. Voice context creates `<main-draft>.md.scratch.md` with the §2 wording it proposes, notifies writer. Writer reviews and merges when substance context releases. Notes added: "voice-context §2 wording suggestion held in scratch during substance §3.5 revision."

**Example 2 — Substantive overlap, block route.**
Substance context is mid-edit on `<main-draft>.md` §3.5 (claimed:substance). Reader-review context surfaces a reader concern that requires a §3.5 wording change. Reader-review context blocks; surfaces the concern as a comment for substance to address before release.

**Example 3 — Writer out-of-band edit.**
Data-mgmt context holds `claimed:data-mgmt` on `process/data_management/file_ownership.md` to update the ownership table. Writer notices a typo on iPad in the same file and fixes it. Data-mgmt context next op: sees writer's typo fix, accepts it, re-applies its own pending update on top, releases the claim.
