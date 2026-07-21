# Issues — User Experience Tracker

This tracks process/plugin friction **you** hit while actually using writing-cowork day to day — not development bugs or feature work (those live in `2_Development/`), and not the GitHub-issue escalation pipeline that specialist contexts in *end-user* vaults use (`inbox/issues/` + `pm-create-issue-report` + `pm-escalate-issue` — that mechanism is part of the shipped product, for vaults this plugin scaffolds, and is unrelated to this file).

Closed/resolved issues move to `1_Project/History/` with their resolution noted.

| Date | Issue | Status | Notes |
|---|---|---|---|
| 2026-07-21 | Project memory was stored in hidden session-managed files, not visible/manageable by the user | Resolved | Moved to `1_Project/Memory/`, rule added preventing new hidden memory files without consent |
| 2026-07-21 | Device-bridge folder access reported disconnected (`connectedFolders: []`) despite the folder having been connected for months and showing connected in the app | Open | Root cause unclear — possibly per-session grants don't persist across new chat sessions even when the project-level connection is unchanged. Re-granting fixed it for this session. Worth raising with Anthropic support if it recurs. |

