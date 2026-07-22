---
name: writing-cowork Skill Usage Signal
description: Filesystem-fingerprint pass estimating which writing-cowork plugin skills are used heavily, lightly, or not at all — not a real invocation count. Covers two vaults (Reconciliation-hypothesis-class project referred to below as "Project A", and Epistemology).
type: analysis / handoff
date: 2026-07-21
author: Claude (Cowork), cloud session
---

# writing-cowork Skill Usage Signal

## What this is and isn't

There is no built-in per-skill invocation counter in Cowork or in this plugin. This
document is an **indirect proxy**: each writing-cowork skill tends to leave a
distinctive trace in a vault (a file it creates, a row format it appends, a
counter it increments). By counting those traces on 2026-07-21 across two
independent vaults running the same plugin, we can rank skills as
clearly-used, lightly-used, or apparently-unused in each — but this is a
signal, not a ledger. Two known blind spots apply to both vaults:

1. **Read-only/display skills leave no trace at all** (`pm-show-kanban`,
   `pm-show-composite-kanban`, `pm-show-claims`, `pm-show-status`, `pm-show-roadmap`,
   `pm-version`, `pm-list-projects`, `pm-list-tasks`). They could run constantly
   and this method would show zero.
2. **Git history itself is out of reach from this cloud session, in both vaults.**
   Each vault's working tree lives in iCloud Obsidian, but per each project's
   `git_setup.md`-equivalent the actual `.git` directory lives outside iCloud
   (`~/.git-repos/<project>/.git/`) specifically to avoid iCloud sync corruption
   — the cloud sandbox's device bridge cannot reach that path. Confirmed for
   Epistemology by reading its `.git` file directly: `gitdir:
   /Users/jburns/.git-repos/epistemology/.git`. That means commit messages, git
   tags, and true commit counts are invisible to this method in both vaults,
   even though several writing-cowork skills (`pm-tag-lock`, `pm-tag-snapshot`)
   exist specifically to create tags, and both vaults show tag names referenced
   in prose (e.g. Epistemology's `project_hub.md` cites `lock/r1-complete`,
   `lock/r2-complete`, `snapshot/2026-07-19-connective-tissue-complete`,
   `snapshot/2026-07-20-voice-restart-entered`, among others). **Anyone with
   real shell access to the Mac could get an exact count via `git log --all
   --grep` against skill names or commit prefixes — that would be strictly
   better evidence than this document, for both vaults.**

## Method

Walked `process/` (active, history, data_management, review, production) plus
`project_hub.md`, `inbox/` and its subfolders, and `.claude/settings.json`, in
each vault, looking for the specific artifact each skill is documented to
produce, and counted occurrences/rows/files as a proxy for "how many times
has this run."

## Findings — Project A (original pass)

### Clearly used heavily

- **`pm-add-task` / `pm-update-task` / `pm-list-tasks`** — `todos.md` carries 85
  short-hash task IDs; 57 rows marked `done`, 12 `in-progress`. This file is
  under constant churn.
- **`pm-run-drift-check`** — 11 dated reports in `process/data_management/drift_reports/`
  (2026-05-12 through 2026-07-20), roughly weekly through May, then a gap, then
  a July burst (07-11, 07-18, 07-20). `.drift_flag` and `.drift_last_run` are
  both live/current, confirming the check runs on an ongoing basis, not just
  at setup.
- **Roadmap skills (`pm-add-milestone`, `pm-init-roadmap`, `pm-show-roadmap`,
  `pm-update-milestone`)** — `roadmap.md` has 20 section headers; the history
  log names `pm-add-milestone`, `pm-init-roadmap`, `pm-update-milestone`,
  `pm-show-roadmap`, and `pm-show-status` explicitly.
