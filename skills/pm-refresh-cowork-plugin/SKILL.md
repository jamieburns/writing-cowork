---
name: pm-refresh-cowork-plugin
description: >
  DEPRECATED-FOR-DEVELOPMENT — use Claude Code CLI for the dev cycle
  (`claude plugin marketplace update` / `claude plugin update`). This
  skill remains as a CONSUMER-SIDE workaround when Cowork's update
  detection fails to land a new plugin version (Anthropic support thread
  215474352137566). Use when the user asks to "refresh a Cowork plugin",
  "force update a plugin", "fix Cowork plugin cache", or any variant of
  forcing Cowork to re-fetch a plugin that won't update through normal
  channels. NOT for active plugin development — develop in Claude Code,
  then use Cowork as the runtime.
metadata:
  version: "0.1.1"
  role: pm
  subset: mvp-foundation
  temporary: true
  consumer-side-only: true
---

# pm-refresh-cowork-plugin

Force Cowork to re-fetch a plugin from its marketplace. Works around the
fact that Cowork has no local marketplace catalog clone — it fetches
catalog metadata from a server-side proxy, and the proxy's cache plus
Cowork's local plugin cache together produce stale installs that don't
update through the UI's "Update plugin" path.

**This skill is consumer-side only.** For plugin **development**, do not
use this. Instead, develop against Claude Code CLI where the documented
slash commands work as expected:

    claude plugin marketplace add <owner/repo>
    claude plugin install <plugin>@<marketplace>
    # iterate on plugin source
    claude plugin validate /path/to/plugin
    git commit && git push
    claude plugin marketplace update <marketplace>
    claude plugin update <plugin>@<marketplace>

Once your plugin works in Claude Code, Cowork consumers (including
yourself) install it via Cowork's Customize UI. When Cowork doesn't pick
up an update — which is the bug this skill addresses — use this skill.

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

Two related Cowork issues, observed 2026-05-20 and tracked in Anthropic
support thread 215474352137566:

1. **No local marketplace catalog clone.** Unlike Claude Code (which
   clones marketplace repos to `~/.claude/plugins/marketplaces/<name>/`
   and refreshes via `git pull`), Cowork stores no catalog on disk.
   The `remoteMarketplaceClient` fetches catalog metadata from an
   Anthropic-side proxy. There is no local file to edit and no
   user-facing way to force a catalog refresh.

2. **Update detection fails.** Even after a plugin is republished and
   the catalog version field is bumped, Cowork's "Update plugin" UI
   button reports no update available. The plugin cache directory
   (`local-agent-mode-sessions/<host>/<workspace>/rpm/plugin_*/`) stays
   pinned to the originally-installed version indefinitely.

The only consumer-side workaround is to nuke the cached plugin directory
while Cowork is quit; on relaunch Cowork sees the missing directory and
re-fetches via the proxy. This skill automates that path lookup and
script preparation.

When Anthropic ships a proper refresh mechanism — a slash command,
UI button that actually invalidates the proxy cache, or any kind of
documented Cowork-side equivalent of `claude plugin marketplace update`
— this skill becomes obsolete. The `metadata.temporary: true` flag is
the signal for that future removal.

For **plugin authors**: do not develop in Cowork. The supported dev
workflow is Claude Code CLI (see the description above). Use this skill
only when something is broken on the consumer side.

## Standalone use

This IS the canonical use — refresh-plugin is invoked when a normal
update has failed to take effect.
