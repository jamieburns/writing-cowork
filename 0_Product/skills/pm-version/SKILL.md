---
name: pm-version
description: >
  Report the loaded writing-cowork plugin version plus a few content
  sentinels for refresh verification. **EXPECTED VERSION: v0.1.17** —
  this string appears in the description so you can verify the loaded
  version at a glance in the system-reminder skill listing without
  running anything. Use when the user asks "what version", "show plugin
  version", "verify the refresh", "did the update land", or any variant
  of confirming which writing-cowork build Cowork is currently using.
  MAINTENANCE: on every `plugin.json` bump, update BOTH the EXPECTED
  VERSION string in this description AND the `Expected for vX.Y.Z:`
  block in the body — they drift independently, and a stale body block
  makes a good install report STALE. Verified 2026-08-04 after all four
  body values were found wrong.
metadata:
  version: "0.1.2"
  role: pm
  subset: utility
  temporary: true
---

# pm-version

Report the loaded writing-cowork plugin version plus a small set of
content sentinels that change between versions, so the user can verify
quickly that a plugin refresh actually landed.

**Temporary skill.** Added in v0.1.9 to make refresh verification
trivial while the Cowork plugin update-detection bug is open (Anthropic
support thread 215474352137566). Remove once that bug is fixed upstream.

## Arguments

None.

## Preconditions

`${CLAUDE_PLUGIN_ROOT}` resolves to the plugin install dir. If unset,
report `CLAUDE_PLUGIN_ROOT not set` and fall back to inspecting the
current writing-cowork plugin via its known cache path
(`~/Library/Application Support/Claude/local-agent-mode-sessions/*/rpm/plugin_*/`
where plugin.json has `"name": "writing-cowork"`).

## Execution

Read these from the plugin root:

1. `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` — extract
   `version` field.
2. `${CLAUDE_PLUGIN_ROOT}/skills/` — count directories that contain a
   `SKILL.md`.
3. `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py` — extract
   `DRIFT_CHECK_VERSION` (grep for the constant assignment near the top
   of the file). Report `not present` if the file or constant is
   missing (indicates a pre-v0.1.17 plugin build, or an incomplete
   install).
4. Sentinels (markers that flip across versions):
   - **pm-show-kanban default `--by`** — read
     `${CLAUDE_PLUGIN_ROOT}/skills/pm-show-kanban/SKILL.md` and grep for
     the `--by=` argument's `default` value. Must equal whatever
     `skills/pm-show-kanban/SKILL.md` actually declares — `status` as of
     v0.1.14. Do not assert a value from memory; read the file.
   - **voice-* skills present** — `ls ${CLAUDE_PLUGIN_ROOT}/skills/`,
     check for any entry starting with `voice-` (Subset 3, v0.1.5+).
   - **kanban template uses dataviewjs** — grep for `dataviewjs` in
     pm-show-kanban SKILL.md (v0.1.8 layout).
   - **pm-version skill present** — trivially yes if this skill is
     running, but worth noting (v0.1.9+).
   - **tools/drift_check.py present** — bundled drift-check
     incorporation (v0.1.17+). Absent in older plugin versions, which
     relied on an external `~/code/cowork-tools/drift_check.py` instead.
   - **pm-sync-project-to-plugin present, pm-migrate-to-shared-tool
     absent** — the migrate skill was replaced by the more general
     sync skill in v0.1.17. If both are present, or neither, flag it —
     that's an inconsistent intermediate state, not a clean version.

## Output template

```
writing-cowork plugin version report
  plugin.json version:               <X.Y.Z>
  skill count (SKILL.md files):      <N>
  drift_check.py version (bundled):  <X.Y.Z | not present>
  pm-show-kanban default --by:       <status | milestone>
  voice-* skills present:            <yes | no>
  kanban uses dataviewjs:            <yes | no>
  pm-version skill present:          yes
  tools/drift_check.py present:      <yes | no>
  pm-sync-project-to-plugin present: <yes | no>
  pm-migrate-to-shared-tool present: <yes | no>

Expected for v0.1.17:
  version=0.1.17
  skill count = 66
  drift_check.py version >= 0.5.1
  default --by = status
  voice-* yes
  dataviewjs yes
  pm-version yes
  tools/drift_check.py yes
  pm-sync-project-to-plugin yes
  pm-migrate-to-shared-tool no

Status: <MATCH | STALE — refresh did not land | NEWER (sentinel out of date — bump pm-version description)>
```

Compare `version` from plugin.json against the expected v0.1.17 baked
into this skill description:

- exact match AND all sentinels match expected row → `MATCH`
- version lower than expected OR sentinel disagrees → `STALE — refresh did not land`
- version higher than expected (sentinel out of date because pm-version's description was not bumped on the last release) → `NEWER`, list which sentinels match the actual loaded version, and surface a reminder that pm-version's EXPECTED VERSION marker needs bumping

## Output on failure

- `CLAUDE_PLUGIN_ROOT not set and no plugin cache dir found for writing-cowork`
- `plugin.json missing or unreadable at <path>`

## Standalone use

Pure read. Safe anytime. Designed to be invoked immediately after any
plugin refresh attempt to confirm the new build actually landed.
