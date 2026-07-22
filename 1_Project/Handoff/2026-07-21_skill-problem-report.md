---
name: writing-cowork Skill Problem Report
description: Concrete, evidence-backed issues found in the drift-check skill and other actively-used writing-cowork skills, plus proposed fixes
type: analysis / handoff
date: 2026-07-21
author: Claude (Cowork), cloud session
addendum_date: 2026-07-22
addendum_author: Claude (Cowork), cloud session — cross-checked against project memory and the vault's own standing plugin-findings doc
---

# writing-cowork Skill Problem Report

Companion to `writing_cowork_skill_usage_signal_2026-07-21.md` (usage-frequency
pass). This document covers actual *problems* found in skills confirmed to be
in regular use — not usage frequency.

**Scope note:** I could not read `~/code/cowork-tools/drift_check.py`'s
source — that folder isn't connected to this session (only names are visible,
contents aren't). Everything below on the drift check is inferred from its
`drift_check.yaml` config and the three dated reports (07-11, 07-18, 07-20),
not from the script itself. Grant folder access if you want the filename/date
fix proposed below verified against the real code before changing it.

---

## 1. Drift check (`pm-run-drift-check`)

### 1a. No time-of-day in report filenames — confirmed, you're right

Reports are named `YYYY-MM-DD.md` (`2026-07-11.md`, `2026-07-18.md`,
`2026-07-20.md`) but the *header inside* each report already carries a full
timestamp (`2026-07-11T10:22:40`). The data exists; the filename just drops
it. Concrete cost: two runs on the same day silently overwrite each other,
with nothing on disk to show the earlier run ever happened. Fix: name reports
`YYYY-MM-DDTHHMM.md` (or similar) instead of just the date. Low-risk, config-
or script-level change — worth confirming in the actual script before editing
since I haven't seen it directly.

> **2026-07-22 addendum — confirmed independently, and the risk is not
> hypothetical.** Checking `process/data_management/drift_reports/` directly
> as of this addendum, the three files actually on disk are
> `2026-07-05.md`, `2026-07-11.md`, and `2026-07-17.md` — a *different* set of
> dates than the 07-11/07-18/07-20 trio this report analyzes below. Both sets
> can't be simultaneously current; taken together they're a live demonstration
> of 1a's exact failure mode (date-only filenames make "which reports exist"
> ambiguous across sessions/machines, and same-day reruns overwrite). This
> raises the fix from "worth doing" to "do it soon" — treat any specific dated
> report cited in this document as a snapshot that may already have been
> overwritten or superseded, not a stable reference.

### 1b. High false-positive rate is burying real problems

The 07-18 report flagged 348 "unaccounted" files; 07-11 flagged 153; 07-20
flagged 94 (dropping after a manual `file_ownership.md` reconciliation pass
on 07-20). Nearly all of the noise is the same few large, clearly-intentional
groups appearing on every run: the full `bible_reference/`/`resources/Bibles/BSB/`
reference corpora (~80 files each time), and — on 07-18 specifically — the
entire `handoffs/*` and `recommendations/*` working trees. `drift_check.yaml`'s
`exclude_prefixes`/`exclude_patterns` hasn't kept pace with the vault's actual
structure. Practical effect: the handful of things that genuinely matter (the
4 stale build outputs, flagged identically and correctly on all three runs)
are buried under hundreds of expected non-issues, which is exactly the
condition under which a report stops getting read carefully. Fix: add
`bible_reference/`, `resources/Bibles/`, `handoffs/`, and `recommendations/`
to `exclude_prefixes` (or give them summary-row treatment the way
`file_ownership.md`'s Conventions section already does for the "long tail").

> **2026-07-22 addendum — concurrence, directly confirmed against the live
> config.** Read `process/data_management/drift_check.yaml` (the file this
> project actually runs against) as part of this addendum:
> `exclude_prefixes` currently lists only `.git`, `.obsidian`,
> `process/snapshots`, and `process/data_management/drift_reports`; none of
> `bible_reference/`, `resources/Bibles/`, `handoffs/`, or `recommendations/`
> appear anywhere in `exclude_prefixes` or `exclude_patterns`. So 1b isn't an
> inference from report contents — it's directly visible in the config file
> that's supposedly already been through a "manual reconciliation pass" (per
> the 07-20 note above). Either that reconciliation touched `file_ownership.md`
> only and never made it back to the yaml, or the yaml edit didn't stick.
> Worth checking `git log -- process/data_management/drift_check.yaml` to see
> whether an exclude-list fix was ever attempted and lost, versus never
> attempted at all.
>
> Separate, smaller discrepancy also worth flagging: this same yaml has
> `build: enabled: false` (comment: "disabled until a pipeline lands"), which
> sits oddly next to 1d's claim below that all three reports "consistently and
> correctly flag the same 4 build outputs as stale." If the build check is
> disabled in config, that 1d behavior would have to be coming from something
> else (a different check, or the config changed between report-runs and now).
> Not asserting 1d is wrong — just flagging the tension for whoever verifies
> against the real script.

