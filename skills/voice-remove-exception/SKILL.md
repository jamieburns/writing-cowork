---
name: voice-remove-exception
description: >
  This skill should be used when the user asks to "remove a voice
  exception", "delete a voice exception", "un-exempt this term", or
  any variant of removing a row from voice_exceptions.md. The
  corresponding term will start being flagged by voice-pass skills
  again.
metadata:
  version: "0.1.0"
  role: voice
  subset: voice
---

# voice-remove-exception

Remove a row from `<vault>/process/active/voice_exceptions.md`. The
corresponding term re-becomes subject to `voice-run-mechanical-pass` and
`voice-audit-terminology` flagging.

Common use case: an exception was added during a now-superseded voice
pass; the writer wants the term re-flagged because the project's voice
has matured.

## Arguments

- **`<term>`** (required) — the term to remove. Must match exactly an
  existing row's Term column (case-sensitive).
- **`--scope=project|file|section`** (optional) — disambiguator when
  the same term appears at multiple scopes. If multiple matches exist
  and `--scope` not supplied, the skill lists all matches and asks
  which to remove.
- **`--in=<file or file:section>`** (optional) — further disambiguator
  for scope=file or scope=section.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify `voice_exceptions.md` exists.
3. Verify at least one row matches `<term>`. If not, abort with `no
   exception found for term <term>; check voice-list-exceptions for
   exact spelling`.

## Execution

1. Read `voice_exceptions.md`.
2. Find rows matching `<term>` (filtered by `--scope` and `--in` if
   supplied).
3. If exactly one match: remove the row.
4. If multiple matches and no scope/in disambiguator: print the
   matches with their scopes/locations and prompt the user to pick.
5. Atomic-write the modified file.

## Output on success

```
Removed voice exception:
  Term: <term>
  Scope: <scope>
  In: <in-or-"project-wide">
  Was added: <original-add-date>

voice-run-mechanical-pass and voice-audit-terminology will now flag this
term again in the specified scope.
```

If user disambiguated between multiple matches:

```
Removed voice exception (1 of <N> matching):
  ...
Other matches remain. To remove additional, re-run with --scope= and --in=.
```

## Output on failure

- `voice_exceptions.md not found at <path>`
- `no exception found for term <term>; check voice-list-exceptions for exact spelling`
- `multiple matches for term <term>; specify --scope= and/or --in= to disambiguate (or accept the interactive prompt)`

## Standalone use

Common standalone invocation: cleanup after a voice-pass evolution
where the previously-exempt variant is no longer intentional.
