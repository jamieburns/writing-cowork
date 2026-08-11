---
name: personal-plugin-marketplace
description: Raw reference notes on Jamie's  plugin distribution setup.
type: reference
originSessionId: 988852c3-1715-4f55-8d1f-6cfeedc2a4a6
---
**Catalog repo:** `github.com/jamieburns/cowork-plugins-marketplace` (public). Catalog name: `jamie-cowork-plugins`.
**Plugin source repo:** `github.com/jamieburns/writing-cowork` (public).

Cowork has **no local marketplace catalog clone** — catalog metadata is fetched on demand from Anthropic's server-side proxy. There is no local file to edit and no documented way to force a catalog refresh in Cowork. `~/.claude/settings.json`'s `extraKnownMarketplaces` is Claude Code CLI only — Cowork ignores it.

Full step-by-step procedure, what works and what doesn't in Cowork's update UI, and the debug log location are now in `1_Project/Process/dev-workflow-and-release.md` — this file is kept as the original raw reference.
