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

## Memory management (2026-07-24, researched + prototyped 2026-07-25) — PARTLY RESOLVED, prototype in flight

Research complete; a prototype is running **in this dev repo** before anything is ported to the plugin. Detail: spine design doc §6, `1_Project/Documents/memory_control_research_2026-07-25.md` (what the platform offers), `1_Project/Documents/memory_management_recommendation_2026-07-25.md` (what to do about it), `1_Project/Documents/memory_gating_test_2026-07-25.md` (the pending experiment).

**The empirical finding that reframed this (2026-07-25):** the two stores had already diverged in this repo. `feedback_visible_memory_only.md` — the rule saying "don't write to the hidden store" — existed **only in the vault**, which the platform store never loads; the rule sat in the one place the governed mechanism cannot see. Separately, the platform store's project-state file still claimed v0.1.13 and misinformed a live session. Divergence was not a future risk; it had already produced a wrong belief. Both now reconciled.

| Topic | Current state |
|---|---|
| §6c-1 consent-on-write | **Answered:** achievable via a `PreToolUse` hook that matches the memory write and blocks it — the docs are explicit that hooks enforce where instructions only persuade. Not shipped by default; would be a custom build. **Deliberately not building it yet** — depends on two unverified things at once (that Cowork runs hooks, and that matchers catch `mcp__*` calls), and the audit diff gets most of the benefit with none of the risk. |
| §6c-2 suppress / redirect | **Answered:** `autoMemoryEnabled: false` suppresses (user or per-project scope); `autoMemoryDirectory` redirects storage location; `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` is the env-var equivalent. Real documented settings, not workarounds. **Caveat:** all documented for Claude Code CLI; Cowork binding unverified — that is the gating test. |
| §6c-3 audit / cleanup | **Partly answered:** the store is plain markdown and inspectable (`/memory` in CLI); it is *unsurfaced*, not *hidden*. What is genuinely missing is **proactive periodic surfacing** — a drift-check-style flag. Remains to build (step 4). |
| §6c-4 memory / decision / charter-rule boundary | **RESOLVED 2026-07-26** (Jamie confirmed). See "Knowledge routing rule" below — this was the last item blocking the plugin port. |
| §6c-5 trust in unprovenanced memory | Slightly improved: CLI v2.1.214+ stamps a `modified` frontmatter timestamp on memory writes, so there is a recency signal — still no why/inputs provenance like the §4 activity log. |
| Chosen direction | **Make git the consent mechanism.** Put memory where an unapproved write shows up as an uncommitted change: `git status` is the surfacing §6c-3 asks for, `git diff` the review, `git checkout` the reject. Consent-on-write becomes consent-on-commit — weaker in theory, but achievable today **in both runtimes** with no new machinery. |
| Option chosen | **B preferred** (redirect the auto-memory store into `1_Project/Memory/` so there is one pile, auto-loaded and git-visible), **A as fallback** (disable outright, vault-only by discipline). Contingent on the gating test. |
| Load-bearing constraint | Every control found is documented for **Claude Code CLI**; Cowork memory runs through `mcp__remote-devices__project_memory_*`. Jamie develops in CLI but **consumer vaults run in Cowork** — so a settings-based control may protect the dev loop and protect nothing in the product. Controls built on **files + git** are runtime-independent; prefer those. |
| §6e "split by kind" hypothesis | **Adjusted.** All 7 platform-store files were project-specific `writing-cowork` content; zero cross-project user facts. At *project* scope the platform store has no legitimate resident — the split may still hold at *user* scope, but it was doing no work here. |
| Gating test | **Armed 2026-07-25, result pending.** `.claude/settings.json` now sets `autoMemoryEnabled: false` + `autoMemoryDirectory`. A fresh Cowork session distinguishes three outcomes (both bind / only directory binds / neither binds) and also checks whether Cowork loads repo-root `CLAUDE.md` at all. Procedure and outcome table: `memory_gating_test_2026-07-25.md`. **Record the result here when known.** |
| Shipped this pass | Two stores reconciled; repo-root `CLAUDE.md` Tier-1 router created (spine §5) with the marker convention below. |

