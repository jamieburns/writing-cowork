---
name: voice-add-exception
description: >
  This skill should be used when the user asks to "add a voice
  exception", "exempt this term from voice checks", "mark this term as
  intentional", or any variant of adding an entry to
  voice_exceptions.md. Exceptions tell voice-run-mechanical-pass and
  voice-audit-terminology to skip flagged terms.
metadata:
  version: "0.1.0"
  role: voice
  subset: voice
---

# voice-add-exception

Append a new row to `<vault>/process/active/voice_exceptions.md`. The
row records an intentional voice variation that voice-pass skills
should skip (so they don't keep flagging it on every run).

## Arguments

- **`<term>`** (required) — the term, phrasing, or punctuation pattern
  being exempted. Supports a glob or regex if needed (prefix with
  `regex:` to opt into regex mode).
- **`--scope=project|file|section`** (optional, default `project`) —
  the breadth of the exception:
  - `project` — applies everywhere in the vault.
  - `file` — applies only when scanning the specified file.
  - `section` — applies only in the specified section of a file.
- **`--in=<file or file:section>`** (optional, required for `file` and
  `section` scopes) — where the exception applies.
- **`--reason=<text>`** (optional) — short note explaining why this is
  intentional (helps future writer remember).
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify `process/active/voice_exceptions.md` exists. If not, abort
   with `voice_exceptions.md not found at <path>; run
   pm-init-voice-exceptions first`.
3. If `--scope=file` or `--scope=section`, verify `--in=` is supplied.
   Verify the referenced file exists.
4. Verify the same `(term, scope, in)` triple isn't already in the
   exceptions file (no duplicates).

## Execution

1. Read `voice_exceptions.md`.
2. Append a row to the existing markdown table:

   ```
   | <term> | <scope> | <in-or-"-"> | <reason-or-"-"> | <today-iso> |
   ```

3. Atomic-write the modified file.

## Output on success

```
Added voice exception:
  Term: <term>
  Scope: <scope>
  In: <in-or-"project-wide">
  Reason: <reason-or-"none">
  Added: <today>

voice-run-mechanical-pass and voice-audit-terminology will now skip this
term in the specified scope.
```

## Output on failure

- `voice_exceptions.md not found at <path>; run pm-init-voice-exceptions first`
- `--in= required for --scope=file or --scope=section`
- `referenced file not found at <in> path`
- `exception already exists for (<term>, <scope>, <in>); no change`

## Standalone use

Most common standalone invocation: the writer encounters a flagged
item during a voice pass, decides it's intentional, and adds the
exception so future runs skip it. Quick interaction; one row.
