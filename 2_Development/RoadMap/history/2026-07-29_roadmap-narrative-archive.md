# Roadmap narrative archive — swept 2026-07-29

Everything below was removed from `Roadmap.md` when that file was reduced to
status-only. It is kept verbatim as frozen history: the reasoning, the research
trail, and the superseded plans. Nothing here is current. Open work items were
extracted to `1_Project/Todos.md` before this sweep; commitments already live in
`1_Project/Decisions.md`.

---

# writing-cowork Roadmap

High-level phase/version summary. Full detail for each version lives in its own folder under `2_Development/RoadMap/`.

| Version | Status | Summary |
|---|---|---|
| v0.1.1 – v0.1.9 | Shipped | Foundation, Planning (Subset 2), Voice/tone (Subset 3), refresh-workaround skill, MVP validated |
| v0.1.10 – v0.1.11 | Shipped | Dev-workflow hardening (Claude Code CLI as the dev environment), pm-refresh rewritten as a documented consumer-side workaround |
| v0.1.12 – v0.1.13 | Shipped | `inbox/README.md` scaffold, `inbox/issues/` convention + `pm-create-issue-report` + `pm-escalate-issue` (GitHub routing) |
| **v0.1.14** | **Shipped, released, in successful daily use for 2 months (confirmed 2026-07-21)** | Assignee column (6 skills + role_taxonomy template). `pm-version`'s marker was stale at v0.1.13 pointing to this exact version — fixed 2026-07-21. |
| v0.1.15 | Shipped to Claude Code CLI; **not yet refreshed in Cowork** | Full `0_Product/` consolidation via a `git-subdir` marketplace source; `research_and_analysis/` + `production/` folder-naming conventions. |
| **v0.1.16** | **Content complete 2026-07-27** — folded into the v0.1.17 release (never released standalone) | **Information architecture spine.** Shipped so far: `CLAUDE.md` Tier-1 router + ownership-marker convention; visible project memory (`process/memory/` + `INDEX.md`); memory settings (Option B redirect, path computed at install); activity log (`process/Log.md`, newest-last); `file_ownership.md` as the plugin-managed provenance registry; `pm-install-router`, `pm-init-memory`, `pm-init-log`, `pm-close-session`; `drift_check.py` v0.3.0 with `session_hygiene` checks. `pm-setup-project` now runs 23 sub-skills. |
| **v0.1.17** | **Content complete 2026-07-27** | Claude Code hooks **dropped**. Enforcement is now a git `post-commit` session-hygiene hook (`pm-install-git-hooks`) — runs on the host in every runtime, fires at commit, never blocks. Orientation via router + hub Attention block; periodic scheduled drift check as the sweep. |
| v0.1.19 | Deferred | Production-pipeline tooling. |
| v0.2.0 | Deferred | `pm-sync-project-to-plugin` (drift-check config + vault layout + router migration in one mechanism). |

**Version shorthand:** elsewhere in this repo (`Decisions.md`, the spine doc) these are written as v0.16, v0.17, v0.19 — dropping the leading `1.`. They mean v0.1.16, v0.1.17, v0.1.19. v0.2.0 is genuinely the next minor and comes after v0.1.19.

### v0.1.16 / v0.1.17 — content complete; only the release remains

Everything previously listed here is **done**: handoff lifecycle (both gitignores, single-slot path, `pm-close-session` names it), ownership markers across the regenerated templates, and the `DRIFT-ATTENTION` question — **resolved by deciding not to rename** (two marker families with different semantics; see `Decisions.md`).

Outstanding is the release itself, and two of the three steps are Jamie's:

1. ~~`plugin.json` version + description~~ **done** (v0.1.17).
2. ~~`pm-version` EXPECTED VERSION sentinel~~ **done** (v0.1.17).
3. **Marketplace catalog description** in `cowork-plugins-marketplace` — not a connected folder in the working session, so untouched.
4. **Cowork-side refresh** — the marketplace uninstall/reinstall procedure in `1_Project/Process/dev-workflow-and-release.md`.
5. Optional: a `release/v0.1.17-*` tag, matching `release/v0.1.14`.

**Known risk going in:** the `post-commit` hook has been written and its underlying checks tested, but `pm-install-git-hooks` has **never been executed** and the hook has never fired. This dev repo is the obvious first test. The memory settings are likewise unverified in Cowork, and #40495 suggests they may be inert — the hook does not depend on them, which is the point of putting enforcement there.

### v0.1.17 gate — **ANSWERED 2026-07-27: hooks do not run in Cowork**

Hooks are a **Claude Code CLI** mechanism. The 2026-07-25 research established that every memory control the platform documents is CLI-documented, and that **consumer vaults run in Cowork**, where binding is unverified. Two specific unknowns block v0.1.17:

1. Does Cowork execute hooks at all?
2. Do hook matchers catch MCP tool calls (`mcp__*`), not just `Write`/`Edit`?