- **`pm-create-hub-update-request` + `pm-process-inbox-item` (hub-update route)**
  — corrected from an earlier same-day pass: `process/history/` holds multiple
  archived hub-update cover-notes (`2026-05-20-phase-10-closure_hub-update-request.md`,
  `2026-05-20-phase-11-reauthor_hub-update-request.md`, one cancelled variant, plus
  several `*_cover.md` files for promotion-style handoffs). These are processed
  and archived, which is exactly the intended lifecycle — this route is a real
  working part of the workflow, not a dead one.
- **Voice mechanical-pass tooling (`voice-run-mechanical-pass`, `voice-audit-terminology`)**
  — `voice_exceptions.md` exists specifically because these skills kept
  re-flagging an intentional rename ("From Eden to New Creation"), which is
  what motivated creating the exceptions registry in the first place. History
  log also shows 3 hits on "voice-pass-" workstreams, and there's a whole
  stalled git branch (`voice-pass-2026-05`) dedicated to this work per
  `git_setup.md`.

### Used, but lightly

- **`pm-claim-file` / `pm-release-file`** — `file_ownership.md` has 187 tracked
  file rows total but only 2 ever marked `claimed:voice` (one of those is
  currently released). The claim/release protocol exists and has been
  exercised, but it's far from the default mode of work — most files are
  apparently edited without going through an explicit claim.
- **`voice-add-exception`** — exactly 1 row in `voice_exceptions.md`. Used at
  least once; no evidence of repeated use.

### Apparently unused (as far as filesystem traces show)

- **`pm-create-promotion-request` / promotion-route inbox processing** —
  `inbox/promotion/` was not observed to contain any pending or archived
  cover-notes beyond the general `README.md`. Some promotion-style artifacts
  appear to have been handled ad hoc (the `*_cover.md` files in `history/`
  look promotion-shaped), so this may be under- rather than zero-used.
- **`pm-create-issue-report` / `pm-escalate-issue`** — no issue cover-notes
  found in `inbox/issues/` or `history/`. No evidence this route has ever
  fired.
- **`pm-schedule-review`** — no corresponding scheduled-task references found
  in project docs.
- **`voice-capture-sample` / `voice-confirm-sample` / `voice-shift-terminology`
  / `voice-recommend-wording` / `voice-list-exceptions` / `voice-remove-exception`**
  — beyond the single confirmed exception row, no other trace of these firing.

### One-time by design (ran once at project creation, not a usage gap)

`pm-setup-project`, `pm-init-vault`, `pm-init-git`, `pm-init-github`,
`pm-init-project-cowork-settings`, `pm-init-reader-review-tracking`,
`pm-init-todos`, `pm-init-voice-exceptions`, `pm-init-voice-handoff`,
`pm-install-charter`, `pm-install-claim-dispute-protocol`,
`pm-install-drift-check-config`, `pm-install-for-other-contexts`,
`pm-install-handoff`, `pm-install-hierarchy-and-ownership`,
`pm-install-project-hub`, `pm-install-tagging-conventions`,
`pm-finalize-scaffold-commit`, `pm-register-project`,
`pm-place-lift-decisions` (conditional, only if `--decisions=` was passed).
All of these are bootstrap-only skills; a low or single "usage count" is
expected behavior, not evidence anyone should use them more.

### Invisible to this method (read-only/display skills)

`pm-show-kanban`, `pm-show-composite-kanban`, `pm-show-claims`,
`pm-show-status`, `pm-show-roadmap`, `pm-version`, `pm-list-projects`. These
skills only read and display state; they leave no artifact behind, so this
filesystem sweep cannot tell you anything about their real usage frequency —
treat the "no signal" here as "unmeasured," not "unused."

### Tag/version skills — signal exists but is out of reach

`pm-tag-lock` and `pm-tag-snapshot` almost certainly have run — `project_hub.md`
references a lock tag (`lock/2026-07-20-projectA-replan-transition`) — but
actual tag history lives in the external `.git` directory this session
cannot reach. Treat this as a real, probably-nonzero usage that this method
simply cannot count.

## Findings — Epistemology vault