### 1c. `inventory_missing` list is static across all three runs — needs a look

The exact same ~24 entries (`inbox/external/`, `inbox/promotion/`, several
`process/active/*.md` files) appear verbatim in the 07-11, 07-18, *and*
07-20 reports. Either nobody has acted on this list across 9 days because
it's drowned out by 1b's noise, or the ownership table itself has stale
entries pointing at files that were intentionally removed (as happened with
`step10_synthesis.md` and `kanban_view.md`, both resolved on 07-20 per
`file_ownership.md`'s changelog — so this mechanism does get fixed
eventually, just not for this list yet). Worth a manual pass to confirm which.

> **2026-07-22 addendum — matches a broader, independently-documented pattern
> of drift-check unreliability.** Project memory (`reference_epistemology_paths.md`)
> records a **separate, earlier** finding from 2026-07-11: "Drift MATCHER
> unreliable (open) — the 2026-07-11 report flagged 214 'unaccounted' + 16
> 'orphan', but the count is largely artifact — it includes `.gitkeep`s,
> intentionally-untracked graphics PNGs, archived `process/history/`
> cover-notes, AND at least one genuinely-registered file
> (`analysis/appendix_a_apostolic_sacramental.md` is in the 'unaccounted' list
> yet has a proper `file_ownership.md` row)." That memory explicitly warns
> "do NOT treat the drift counts as a real backlog until the matcher (path
> normalization / ownership-row parsing / yaml tracked-scope) is reviewed."
> This is a second, independent line of evidence — the false-positive problem
> isn't confined to the exclude-list gap in 1b; the matcher itself has a
> genuine-file false-positive bug on top of that. The two should probably be
> fixed together rather than treating 1b's exclude-list patch as sufficient.
> `reference_epistemology_paths.md` also names two `todos.md` rows tracking
> adjacent drift-check work — `e1a2656d` (cross-phase blocking) and `63d32305`
> (status-block staleness) — and notes the matcher-reliability fix is "a
> third, not yet a formal row" as of that memory's writing. Worth confirming
> whether a row has been opened for it since.

### 1d. Build-staleness check looks correct and useful — no issue

All three reports consistently and correctly flag the same 4 build outputs
as stale (last built 2026-05-12/05-20, source changed 2026-06-26 — ~889–1082
hours stale). This part of the skill is working as intended; flagging it here
only to contrast with 1b/1c — the signal-to-noise problem is specific to the
inventory checks, not the whole skill.

> **2026-07-22 addendum — flagging a tension, not a refutation.** See the
> `build: enabled: false` note under 1b above. If that config value was in
> effect during the 07-11/07-18/07-20 runs, this section's premise (the build
> check "is working as intended") would need re-examination — either the
> check ran anyway from a different code path, the yaml changed after those
> reports ran, or this project's `drift_check.yaml` isn't actually the one
> that produced them. Not enough evidence here to say which; just don't take
> 1d as settled without checking that specific config value against the
> report dates.

### 1e. Silent-fail mode in *scheduled* runs — separate axis from 1a–1d, worth tracking alongside them (new, 2026-07-22)

Not from this report, but squarely in "drift-check-adjacent tooling
problems": project memory (`feedback_offline_silent_fail.md`) documents that
scheduled/offline drift-check-style runs can lose their output entirely when
the network drops mid-run and the task hangs — a 2026-06-06 batch lost 5 of 7
task outputs during a patchy-wifi period. The memory is explicit that this
is an **environmental** hang (network-drop → task stuck → nothing written),
not a structural defect in the offline runtime, and that runs have been
reliable since on a stable connection. Flagging it here because it's the same
family of concern as 1a (silent loss of report history) but with a different
root cause (connectivity, not naming) and a different existing mitigation
(a STARTED/COMPLETED ledger + morning reconciliation sweep, already adopted
per that memory) rather than a proposed one. No action needed beyond keeping
the ledger habit — listed for completeness so a future reader doesn't
conflate this with 1a or think it's unaddressed.