**Both answered, both negative.** [#40495](https://github.com/anthropics/claude-code/issues/40495) (open, canonical) documents that Cowork silently ignores *all* settings sources — user hooks never fire, managed settings are ignored, env vars are not forwarded — with root causes given (config-dir mismatch, and the sandbox being a Linux VM so it resolves the Linux managed-settings path). [#47993](https://github.com/anthropics/claude-code/issues/47993) states SessionStart hooks do not fire and was closed as a duplicate of it. [#63360](https://github.com/anthropics/claude-code/issues/63360) verified hands-on that `UserPromptSubmit` and `Stop` never fire and that `/hooks` does not exist in Cowork. Full record in `1_Project/Decisions.md` → "Hooks in Cowork".

**So enforcement-by-hook cannot reach consumer vaults.** Convention plus `pm-close-session` is the ceiling there. Note also that #47993 lists "CLAUDE.md with blocking instructions" among the *inadequate* workarounds — that is our Tier-1 router, so the router should be understood as steering, not enforcing.

**Final v0.1.17 shape — Claude Code hooks dropped entirely (2026-07-27).** Not CLI-only, not deferred: a CLI-only hook would protect the one environment least in need of it while adding a mechanism to maintain alongside the skill it duplicates. Three runtime-independent layers replace it:

| Layer | Mechanism | Trigger |
|---|---|---|
| Orientation | `CLAUDE.md` router + the hub's `## Attention` block (pre-computed by `drift_check`) | session start — by *content*, not execution |
| **Enforcement** | **git `post-commit` hook** (`pm-install-git-hooks`) | every commit |
| Sweep | scheduled `pm-run-drift-check` (via `pm-schedule-review`) | periodic |

Git hooks are unrelated to Claude Code hooks — they run on the host wherever `git` runs, so no agent runtime is involved. And the commit is the *right* trigger: the control model is that git is the consent mechanism, consent happens at commit, and session-close was only ever a proxy for "before this becomes permanent." Unlike session-close it cannot be forgotten. `post-commit` rather than `pre-commit` is deliberate — it cannot block, because a blocking check gets `--no-verify`'d and these findings are things to notice, not reasons to reject a commit.

Superseded — the original hook-based plan, retained for context: SessionStart hook for orientation, SessionEnd/Stop hook invoking `pm-close-session`, and a `PreToolUse` consent-gate on memory writes (spine §6c-1). All three are dead in Cowork.

## Carried-over decisions from `DECISIONS_v014.md` — not yet shipped

`DECISIONS_v014.md` locked three workstreams for v0.1.14: Assignee Column, Review Skills (Subset 4, 13 skills), and Drift Enhancements. Only Assignee Column shipped — confirmed by skill listing: no `review-*` or `cycle-*` skills exist anywhere in the current 65 skills (only the pre-existing `pm-init-reader-review-tracking` and `pm-schedule-review`). Drift Enhancements' status wasn't independently re-verified in this pass (they may be embedded as code changes to `pm-run-drift-check`/`drift_check.py` rather than new skill names, which wouldn't show up in a skill-name check).

These are open, not urgent — pick up whenever you're ready to resume feature work:

- Review Skills (Subset 4, 13 skills per the locked decision) — full scope in `2_Development/RoadMap/v0.1.14/ASSESSMENT_REVIEW_SKILLS_v014.md`
- Drift Enhancements (cross-phase dependency detection, status-staleness timestamps, `.gitkeep` inflation fix) — full scope in `2_Development/RoadMap/v0.1.14/ASSESSMENT_DRIFT_ENHANCEMENTS_v014.md`. Worth a quick check of `pm-run-drift-check`/`drift_check.py` before assuming this is unshipped.

## Deferred, being handled separately (per user, 2026-07-21)

- Subset 5 (Substance, 3 skills) — user will clean this up separately, not part of this housekeeping pass.

## Anthropic support thread 215474352137566

**Status (checked 2026-07-21): no reply beyond the initial acknowledgment** — Jamie checked email directly, nothing further came in. Followed up with a web search against current Anthropic docs/changelog/GitHub issues to see if any of the four original items shipped a fix since May 2026. None have:

1. **Update detection / stale plugin cache** — still broken. [GitHub #69020](https://github.com/anthropics/claude-code/issues/69020) is the closest match (Cowork installs stale cached plugin, ignores marketplace updates), still open, cross-references 3 sibling issues with the same pattern. Checked Cowork changelog through June 2026 (v1.11847.5, v1.11187.4) — no marketplace-cache or update-detection fix mentioned. `pm-refresh-cowork-plugin`'s marketplace-uninstall-reinstall workaround is still necessary.
2. **"Save plugin" generic validation error** — root cause now public via [GitHub #56376](https://github.com/anthropics/claude-code/issues/56376): Cowork's client discards the server's detailed `validation_errors[]` array and shows only a generic toast. Still open.
3. **Bonus finding, actionable:** [GitHub #63081](https://github.com/anthropics/claude-code/issues/63081) — Cowork's upload validator silently fails on angle brackets (`<vault>`, `<name>`, etc.) in a `SKILL.md`'s `description:` frontmatter field, even inside backticks. **16 of this plugin's 60 skills have this exact pattern** (e.g. `pm-add-task` references `` `<vault>/process/active/todos.md` `` in its description) — likely explains the original "Save plugin" failure even though `claude plugin validate` passed. Workaround: `<vault>` → `[vault]`. Low urgency since the dev workflow here doesn't use the "Save plugin" button, but a real, cheap cleanup if ever wanted. List of affected skills is in the session record; re-grep with: `awk '/^---$/{c++;next} c==1' skills/*/SKILL.md` scoped to the `description:` block if picking this up.
4. **extraKnownMarketplaces / private catalogs** — Anthropic shipped **organization-level** private marketplaces (support.claude.com confirms private/internal source repos for org marketplaces), which doesn't address a personal/individual setup like this one. The feature that would actually help — [GitHub #66184](https://github.com/anthropics/claude-code/issues/66184), Cowork's Personal tab accepting custom marketplace URLs — is still open, marked "Critical — blocking my work" by another user.

**Net: nothing has shipped that resolves any of the four original items.** No follow-up to Anthropic is warranted right now beyond what's already on file — the honest status is "still broken, still open" across the board. Re-check this section if picking the thread back up, rather than re-researching from scratch.

## Legacy / uncertain work items

- Phase 9 (legacy `todos.md` migration to vault) — no `todos.md` was found in this repo during the reorg; if this refers to something in a different (end-user) vault, track it there instead.
