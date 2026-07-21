---
name: Self-contained scripts when Cowork must be quit
description: Any operation requiring Cowork to be quit must be packaged as a single Terminal-runnable script prepared BEFORE the user quits. No mid-quit coordination.
type: feedback
originSessionId: 988852c3-1715-4f55-8d1f-6cfeedc2a4a6
---
When a workflow requires Cowork to be quit (cache-nuke, manifest edits, anything touching live plugin state), package the whole sequence as a self-contained script the user runs from Terminal after Cmd-Q. Do NOT plan a "quit, then tell me, then I'll run a command" handoff — that doesn't work, because once Cowork is quit, this chat is gone and there's no way to coordinate.

**Why:** Twice in one session a "quit Cowork, confirm to me, I'll do step 2" workflow was planned. Both times the user (correctly) called out that this is impossible.

**How to apply:**
1. Prepare the full script BEFORE the user quits Cowork. Write it to `/tmp/<descriptive-name>.sh`.
2. Script should be self-verifying — check Cowork is actually quit (`pgrep -x "Claude"`) and abort with a clear error if not.
3. Script should be self-healing — back up any files it modifies, validate the result, leave restoration instructions in the output.
4. Script should be end-to-end — do the cleanup, the edits, AND the relaunch. User runs ONE thing.
5. Tell the user: Cmd-Q Cowork, then in Terminal: `bash /tmp/<name>.sh`. Single transaction.
