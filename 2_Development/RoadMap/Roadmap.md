# writing-cowork Roadmap

High-level phase/version summary. Full detail for each version lives in its own folder under `2_Development/RoadMap/`.

| Version | Status | Summary |
|---|---|---|
| v0.1.1 – v0.1.9 | Shipped | Foundation, Planning (Subset 2), Voice/tone (Subset 3), refresh-workaround skill, MVP validated |
| v0.1.10 – v0.1.11 | Shipped | Dev-workflow hardening (Claude Code CLI as the dev environment), pm-refresh rewritten as a documented consumer-side workaround |
| v0.1.12 – v0.1.13 | Shipped | `inbox/README.md` scaffold, `inbox/issues/` convention + `pm-create-issue-report` + `pm-escalate-issue` (GitHub routing) |
| v0.1.14 | **Status unclear — see below** | Assignee column (6 skills + role_taxonomy template) committed. Review Skills (Subset 4, 13 skills) and Drift Enhancements were locked in `DECISIONS_v014.md` but not obviously committed. |
| v0.1.15+ | Not started | `review-prep-reader-bundle`'s PM-side packaging counterpart (deferred from v0.1.14 decision) |

## ⚠️ v0.1.14 needs a status check

`plugin.json` says `0.1.14`. The only v0.1.14-labeled commit in git history is `c6fbc9e [v014] Assignee column`. `DECISIONS_v014.md` locked decisions for Review Skills and Drift Enhancements too — unclear if those were implemented, abandoned, or are still in flight. `pm-version`'s marker still says v0.1.13, which is itself evidence the release checklist wasn't completed. **First task of the next dev session: figure out what's actually true about v0.1.14 before doing anything else.**

## Legacy / carried-over work items

- Subset 4 (Review, 13 skills per the locked v0.1.14 decision)
- Subset 5 (Substance, 3 skills — mentioned in earlier project notes, not detailed in any current design doc found during this reorg — worth confirming this is still wanted)
- Phase 9 (legacy `todos.md` migration to vault) — no `todos.md` was found in this repo during the reorg; if this refers to something in a different (end-user) vault, track it there instead
