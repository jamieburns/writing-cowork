---
name: pm-init-voice-handoff
description: >
  This skill should be used when the user asks to "initialize voice handoff",
  "install the voice handoff doc", "create voice_handoff.md", or any variant
  of placing the writing-cowork voice/tone briefing document into a new
  vault. Copies templates/voice_handoff.md into the vault's
  process/active/ directory, substituting placeholders. Invoked by
  pm-setup-project; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-init-voice-handoff

Install `process/active/voice_handoff.md` from the plugin's template. The
voice handoff is the briefing surface for any voice/tone chat picking up
work on the project — it documents the project's voice modes (e.g.,
Connect/Convince/Convey), terminology baseline, and tone exceptions.

The template ships with generic placeholders and a skeleton structure;
writers and voice/tone specialists fill in project specifics during the
first voice pass.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/active/` exists (pm-init-vault created it).
3. Verify `<vault-path>/process/active/voice_handoff.md` does NOT already
   exist.
4. Verify the plugin's `templates/voice_handoff.md` exists.

## Execution

1. Read template, substitute `{{name}}`, `{{title}}`, `{{date_iso}}`,
   `{{vault_path}}`.
2. Atomic-write to `<vault-path>/process/active/voice_handoff.md`.

## Output on success

```
Installed voice_handoff.md at <vault-path>/process/active/voice_handoff.md
```

## Output on failure

- `process/active directory missing; run pm-init-vault first`
- `voice_handoff.md already exists at <path>; remove it first or skip this step`
- `templates/voice_handoff.md not found in plugin install`

## Standalone use

Same preconditions.
