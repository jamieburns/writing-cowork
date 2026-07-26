---
name: release-checklist-version-in-description
description: "Every writing-cowork version bump must update three places (plugin.json version, pm-version EXPECTED VERSION marker, and the (vX.Y.Z) tag in plugin/catalog descriptions) so Cowork's UI shows the version without opening files."
type: feedback
originSessionId: 988852c3-1715-4f55-8d1f-6cfeedc2a4a6 (promoted from the platform store 2026-07-25)
---

When bumping `writing-cowork`'s `plugin.json` version (e.g. v0.1.13 → v0.1.14), update three places, not just one:

1. **`plugin.json` `version`** field — the source of truth.
2. **`skills/pm-version/SKILL.md`** — bump the `EXPECTED VERSION: v0.1.X` marker in the description (visible at a glance in the system-reminder skill listing) AND the `Expected for v0.1.X` line in the output template. Two replace-all edits per release.
3. **Plugin description text** — append or update `(v0.1.X)` at the end of:
   - `plugin.json`'s `description` field
   - `<marketplace-repo>/.claude-plugin/marketplace.json` plugin entry `description` field

   These two should mirror each other (the catalog entry's description is what Cowork's Browse-Plugins UI shows).

**Why:** Jamie cannot find a way to check which version of a plugin is installed in Cowork without opening the cached `plugin.json` file. Putting `(v0.1.X)` in the visible description text gives at-a-glance verification through the UI alone. (Asked 2026-05-20 after the v0.1.13 reinstall.)

**How to apply:** Treat this as a mandatory step in any release commit. Avoid re-adding a separate `version` field to the marketplace catalog entry — the Anthropic docs explicitly warn that catalog-level and `plugin.json` versions can silently mismatch.

**Polished procedure:** `1_Project/Process/dev-workflow-and-release.md` §"Release checklist" is the manual; this file is the origin record.

**Provenance note (2026-07-25):** this memory existed *only* in the hidden platform store and was missed by the 2026-07-21 migration to visible vault memory. Promoted here during the memory-management prototype pass. Its absence is one of the three divergence failures documented in `1_Project/Documents/memory_management_recommendation_2026-07-25.md`.
