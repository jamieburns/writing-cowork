---
name: pm-place-lift-decisions
description: >
  This skill should be used when the user asks to "place the lift decisions",
  "copy the pre-lift decisions doc to the vault", "install the decisions
  document for this lift", or any variant of placing a writer-supplied
  pre-lift decisions doc at the vault root. Conditional sub-skill: only
  runs when pm-setup-project is invoked with `--decisions=<file>`.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-place-lift-decisions

Copy a writer-supplied decisions document into the vault root. This is the
"pre-lift decisions" doc that captures answers to the lift questionnaire
before the manual or scripted lift sequence begins. Lifted from
`~/code/cowork-tools/lift/` workflow; this skill is the integration point
between that workflow and the plugin.

This skill is the only conditional one in the pm-setup-project sequence —
it runs only when `--decisions=<file>` was supplied to the orchestrator.
When `--decisions` is absent, the orchestrator skips this skill silently.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<decisions-file>`** (required) — absolute path to the writer's
  decisions doc. Typically `_scratch/<project>_lift_decisions_draft.md`
  inside the source project, but can be anywhere.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<decisions-file>` exists and is a regular file.
3. Determine the destination filename: keep the source basename
   unchanged. E.g., `<vault>/<source-basename>`.
4. Verify the destination does NOT already exist.

## Execution

1. Read `<decisions-file>` content.
2. Atomic-write to `<vault-path>/<source-basename>`.

No placeholder substitution — the decisions doc is writer-authored content,
not a template.

## Output on success

```
Placed decisions doc at <vault-path>/<filename>
  Source: <decisions-file>
```

## Output on failure

- `<decisions-file> does not exist or is not a regular file`
- `<destination> already exists; remove it first or skip this step`
- `permission denied reading <decisions-file>`

## Standalone use

Same preconditions. Useful when the writer realizes mid-project that they
want their decisions doc preserved in the vault and didn't supply it at
setup time.
