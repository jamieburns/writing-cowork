---
name: pm-install-claim-dispute-protocol
description: >
  This skill should be used when the user asks to "install the claim dispute
  protocol", "create claim_dispute_protocol.md", "set up the file claim
  resolution doc", or any variant of placing the writing-cowork claim/release
  reference doc. Copies templates/claim_dispute_protocol.md into the vault's
  process/data_management/ directory. Pure reference doc — only project name
  is substituted. Invoked by pm-setup-project; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-install-claim-dispute-protocol

Copy `${CLAUDE_PLUGIN_ROOT}/templates/claim_dispute_protocol.md` from the plugin to
`<vault>/process/data_management/claim_dispute_protocol.md`. The doc defines
how the multi-context file-claim resolution works (Options A/B/C, default
behavior, out-of-band writer edits, recording). Reference doc — only the
project name is substituted; the protocol itself is project-invariant.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/data_management/` exists.
3. Verify `<vault-path>/process/data_management/claim_dispute_protocol.md`
   does NOT already exist.
4. Verify the plugin's `${CLAUDE_PLUGIN_ROOT}/templates/claim_dispute_protocol.md` exists.

## Execution

1. Read template, substitute `{{name}}`, `{{title}}`, `{{date_iso}}`.
2. Atomic-write to
   `<vault-path>/process/data_management/claim_dispute_protocol.md`.

## Output on success

```
Installed claim_dispute_protocol.md at <vault-path>/process/data_management/claim_dispute_protocol.md
```

## Output on failure

- `data_management directory missing; run pm-init-vault first`
- `claim_dispute_protocol.md already exists at <path>; remove it first or skip this step`
- `${CLAUDE_PLUGIN_ROOT}/templates/claim_dispute_protocol.md not found in plugin install`

## Standalone use

Same preconditions.
