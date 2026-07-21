# Decisions — Current State

This file holds the **current resting state** of decisions only — the latest answer, not the history of how we got there. Full rationale and dated lockdown records live in `2_Development/RoadMap/v0.1.14/DECISIONS_v014.md` and future version-specific decision files.

When a decision changes, update the row here; don't append a new one. The old value's rationale stays in the versioned RoadMap detail file where it was originally locked.

---

## Repo structure & housekeeping

| Topic | Current decision |
|---|---|
| Sync capability | Not delivered, never will be from this plugin. Discipline is Obsidian + iCloud across Mac/phone/tablet, managed outside Cowork. See `1_Project/Memory/feedback_no_sync_capability.md`. |
| `0_Product` folder | `templates/` lives here (moved 2026-07-21). `skills/` and `.claude-plugin/` stay at repo root **for now** — see "Full 0_Product consolidation" below for why this could change later. |
| `docs/`, `lift/` | Removed by Jamie 2026-07-21 (intentional cleanup, not a bug — I initially misread this and wrongly restored them, then corrected). Next development pass will write a new lift process from scratch. |
| `10_DeveloperSpace/` | Jamie's personal notes-to-self space. Git-managed (tracked, not gitignored) but excluded from Claude's reads via `.claudeignore` (which IS tracked in git — only the folder's contents are hidden, not the exclusion mechanism itself). |
| Reorg scope | This dev repo only. Does NOT change what `pm-init-vault`/`pm-setup-project` scaffold for new end-user writing projects. |
| Memory management | All memories live as visible files in `1_Project/Memory/`, not in hidden session-managed storage. No new memory files outside this location without explicit user consent. |

## Plugin development (carried over from `DECISIONS_v014.md`)

**v0.1.14 status (confirmed by Jamie, 2026-07-21): released, in successful daily use for 2 months.** Only the Assignee Column workstream actually shipped — confirmed by skill listing, no `review-*`/`cycle-*` skills exist. Review Skills and Drift Enhancements were locked decisions but are open work, not urgent, see `2_Development/RoadMap/Roadmap.md`.

| Topic | Current decision |
|---|---|
| Review Skills (Subset 4) | Locked: integrate 13 skills (cycle management + in-cycle feedback workflow), unified delivery. **Not yet shipped.** |
| Review setup mechanism | Extend `pm-init-reader-review-tracking` rather than creating a parallel skill |
| Reader-bundle pattern | Add `review-prep-reader-bundle`; PM-side packaging deferred to v0.1.15+ |
| Cross-phase dependency detection | Warn on ANY cross-phase dependency by default; per-project override in `drift_check.yaml`. **Ship status unverified** — may be embedded in existing `pm-run-drift-check`/`drift_check.py` code rather than a new skill name. |
| Status staleness format | `<!-- ROLE-STATUS-UPDATED-YYYY-MM-DD -->`, embedded comment. Ship status unverified, same caveat as above. |
| Staleness threshold | Global 14-day default, per-project override. Ship status unverified. |
| Assignee sourcing | Read role taxonomy from `charter.md`. **Shipped in v0.1.14.** |
| Assignee kanban grouping | `--by=assignee` as an alternative mode, not always-on column. **Shipped in v0.1.14.** |

## Full 0_Product consolidation — DONE for Claude Code CLI, Cowork not yet tested (2026-07-21)

Executed: `writing-cowork` restructured to v0.1.15 (`.claude-plugin/`, `skills/`, `templates/` all under `0_Product/`, commit `d524b90`), `cowork-plugins-marketplace` updated to catalog `1.0.10` with a `git-subdir` source pointing at `path: "0_Product"` (commit `30a73a5`). Both pushed to GitHub.

**Verified via Claude Code CLI:** `claude plugin marketplace update jamie-cowork-plugins` + `claude plugin update writing-cowork@jamie-cowork-plugins` reported success, jumping straight to 0.1.15. Confirmed by inspecting the actual cache directly (not just trusting the CLI's success message): `~/.claude/plugins/cache/jamie-cowork-plugins/writing-cowork/0.1.15/` has `.claude-plugin/`, `skills/` (60 skills), `templates/`, `Documents/`, `README.md` directly at its root — the sparse git-subdir checkout correctly flattened `0_Product/`'s contents, no nested wrapper. `plugin.json` reads back correctly. This resolves the open question about whether `git-subdir` actually works.

**Not yet done: Cowork side.** Per the agreed plan, Cowork's install hasn't been touched. Next step, when ready: the marketplace-level uninstall/reinstall procedure (`1_Project/Process/dev-workflow-and-release.md`), then verify with `pm-version`. If Cowork's installer doesn't support `git-subdir` the way Claude Code CLI's does, this is where it would surface — have the rollback plan ready first (revert the marketplace source back to plain `github`+`repo` pointing at the old repo-root layout, which still exists in git history at commit `c6fbc9e` if needed, though `writing-cowork` itself would also need reverting since `0.1.14`'s repo-root layout no longer exists on `main`).

## Historical: original research before execution (2026-07-21, superseded by the above)

Jamie's actual goal for `0_Product`: the whole shipped plugin (`.claude-plugin/`, `skills/`, `templates/`) living together there, kept pristine and separate from dev notes — not just a pointer/README. `templates/` achieves this already. `skills/`/`.claude-plugin/` can't move to a subfolder of *this repo* under the plugin loader's default assumption (plugin root = wherever `.claude-plugin/plugin.json` lives = repo root, for a normal install) — **but there is a real mechanism that would make it possible:**

Claude Code's marketplace schema supports a `git-subdir` source type:
```json
"source": {
  "source": "git-subdir",
  "url": "jamieburns/writing-cowork",
  "path": "0_Product",
  "ref": "main"
}
```
This makes the *subdirectory* the effective plugin root for install purposes — via a sparse partial clone. If `cowork-plugins-marketplace`'s catalog entry for `writing-cowork` used this instead of the current `github`+`repo` source, `0_Product/` could genuinely contain the entire plugin (`.claude-plugin/`, `skills/`, `templates/`) with dev/process/roadmap content fully separated in `1_Project/`/`2_Development/`.

**Why held off:** two blockers, both about doing this safely rather than about whether it's possible.
1. Docs describe `git-subdir` specifically for Claude Code CLI. Given Cowork's marketplace/plugin system has repeatedly diverged from documented CLI behavior (stale-cache bug, ignored `extraKnownMarketplaces`, undocumented validation failures — see `2_Development/RoadMap/Roadmap.md`), Cowork support for `git-subdir` is **unverified**. If unsupported, the next Cowork-side refresh could break the plugin you use daily until manually rolled back.
2. This requires a coordinated change across two repos (`writing-cowork` + `cowork-plugins-marketplace`) landing together — moving one without the other breaks the next `claude plugin update` immediately. Session access to `cowork-plugins-marketplace` wasn't granted this pass.

**To revisit:** grant folder access to `cowork-plugins-marketplace`, or make the marketplace.json edit yourself using the snippet above (adjust `path` if `.claude-plugin` and `skills` haven't actually moved into `0_Product` yet — do that move in `writing-cowork` first, then the marketplace edit, then test via `claude plugin marketplace update` + `claude plugin update` in Claude Code CLI *before* attempting any Cowork-side refresh).

## Resolved during reorg (2026-07-21)

`plugin.json` was at v0.1.14 while the `pm-version` skill's EXPECTED VERSION marker still said v0.1.13 — a release-checklist gap (marker wasn't bumped when v0.1.14 shipped). Fixed: marker, "Expected for" block, and skill-count sentinel (58→60) all updated in `skills/pm-version/SKILL.md`.

**Still open, not resolved here:** Anthropic support thread 215474352137566's current status — filed via support.claude.com, no connector/API access to check it. Needs Jamie to check directly. Subset 5 (Substance) — user is handling separately.