### Clearly used heavily

- **`pm-add-task` / `pm-update-task` / `pm-list-tasks`** — `todos.md` carries
  247 short-hash task ID rows by direct tally (193 `done`, 45 `planned`, 5
  `in-progress`, plus a handful of rows with irregular cell spacing that a
  naive grep undercounts by a few). The running prose log at the top of the
  file re-derives its own count by hand at every single edit (dozens of dated
  entries, each restating "Counts (direct tally): N / done / planned /
  in-progress") — that log is itself strong secondary evidence of extremely
  heavy `pm-update-task`/`pm-add-task` churn, independent of the row count.
- **`pm-run-drift-check`** — 3 dated reports in
  `process/data_management/drift_reports/` (2026-07-05, 2026-07-11, 2026-07-17)
  plus a live `.drift_flag` and `.drift_last_run` (most recent 2026-07-17,
  timestamp current as of this pass). Lighter cadence than Project A's 11
  reports, but the tooling is unambiguously wired up and running — nightly
  launchd job confirmed in project memory, with a documented and resolved FDA
  permission gotcha.
- **Roadmap skills (`pm-add-milestone`, `pm-init-roadmap`, `pm-show-roadmap`,
  `pm-update-milestone`)** — `roadmap.md` has 14 section headers spanning 6
  completed phases (Baseline, Baseline Review, Structure, Structure Review,
  Connective Tissue) plus one active (Voice) and two planned (R3, Prep and
  Production, R4), each phase carrying its own completion tag reference. This
  is a heavily-maintained, actively-evolving document, not a one-shot
  scaffold artifact.
- **Hub-update / drift-attention tooling (`pm-create-hub-update-request` +
  tool-managed drift blocks)** — `project_hub.md` carries a live
  `DRIFT-ATTENTION-START/END` block and `file_ownership.md` carries a live
  `DRIFT-FOOTER-START/END` block, both explicitly tool-owned per the vault's
  own conventions doc. `project_hub.md` prose also documents a **second,
  parallel per-chat-role status-block convention** (`ROLE-STATUS-START/END`)
  introduced 2026-05-16 specifically to reduce reliance on the
  inbox/promotion round-trip for routine "what am I working on" updates — see
  Mixed Signals below.
- **`pm-create-issue-report`** — unlike Project A, this route has fired at
  least once: `process/history/2026-07-17_issue_ct2-out-of-scope-findings_local.md`
  is a processed-and-archived issue cover-note. Single confirmed instance, but
  a confirmed one.

### Used, but lightly

- **`pm-claim-file` / `pm-release-file`** — `file_ownership.md` has 129 tracked
  file rows (by direct `|`-row count including header rows) with exactly 2
  live `claimed:` markers found (`claimed:analysis`, `claimed:review`) at the
  moment of this snapshot. Directionally the same story as Project A: the
  protocol exists and is actively exercised, but most edits do not appear to
  route through an explicit claim.
- **`voice-add-exception`** — `voice_exceptions.md` carries roughly 20 rows
  (project-wide terminology/spelling exceptions plus one section-scoped
  Scripture-translation exception), a meaningfully higher count than Project
  A's single row. Clearly used more than once here, though still a small
  registry relative to the vault's overall size.

### Apparently unused (as far as filesystem traces show)

- **`pm-create-promotion-request`** — `inbox/promotion/` contains only its
  `.gitkeep`; no pending or archived promotion cover-notes were found there.
  As in Project A, promotion-shaped artifacts appear to be processed and
  archived directly into `process/history/` (several `*_to_pm.md`,
  `*_hub_update_request.md`, and `*_findings.md`-style files exist there)
  rather than staged through `inbox/promotion/` first — this looks like the
  same "ad hoc, not zero" pattern as Project A, not a genuinely dead route.
- **`pm-escalate-issue`** — the one issue report found
  (`2026-07-17_issue_ct2-out-of-scope-findings_local.md`) was resolved locally
  per its filename (`_local`); no evidence any issue was escalated to
  GitHub via `pm-escalate-issue`.
- **`pm-schedule-review`** — no scheduled-task references found in
  `project_hub.md` or elsewhere in `process/`. Same null result as Project A.
- **`voice-capture-sample` / `voice-confirm-sample` / `voice-shift-terminology`
  / `voice-recommend-wording` / `voice-list-exceptions` / `voice-remove-exception`**
  — no trace beyond the `voice_exceptions.md` rows already counted above.
  Notably this vault *does* show several `writer_voice_sample*.md` files in
  `process/active/` (per-mode voice samples: connect, convey, convince,
  cover) — these look like they could plausibly be `voice-capture-sample` /
  `voice-confirm-sample` output, which would make this a **stronger positive
  signal than Project A showed**, not a null. Flagged as uncertain rather than
  scored, since the artifact-to-skill mapping isn't as clean as (e.g.) the
  drift-report/`pm-run-drift-check` pairing — see Mixed Signals.

### One-time by design (ran once at project creation, not a usage gap)

Same bootstrap-only list as Project A applies here — `pm-setup-project`,
`pm-init-vault`, `pm-init-git`, `pm-init-github`,
`pm-init-project-cowork-settings`, `pm-init-reader-review-tracking`,
`pm-init-todos`, `pm-init-voice-exceptions`, `pm-init-voice-handoff`,
`pm-install-charter`, `pm-install-claim-dispute-protocol`,
`pm-install-drift-check-config`, `pm-install-for-other-contexts`,
`pm-install-handoff`, `pm-install-hierarchy-and-ownership`,
`pm-install-project-hub`, `pm-install-tagging-conventions`,
`pm-finalize-scaffold-commit`, `pm-register-project`,
`pm-place-lift-decisions` (conditional). Epistemology's `.claude/settings.json`
confirms a scoped, single-project Cowork config consistent with a one-time
`pm-init-project-cowork-settings` run, not repeated re-scaffolding.

### Invisible to this method (read-only/display skills)

Same list and same caveat as Project A: `pm-show-kanban`,
`pm-show-composite-kanban`, `pm-show-claims`, `pm-show-status`,
`pm-show-roadmap`, `pm-version`, `pm-list-projects`. Zero signal here means
"unmeasured," not "unused" — these commands are plausibly run constantly
given how often the vault's owner (per `project_hub.md`'s heavy
Attention/Workstream-status structure) would need a "where am I" view.

