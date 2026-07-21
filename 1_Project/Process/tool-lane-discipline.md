# Tool Lane Discipline

How work is split across sandbox/device tools and the real Mac filesystem. Distilled from `1_Project/Memory/feedback_sandbox_host_lanes.md`.

| Operation type | Tool |
|---|---|
| Create / edit file contents (drafting, non-git) | Write/Edit in cloud sandbox, or write via `device_bash`/osascript |
| Read a file | Read tool, or `device_bash cat` |
| Inspect filesystem (ls, find, grep, `git log`, `git status`) | `device_bash` — fine for read-only |
| Anything that MUTATES `.git/` (add, commit, push, merge, tag, rebase) | `mcp__remote-devices__Control_your_Mac__osascript` |
| Run host CLIs not in the mounted sandbox (`gh`, `brew`, etc.) | osascript |
| Clearing a stuck `.git/index.lock` | osascript — mounted views (cloud sandbox AND `device_bash`) can create the lock file but hit EPERM trying to remove it |

**osascript syntax:** `do shell script "export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin; ..."` — the default shell PATH omits Homebrew-installed tools like `gh`.
