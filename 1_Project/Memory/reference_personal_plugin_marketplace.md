---
name: personal-plugin-marketplace
description: "Raw reference notes on Jamie's two-client plugin distribution setup. See 1_Project/Process/dev-workflow-and-release.md for the polished, current procedure."
type: reference
originSessionId: 988852c3-1715-4f55-8d1f-6cfeedc2a4a6
---

Jamie's plugin distribution is split between two clients that share the plugin format but have entirely separate plugin systems:

- **Claude Code CLI** — the dev environment. All documented slash/CLI commands work as expected.
- **Cowork** — the runtime where the plugin's skills get invoked in writing sessions. Limited and unreliable plugin management UI.

**Catalog repo:** `github.com/jamieburns/cowork-plugins-marketplace` (public). Catalog name: `jamie-cowork-plugins`.
**Plugin source repo:** `github.com/jamieburns/writing-cowork` (public).

Cowork has **no local marketplace catalog clone** — catalog metadata is fetched on demand from Anthropic's server-side proxy. There is no local file to edit and no documented way to force a catalog refresh in Cowork. `~/.claude/settings.json`'s `extraKnownMarketplaces` is Claude Code CLI only — Cowork ignores it.

Full step-by-step procedure, what works and what doesn't in Cowork's update UI, and the debug log location are now in `1_Project/Process/dev-workflow-and-release.md` — this file is kept as the original raw reference.