### Tag/version skills — signal exists but is out of reach

Stronger circumstantial evidence than Project A: `project_hub.md` names at
least 7 distinct lock/snapshot tags (`lock/2026-05-20-role-taxonomy-pm-analysis-review-voice`,
`lock/r1-complete`, `lock/r2-complete`, `snapshot/2026-05-24-baseline-0-complete`,
`snapshot/2026-05-25-baseline-complete`, `snapshot/2026-07-10-voice-deferred-connective-tissue`,
`snapshot/2026-07-19-connective-tissue-complete`, `snapshot/2026-07-20-voice-restart-entered`),
one per major phase transition. `pm-tag-lock`/`pm-tag-snapshot` have almost
certainly run at least 7–8 times, but as in Project A the authoritative count
lives in the external `.git` directory (`~/.git-repos/epistemology/.git/`,
confirmed by reading the vault's `.git` pointer file) and is out of reach
from this cloud session.

## Mixed signals

Genuine disagreements between the two passes that can't be chalked up to
"Project A does X, Epistemology does Y" — cases where the same skill or route
looks used in one vault and unused in the other, or where the evidence within
one vault points two directions at once.

- **Hub-update routing: two competing mechanisms, unclear which is primary.**
  Project A's strongest positive signal for `pm-create-hub-update-request` +
  `pm-process-inbox-item` was a set of archived cover-notes in
  `process/history/`. Epistemology's `inbox/promotion/` and hub-update
  cover-note evidence is comparably thin, but `project_hub.md` documents that
  as of 2026-05-16 the vault *deliberately moved away* from the
  inbox/promotion round-trip for routine status updates, replacing it with
  chat-owned `ROLE-STATUS-START/END` blocks written directly into the hub.
  That's not "Epistemology uses a different skill" — it's evidence that
  **the inbox/promotion-request skill route may have been actively
  deprecated in practice** in at least one vault, which changes the
  interpretation of "apparently unused" for `pm-create-promotion-request`
  from "nobody happened to use it" to "a documented process decision routed
  around it." Project A shows no equivalent decision documented, so its low
  promotion-route usage reads more like an unexercised feature. Recommend
  treating `pm-create-promotion-request` usage-rate as **skill-appropriate-but-
  situationally-bypassed**, not simply low across the board, before drawing
  any conclusion about the skill's value.
- **`voice-capture-sample` family: plausible hit in one vault, clean zero in
  the other, same evidentiary strength.** Project A reports a flat zero for
  `voice-capture-sample` / `voice-confirm-sample` beyond the one exception
  row. Epistemology has no direct trace of the skill name either, but does
  have five `writer_voice_sample*.md` files in `process/active/` that are
  plausibly this skill's output (or could equally be hand-authored reference
  material the writer produced without the skill at all — nothing in the
  filename or content pattern conclusively distinguishes "skill-produced"
  from "manually placed"). This is a real disagreement in what the same
  absence-of-a-distinctive-trace should be read as, not just a count
  difference — Project A's zero is a clean null, Epistemology's is an
  ambiguous one. Do not average these into a single "lightly used" verdict
  across projects; they're different strengths of evidence.
