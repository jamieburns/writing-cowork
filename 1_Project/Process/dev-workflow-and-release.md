# Dev Workflow & Release Procedure

How we develop and ship writing-cowork. Distilled from `1_Project/Memory/reference_personal_plugin_marketplace.md`.

## Environments

The `claude` binary lives at `~/.local/bin/claude` — **not** on the Homebrew path. Anything invoking it via `osascript` must export a PATH including `$HOME/.local/bin`, or it fails with `claude: command not found`.

## One-time setup (per machine)

Recovered 2026-07-26 from the hidden memory store during its retirement — it existed nowhere else.

```bash
# Required for HTTPS-only git auth — Claude Code's "github" marketplace source
# forces SSH clones otherwise.
git config --global url."https://github.com/".insteadOf git@github.com:

# Add the marketplace
claude plugin marketplace add jamieburns/cowork-plugins-marketplace

# Install the plugin (needs GITHUB_TOKEN; gh auth provides it)
GITHUB_TOKEN=$(gh auth token) claude plugin install writing-cowork@jamie-cowork-plugins
```

Claude Code keeps versioned plugin caches at `~/.claude/plugins/cache/jamie-cowork-plugins/writing-cowork/<version>/`. Old versions are retained, not clobbered — useful for confirming which version actually landed.

## Per-iteration dev cycle

```bash
cd /Users/jburns/code/writing-cowork
# edit skills/.../SKILL.md or templates/...
# bump plugin.json version (e.g. 0.1.13 → 0.1.14)
claude plugin validate .
git add -A && git commit -m "v0.1.14: ..." && git push

claude plugin marketplace update jamie-cowork-plugins
GITHUB_TOKEN=$(gh auth token) claude plugin update writing-cowork@jamie-cowork-plugins
# "Restart to apply changes" — or inside an active Claude Code session, /reload-plugins
```

## Release checklist — every version bump touches THREE places

1. **`plugin.json` `version`** — source of truth.
2. **`skills/pm-version/SKILL.md`** — bump the `EXPECTED VERSION: v0.1.X` marker in the description AND the `Expected for v0.1.X` line in the output template. Two edits.
3. **Description text** — append/update `(v0.1.X)` at the end of `plugin.json`'s `description` AND the marketplace catalog entry's `description` in `cowork-plugins-marketplace`.

Skipping step 2 or 3 is exactly what caused the open v0.1.13/v0.1.14 discrepancy found during the 2026-07-21 reorg (see `1_Project/Decisions.md`).

Do NOT set `version` in both `plugin.json` and the marketplace catalog entry — `plugin.json` wins silently and a stale catalog version can mask a real one.

## Updating the Cowork-installed copy

**Superseded 2026-08-12 (`7c1b9e04` resolved).** The quit/relaunch/uninstall ritual below was written against Cowork's plugin-refresh behavior as observed through 2026-07-21. It was retested twice against a throwaway plugin (`refresh-probe`, in `0100_TestProduct/`, not shipped product) on 2026-08-12 and the simpler procedure now works:

1. **Push the version bump** — plugin repo commit/push, same as always.
2. **Update the marketplace first, not the plugin.** In Customize → Plugins → Marketplaces, find the marketplace and press its own Update/refresh control. The plugin-level "Update" button alone does **not** pick up a new version if the marketplace catalog hasn't been refreshed first — updating the marketplace is the step that actually matters.
3. **Give it a bit of time.** Sync isn't instant; a refresh attempted immediately after pushing may not see the new commit yet. Wait, then retry the marketplace update if the first attempt shows nothing new.
4. **Open a new context/chat to verify.** A session that already loaded the plugin keeps its own loaded copy for that session's lifetime — checking in the *same* context that was open during the update will not show the new version even after the update succeeded. Verify from a fresh chat.

