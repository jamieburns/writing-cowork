# 0_Product

What this project ships.

**Physically inside this folder:**

- `templates/` — scaffold templates skills copy into new vaults. Moved here 2026-07-21; all 12 referencing skills updated to `${CLAUDE_PLUGIN_ROOT}/0_Product/templates/...`.
- `Documents/` — reference/output documents for the product itself (as distinct from process or development docs — see the sibling `Documents/` folders under `1_Project/` and `2_Development/`).

**Physically at repo root, not here — cannot move:**

- `skills/` — the 60 (and counting) skills that make up the plugin
- `.claude-plugin/plugin.json` — the plugin manifest
- `.claude/settings.json` — this dev repo's own Cowork project settings

Claude Code's plugin loader requires `skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`, `.lsp.json`, `monitors/`, `bin/`, and `settings.json` to live at the **plugin root** — this is not configurable via `plugin.json`. Nesting them under a subfolder breaks the plugin for both Claude Code and Cowork. `templates/` had no such constraint (not a reserved plugin directory name), so it moved; `skills/` and `.claude-plugin/` do and stay put.

**Removed 2026-07-21:** `docs/` (was empty) and `lift/README.md` (the staged vault-setup procedure) — Jamie cleaned these up directly; the next development pass will capture a new lift process from scratch rather than carry the old one forward.

**Decision recorded:** 2026-07-21, during the housekeeping/reorg pass. See `1_Project/Decisions.md`.