- **Claim/release protocol: same low rate, opposite framing risk.** Both
  vaults show ~1–2% of tracked files ever marked `claimed:` (2/187 in Project
  A, 2/129 in Epistemology). Taken together this looks like consistent
  evidence the claim/release protocol is a rarely-exercised safety valve
  rather than the default editing mode — but Epistemology's
  `claim_dispute_protocol.md` and multi-role structure (pm / analysis /
  review / voice / writer, each with distinct commit prefixes) is far more
  elaborated than anything visible in Project A's notes, suggesting the
  *infrastructure* investment in claim/release is higher in Epistemology even
  though the *usage* rate is statistically identical. If usage rate alone is
  used to judge whether this skill pair is "worth keeping," these two vaults
  would say the same thing (rarely used); if investment/design signal is
  weighed instead, they'd disagree. Flagging so a downstream reader doesn't
  pick one lens implicitly.
- **Issue reporting: zero vs. one, but the one instance argues against the
  route's growth path.** Project A shows zero fired issue reports. Epistemology
  shows exactly one, and it was resolved locally (filename-tagged `_local`)
  rather than escalated via `pm-escalate-issue`. So the one positive data
  point Epistemology contributes doesn't actually support "the
  issue→escalate pipeline works end-to-end" — it's a data point for
  "issues get filed and then handled without ever reaching the escalate
  step," which is arguably a different, more specific finding than either
  "unused" or "used." Recommend not folding this into a simple two-vault
  usage-rate average for `pm-create-issue-report`/`pm-escalate-issue` as a
  pair; they should be scored separately, and neither vault has fired the
  escalate half yet.

## Recommendation

If you want an authoritative count rather than this proxy, the highest-value
next step is a `git log --all` sweep on the Mac itself (via a terminal or the
`osascript` bridge), grepping commit messages for skill names or the
`[voice]` / `[review-mgmt]` / `[analysis]` / `[data-mgmt]` branch/prefix
conventions already in use in each vault. That would convert both halves of
this document from "signal" to "ledger," and would also resolve the Mixed
Signals items above that currently can't be settled from filesystem traces
alone — in particular the `writer_voice_sample*.md` provenance question and
the true promotion/hub-update route split.
