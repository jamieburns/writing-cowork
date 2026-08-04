---
name: Skill Inventory Reduction — work order
description: Removal list for 7 skills, plus a design for demoting the 27-skill bootstrap family to one orchestrator skill. Written from Cowork; execute in Claude Code CLI.
type: analysis / work order
date: 2026-07-31
author: Claude (Cowork), cloud session
source: 1_Project/Handoff/2026-07-21_skill-usage-signal.md
---

# Skill Inventory Reduction — work order

**Execute in Claude Code CLI, not here.** `CLAUDE.md` invariant: *develop in
Claude Code CLI; Cowork is the runtime consumer; never develop plugin changes
from inside Cowork.* This document is a spec, not a change.

## Measured baseline (2026-07-31, from `0_Product/skills/`)

| | |
|---|---|
| Skills on disk | 66 |
| Total frontmatter description text | 26,917 chars ≈ **6,700 tokens, every turn** |
| Bootstrap family (27 skills) | 12,913 chars ≈ **3,230 tokens/turn — 47%** |

> **Correction, 2026-08-04 — this baseline measures the wrong artifact.**
> The table above is the repo at 0.1.17. Cowork is not running that. It serves an
> account-synced snapshot, and that snapshot is **0.1.14**. Measured directly from
> `/root/.claude/plugins/synced/writing-cowork/skills/`:
>
> | | Repo (0.1.17) | **Actually loaded (0.1.14)** |
> |---|---|---|
> | Skills | 66 | **60** |
> | Description chars | 26,917 | **24,914** |
> | Tokens/turn | ~6,700 | **~6,230** |
> | Bootstrap family | 27 skills, ~3,230 tok (47%) | **21 skills, ~2,640 tok (42%)** |
>
> Same conclusion, ~7% smaller. The Tier-1 target holds: six of the eight most
> expensive entries are bootstrap — `pm-init-project-cowork-settings` (723 chars),
> `pm-init-github` (651), `pm-version` (638), `pm-init-git` (637),
> `pm-refresh-cowork-plugin` (626), `pm-init-vault` (620), `pm-setup-project` (596),
> `pm-init-voice-handoff` (562).
>
> **The sequencing consequence is larger than the number.** Deleting a skill from
> this repo does not change the loaded snapshot, so it does not change the token
> bill. Proof: `pm-migrate-to-shared-tool` is absent from `0_Product/skills/` and
> still appears in Cowork's live skill listing. Every saving in this document is
> gated on `7c1b9e04` landing. See `Decisions.md`, 2026-08-04.

Only `name` + `description` are preloaded per turn. SKILL.md **bodies** load on
invocation; subdirectory files load only when a body says to read them. So the
recurring cost of a skill is its description, and the lever is *entry count*,
not body size.

---

## Part 1 — Removals

Confirmed against the source tree. **`pm-migrate-to-shared-tool` is already gone
upstream** (superseded by `pm-migrate-todos-schema`), so the list is 7, not 8.

Saving: 2,589 chars ≈ **647 tokens/turn**.

| # | Skill | Ripple edits required (shipping files only) |
|---|---|---|
| 1 | `pm-show-kanban` | `pm-init-todos/SKILL.md`, `pm-version/SKILL.md` |
| 2 | `pm-show-composite-kanban` | `pm-migrate-todos-schema/SKILL.md` (special-cases the legacy format) |
| 3 | `pm-escalate-issue` | **`templates/inbox_README.md` — ships into every vault**, `pm-create-issue-report/SKILL.md`, `pm-process-inbox-item/SKILL.md` |
| 4 | `pm-schedule-review` | `pm-install-git-hooks/SKILL.md` |
| 5 | `pm-refresh-cowork-plugin` | **`1_Project/Process/dev-workflow-and-release.md` — release step 2 points at it** |
| 6 | `pm-enable-project` | `pm-setup-project/SKILL.md`, `pm-sync-project-to-plugin/SKILL.md` |
| 7 | `pm-disable-project` | `pm-setup-project/SKILL.md` |

### Retire to docs, do not simply delete

Three carry real procedure that should survive as prose in `0_Product/Documents/`
(currently empty) — zero context cost, still greppable:

- **`pm-refresh-cowork-plugin`** (940 words). This is the workaround for the
  live Cowork plugin-cache bug (Anthropic thread 215474352137566) — the same bug
  you are inside right now: Cowork has **v0.1.13** loaded against **0.1.17** on
  disk. Inline the procedure into `dev-workflow-and-release.md` *before* deleting
  the skill, or release step 2 becomes a dangling pointer.
- **`pm-escalate-issue`** (757 words) — the `gh` CLI escalation procedure.
- **`pm-enable-project` / `pm-disable-project`** — collapse to two lines in the
  registry doc: flip `enabled:` in `~/.config/cowork/registry.yaml`.

### Two things to settle before deleting

1. **A locked decision covers the kanban feature.** `Decisions.md` carries
   *"Assignee kanban grouping — `--by=assignee` as an alternative mode… Shipped
   in v0.1.14."* Removing the kanban skills retires a shipped v0.1.14 feature.
   Your own rule: revising a lock requires an explicit decision-log entry. Write
   the entry as part of the change, not after.
2. **Pre-existing dangling references.** `pm-version/SKILL.md` and
   `pm-sync-project-to-plugin/SKILL.md` still name `pm-migrate-to-shared-tool`,
   which no longer exists. Nothing caught this — **another instance of the
   v0.1.18 class: the checker reports clean instead of "I could not read that."**
   A `drift_check` rule that resolves every `pm-*`/`voice-*` name mentioned in a
   shipping file against `skills/` would have caught it, and would make the
   removals above self-verifying.

