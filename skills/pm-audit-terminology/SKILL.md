---
name: pm-audit-terminology
description: >
  This skill should be used when the user asks to "audit terminology",
  "check for inconsistent terms", "find terminology drift", "do a
  terminology scan", or any variant of detecting terminology
  inconsistencies across a scope. Detect-and-report only; never mutates
  the source. Produces a dated report at
  process/active/terminology_scan_YYYY-MM-DD.md.
metadata:
  version: "0.1.0"
  role: voice
  subset: voice
---

# pm-audit-terminology

Scan a scope of the vault for terminology inconsistencies. Detect words
or phrases that appear in multiple forms (e.g., "Reflection Pattern" vs.
"reflection pattern" vs. "RP") and surface them for writer adjudication.
**Detect only — never auto-rewrite.** That's `pm-shift-terminology`'s
job (separate skill, writer-driven).

The output is a markdown report; the writer reads it, decides which
inconsistencies are intentional vs. drift, and uses `pm-shift-terminology`
to apply chosen unifications.

## Arguments

- **`<scope>`** (required) — vault-relative path to a file, directory,
  or glob.
- **`--ignore-exceptions`** (optional, flag) — skip
  `voice_exceptions.md` consultation. Default: respect.
- **`--min-frequency=<N>`** (optional, default 2) — only flag terms
  appearing this many times across the scope (low-frequency variants are
  often quotes or one-off mentions, not drift).
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify the resolved `<scope>` matches at least one file.
3. Verify `process/active/voice_exceptions.md` exists (warn if not and
   `--ignore-exceptions` not set).
4. Verify `process/active/` is writable (the report goes there).

## Execution

1. Scan all files in scope.
2. Build a frequency map of multi-word phrases (1-4 words) and proper
   nouns. Identify candidate-variant clusters by case-folding and minor
   morphological normalization (singular/plural, possessive).
3. Filter clusters where:
   - All variants appear ≥ `--min-frequency`.
   - At least two distinct forms exist.
   - Not on `voice_exceptions.md` (unless `--ignore-exceptions`).
   - Not inside `::: passthrough` blocks, blockquotes, or
     `<!-- exception -->` markers.
4. Write report at
   `<vault>/process/active/terminology_scan_<YYYY-MM-DD>.md` with:
   - Header: date, scope, options.
   - Per cluster: the variants found with counts and file locations,
     plus a writer-fillable "Decision" line ("unify to X" / "intentional
     variation" / "deferred").
5. Do NOT modify any source files. Pure read + write of the report.

## Output on success

```
Audit complete for <scope>:
  Files scanned: <N>
  Terminology clusters found: <C>
  Report: <vault>/process/active/terminology_scan_<date>.md

Next: review the report; for each cluster you want unified, run
pm-shift-terminology with the chosen canonical form.
```

## Output on failure

- `scope <path> matches no files; refine the path or glob`
- `process/active/ not writable; report cannot be written`
- `report already exists at <path> for today; remove or rename first, or supply --date=<override>`

## Standalone use

Run periodically to surface terminology drift. Common cadence: before
each external review distribution, or after a long writing burst.
Useful as a self-criticism prompt — surprises in the report often
signal sloppy revision.
