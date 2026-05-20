---
name: pm-shift-terminology
description: >
  This skill should be used when the user asks to "shift a term",
  "rename a term across the draft", "change <X> to <Y> in voice-edited
  sections", or any variant of a zone-aware terminology rename. Applies
  the rename only to voice-edited zones (detected via [voice] commit
  prefix scan + writer override); leaves not-yet-voice-edited zones
  alone with a lookback report.
metadata:
  version: "0.1.0"
  role: voice
  subset: voice
---

# pm-shift-terminology

Zone-aware X → Y rename across the vault. The challenge: a draft has
sections at different states of voice-pass completion. Some sections
have been voice-edited (where the new term should apply); others are
pre-voice-pass (where the rename should be deferred until those
sections get voice-touched, to avoid sweeping prematurely).

Zone detection: scan git history for `[voice]`-prefixed commits; sections
touched by those commits are "voice-edited" zones. Writer can override
per shift with `--all` (apply everywhere) or `--zone=<path>` flags.

## Arguments

- **`<old>`** (required) — the term to replace (case-sensitive unless
  `--case-insensitive`).
- **`<new>`** (required) — the canonical replacement.
- **`<scope>`** (optional) — vault-relative path to limit the scan.
  Default: whole vault (excluding gitignored patterns).
- **`--all`** (optional, flag) — apply everywhere regardless of zone.
- **`--zone=<path>`** (optional) — limit to a specific path; overrides
  the [voice] commit-prefix zone detection.
- **`--case-insensitive`** (optional, flag) — match case-insensitively
  but preserve the case of the original in the replacement (Title-case
  → Title-case, lowercase → lowercase).
- **`--dry-run`** (optional, flag) — feedback only, no writes.
- **`--ignore-exceptions`** (optional, flag) — skip voice_exceptions.md.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify the project is git-tracked (zone detection needs `git log`).
   If not git-tracked AND `--all` not set, abort with `zone detection
   requires git history; use --all or initialize git first`.
3. Verify `<old>` actually appears in scope (no-op silently otherwise,
   but report what was checked).

## Execution

1. **Detect voice-edited zones.** Run `git log --oneline --grep='^\\[voice\\]'`
   to find voice-pass commits. For each commit, `git show --name-only`
   to list files touched. Set of touched-files = voice-edited zone.
   Unless `--all` or `--zone=` override; those skip this step.

2. **Feedback-first about breakage.** Search the scope for `<old>`.
   For each occurrence, classify:
   - In voice-edited zone → will be replaced (`<old>` → `<new>`).
   - Not in voice-edited zone → deferred (lookback list).
   - In voice_exceptions.md (unless ignored) → skipped per exception.
   - Inside `::: passthrough`, blockquote, or `<!-- exception -->` →
     skipped per structure.

   Present the classification BEFORE doing any writes. Counts + sample
   locations per class. Prompt the user: `Proceed with <N> replacements?
   [y/n]`. Per locked decision: writer adjudicates.

3. **Auto-apply** in current + not-yet zones per user confirmation:
   - "current" zones = voice-edited; replace immediately.
   - "not-yet" zones = pre-voice-pass; **append entry to a lookback
     log** at `<vault>/process/active/terminology_lookback.md` so when
     those sections later get voice-edited, the writer remembers to
     finish the shift.

4. Atomic-write each modified file. Commit with `[voice]` prefix if
   git-tracked.

## Output on success

```
Shifted "<old>" → "<new>":
  Voice-edited zones: <N> files modified, <M> occurrences replaced
  Not-yet zones: <P> occurrences logged to lookback for later
  Skipped (exceptions): <Q>
  Skipped (passthrough/blockquote/inline-exception): <R>
  Commit(s): <list of [voice] hashes>
  Lookback log: <vault>/process/active/terminology_lookback.md
```

## Output on failure

- `zone detection requires git history; use --all or initialize git first`
- `<old> not found in scope; refine the scope or check the term`
- `permission denied writing to <file>`

## Standalone use

Typical flow: writer reads `pm-audit-terminology`'s report, picks a
cluster, runs `pm-shift-terminology` for the chosen unification. Each
shift is a small, reviewable, reversible commit.