### Not removed, per your call

- **Rest of bin D stays** — `pm-show-status`, `pm-show-roadmap`, `pm-show-claims`,
  `pm-version`, `pm-list-projects`, `pm-list-tasks`, `voice-list-exceptions`,
  `pm-tag-lock`, `pm-tag-snapshot`. Used regularly; the filesystem method simply
  cannot see read-only skills. Record this so the next usage sweep does not
  re-flag them.
- **All voice skills stay**, including `voice-capture-sample`,
  `voice-confirm-sample`, `voice-shift-terminology`, `voice-recommend-wording`,
  `voice-remove-exception`.
- **`pm-create-promotion-request` stays** — its zero-trace reading was confounded
  by a documented 2026-05-16 decision to route around it, not by disuse.

---

## Part 2 — The bootstrap family: better than a skill

You asked whether md files in the plugin could replace once-only skills. Yes —
and the mechanism is already supported. Three tiers, by how much judgment the
step needs.

### Tier 1 — script it (16 skills → 1 manifest + 1 script)

`pm-install-charter`, `pm-install-handoff`, `pm-install-project-hub`,
`pm-install-tagging-conventions`, `pm-install-claim-dispute-protocol`,
`pm-install-for-other-contexts`, `pm-install-hierarchy-and-ownership`,
`pm-install-drift-check-config`, `pm-init-vault`, `pm-init-todos`,
`pm-init-roadmap`, `pm-init-voice-exceptions`, `pm-init-voice-handoff`,
`pm-init-reader-review-tracking`, `pm-init-log`, `pm-init-memory`.

Every one is *copy template X to path Y, substitute placeholders*. That is a
deterministic file operation with no judgment in it — a script, not a skill.
Replace with `0_Product/scaffold_manifest.yaml` (template → destination →
substitutions → required?) driven by `0_Product/tools/scaffold.py`.

Three wins beyond context:

- Adding a scaffold file becomes **a manifest row**, not a new skill.
- A script **exits nonzero**. This is your v0.1.18 "fail loudly" class solved
  structurally for 16 steps at once — a skill body cannot be made to fail.
- A script is **unit-testable**; a skill body is not.

### Tier 2 — procedure markdown, read on demand (9 skills → 9 files, 0 entries)

`pm-init-git`, `pm-init-github`, `pm-init-project-cowork-settings`,
`pm-install-router`, `pm-install-git-hooks`, `pm-finalize-scaffold-commit`,
`pm-register-project`, `pm-place-lift-decisions`, `pm-resume-setup`.

These branch on judgment (`--git=none|existing|new-github`, PyYAML preflight,
resume-from-failure). Move each body verbatim to
`0_Product/skills/pm-setup-project/procedures/<name>.md`. `pm-setup-project`'s
SKILL.md becomes a thin orchestrator: run the manifest, then read exactly the
procedure file the current stage needs. `pm-resume-setup` becomes
`pm-setup-project --resume`.

### Tier 3 — plain docs, no skill at all

Once-per-machine or once-per-problem: `pm-refresh-cowork-plugin` (above),
`pm-migrate-todos-schema`, arguably `pm-sync-project-to-plugin` (whose 1,122-char
description is the single most expensive entry in the plugin). Park in
`0_Product/Documents/`.

### Net

27 bootstrap entries → 1. **~3,230 tokens/turn → ~150.** With Part 1, the plugin
drops from ~6,700 to roughly **~2,900 tokens/turn.**

### What you give up — honestly

1. **Standalone retrofit invocation.** "Install the project hub on this existing
   vault" stops auto-routing; it becomes `pm-setup-project --only=project-hub`.
   Two vaults show no trace of standalone use — but absence of trace is not
   proof, and you are the only witness who would know.
2. **Discoverability.** The skill listing currently doubles as the scaffold
   inventory. Replace with a table in `0_Product/README.md`.
3. **Migration risk, concentrated in the one path you cannot test incrementally.**
   A broken setup path is discovered at the *next new project*, possibly months
   out. Mitigation, per your own positive-control note: scaffold a throwaway
   vault in `/tmp` with the current skills, scaffold another with the manifest,
   and `diff -r`. Byte-identical or it does not ship.

---

## Recommended sequencing

The cheapest win is not in this repo at all.

- **Step 0 — session settings, minutes, no code.** Disable the
  `product-management` plugin (9 skills, software-PM domain, includes the
  near-duplicate pair `brainstorm` / `product-brainstorming`),
  `cowork-plugin-management` (2 skills duplicating the built-in `cowork-plugin`),
  and `apple-contacts-table` / `morning`. Rough order **1,500–2,500 tokens/turn
  for zero refactor risk** — comparable to Part 1, at a fraction of the cost.
- **Step 1 — land v0.1.17.** Three steps already in the session handoff. Do not
  start a refactor while debugging through a four-version plugin-cache gap.
- **Step 2 — v0.1.18: the removals** (Part 1) plus the dangling-reference
  drift_check rule, which belongs with the "fail loudly" class you already
  scoped for that version.
- **Step 3 — v0.1.19: the bootstrap refactor** (Part 2), Tier 1 first — it is
  the largest saving, the most mechanical, and the easiest to verify by diff.

## Verification for each step

- `claude plugin validate .` after every skill deletion.
- `grep -rn "<removed-skill-name>" 0_Product/ 1_Project/Process/` returns nothing
  outside `History/` and `Handoff/`.
- `pm-version` sentinels updated; `plugin.json`, the `pm-version` EXPECTED
  VERSION marker, and both catalog descriptions bumped together.
- A `Decisions.md` entry retiring the v0.1.14 kanban lock.
