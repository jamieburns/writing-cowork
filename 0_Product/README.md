# 0_Product

What this project ships. This directory is the actual Claude Code plugin root.

- `.claude-plugin/plugin.json` — the plugin manifest
- `skills/` — the 60 (and counting) skills that make up the plugin
- `templates/` — scaffold templates skills copy into new vaults
- `Documents/` — reference/output documents for the product itself

**How this works:** `cowork-plugins-marketplace`'s catalog entry for `writing-cowork` uses a `git-subdir` source pointing at this subdirectory (`path: "0_Product"`), so Claude Code's plugin loader treats this folder — not the repo root — as the plugin root. `${CLAUDE_PLUGIN_ROOT}` in any skill resolves to this directory.

`.claude/settings.json` at the repo root is unrelated to this — that's this *dev repo's own* Cowork project setting (enabling writing-cowork while working in this repo), not part of the shipped plugin.

**Verification status:** restructured 2026-07-21 (v0.1.15). Tested via Claude Code CLI's marketplace-update cycle before any Cowork-side refresh was attempted — see `1_Project/Decisions.md` for the result.

**Removed 2026-07-21 (earlier housekeeping pass):** `docs/` (was empty) and `lift/README.md` — Jamie's own intentional cleanup; a new lift process will be written from scratch in a future development pass.
