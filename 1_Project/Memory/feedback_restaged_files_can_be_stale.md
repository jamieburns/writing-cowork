---
name: restaged-files-can-be-stale
description: "device_stage_files can serve a cached copy when re-staging a path staged earlier in the same session — it reports the new size but the sandbox mount still holds the old bytes. Verify content, not the tool's report."
type: feedback
originSessionId: memory-management-port-2026-07-27
---

**Rule:** when re-staging a device path that was already staged earlier in the same session, do **not** trust the staged copy. Verify the content (grep for something you know you added), or bypass staging entirely and edit on the host.

**Why:** hit on 2026-07-27 during the plugin port. `pm-setup-project/SKILL.md` had been staged early in the session at 12883 bytes, then edited and written back to the device at ~13.4KB and committed. Re-staging the same path returned `{"bytes": 13458}` — the *correct* new size — but `/mnt/user-data/uploads/.../SKILL.md` still contained the original 12883 bytes from the first stage. A patch script run against that stale copy silently renumbered the wrong table and would have reverted the earlier work if written back.

This is the same failure class as the hidden-memory divergence that started this whole workstream: **a stale snapshot mistaken for current state, where nothing errors.** The tool's success report described the device file, not the bytes actually delivered.

**How to apply:**
1. Prefer editing on the host (osascript + a base64-encoded script) over stage → edit → commit, for any file this session has already written once.
2. If you do re-stage, immediately verify with a `grep` for a string you know is in the new version. Cheap, and it catches this instantly.
3. Make patch scripts **self-guarding** — assert the expected pre-state before mutating (e.g. `if 'pm-init-log' in s: already patched, exit` / `if 'pm-init-memory' not in s: wrong version, abort`). A guarded script that refuses to run beats a clean-looking script that corrupts.
4. Trust file *content* over tool *reports*. A size in a JSON response is not evidence that the bytes on the mount changed.