---

## 2. Audit-trail / operative-content separation (a documented, self-caught failure — in progress, not closed)

Not a "skill" in the writing-cowork sense, but a process convention the pm
context is actively remediating (`process/active/audit_trail_separation_handoff.md`).
Flagging here because it's a real, evidenced problem with consequences for
work quality, not a hypothetical:

- Rule documents like `gradient_scoring_plan.md` had audit narrative
  (dated revision history, self-correction notes) embedded inline with
  operative scoring rules, in the same prose register, with no marker
  distinguishing "follow this" from "here's how we got here."
- **This already contaminated real work once**, not just readability: the
  handoff's own mtime cross-reference confirms Nehemiah, Isaiah, and Pass B
  (2 Chronicles, Deuteronomy, Song of Songs, Lamentations, Jonah) were all
  scored while `gradient_scoring_plan.md` was in its contaminated state.
  Resolution is a full re-run of those passes after cleanup — not yet done
  as of the handoff's last update.
- Items 1–4 of the handoff (extract the history, audit `review/` for the same
  pattern, check outside `review/`, codify the convention in the charter) are
  marked done. **Item 5 — verifying the review pipeline's context-assembly
  step actually excludes audit files from what reviewer agents see at
  runtime — is explicitly reframed as "no automated context-assembly step
  exists to audit; dispatch is manual."** That means the fix depends on every
  future dispatch manually following `review_test_harness.md`'s stated-inputs
  list correctly, with no structural guarantee. This is the live gap.

> **2026-07-22 addendum — a related, independently-documented mitigation
> already in use, worth cross-linking.** Project memory
> (`feedback_subagent_review_reads.md`) records the writer's 2026-06-09
> direction to use sub-agents with tight extraction prompts (verbatim quotes,
> word caps, attribution questions) to pull review-corpus content, rather
> than loading full persona files into main context. That's a *different*
> problem (context budget, not audit/operative contamination), but the
> underlying mechanism — "manual, prompt-level discipline standing in for a
> structural guarantee" — is the same shape as item 5's gap here. Both point
> at the same broader theme: this pipeline currently relies on humans/chats
> correctly following a manual protocol at dispatch time, with nothing
> enforcing it in code. If a structural context-assembly step is ever built
> (closing item 5), it would be worth designing it to also solve the
> sub-agent-extraction case, since they're the same kind of fix.

---

## 3. Task-tracking skills (`pm-add-task` / `pm-update-task` / `pm-close-task`) — no gate-dependency enforcement

