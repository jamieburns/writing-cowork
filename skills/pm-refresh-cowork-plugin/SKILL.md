---
name: pm-refresh-cowork-plugin
description: >
  This skill should be used when the user asks to "refresh a Cowork plugin",
  "force update a plugin", "pull the latest plugin version", "fix Cowork plugin
  cache", or any variant of forcing Cowork to re-fetch a plugin that won't
  update through normal channels. TEMPORARY workaround — exists because
  Cowork's nominal update mechanism is broken (anthropics/claude-code #38271).
  Should be deprecated when Anthropic ships a force-refresh affordance.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
  temporary: true
---

# pm-refresh-cowork-plugin

Force Cowork to re-fetch a plugin from its marketplace. Works around the
known bug where Cowork's marketplace sync returns `status=success` with
`0 downloaded` even when a new version is genuinely available upstream.

**This is a temporary workaround.** When Anthropic ships a proper
force-refresh mechanism (UI button or CLI equivalent), this skill should
be deprecated. Until then, this is the only reliable way to deploy a
plugin update.

## Arguments

- **`<plugin-name>`** (required) — the plugin to refresh (e.g.,
  `writing-cowork`). Must match the `name` field in
  `rpm/manifest.json`.

## Preconditions

1. Locate Cowork's `rpm/manifest.json` by globbing under
   `~/Library/Application Support/Claude/local-agent-mode-sessions/`.
   Expect path pattern:
   `local-agent-mode-sessions/<account-hash>/<workspace-hash>/rpm/manifest.json`.
   If multiple matches (e.g., multiple accounts), use the most recently
   modified one or ask the user which to operate on.
2. Read `rpm/manifest.json`. Verify a plugin entry with name `<plugin-name>`
   exists. If not, abort with `plugin <name> not in rpm/manifest.json;
   nothing to refresh — is it actually installed?`.
3. Extract the plugin's `id` field (e.g., `plugin_01Uf68BxuF1xnBs2L2U8bijY`).
4. Verify the cached plugin directory exists at
   `<rpm-root>/plugin_<id>/`.

## Execution

The refresh must happen with Cowork quit (Cowork holds file locks on the
plugin dir). The skill cannot quit Cowork itself without killing the chat
session that invoked it. Instead, the skill prepares a one-shot refresh
script at `/tmp/cowork-refresh-<plugin-name>.sh` and instructs the user to:

1. Quit Cowork (Cmd-Q).
2. Run the prepared script from Terminal.
3. Relaunch happens automatically at the end of the script.

The refresh script content:

```bash
#!/bin/bash
set -e
# Wait briefly for Cowork to fully terminate
sleep 2
# Remove the cached plugin
rm -rf "<rpm-root>/plugin_<id>"
# Relaunch Cowork
open -a Claude
echo "Refresh complete. Cowork relaunching."
```

Use the exact resolved `<rpm-root>` and `<id>` values. Write atomically
(`.tmp` then `mv`). Make the script executable (`chmod +x`).

On Cowork relaunch, the marketplace sync will detect the missing plugin
and re-fetch it fresh from GitHub.

## Output on success

```
Prepared refresh script for <plugin-name>:
  Plugin ID: <id>
  Cache path: <rpm-root>/plugin_<id>/
  Script: /tmp/cowork-refresh-<plugin-name>.sh

To apply the refresh:
  1. Quit Cowork (Cmd-Q)
  2. In Terminal, run: bash /tmp/cowork-refresh-<plugin-name>.sh
  3. Cowork will relaunch automatically with the plugin re-fetched.

Verify the new version installed by checking rpm/manifest.json's
updatedAt field, or counting SKILL.md files in the new plugin cache.
```

## Output on failure

- `plugin <name> not in rpm/manifest.json; nothing to refresh`
- `cached plugin directory not found at <path> — already removed or never installed?`
- `multiple manifest.json files found under local-agent-mode-sessions/; specify --account=<hash> to disambiguate`
- `permission denied writing to /tmp/`

## Why this skill exists (full context)

Cowork has a known bug (anthropics/claude-code #38271) where
`pollSyncUntilDone` returns `status=success` with `0 downloaded, 0 removed`
even when the upstream marketplace has a new plugin version. The "update"
button, app reload, plugin uninstall/reinstall, and marketplace
uninstall/reinstall all fail to trigger a re-fetch.

The only reliable workaround is to remove the cached plugin directory
while Cowork is quit. This skill automates the lookup of the correct
cache path (which is buried under session-hashed directories) and
prepares the one-shot script.

When Anthropic ships a proper refresh mechanism (UI affordance,
slash command, or CLI), this skill should be marked deprecated and
eventually removed. The `metadata.temporary: true` flag in the
frontmatter is a signal to that future cleanup.

## Standalone use

This IS the canonical use — refresh-plugin is invoked when a normal
update has failed to take effect.
