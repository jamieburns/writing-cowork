---
name: pm-version
description: >
  Report the loaded writing-cowork plugin version plus a few content
  sentinels for refresh verification. **EXPECTED VERSION: v0.1.13** —
  this string appears in the description so you can verify the loaded
  version at a glance in the system-reminder skill listing without
  running anything. Use when the user asks "what version", "show plugin
  version", "verify the refresh", "did the update land", or any variant
  of confirming which writing-cowork build Cowork is currently using.
  MAINTENANCE: bump the EXPECTED VERSION string in this description
  every time `plugin.json` version is bumped (release-process step).
metadata:
  version: "0.1.1"
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
3. Sentinels (markers that flip across versions):
   - **pm-show-kanban default `--by`** — read
     `${CLAUDE_PLUGIN_ROOT}/skills/pm-show-kanban/SKILL.md` and grep for
     the `--by=` argument's `default` value (should be `milestone` in
     v0.1.8+, `status` in older).
   - **voice-* skills present** — `ls ${CLAUDE_PLUGIN_ROOT}/skills/`,
     check for any entry starting with `voice-` (Subset 3, v0.1.5+).
   - **kanban template uses dataviewjs** — grep for `dataviewjs` in
     pm-show-kanban SKILL.md (v0.1.8 layout).
   - **pm-version skill present** — trivially yes if this skill is
     running, but worth noting (v0.1.9+).

## Output template

```
writing-cowork plugin version report
  plugin.json version:           <X.Y.Z>
  skill count (SKILL.md files):  <N>
  pm-show-kanban default --by:   <status | milestone>
  voice-* skills present:        <yes | no>
  kanban uses dataviewjs:        <yes | no>
  pm-version skill present:      yes

Expected for v0.1.13:
  version=0.1.13
  skill count >= 58
  default --by = milestone
  voice-* yes
  dataviewjs yes
  pm-version yes

Status: <MATCH | STALE — refresh did not land | NEWER (sentinel out of date — bump pm-version description)>
```

Compare `version` from plugin.json against the expected v0.1.13 baked
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
