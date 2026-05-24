---
name: pm-init-voice-exceptions
description: >
  This skill should be used when the user asks to "initialize voice
  exceptions", "create voice_exceptions.md", "set up the voice exceptions
  file", or any variant of creating the empty voice-exceptions tracking
  document. Creates an empty (header-only) voice_exceptions.md in the
  vault's process/active/ directory. Invoked by pm-setup-project;
  also usable standalone.
  
  **Lift Procedure Integration:** Invoked during project setup (stage 2).
  See ~/code/cowork-tools/lift/README.md for full lift workflow.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-init-voice-exceptions

Create an initially-empty `process/active/voice_exceptions.md` with a
minimal header. This file accumulates voice-pass exceptions — terms,
phrasings, or constructions that are deliberately permitted despite
violating a general voice rule, recorded so future voice passes don't
flag them again.

The file starts empty (header only). Exceptions are added by
`voice-add-exception` and queried by `voice-list-exceptions`
(both shipping in Subset 3 — Voice/tone).

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug; used in the header line.
- **`--title=<title>`** (optional) — human-readable title.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/active/` exists.
3. Verify `<vault-path>/process/active/voice_exceptions.md` does NOT
   already exist.

## Execution

Atomic-write the following content to
`<vault-path>/process/active/voice_exceptions.md`:

```markdown
# Voice exceptions — <title>

Created: <date_iso>

Tracked here: terms, phrasings, or constructions that are deliberately
permitted despite violating a general voice rule. Each exception is one
row; the columns capture the term, its scope (project | file | section),
the file/location (when scope < project), and a rationale.

| Term | Scope | In | Reason | Added |
|------|-------|----|--------|-------|
```

The empty table header is intentional — `voice-add-exception` appends
rows to it.

## Output on success

```
Initialized voice_exceptions.md at <vault-path>/process/active/voice_exceptions.md
```

## Output on failure

- `process/active directory missing; run pm-init-vault first`
- `voice_exceptions.md already exists at <path>; remove it first or skip this step`

## Standalone use

Same preconditions.