No quit/relaunch required, no marketplace uninstall/reinstall required. Confirmed reproducible: two independent version bumps (`0.0.1`→`0.0.2`, `0.0.2`→`0.0.3` + a brand-new skill file), both picked up cleanly following this sequence, verified via a `pm-version`-style sentinel skill from a fresh context each time.

**What changed since the old procedure was written:** likely the 2026-07-21 Claude Desktop release (v1.24012.0) — "Added an option to keep custom plugin marketplaces up to date automatically, and fixed a marketplace refresh reporting success before the sync ran." That's the same bug class the old procedure was working around. See `Decisions.md` for the full test writeup.

**Not yet retested on the real `writing-cowork` plugin/`jamie-cowork-plugins` marketplace** — `refresh-probe` is a throwaway, structurally simple (one skill, no hooks, no drift_check) stand-in. The next real v0.1.17 release attempt is the first live test of whether this simplified procedure holds for the actual product. If it does, this whole section collapses to the four steps above with no fallback needed. If the real release still needs the old ritual, that's a meaningful difference worth its own `Decisions.md` entry — don't assume it transfers.

<details>
<summary>Old procedure (2026-07-21 through 2026-08-11), kept for reference in case the real plugin still needs it</summary>

**"Update plugin" button is unreliable** — Anthropic's marketplace proxy caches at the marketplace level; a plugin-level update doesn't invalidate it. Verified: a plugin-directory cache nuke does NOT work either — Cowork just re-fetches the stale cached version.

**What works: marketplace-level uninstall + reinstall** (`pm-refresh-cowork-plugin` documents this in skill form):

1. Cmd-Q, relaunch.
2. Customize → Plugins → uninstall `writing-cowork`.
3. Cmd-Q, relaunch.
4. Customize → Marketplaces → uninstall `jamie-cowork-plugins`. **This is the step that clears the proxy cache.**
5. Cmd-Q, relaunch.
6. Customize → Browse Plugins → Personal → re-add `jamieburns/cowork-plugins-marketplace`.
7. Cmd-Q, relaunch.
8. Customize → Plugins → install `writing-cowork`.
9. Cmd-Q, relaunch. Open a new chat. Verify via `pm-version`.

Total ~3-5 minutes. The repeated quits are empirically necessary.

**What does NOT work in Cowork:** "Update plugin" button, "Save plugin" button (generic validation-failed error even when `claude plugin validate` passes — undocumented Cowork-side bug), drag-drop `.plugin` zip, plugin-only uninstall/reinstall without the marketplace step.

</details>

## Cowork internals (for debugging only)

Also recovered 2026-07-26 from the retired memory store.

Cowork's plugin install is entirely separate from Claude Code's, at
`~/Library/Application Support/Claude/local-agent-mode-sessions/<host>/<workspace>/rpm/plugin_<id>/`,
with a `manifest.json` entry in the parent `rpm/` directory. Cowork has **no local marketplace catalog clone** — catalog metadata is fetched on demand from Anthropic's server-side proxy, so there is no local file to edit and no documented way to force a catalog refresh.

`~/.claude/settings.json`'s `extraKnownMarketplaces` is Claude Code CLI only; Cowork ignores it. (Two GitHub issue numbers were recorded alongside this in the old memory file. They are **unverified** — per `1_Project/Memory/feedback_verify_agent_citations.md`, agent-supplied issue numbers get checked before being quoted, and these never were. Deliberately omitted rather than propagated.)

## Repo visibility toggle

```bash
gh repo edit jamieburns/<repo> --visibility private --accept-visibility-change-consequences
gh repo edit jamieburns/<repo> --visibility public  --accept-visibility-change-consequences
```

The `--accept-visibility-change-consequences` flag is required by `gh`.

## Debug log

`~/Library/Logs/Claude/claude.ai-web.log` — search `remoteMarketplace`, `pollSyncUntilDone`, `PluginsFetcher`.

## Anthropic support

Thread `215474352137566` — filed with the cache-proxy observations above. Status unknown as of this reorg (2026-07-21); check before filing anything new.
