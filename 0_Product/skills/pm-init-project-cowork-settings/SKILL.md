---
name: pm-init-project-cowork-settings
description: >
  This skill should be used when the user asks to "enable writing-cowork in
  this project", "set up Cowork project settings", "scope writing-cowork to
  this vault", or any variant of writing the per-project Cowork settings
  file that enables writing-cowork for that project. Writes
  `<vault>/.claude/settings.json` with `enabledPlugins` set so that Cowork
  loads writing-cowork only when operating in this project. Invoked by
  pm-setup-project as part of the initial scaffold; also usable standalone
  for retrofitting onto an existing vault.
  
  **Lift Procedure Integration:** Invoked during project setup (stage 1).
  See ~/code/cowork-tools/lift/README.md for full lift workflow.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-init-project-cowork-settings

Write `<vault>/.claude/settings.json` with an `enabledPlugins` entry that
enables writing-cowork for this project. This is the per-project counterpart
to a user-level global disable of writing-cowork — the plugin is available
everywhere but only active in projects that opt in via this file.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault directory.
- **`<name>`** (required) — project slug; used in any informational output,
  not in the settings content itself.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/.claude/settings.json` does NOT already exist. If
   it does, abort with `settings.json already exists at
   <vault>/.claude/settings.json; merge the enabledPlugins entry manually
   or remove the file first`. Do not overwrite a file the user may have
   customized.

## Execution

1. Create `<vault-path>/.claude/` if it doesn't exist (`mkdir -p`).
2. Atomic-write the following content to
   `<vault-path>/.claude/settings.json`:

   ```json
   {
     "enabledPlugins": {
       "writing-cowork@jamie-cowork-plugins": true
     }
   }
   ```

3. Validate the result parses as JSON before committing the write
   (write to `.tmp`, parse, then `mv` to `settings.json`).

The marketplace name (`jamie-cowork-plugins`) is the personal marketplace
Jamie maintains at `github.com/jamieburns/cowork-plugins-marketplace`.
Other users adopting writing-cowork would substitute their own marketplace
name; this skill's content is therefore project-specific (the marketplace
ID is fixed to the current author's setup). A future v2 enhancement could
parameterize the marketplace ID per-installation.

## Output on success

```
Initialized Cowork settings at <vault-path>/.claude/settings.json
  enabledPlugins: writing-cowork@jamie-cowork-plugins = true
```

## Output on failure

- `settings.json already exists at <path>; merge the enabledPlugins entry manually or remove the file first`
- `permission denied writing to <vault-path>/.claude/`

## Standalone use

When invoked outside the orchestrator (e.g., retrofitting an existing
writing project that predates per-project plugin scoping), the same
preconditions apply. Useful for enabling writing-cowork in vaults set up
before this skill existed.
