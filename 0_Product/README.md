# 0_Product

This folder is a pointer, not a container.

Claude Code's plugin loader requires `skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`, `.lsp.json`, `monitors/`, `bin/`, and `settings.json` to live at the **plugin root** — this is not configurable via `plugin.json`. Nesting them under a subfolder (like `0_Product/skills/`) breaks the plugin for both Claude Code and Cowork.

So: the actual product — what this project ships — lives at the repo root, not here:

- `skills/` — the 58 (and counting) skills that make up the plugin
- `templates/` — scaffold templates skills copy into new vaults
- `.claude-plugin/plugin.json` — the plugin manifest
- `docs/` — user-facing documentation (currently empty)
- `lift/README.md` — the staged vault-setup procedure
- `.claude/settings.json` — this dev repo's own Cowork project settings

This folder exists so the 0/1/2 numbering is complete and the intent is documented, without physically risking the shipped plugin.

**Decision recorded:** 2026-07-21, during the housekeeping/reorg pass. See `1_Project/Decisions.md`.
