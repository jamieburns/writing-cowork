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
  version: "0.1.2"
  role: pm
  subset: mvp-foundation
  temporary: true
  consumer-side-only: true
---

# pm-refresh-cowork-plugin

Walk the user through the marketplace-level uninstall/reinstall sequence
that forces Cowork's proxy to refetch current catalog content. This is
the only consumer-side procedure that has been observed to invalidate
Anthropic's marketplace proxy cache for a personal-marketplace plugin
(verified 2026-05-20 against writing-cowork).

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
up an update through the "Update plugin" button — which is the bug this
skill addresses — use this skill.

## Arguments

- **`<plugin-name>`** (required) — the plugin to refresh (e.g.,
  `writing-cowork`).
- **`<marketplace-name>`** (required) — the marketplace the plugin
  belongs to (e.g., `jamie-cowork-plugins`).
- **`<marketplace-repo>`** (required) — the github `owner/repo` of the
  marketplace catalog (e.g., `jamieburns/cowork-plugins-marketplace`).
  Needed when re-adding the marketplace through Cowork's UI.

## Preconditions

1. Locate Cowork's `rpm/manifest.json` by globbing under
   `~/Library/Application Support/Claude/local-agent-mode-sessions/`.
2. Verify a plugin entry with name `<plugin-name>` exists in the
   manifest. If not, abort with `plugin <name> not in manifest;
   nothing to refresh — is it actually installed?`.
3. Read the entry's `marketplaceId` and `marketplaceName` fields and
   sanity-check they match `<marketplace-name>`.

## Execution

The refresh is a manual UI sequence — there is no automation path that
works. Cowork does not expose `/plugin marketplace update` as a slash
command, and a full plugin-cache nuke (the previous approach) does NOT
invalidate the proxy cache (reproduced 2026-05-20 17:07 local — see Why
section below).

The procedure that DOES work — proven 2026-05-20 22:31 local:

1. Quit Cowork (Cmd-Q).
2. Relaunch Cowork.
3. Open **Customize → Plugins**. Uninstall `<plugin-name>`.
4. Quit Cowork (Cmd-Q).
5. Relaunch Cowork.
6. Open **Customize → Marketplaces**. Uninstall (remove) the marketplace
   `<marketplace-name>`. This is the step that invalidates the proxy
   cache; without it, the next install just pulls the same stale
   content.
7. Quit Cowork (Cmd-Q).
8. Relaunch Cowork.
9. Open **Customize → Browse Plugins → Personal**. Re-add the marketplace
   `<marketplace-repo>` (e.g. `jamieburns/cowork-plugins-marketplace`).
10. Quit Cowork (Cmd-Q).
11. Relaunch Cowork.
12. Open **Customize → Plugins**. Install `<plugin-name>` from the just-
    re-added marketplace.
13. Quit Cowork (Cmd-Q).
14. Relaunch Cowork. Open a new chat. Verify the new version is loaded
    by checking pm-version (or whatever sentinel the plugin provides),
    counting SKILL.md files, or reading the cached `plugin.json`.

The repeated Cmd-Q cycles are not ceremony — Cowork holds state in
memory and the cleanest way to ensure each step actually takes effect
is to fully restart between steps. Skipping quits has produced
inconsistent results.

## Output (when the user invokes this skill)

Render the numbered procedure above with the user's `<plugin-name>`,
`<marketplace-name>`, and `<marketplace-repo>` substituted into the
relevant lines. Set expectations:

- Expected time: ~3–5 minutes (mostly waiting for Cowork to relaunch
  fourteen times).
- No script will be generated — this is UI navigation only.
- If the marketplace catalog has not been bumped on github since the
  last install, the refresh will succeed but produce the same version
  that's already cached. Make sure the new version is on
  `https://raw.githubusercontent.com/<owner>/<plugin-repo>/main/.claude-plugin/plugin.json`
  before starting.

## Output on failure

- `plugin <name> not in manifest; nothing to refresh`
- `manifest's marketplaceName does not match the supplied <marketplace-name>`

## Why this skill exists (full context)

Two related Cowork behaviors, observed 2026-05-20 and tracked in
Anthropic support thread 215474352137566:

1. **No local marketplace catalog clone.** Unlike Claude Code (which
   clones marketplace repos to `~/.claude/plugins/marketplaces/<name>/`
   and refreshes via `git pull`), Cowork stores no catalog on disk.
   The `remoteMarketplaceClient` fetches catalog metadata from an
   Anthropic-side proxy. There is no local file to edit and no
   user-facing way to force a catalog refresh short of removing and
   re-adding the marketplace.

2. **Update detection fails at the plugin level.** Cowork's "Update
   plugin" UI button reports no update available even when the upstream
   catalog references a newer commit. A full plugin-cache nuke
   (`rm -rf plugin_<id>/`) followed by relaunch does NOT solve this —
   Cowork re-fetches via the proxy, and the proxy serves whatever it
   has cached at the marketplace level. Verified 2026-05-20 17:07:
   nuked plugin dir + nuked manifest entry + relaunch produced v0.1.3
   from a proxy whose upstream sources had been at v0.1.10 for hours.

The marketplace-level uninstall + reinstall sequence above is what
actually clears the proxy cache. The repeated quits are empirically
necessary — the sequence has been observed to fail when Cowork is not
fully restarted between steps.

For **plugin authors**: do not develop in Cowork. The supported dev
workflow is Claude Code CLI (see the description above). Use this
procedure only when something is broken on the consumer side and you
need new skills loaded into Cowork at runtime.

## Standalone use

This IS the canonical use — invoked when a normal "Update plugin" has
failed to take effect.
