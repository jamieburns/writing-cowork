---
name: voice-list-exceptions
description: >
  This skill should be used when the user asks to "list voice
  exceptions", "show me what's exempt from voice checks", "what
  intentional voice variations are recorded", or any variant of
  querying voice_exceptions.md with optional filters.
metadata:
  version: "0.1.0"
  role: voice
  subset: voice
---

# voice-list-exceptions

Read `<vault>/process/active/voice_exceptions.md` and render the
exceptions as a scannable table, with optional filters.

## Arguments

- **`--scope=project|file|section`** (optional) — filter to exceptions
  of a specific scope. Default: all.
- **`--in=<file or file:section>`** (optional) — filter to exceptions
  applying to a specific location.
- **`--term=<text>`** (optional) — filter to exceptions whose term
  matches (substring match).
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify `voice_exceptions.md` exists. If absent, output `no voice
   exceptions file; run pm-init-voice-exceptions first` and exit
   cleanly.

## Execution

1. Read `voice_exceptions.md`.
2. Parse the table rows.
3. Apply filters.
4. Render as a table: `Term | Scope | In | Reason | Added`.
5. Summary line at the bottom: total exceptions matching filter, plus
   breakdown by scope.

## Output on success

```
Voice exceptions in <vault>/process/active/voice_exceptions.md (filter: <description>):

  Term                          Scope     In                   Reason                 Added
  ----------------------------  --------  -------------------  ---------------------  ----------
  okay-not-OK                   project   -                    intentional informal   2026-05-12
  preface-scaffold              file      voice_handoff.md     section header         2026-05-15
  ...

  Showing <X> of <Y> total exceptions.
  Scope breakdown: project=<n>, file=<n>, section=<n>.
```

If no exceptions match the filter:

```
No voice exceptions match the filter.
Total exceptions in file: <Y>.
```

## Output on failure

- `voice_exceptions.md not found at <path>; run pm-init-voice-exceptions first`
- `invalid filter: <value>`

## Standalone use

Pure read. Useful before starting a voice pass — see what's already
exempt so you don't re-flag the same items mentally.