### CLAUDE.md marker convention (new 2026-07-25, prototype — not yet in the plugin)

Plugin-managed markdown files delimit ownership with block-level HTML comments: `BEGIN/END WRITING-COWORK MANAGED: <block-name>` for plugin-owned content regenerated on sync, and `BEGIN/END PROJECT-OWNED` for content the plugin never touches.

**Pre-existing marker to reconcile (found 2026-07-26):** `templates/project_hub.md` already uses `<!-- DRIFT-ATTENTION-START -->` / `<!-- DRIFT-ATTENTION-END -->` for the drift-check-written Attention block — the same idea under different naming, and `drift_check.py` greps for those exact strings. Left alone for now rather than renamed, because renaming breaks the tool. Reconciling the two naming schemes is part of the open marker-coverage decision (spine §10.9); the general convention should absorb the drift block as a named instance (`MANAGED: drift-attention`) when the tool can be updated in the same change. Comments are stripped before the file enters model context, so markers cost no runtime tokens — but that also means the model cannot see them, so each managed file carries one short *visible* line stating the boundary. **`.claude/settings.json` is the exception:** JSON has no comments, so its provenance is documented in the gating-test doc instead. Port target: a `--target=router` mode on `pm-sync-project-to-plugin`, per the skill-consolidation precedent above (one mechanism per "bring this vault current" job).


## Knowledge routing rule (2026-07-26) — LOCKED

Confirmed by Jamie. Resolves spine §6c-4 / §10.6, the last decision blocking the plugin port. Ships in `templates/charter.md` (§"Knowledge routing") and in the `router-orientation` block of `templates/CLAUDE.md`.

Every durable fact has exactly **one** home, determined by what kind of thing it is:

| Kind of thing | Home | Test |
|---|---|---|
| A repeatable **operating procedure** | the relevant `process/` doc | "this is how we do X" — followable as steps |
| A raw **observation or correction** | `process/memory/` (`1_Project/Memory/` in this dev repo) | "we learned X" — a fact, not yet a procedure |
| A **commitment or choice** | the decisions record (this file) | "we decided X, and it stands until revisited" |
| A **standing constraint** on how work is done | `charter.md` | "X is always true of how this project runs" |

Memory is the raw log; a process doc is the manual. When a memory matures into a repeatable procedure, write the process doc and keep the memory file as its origin record — do not duplicate content in both. If a fact seems to belong in two places, one of them is a pointer; two live copies drift and the stale one keeps being read as current.

**Empirical basis:** on 2026-07-26 a session given a durable operating rule ("always run `claude plugin validate .` before committing a version bump") routed it to `1_Project/Process/dev-workflow-and-release.md` plus an activity-log entry, not to either memory store — landing in two git-visible files and zero invisible ones. The rule above generalizes that observed behaviour rather than imposing a new one.

## Plugin port — memory management (2026-07-26) — IN PROGRESS

First slice of stage 3. New in `0_Product/`:

| Artifact | Purpose |
|---|---|
| `templates/CLAUDE.md` | Tier-1 router for consumer vaults; two managed blocks (`router-orientation`, `router-skills`) plus a `PROJECT-OWNED` block. Carries the knowledge-routing rule and the skill-routing map. |
| `templates/memory_index.md` | `process/memory/INDEX.md` manifest — the Reference-layer Tier-2 manifest, ships empty. |
| `templates/charter.md` | Gained §"Knowledge routing" (the rule above) as the first Operating rule. |
| `skills/pm-install-router/` | Places `CLAUDE.md` at vault root. **Refuses to overwrite an existing `CLAUDE.md`** — no merge, no silent rewrite. |
| `skills/pm-init-memory/` | Creates `process/memory/` + `INDEX.md`. |
| `skills/pm-setup-project/` | Both wired into the orchestration: 20 sub-skills → **22**, router at step 9 (after the hub it points at), memory at step 13 (with data-management scaffolding). Narration groups 3 and 4 updated; stale "15/19/20 sub-skills" counts corrected throughout. |