`todos.md` contains 13 rows explicitly marked `UNDONE`, `reverted`,
`Retired`, or `Re-scoped` out of 85 total task rows (~15%). The clearest
concrete case: tasks **I3.2** (`d64cca0b`, "Lock markers applied to
deliverable layer") and **I3.3** (`42917629`, "Hub recent-history lock event
entry") were both marked `done` on 2026-05-20, then had to be manually
reverted to `planned` the same day after the writer pointed out that
voice/tone work should gate Phase 12 lock, and this dependency hadn't been
enforced when the tasks were closed. The inline note even records that an
inbox cover-note referencing the (incorrect) closure had to be pulled before
the librarian processed it.

This isn't a fatal flaw — the correction happened same-day and is fully
documented — but it shows the task-tracking skills don't check a task's
declared `Milestone`/`Depends-on` relationship before allowing `done`, so
sequencing mistakes are only caught by a human re-reading the list, not
prevented at close-time. Given ~15% of all tracked tasks needed some kind of
manual correction after the fact, a lightweight "does this task's milestone
dependency actually permit closing?" check at `pm-close-task`/`pm-update-task`
time would likely pay for itself.

> **2026-07-22 addendum — strong concurrence; the underlying todos.md
> mechanism has a second, independently-documented reliability problem that
> compounds this one.** Project memory (`feedback_todos_count_ledger_drift.md`)
> documents that `todos.md` carries **two separate hand-maintained count
> ledgers that drift apart from each other and from the live table** — as of
> 2026-06-15 they read 212 vs 217 against a true table count of 220 (none
> agreed), and a 2026-07-17 recheck found a *fresh* discrepancy (229 claimed
> vs 238 by direct tally) that predated that session's edits. The standing
> workaround is to never trust the prose ledgers and instead tally the live
> Status column directly with `awk` (command preserved in that memory).
> Combined with this section's dependency-gate gap, the picture is: `todos.md`
> has at least two distinct classes of self-reported-state-vs-reality drift
> (task status vs. declared dependency; summary counts vs. table rows), and
> in both cases the *fix currently in place is "a human re-derives ground
> truth from the raw table,"* not anything enforced by the tracking skills
> themselves. If `pm-add-task`/`pm-update-task`/`pm-close-task` ever gain
> structural validation (per this section's suggested fix), collapsing the
> two count ledgers into one computed-not-hand-maintained value (flagged as
> "a worthwhile cleanup" in that memory) would be a natural companion fix —
> same root cause, same skill surface.
>
> Additionally, a **separate but adjacent finding already logged upstream**
> in this vault's own plugin-feedback doc
> (`process/active/plugin_findings_for_writing_cowork.md`, "M1" and the
> "cross-phase dependency change" item) proposes exactly the kind of
> structural fix this section is asking for, from the other direction: adding
> an `Assignee` column (already adopted vault-side as a convention, not yet
> upstreamed) and a `drift_check.yaml` check (`cross_phase_dependency_change`)
> that would flag `depends-on` edits crossing phase boundaries as part of the
> nightly drift report, rather than only at close-time. That's a
> drift-check-side complement to this section's close-time-gate proposal —
> worth doing both, since one catches the mistake before commit and the other
> catches it if it slips through anyway.

---

## 4. Additional plugin/skill issues already on record in this vault (new section, 2026-07-22)

The vault already maintains a living upstream-feedback document at
`process/active/plugin_findings_for_writing_cowork.md` (created 2026-05-20,
last updated 2026-05-22, PM-owned) that tracks writing-cowork plugin/skill
findings independent of this report. It significantly overlaps in spirit with
sections 1–3 above but covers different concrete gaps. Pulling the open items
forward here so all known Cowork-tooling issues live in one place, with
concurrence/difference noted against this report's findings:

- **Skill-family gaps, not bugs.** No `analysis-*` skill family exists for
  substance-authorship work (the plugin's `pm-*`/`voice-*`/`review-*`
  vocabulary implicitly collapses PM and analysis into one role, which
  reportedly cost extra cycles at the 2026-05-20 role-shift). No
  `pm-migrate-existing-project` workflow exists for vaults lifted manually
  before the plugin existed. No `pm-init-review-tracking` skill scaffolds the
  Review workstream's four-file model (`queue.md`/`log.md`/`findings/`/
  `reviewer_tracking.md`) the way `pm-init-reader-review-tracking` scaffolds
  only the reviewer-tracking piece. These are gaps in coverage, distinct from
  sections 1–3's gaps in correctness — worth keeping separate in any
  prioritization, since a missing skill and a buggy skill call for different
  fixes.
- **Drift-check findings that directly extend section 1.** Two items here
  are effectively earlier drafts of, or companions to, findings already
  covered above: "drift check should monitor cross-phase blocking changes"
  and "drift check should monitor chat-managed status block staleness" (both
  proposed as new `drift_check.yaml` checks) extend 1b/1c's theme that the
  drift check's coverage hasn't kept pace with how the vault actually works.
  Separately, "drift report's promotion-folder count includes `.gitkeep`"
  (so an empty `inbox/promotion/` reports as count 1, not 0) is a small,
  concrete instance of the same false-positive-noise problem as 1b, just at
  the inbox-count level rather than the file-inventory level — same root
  cause (the tool doesn't distinguish structural placeholders from real
  content), different surface.
- **`pm-version` self-reports staleness incorrectly.** The skill's own
  description hardcodes "EXPECTED VERSION: v0.1.9" as a literal string; the
  installed version was v0.1.10 (newer), so the skill reported "NEWER THAN
  EXPECTED" — a false-positive staleness warning baked into every release
  that doesn't also hand-edit this string. This is a distinct, narrower
  instance of the same class of problem as 1a/1b: a tool's own bookkeeping
  (filename, exclude-list, hardcoded version literal) silently falling out of
  sync with the real state it's supposed to describe.
- **macOS-specific setup gaps, independently confirmed.** "Full Disk Access
  grant required for launchd-spawned drift check" in that doc matches, in
  detail, the FDA gotcha independently documented in project memory
  (`reference_epistemology_paths.md`): launchd-spawned `/usr/bin/python3`
  silently fails against iCloud paths with `[Errno 1] Operation not
  permitted` until FDA is (re-)granted, and the grant can silently drop after
  a CLT rebuild replaces the binary inode. Memory records this actually
  happened and was diagnosed 2026-07-11 (after being mis-theorized earlier as
  a `registry.yaml` case-mismatch — that theory is confirmed wrong, per the
  same memory) and required a manual PM refresh plus a still-outstanding
  writer GUI action to re-grant FDA. This is a second independent
  confirmation of "silent-fail is the worst failure class" as a recurring
  theme across this report and the plugin-findings doc — worth treating FDA
  self-test (the plugin-findings doc's suggested fix: `pm-setup-project` runs
  `launchctl kickstart` and inspects the error log before declaring setup
  complete) as higher priority given it has now caused a real, if bounded,
  outage. PyYAML-as-precondition and the iCloud + `--separate-git-dir` +
  `gh repo create` incompatibility are adjacent, lower-severity setup gaps in
  the same doc, not independently re-confirmed here.
- **A process-tooling reliability issue outside the plugin proper, but in the
  same "silent state drift" family:** project memory
  (`feedback_commit_race_attribution.md`) documents that in this
  multi-actor, osascript-driven git workflow, staging changes in one shell
  call and committing in a later one leaves a race window where a concurrent
  actor's commit can sweep up your staged files under the wrong commit
  prefix — observed once (content landed correctly, attribution didn't).
  Adopted mitigation: stage-and-commit in a single atomic call, ASCII-only
  commit messages (osascript mangles special characters and can fail the
  commit outright), and verify `git log -1` afterward. Not a skill bug
  specifically, but relevant to any future skill work that automates git
  operations against this vault — a `pm-*` skill that separates staging from
  committing into two tool calls would reintroduce exactly this race.

---

## Summary table

| Area | Skill(s) | Status | Severity |
|---|---|---|---|
| Report filenames lack time-of-day | `pm-run-drift-check` | Confirmed, fix proposed; **2026-07-22: live evidence of the exact failure (dated-file drift across sessions)** | Medium — silent overwrite risk |
| Exclude list stale vs. vault structure | `pm-run-drift-check` | Confirmed, fix proposed; **2026-07-22: directly verified against live `drift_check.yaml` — fix not yet applied to config** | Medium-high — buries real signal |
| Static `inventory_missing` list | `pm-run-drift-check` | Needs manual triage; **2026-07-22: compounds a separately-documented matcher false-positive bug (open since 2026-07-11)** | Low-medium |
| Build-staleness check | `pm-run-drift-check` | Working correctly; **2026-07-22: flagging a tension — live config shows `build.enabled: false`, worth re-checking before trusting this line** | None (pending re-check) |
| Silent-fail on scheduled/offline runs | scheduled-task infra (drift-adjacent) | **New 2026-07-22** — environmental (network-drop), mitigated via ledger, not a code defect | Low (mitigated) |
| Audit-trail contamination reaching reviewer agents | process convention (charter/handoff) | In progress, item 5 open | High — already affected real scoring passes |
| No dependency-gate check before task close | `pm-add-task`/`pm-update-task`/`pm-close-task` | Not yet addressed; **2026-07-22: compounds a separately-documented dual-ledger count-drift bug in the same file** | Medium — ~15% of tasks needed correction |
| Missing `analysis-*`/`pm-init-review-tracking`/`pm-migrate-existing-project` skill families | plugin coverage gaps | **New 2026-07-22 (pulled from standing plugin-findings doc)** — open, not yet built | Medium — causes ad hoc, inconsistent workarounds |
| `pm-version` hardcoded expected-version string | `pm-version` | **New 2026-07-22** — open | Low — cosmetic false-positive |
| Full Disk Access / launchd + iCloud fragility | `pm-setup-project` (macOS) | **New 2026-07-22** — open; has already caused a real outage, per memory | Medium-high — silent-fail class |
| Commit-race attribution under concurrent osascript git ops | any skill automating git | **New 2026-07-22** — mitigated by convention (atomic stage+commit), not structurally prevented | Low-medium |

## Recommended next step

If you want the drift-check fixes verified against real code rather than
inferred from config + output, grant this session (or a future one) access to
`~/code/cowork-tools/` — right now only directory names are visible, not file
contents.

**2026-07-22 addendum:** Also worth reconciling, in the same pass, the two
drift-check items already logged as open in `todos.md`
(`e1a2656d` cross-phase blocking, `63d32305` status-block staleness) plus the
not-yet-formalized matcher-reliability fix (see 1c addendum above) against
whatever the real `drift_check.py` turns out to contain — several of this
report's proposed fixes (exclude-list additions, `.gitkeep` exclusion,
report-filename timestamping) are small enough to bundle into one script
edit + one config edit once the source is visible, rather than filing as
separate follow-ups.
