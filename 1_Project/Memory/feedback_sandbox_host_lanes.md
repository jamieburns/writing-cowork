---
name: Sandbox vs. host lane discipline
description: How to split work between sandbox/device bash, file tools, and osascript when operating on this user's repos. Avoids the git-lock-unlink issue.
type: feedback
originSessionId: 8092c0b2-4c4e-4724-ab0f-d17a1161895a (updated 2026-07-21)
---

When working on writing-cowork or any repo under `~/code/`, use this tool split:

| Operation type | Tool |
|---|---|
| Create / edit file contents | Write / Edit (cloud), or write via osascript heredoc on host |
| Read a file | Read, or device_bash `cat` |
| Inspect filesystem (ls, find, grep, status checks, `git log`, `git status`) | device_bash / sandbox bash — fine for read-only |
| Anything that MUTATES `.git/` (add, commit, push, merge, tag, rebase) | `mcp__remote-devices__Control_your_Mac__osascript` |
| Run host CLIs not in sandbox (`gh`, `brew`, etc.) | osascript |

**Why:** Mounted/bind-mounted views of the real filesystem (whether the cloud sandbox or the local `device_bash` VM) can create files in `.git/` but not reliably unlink them (EPERM on the mount layer). Git's normal flow creates `.lock` files mid-operation and removes them on success; the commit lands, but a leftover lock blocks the NEXT git command until manually cleared.

**Confirmed again 2026-07-21:** this isn't unique to the original cloud-sandbox case — `device_bash` (the local device-bridge VM) hit the exact same symptom: a stale `.git/index.lock` caused `unable to unlink ... Operation not permitted` on a plain `git status`. Running the same command via osascript (directly on the real Mac filesystem, no mount layer) worked immediately and cleanly removed the stale lock.

**How to apply:** Default to osascript for any git mutation, and for clearing a stuck lock. Use device_bash/sandbox bash freely for read-only inspection. Never mix — don't run `git commit` from a mounted-view bash hoping the locks come out clean. They won't.

**Osascript syntax tip:** `do shell script "..."` needs `export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin` because the default shell PATH doesn't include `gh` or other Homebrew-installed tools. Stdout returns as a single concatenated string — fine for commit/push, awkward for long output; route long output to a tempfile and `cat` it back if needed.
