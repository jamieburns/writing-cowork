---
name: restaged-files-can-be-stale
description: "device_stage_files pins its copy to the FIRST stage of a path for the whole session. Re-staging never refreshes it, and the tool reports the device file's real size while serving old bytes. Edit on the host instead."
type: feedback
originSessionId: memory-management-port-2026-07-27
---

**Rule:** a file staged into the sandbox is a **point-in-time copy pinned to the first stage of that path**. Re-staging does **not** refresh it. For any file this session has already staged once, edit it on the host via `osascript`, or verify the staged content with a `grep` before trusting it.

**Why:** hit on 2026-07-27 during the plugin port, then confirmed by direct test. `pm-setup-project/SKILL.md` was staged early at 12883 bytes, then edited, written back, and committed twice. Two later re-stages reported `{"bytes": 13458}` and `{"bytes": 13707}` — both the correct current size on the Mac — while `/mnt/user-data/uploads/.../SKILL.md` still held the original **12883 bytes, mtime Jul 26 15:45**. The stale copy survived **two re-stage attempts across 20+ hours**, so this is not a short TTL: the copy is effectively write-once per path per session.

A patch script run against that stale copy renumbered the wrong table and would have reverted the previous slice if written back.

**What makes it dangerous:** the tool's JSON response describes the file **on the device** — size and mtime both accurate — while the mount serves different bytes. Every signal reads "fresh." Nothing errors. This is the same failure shape as the hidden-memory divergence that started this workstream: *a snapshot mistaken for live state, where the reporting layer describes the source rather than what was delivered.*

**The lanes, and which ones copy:**

| Lane | Runs on | Copies? |
|---|---|---|
| `Read`/`Write`/`Edit`/`Bash` | cloud VM | VM filesystem only |
| `device_stage_files` | Mac → VM | yes — snapshot, pinned to first stage |
| `device_commit_files` | VM → Mac | yes — writes to real disk |
| `osascript` | the Mac itself | **no copy** — safe lane |

**How to apply:**
1. Stage a path **once** per session. After the first write-back, treat that staged copy as dead.
2. For repeat edits, run a script on the host: write it locally, `base64 -w0` it, then `echo '<b64>' | base64 -d > /tmp/x.py && /usr/bin/python3 /tmp/x.py` via `osascript`. Base64 avoids AppleScript quoting entirely.
3. Make patch scripts **self-guarding** — assert expected pre-state before mutating (`if 'new-marker' in s: already patched, exit` / `if 'expected-anchor' not in s: wrong version, abort`). A guarded script that refuses to run beats a clean-looking one that corrupts.
4. Trust file **content** over tool **reports**. A size in a JSON response is evidence about the source file, not about the bytes on the mount.