**Second slice landed 2026-07-27** — §10.7–10.11 all answered, so the deferred items shipped: `pm-init-project-cowork-settings` v0.2.0 (Option B redirect by default, `--memory=disable` as the Option A fallback, path **computed at install** since `autoMemoryDirectory` requires an absolute path); `templates/log.md` + `pm-init-log` (`process/Log.md`, newest-last); and `file_ownership.md` extended into the **plugin-managed provenance registry** that answers the JSON problem. `pm-setup-project` now runs **23** sub-skills. Still open: rolling ownership markers across the remaining templates — see the regenerated/scaffold-once distinction below.

**Marker coverage needs two classes, not one** (refines §10.9's "yes to all files"): **regenerated** files have their marked blocks rewritten on sync (`CLAUDE.md`, the pure-reference docs) and need `BEGIN/END` markers; **scaffold-once** files are written once and belong to the user thereafter (`charter.md`, `project_hub.md`, roadmap, todos, `Log.md`, memory `INDEX.md`) and need only a provenance row in `file_ownership.md`. Blanket-wrapping everything would have the plugin claim ownership of files the writer actually owns — and `Log.md` in particular must never be rewritten. Both classes are now tabulated in the `file_ownership.md` template.

**Consumer memory location:** `process/memory/`, parallel to `process/active/` and `process/data_management/`. New convention introduced by this slice; not previously specified.

## Memory management — open questions resolved (2026-07-26)

Jamie's answers to spine §10 items 7–11, plus the `pm-install-router` merge requirement.

| # | Question | Decision |
|---|---|---|
| 7 | Default memory model | **Option B** — redirect the auto-memory store into the vault memory directory. Proceed in this direction. **Option A (disable outright) retained as fallback** if something bad surfaces. |
| 8 | Path portability | **Compute at install.** The template ships no path; the setup/sync skill resolves the absolute path at install time and writes it. |
| 9 | Marker coverage | **All plugin-managed files.** JSON handled per the recommendation below. |
| 10 | Activity log | **Confirmed** — `Log.md` at the process root, newest-last, rolls at phase/version close. Consumer equivalent: `process/Log.md`. |
| 11 | Fate of the platform store | **Retired.** Every entry reviewed and dispositioned; retained content promoted; store left empty. Done 2026-07-26 — see below. |

### JSON provenance — recommendation (§10.9)

The marker convention is markdown-only. Three-part answer:

1. **Where we control the format, use YAML.** `drift_check.yaml` already does; any *new* plugin-managed config should be YAML, which takes `#` comments and can carry the same `BEGIN/END WRITING-COWORK MANAGED` markers verbatim.
2. **`.claude/settings.json` we do not control** — the filename and JSON parsing are dictated by Claude Code / Cowork. It cannot become YAML.
3. **For that file, record provenance in `file_ownership.md`** rather than in the file. That table already exists as the vault's file inventory with ownership and status columns; extend it with a `plugin:writing-cowork` owner value and a managed-blocks column.

Why the ownership table over the alternatives: a `"_comment"` key inside `settings.json` *might* work, but unknown-key tolerance is unverified and a strict schema would reject the whole file — and the failure mode for that particular file is "the plugin stops loading," which is the worst place to take an unverified risk. A sidecar `settings.provenance.md` is safe but invents a parallel mechanism. The ownership table reuses machinery that already exists (consistent with the one-mechanism-per-job precedent above), is format-agnostic so it covers JSON, YAML and markdown uniformly, and answers a question that currently cannot be answered at all — *which files does the plugin manage?* — in one place instead of requiring every file to be opened.

**Division of labour:** in-file markers stay the convenience for markdown (visible at the point of editing, free at runtime); `file_ownership.md` becomes the authoritative registry of what the plugin owns. Testing whether `settings.json` tolerates a `"_comment"` key is a nice-to-have, off the critical path.

### `pm-install-router` — merge required (supersedes the refuse-to-overwrite behaviour)

v0.1.0 refused to touch an existing `CLAUDE.md`. Reworked to **v0.2.0** with four modes: **install** (clean vault), **refresh** (our markers present — regenerate managed blocks, copy `PROJECT-OWNED` through byte-for-byte), **adopt** (a foreign `CLAUDE.md` — move its entire content verbatim into `PROJECT-OWNED` under a dated heading, discarding nothing), and **abort** (malformed/unbalanced markers — never guess block boundaries, because a bad guess silently destroys content). Every write to an existing file takes a timestamped `.bak-`, shows a unified diff, and prompts; `--dry-run` shows the diff without writing. In adopt mode the rule is *keep the user's content whole rather than classify it* — sorting their prose into managed blocks is a judgement call that is sometimes wrong, and being wrong loses their words.

### Platform memory store — retirement record (2026-07-26)

All 8 entries reviewed individually against the vault before disposal, not assumed stale. **The assumption would have been wrong:** `reference_personal_plugin_marketplace.md` held ~6KB of detail against the vault's 1.4KB summary, including content in neither the vault memory nor the process doc.

| Entry | Disposition |
|---|---|
| `reference_personal_plugin_marketplace.md` | **Retained** — one-time per-machine setup (the `url.insteadOf` HTTPS/SSH git config fix, marketplace add, install), Cowork's internal plugin install path, and the `gh repo edit --visibility` commands promoted into `Process/dev-workflow-and-release.md` per the routing rule (operating procedure → process doc). Two GitHub issue numbers **deliberately dropped** as unverified, per `feedback_verify_agent_citations.md`. |
| `feedback_workarounds_warrant_doc_check.md` | **Partly retained** — Jamie's originating quote and the "this is not anti-workaround" qualification appended to the vault copy. |
| `feedback_self_contained_quit_scripts.md` | **Partly retained** — the bad-pattern/good-pattern examples appended to the vault copy. |
| `feedback_sandbox_host_lanes.md` | **Discarded** — stale (pre-rename tool names, missing the 2026-07-21 device_bash addendum); vault copy is a superset. |
| `feedback_verify_agent_citations.md` | **Discarded** — vault copy equivalent. |
| `feedback_release_includes_version_in_description.md` | **Discarded** — already promoted to the vault 2026-07-25. |
| `project_writing_cowork_v013_state.md` | **Discarded** — stale v0.1.13 snapshot, already tombstoned. |
| `MEMORY.md` | **Zero entries.** Left as a 3-line retirement notice pointing at `1_Project/Memory/`, not fully blank — a session that still loads this store should be told where to go rather than handed a void. Say the word to blank it completely. |

**Tool constraint found:** `project_memory_write` has **no delete affordance** — only create/overwrite. Files can be blanked to zero bytes (verified) but the filenames persist in the store listing. Genuine deletion, if wanted, needs the desktop UI. For the plugin this matters: any future "audit and clean the hidden store" tooling can empty entries but cannot remove them.

## Enforcement — pm-close-session (2026-07-27) — SPECIFIED

Resolves spine §8. The skill that keeps the spine from rotting: folders enforce nothing, and promotion + logging are exactly what a session skips when it runs short of room.

| Topic | Decision |
|---|---|
| Step order | survey → promote → sweep → log → commit → **handoff last**. Load-bearing: the handoff is written only after promotion commits, or it becomes a source of truth again. |
| Survey includes `git diff` | Content, not just `git status` names. Only a content diff reveals a change that silently reverted something — this is the detector for stale-copy edits. |
| Sweep split | Hidden-store check is **agent-performed inside the skill** (in Cowork that store is behind an MCP tool no script can reach). All file/git checks **delegate to `pm-run-drift-check`** via a new `session_hygiene:` block in `drift_check.yaml` — one implementation, per the one-mechanism-per-job precedent. |
| Red flags | **Block the close** by default. `--force` overrides and the override is recorded in the log entry. |
| Commit-hash circularity | The log entry names the commit carrying the change, but the log is itself committed; `--amend` changes the hash. **Two commits**: content, then log naming that hash. The log trails by one commit — correct over elegant, because the hash stays real and greppable. |
| Don't assume, verify | The sweep instructs reviewing each hidden-store entry against the vault rather than assuming duplicates. On this project's own retirement pass that assumption would have been wrong. |

**Also fixed in `drift_check.yaml`:** `inbox.buckets` was missing `issues`, so the bucket `pm-create-issue-report` writes to was never monitored. Pre-existing gap, unrelated to this workstream.

## drift_check.py lives in two locations — intentional (2026-07-27)

Confirmed by Jamie. **Not drift; do not "reconcile" or delete either copy.**

| Copy | Status |
|---|---|
| `0_Product/tools/drift_check.py` | **Canonical.** Bundled into the plugin 2026-07-22; now **v0.3.0** (session-hygiene checks). All new work goes here. Referenced by `templates/drift_check.yaml` as `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py`. |
| `~/code/cowork-tools/drift_check.py` | **The original, retained on purpose** for projects that have not yet transitioned to the bundled copy. Sits at the pre-bundling revision (~41 lines behind) and that is expected. |

Consequence: `pm-migrate-to-shared-tool` and `pm-run-drift-check`'s references to the cowork-tools path stay **valid** — they serve untransitioned vaults. A future session noticing the two copies differ should read this row rather than treating it as an inconsistency to fix.

## Hooks in Cowork — researched 2026-07-27 — **ANSWERED: hooks do not run**

The v0.1.17 gate is settled, and it **fails**. Three GitHub issues, one with hands-on verification:

| Issue | State | Finding |
|---|---|---|
| [#40495](https://github.com/anthropics/claude-code/issues/40495) | **Open** (2026-03-29) | Canonical. **Cowork silently ignores all settings sources.** User hooks in `~/.claude/settings.json` never fire; managed/MDM settings ignored; env vars not forwarded. Root causes given: config-dir mismatch (sandbox looks for `cowork_settings.json` under `/sessions/<name>/mnt/.claude/`), platform mismatch (the sandbox is a **Linux VM**, so it resolves `/etc/claude-code/managed-settings.json` rather than the macOS path), and env vars not passed into the sandbox. |
| [#47993](https://github.com/anthropics/claude-code/issues/47993) | Closed as duplicate of #40495 | States plainly: "Cowork sessions do not fire SessionStart hooks defined in `~/.claude/settings.json` or in plugins." |
| [#63360](https://github.com/anthropics/claude-code/issues/63360) | Open, labelled `area:cowork`/`area:hooks` | Verified 2026-05-28: `UserPromptSubmit` did not fire, `Stop` did not fire, and **`/hooks` does not exist in Cowork** ("Unknown skill: hooks"). The reporter's script works when run directly in Terminal — "Cowork just never triggers it." |

**Consequences, in order of importance:**

1. **v0.1.17 as conceived is dead.** SessionStart / SessionEnd / `PreToolUse` hooks cannot deliver enforcement to consumer vaults, because consumer vaults run in Cowork. Convention plus `pm-close-session` **is the ceiling** there.
2. **The §6c-1 memory consent-gate is off the table** for Cowork. Deferring it in the v0.1.16 pass was right, and it should now be marked not-viable rather than pending.
3. **Spine §6d is vindicated, not paranoid.** "A control built on Claude Code settings or hooks may protect the dev loop and protect nothing in the shipped product" is now documented fact, not a cautious hypothesis.
4. **Expectations for the memory-settings gating test should be low.** #40495 concerns *user-scope* `~/.claude/settings.json`; ours are *project-scope* `<vault>/.claude/settings.json`, and `enabledPlugins` demonstrably works there — so project scope is read for at least some keys. Still worth running, but a negative result would be unsurprising.
5. **Sobering detail:** #47993 lists "CLAUDE.md with blocking instructions" among the *inadequate* workarounds — "unreliable, Claude skips them when the user's first message is engaging." That is precisely our Tier-1 router. We are at the documented ceiling, and should not expect the router alone to enforce anything.

**What v0.1.17 should become instead.** Scheduled tasks **do** work in Cowork — the plugin already ships `pm-schedule-review`. A scheduled `pm-run-drift-check` is a runtime-independent enforcement backstop that catches what an unrun `pm-close-session` would have missed: uncommitted durable content, stranded log entries, memory-path drift. Not equivalent to a session-end hook (it is periodic, not guaranteed at close), but it is the strongest mechanism actually available in the runtime that matters. Hooks remain worth adding **for the Claude Code CLI dev loop only**, clearly scoped as such.

## Handoff — two distinct artifacts, do not conflate (corrected 2026-07-27)

The 2026-07-23/24 handoff decision said "`pm-install-handoff` updated to place handoffs in the gitignored single-slot location." **That conflates two different files** and taking it literally would have made a durable State doc ephemeral.

| Artifact | Kind | Fate |
|---|---|---|
| `process/data_management/handoff.md` | **State — tracked** | The *living librarian handoff*, read first when picking up the librarian role in a new chat. Installed by `pm-install-handoff`, which is **unchanged**. Never gitignored. |
| `process/handoff/session-handoff.md` | **Ephemeral — gitignored** | The session-close baton. Written by `pm-close-session`, single-slot; the next kickoff reads it, promotes the durable content, deletes it. New in v0.1.16. |

Shipped: `process/handoff/` added to the vault `.gitignore` written by `pm-init-vault`; `1_Project/Handoff/` added to this repo's `.gitignore` (the stale 2026-07-23 handoff is now correctly ignored); `pm-close-session` names the path explicitly and warns against the confusion.

## Claude Code hooks — dropped entirely (2026-07-27)

Confirmed by Jamie. Not "CLI-only", not "deferred" — **off the roadmap**.

Rationale: they do not run in Cowork (see "Hooks in Cowork" above), and consumer vaults run in Cowork. A CLI-only hook would be a second enforcement path protecting the one environment least in need of it — the dev loop, where attention is already high — while adding a mechanism to maintain, document, and keep in sync with the skill it duplicates. One mechanism per job.

Replaced by three layers, all runtime-independent:

| Layer | Mechanism | Trigger |
|---|---|---|
| Orientation | `CLAUDE.md` router + the hub's `## Attention` block (written by `drift_check`) | session start — by *content*, not execution |
| **Enforcement** | **git `post-commit` hook** (`pm-install-git-hooks`) | every commit |
| Sweep | scheduled `pm-run-drift-check` (via `pm-schedule-review`) | periodic |

**Why the commit is the right trigger.** The control model is that *git is the consent mechanism* and consent happens at commit. Session-close was always a proxy for "before this work becomes permanent" — the commit **is** that moment. Unlike session-close it cannot be forgotten, and unlike a Claude Code hook it runs in every runtime, because git runs on the host and no agent runtime is involved.

**Why `post-commit`, not `pre-commit`.** It cannot block, deliberately. A blocking check gets `--no-verify`'d the first time someone is in a hurry, and a check that is routinely bypassed is worse than one that always reports. The findings are things to notice, not reasons to reject a commit.

**What orientation loses without a hook.** A hook could *execute* and inject computed state; `CLAUDE.md` can only *instruct*. The gap is covered by the hub's Attention block, which the scheduled drift check pre-computes into a file the router already points at. What cannot be recovered is a compliance guarantee — the router steers, it does not enforce.

## DRIFT-ATTENTION markers — kept as a distinct family, not renamed (2026-07-27)

Previously flagged as an inconsistency to reconcile (spine §10.9). **Decided: do not rename.** These are two marker families with genuinely different semantics:

| Family | Written by | Meaning |
|---|---|---|
| `BEGIN/END WRITING-COWORK MANAGED:` | plugin sync | regenerated from template; hand edits inside are lost |
| `DRIFT-ATTENTION-START/END` | `drift_check.py` at runtime | tool-written state, refreshed every run |

Renaming would force one vocabulary onto two different things and require migrating every live vault's hub for cosmetic gain. The ownership question is already answered by the distinct name plus the row in `file_ownership.md`. Recorded so this stops resurfacing as drift.

## Status files carry no history (2026-07-29) — LOCKED

**Decided:** `2_Development/RoadMap/Roadmap.md` is a **status file**. It answers
"where is each version, right now" and nothing else. Narrative, research trails,
superseded plans, and "here is how we got here" do not belong in it.

This is the State record kind applied honestly: State is *overwritten in place
and kept small*. A roadmap that accretes the reasoning behind every version is a
Log wearing a State file's name, and it stops being readable at a glance — which
is the only thing a status file is for.

**Three destinations, one home per fact:**

| Kind | Home |
|---|---|
| Version status, right now | `2_Development/RoadMap/Roadmap.md` |
| Work not yet done | `1_Project/Todos.md` |
| A commitment already made | `1_Project/Decisions.md` |
| Superseded narrative worth keeping | `2_Development/RoadMap/history/` |

The 2026-07-29 sweep moved 82 lines of roadmap down to 45, archiving the
narrative verbatim to `history/2026-07-29_roadmap-narrative-archive.md`. It was
archived rather than deleted: "git has it" is technically true and practically
useless, because recovering a rationale then means bisecting commits, which
nobody does.

## Todos.md — the work list (2026-07-29) — LOCKED

**Decided:** work items live in `1_Project/Todos.md`, using the plugin's own
`pm-init-todos` schema (`ID | Description | Milestone | Assignee | Status |
Added | Notes`), so this repo dogfoods `pm-add-task` / `pm-update-task` /
`pm-list-tasks` / `pm-close-task` rather than inventing a private format.

It sits in `1_Project/` as a peer of `Decisions.md` rather than in
`process/active/` — this repo is plugin *source*, not a writing vault, and
introducing a `process/` tree here would put a second organizing scheme in
competition with `1_Project/` and `2_Development/`.

**Dogfooding paid immediately.** Adopting the schema surfaced a real defect
within minutes: `drift_check.py:496` expects `id | title | status | priority |
milestone | depends-on` — a column set **no template produces**. Any checker
reading todos rows is operating on a schema that does not exist in the wild.
Tracked as task `a4e1c7b2`; it also unblocks the long-stalled dependency-gate
work (`5b3e8c72`), whose "the `depends-on` column doesn't exist" objection turns
out to have been half right in the most confusing possible way.

## Dated handoffs — swept, not deleted (2026-07-29)

The four dated handoffs in `1_Project/Handoff/` were reviewed item by item
against current source. Findings:

- Both 2026-07-23 manual cleanup steps are **done** (`pm-migrate-existing-project/`
  removed, no stale `.git/index.lock`).
- Everything still genuinely open was promoted to `Todos.md` with its provenance
  recorded — nine verified items plus four decisions needing Jamie.
- Several inherited claims were **stale and were corrected rather than copied**,
  which is the reason this took a source-verification pass rather than a
  transcription: the `depends-on`-doesn't-exist claim, and the matcher
  false-positive whose sourcing was already struck on 2026-07-22.

The pile itself is left in place; disposition is Jamie's call, tracked as
`d84a0c63`. Nothing is lost either way now that the contents are promoted.
