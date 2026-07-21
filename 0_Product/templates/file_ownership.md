# File ownership — {{title}}

Tracking table for vault files. Drift-check footer at the bottom.

**Last updated:** {{date_iso}} (initial scaffold)

---

## Conventions

**Status values:**

- `canonical` — load-bearing, primary reference
- `working` — in active development
- `archived` — closed / superseded; retained for history
- `claimed:<context>` — currently being edited by named context (cleared on commit)

**Owner values:**

Default is **`data-mgmt`** — the librarian context owns operational care of every file by default. The writer authors content; the librarian handles placement, drift, versioning, build, and external artifact generation.

Other values, used only when that context has explicitly claimed the file or is mid-edit:

- `writer` — writer is actively editing (Obsidian on Mac / iPad / iPhone) or has signaled intent.
- `substance` — substance-execution context (when active).
- `voice` — voice/tone advisory context (when active).
- `reader-review` — reader-review triage context (when active).

Claims release on commit; Owner returns to `data-mgmt`. **Mode boundary still applies:** `data-mgmt` ownership of a file does not authorize substance edits to its content.

---

## Project navigation

| File | Status | Owner | Notes |
|------|--------|-------|-------|
| `project_hub.md` | canonical | data-mgmt | Where-am-I navigation; tool-managed Attention block, librarian-edited otherwise. |
| `.gitignore` | canonical | data-mgmt | Git ignore patterns. |

## Data-management artifacts (process/data_management/)

| File | Status | Owner | Notes |
|------|--------|-------|-------|
| `charter.md` | canonical | data-mgmt | Role definition, scope, operating rules. |
| `handoff.md` | canonical | data-mgmt | Living handoff — read first when picking up librarian role in a new chat. |
| `for_other_contexts.md` | canonical | data-mgmt | How non-librarian chats interact with the librarian. |
| `file_hierarchy.md` | canonical | data-mgmt | Layout + navigation-by-task. |
| `file_ownership.md` | canonical | data-mgmt | This file. |
| `claim_dispute_protocol.md` | canonical | data-mgmt | Multi-chat claim resolution. |
| `tagging_conventions.md` | canonical | data-mgmt | Git tag namespaces + workflow. |
| `drift_check.yaml` | canonical | data-mgmt | Per-project drift-check config (read by ~/code/cowork-tools/drift_check.py). |

## Process — active (process/active/)

| File | Status | Owner | Notes |
|------|--------|-------|-------|
| `voice_handoff.md` | canonical | data-mgmt | Voice/tone context handoff. |
| `voice_exceptions.md` | working | data-mgmt | Intentional voice-rule exceptions. |
| `reviewer_tracking.md` | working | data-mgmt | Per-reviewer engagement status. |
| `roadmap.md` | working | data-mgmt | Project roadmap. |
| `todos.md` | working | data-mgmt | Granular task list. |

## Inbox (inbox/)

| Path | Status | Owner | Notes |
|------|--------|-------|-------|
| `inbox/promotion/` | (empty) | data-mgmt | Artifacts from other chats requesting placement; hub-update requests. |
| `inbox/hub-updates/` | (empty) | data-mgmt | (Optional separation) hub-update-only requests. |

## Writer-managed (added as project develops)

Rows for substantive writing artifacts (drafts, deliverables, analysis files, graphics, subprojects) are added by the librarian as the writer produces them. Initial table covers only the setup-time scaffold.

---

## Drift-check footer

This footer is written by `~/code/cowork-tools/drift_check.py` on each run. Each run writes a status line below; a `DRIFT` line points at a detailed report under `drift_reports/`.

<!-- DRIFT-FOOTER-START -->
- Last drift check: **(not yet run)**
<!-- DRIFT-FOOTER-END -->

**Operation.** Scans vault for files not listed in this table; validates cross-references in core docs; compares source-markdown mtimes against built deliverable mtimes (if `build:` enabled in `drift_check.yaml`); counts inbox items (flags those past `overdue_days` as overdue); surfaces gitignored generated artifacts present in vault. Silent if clean. On drift: writes detailed report to `drift_reports/<date>.md`, sets `.drift_flag` marker file, populates the hub `## Attention` block. Resolving the underlying drift causes the next run to clear all three.
