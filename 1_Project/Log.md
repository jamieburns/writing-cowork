# Activity Log

The single **shared, append-only** activity log for this repo — the semantic layer over git's mechanical layer. One entry per durable change: what, why, from what inputs, and the commit that carried it.

**Kind:** Log (append-only; never overwrite an entry). **Schema** and rationale: `1_Project/Documents/information_architecture_spine_2026-07-24.md` §4.

**Conventions**
- **Append-only, newest-last.** Sessions orient by reading the *tail*.
- **Author-stamped** — the role or `user` responsible for the change.
- **Index-first** — terse and scannable; the primary reader is the next session reloading state cheaply, not a prose reader.
- Rolls to `1_Project/History/` at phase/version close so this live file stays bounded.

> **Bootstrap note (2026-07-26):** this file was created ahead of its formal v0.16 build (the Log was a decided-form / deferred-mechanics organ per the spine). The location `1_Project/Log.md` and the newest-last convention are provisional — the v0.16 `pm-close-session` work may confirm or revise them.

---

## Entry schema

```
- <YYYY-MM-DD> · <author: role|user> · <action>
  why: <one line>
  inputs: <files / decisions read>
  changed: <files written>  · commit: <hash | uncommitted>
```

---

## Entries

- 2026-07-26 · user → claude · Established validate-before-commit as a hard release gate.
  why: `claude plugin validate .` must always run before committing a version bump — user-directed standing rule, not an optional step.
  inputs: `1_Project/Process/dev-workflow-and-release.md`; spine §4 (log schema)
  changed: `1_Project/Process/dev-workflow-and-release.md` (release-checklist gate); `1_Project/Log.md` (this log created)  · commit: 831608c

- 2026-07-29 · claude · Closed out the information-architecture / memory workstream; v0.1.17 content complete.
  why: memory management moved from an open problem to a shipped model, and the enforcement mechanism changed twice as evidence arrived — hooks do not run in Cowork, so enforcement moved to a git post-commit hook that fires where consent actually happens.
  inputs: spine §5/§6/§8; `Decisions.md`; GitHub #40495/#47993/#63360; `drift_check.py`
  changed: `Roadmap.md` (stale narrative sections corrected); `drift_check.py` (v0.3.1 — log_unlanded no longer flags the schema example)  · commit: 417c755
