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

## Vault layout & folder-naming consistency (2026-07-22)

| Topic | Current decision |
|---|---|
| Cross-project consistency | Explicit design goal of this plugin. Default is to migrate a vault onto current conventions, not let the plugin tolerate multiple naming/config generations indefinitely. Aliasing/tolerating an old name is the exception, reserved for a specific named case where migrating is genuinely unreasonable (e.g. a name baked into an external system) — not a general fallback. |
| `research_and_analysis/` naming | **Rename, not alias** (reversed from an earlier draft recommendation to alias `analysis/`). Applies to consumer vaults; existing vaults migrate via `pm-sync-project-to-plugin --target=layout`. Git history (tag + commit) is the safety net that makes an imperfect automated rewrite acceptable — not the migration skill's own perfection. |
| `production/` folder | Standard name for build/output directories, formalizing prior ad hoc naming (e.g. `BookDeliverables/`). Convention landed 2026-07-22 in `templates/file_hierarchy.md`; the actual production-pipeline tooling stays deferred to v0.19 per `Next Version Goals.md`. |
| Retrofit/migration mechanism | One skill, not a family of similarly-scoped skills — `pm-sync-project-to-plugin` (v0.2.0) covers drift-check config (setup/upgrade/refresh) AND vault folder layout (`--target=layout`) in one mechanism. A standalone `pm-migrate-existing-project` skill was drafted 2026-07-22, then merged same-day rather than shipped as a sibling, following the precedent below. |
| Skill-consolidation precedent | `pm-migrate-to-shared-tool` (narrow: embedded-script → shared-script only) was superseded by `pm-sync-project-to-plugin` (broader: setup/upgrade/refresh). This precedent is why the 2026-07-22 vault-layout migration work was folded into the same skill rather than shipped standalone — one mechanism per "bring this vault current" job, not several overlapping ones that can drift apart. |

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

## Information Architecture Spine (2026-07-24) — LOCKED

Full design + rationale: `1_Project/Documents/information_architecture_spine_2026-07-24.md`. This table is the resting-state summary; that doc is the detail record. Implementation lands across v0.16 (log, memory router, close-session, handoff cleanup) and v0.17 (session hooks).

| Topic | Current decision |
|---|---|
| Record taxonomy | Every piece of project knowledge is exactly one of four kinds, each with one home + one lifecycle rule: **State** (what's true now — overwrite in place, kept small), **Log** (what happened + why + inputs — append-only), **Queue** (`inbox/*` — process then archive), **Ephemeral** (handoffs, drift reports, scratch — gitignored/cache, never a source of truth). **Reference** (`resources/`, memory, background) is a read-only sub-case of State. Identical in every vault — this is the consistency lever. |
| State-doc rules | Latest answer only (no history inside a State doc); small and bounded (unbounded growth = leaking Log/Reference content); one home per fact. Generalizes the rule this `Decisions.md` already follows. |
| Consumer-vault decisions ledger | **Confirmed:** ships in the template set. Consumer vaults currently get `charter.md` (rules) but no decisions ledger; add one in the same "current resting state" shape as this file. |
| Activity log — form | One **shared** log (not per-role), every entry **author-stamped** (role or user), **index-first** (terse/scannable; primary reader is the next session reloading state cheaply). Append-only markdown, one file, each entry links its git commit. Entry schema in the design doc. |
| Activity log — length (resolves §4 question) | Roll at **phase/version close** (not per-subphase); closed segment archives to `history/` named for the phase/version, live log starts fresh. Size safety-valve: numbered continuation if one phase's log runs long. Sessions read only the **tail** to orient, so file length is hygiene, not context cost. |
| Routing / three tiers | `CLAUDE.md` = always-loaded **router** (pointers + invariants only, never content — tiny by discipline; this is the context lever) → `project_hub.md` (State manifest + bounded read-set) + `Memory/INDEX.md` (Reference manifest) → topic files on demand. Includes a compact skill-routing map so skill choice is fast and legible. |
| Bounded read-contract | The hub names the exact short set a session reads to orient (hub, decisions, roadmap, todos, log tail, charter). Fixed-size; does not grow with project age. |
| Scope | **Additive "impose the spine"** (confirmed) — keep existing homes, add the missing Log + hub-manifest + `CLAUDE.md` router + consumer-vault decisions ledger; do not tear down the data_management set. |
| Enforcement | Folders enforce nothing. Build a **`pm-close-session`** skill (v0.16): atomically promote durable content → State home, append one author-stamped Log entry, write the single-slot handoff. Session-start orientation is convention now, a **hook** in v0.17. |

## Handoff lifecycle — ephemeral cache, not a permanent artifact (2026-07-23, re-locked 2026-07-24)

**Note:** this decision was recorded 2026-07-23 into an *uncommitted* `Decisions.md` and was lost when uncommitted changes were reverted before this session — a live instance of the exact failure the spine targets (durable content in a transient/uncommitted state evaporates). Re-locked here; commit promptly. Implementation deferred to v0.16 (`10_DeveloperSpace/Next Version Goals.md` v0.16 item 5). Applies to **both** this dev repo and consumer vaults.

| Topic | Current decision |
|---|---|
| Storage model | **Fully ephemeral, gitignored.** Session-close handoffs never enter git; local disk only (iCloud-synced), readable by the next kickoff session off disk. A routing note / baton — never a source of truth. |
| Safety rule (load-bearing) | A kickoff session's **first** job is to promote durable content into its State home (`Decisions.md`, roadmap, log) **before** the handoff is discarded. Ephemerality is only safe *because* durable content is promoted. |
| Cleanup (resolves §8 question) | **Single-slot.** `pm-close-session` writes *the* handoff; the next kickoff reads it, promotes the durable bits, then deletes it — at most one live handoff exists. Gitignored, so deletion is trivial. A drift-check Attention flag surfaces any straggler past a short window (confirm-before-delete, never silent). Existing dated pile in `1_Project/Handoff/` swept once (keep as frozen history or delete — Jamie's call); new ones never accumulate. |
| Scope | Dev repo + consumer vaults; consumer-side ships via a `.gitignore` entry for the handoff location + the drift-check flag; `pm-install-handoff` updated to place handoffs in the gitignored single-slot location. |

## Memory management (2026-07-24) — OPEN, not solved

Not a locked decision — recorded so the open problem is tracked, not lost. Detail in the spine design doc §6.

| Topic | Current state |
|---|---|
| Direction (low-confidence) | Make **vault memory authoritative** (`1_Project/Memory/` visible files + `INDEX.md`), wire `INDEX.md` into the `CLAUDE.md` router. Safe reversible steps only for now: router pointer + a `charter.md` line declaring vault memory authoritative. No new memory machinery until the risk below has a direction. |
| Core unresolved risk | Claude agents write to the **hidden platform memory store without consent**; on a long project this is where unexpected things silently pile up, invisible in Obsidian, never surfaced for review. This is the biggest unsolved control problem in the spine. |
| Open questions | (1) consent-on-write — can memory writes be gated on user approval, or does the platform store write regardless? (2) suppress/redirect the hidden store to visible vault memory, or at least mirror it for review; (3) audit/cleanup of already-accumulated hidden memory (drift-style surfacing: keep / promote / delete); (4) **boundary** — where's the line between memory vs. decision vs. charter-rule (Jamie owns this call, not yet made); (5) how much should a session trust hidden memory with no provenance. |

