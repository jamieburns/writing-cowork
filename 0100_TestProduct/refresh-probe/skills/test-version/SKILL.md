---
name: test-version
description: >
  Report the loaded refresh-probe plugin version. **EXPECTED VERSION: v0.0.2**
  — this string appears here so the loaded version is visible at a glance in
  the system-reminder skill listing, without running anything. Use when the
  user asks "what version is refresh-probe", "did the refresh land", "test
  version", or any variant of checking whether a refresh-probe update was
  picked up by this Cowork session. MAINTENANCE: bump the EXPECTED VERSION
  string here every time plugin.json's version is bumped, as part of each
  test cycle.
metadata:
  version: "0.0.2"
  role: test
  temporary: true
---

# test-version

Single-purpose skill for exercising the Cowork plugin-refresh cycle
(writing-cowork task `7c1b9e04`) without touching the real writing-cowork
install or any working writing project.

**This whole plugin is throwaway.** It exists only to answer one question:
does Cowork actually pick up a plugin version bump when you press "Update
plugin" (or run the full quit/relaunch/marketplace-reinstall procedure),
without any of the confounding factors a real plugin has (60+ skills,
drift_check, hooks, memory settings). Delete the plugin, its marketplace
entry, and this source folder once `7c1b9e04` is resolved.

## Arguments

None.

## Execution

1. Read `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` and extract the
   `version` field.
2. Report it plainly, in the output template below. Do not infer or recall a
   version from memory — read the file fresh every time this skill runs.

## Output template

```
refresh-probe plugin version report
  plugin.json version: <X.Y.Z>
  skill description EXPECTED VERSION marker: <vX.Y.Z>

Compare against what you expected to see after the last refresh attempt.
MATCH = refresh landed. STALE = still serving an older cached version.
```

## Standalone use

Pure read, no side effects. Safe to run any number of times, in any project,
at any point in a refresh test cycle.
