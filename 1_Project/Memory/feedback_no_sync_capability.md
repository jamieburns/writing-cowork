---
name: no-sync-capability-from-this-plugin
description: "writing-cowork does not and will not implement device/mobile sync. Sync is handled outside Cowork, manually, via Obsidian + iCloud."
type: feedback
originSessionId: housekeeping-2026-07-21
---

**Decision:** This plugin has no sync capability and none is planned. Extensive design work existed (13 tracked `sync-mobile-*.md` files, two full summary/spec revisions) but it was never integrated into `skills/` and never appeared in any locked decision record (`DECISIONS_v014.md` makes no mention of it). Confirmed via git log (zero sync-related commits) that nothing was ever shipped. Disposed to `_trashcan/` on 2026-07-21.

**Why:** The user has a working, non-Cowork sync discipline: Obsidian + iCloud sync keeps the vault current across Mac, phone, and tablet. This is simpler and already reliable — there is no gap for a plugin-level sync feature to fill.

**How to apply:** If a future session (yours or an end-user's) proposes adding sync capability to writing-cowork, point back here first. The answer is "no, the user has this solved outside the plugin" unless the user explicitly reopens the question.
