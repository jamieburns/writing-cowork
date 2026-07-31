# `git status` from the sandbox view is a WRITE, not read-only

**Type:** feedback · **Recorded:** 2026-07-30

## The rule

Run **no** git command — not even `git status` — against the mounted sandbox
view of the repo. Only `git log`, `git show`, `git diff` and other commands that
never touch the index are safe there. Everything else goes through osascript on
the host.

## Why

The recorded invariant in `CLAUDE.md` says *"Git mutations go through osascript.
Anything that writes `.git/` (add, commit, push, tag) runs via the host…
**Read-only inspection is fine anywhere.**"* That last sentence is wrong, and it
cost a commit cycle on 2026-07-30.

`git status` refreshes the index, so it **creates `.git/index.lock`** before it
can do so. From the sandbox mount the create succeeds and the unlink fails:

```
warning: unable to unlink '.../.git/index.lock': Operation not permitted
```

The command still prints correct output, so it looks like it worked. What it
leaves behind is a zero-byte orphan lock that blocks the next **host-side**
`git add` or `git commit` with `fatal: Unable to create '.git/index.lock':
File exists`. The failure surfaces minutes later, in a different lane, and
reads like a crashed git process rather than like the read you just did.

This is the same EPERM pattern already recorded in
[Sandbox vs. host lane discipline](feedback_sandbox_host_lanes.md) — that note
identified the symptom but attributed it to mutations. The trigger is broader.

## How to apply

- Inspect state with `git log --oneline`, `git show`, `git diff` — index-free.
- For anything else, including `git status`, use osascript on the host.
- On `fatal: Unable to create '.git/index.lock': File exists`, do not assume a
  crashed process. Check `ls -la .git/index.lock` first: **zero bytes plus no
  live git process in `ps` means an orphan** and it is safe to `rm`. A non-empty
  lock, or a live git process, is a real in-flight write — leave it alone.
- `Decisions.md` recorded "no stale `.git/index.lock`" as a completed cleanup on
  2026-07-23. It came back the same way. Treat recurrence as expected until the
  invariant text itself is corrected — tracked as task `d51c9a27`.
