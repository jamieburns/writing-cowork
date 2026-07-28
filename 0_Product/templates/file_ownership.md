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
| `CLAUDE.md` | canonical | plugin:writing-cowork | Tier-1 router, loaded every turn. Managed blocks: `router-orientation`, `router-skills`. `PROJECT-OWNED` block is yours. |
| `.gitignore` | canonical | data-mgmt | Git ignore patterns. |
| `.claude/settings.json` | canonical | plugin:writing-cowork | Plugin scoping + memory redirect. **JSON — carries no markers**; this row is its provenance record. |

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
| `drift_check.yaml` | canonical | data-mgmt | Per-project drift-check config (read by ${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py, bundled with the plugin). |

## Process — memory (process/memory/)

| File | Status | Owner | Notes |
|------|--------|-------|-------|
| `INDEX.md` | canonical | data-mgmt | Memory manifest — Reference-layer Tier-2 manifest reached from the router. |
| `<type>_<slug>.md` | working | data-mgmt | Topic files, added as things are learned. Git-tracked so an unreviewed write shows in `git status`. |

## Process — activity log (process/)

| File | Status | Owner | Notes |
|------|--------|-------|-------|
| `Log.md` | canonical | data-mgmt | Append-only activity log, newest-last. **Never overwrite an entry.** Rolls to `process/history/` at phase close. |

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

## Plugin-managed files — provenance registry

Which files the **plugin** owns, as opposed to the librarian or the writer. This table is the authoritative answer; the in-file `BEGIN/END WRITING-COWORK MANAGED` markers are a convenience at the point of editing, not the registry.

Two ownership classes, and the difference matters:

- **Regenerated** — the plugin rewrites the marked blocks on sync. Hand edits *inside a managed block* are lost. Edit the `PROJECT-OWNED` block instead.
- **Scaffold-once** — the plugin wrote the initial file and never touches it again. It is yours from that moment; edit freely.

| File | Class | Managed blocks | Notes |
|------|-------|----------------|-------|
| `CLAUDE.md` | regenerated | `router-orientation`, `router-skills` | `PROJECT-OWNED` preserved byte-for-byte across syncs. |
| `.claude/settings.json` | regenerated | *(none — JSON)* | Provenance lives here only. Never add a `"_comment"` key; a strict reader rejecting this file means the plugin stops loading. |
| `process/data_management/claim_dispute_protocol.md` | regenerated | whole file | Pure reference doc; no project-specific content. |
| `process/data_management/tagging_conventions.md` | regenerated | whole file | Pure reference doc. |
| `process/data_management/charter.md` | scaffold-once | — | Operating rules; you will edit these. Plugin does not reclaim it. |
| `process/data_management/drift_check.yaml` | scaffold-once | — | YAML, so it *can* take comments and markers if it ever becomes regenerated. |
| `process/memory/INDEX.md` | scaffold-once | — | Yours the moment it exists. |
| `process/Log.md` | scaffold-once | — | Append-only; the plugin must never rewrite it. |
| `process/data_management/git-hooks/post-commit` | scaffold-once | — | Session-hygiene hook. Paths resolved at install; `core.hooksPath` points here. Tracked, so it travels with a clone. |
| `project_hub.md` | scaffold-once | `DRIFT-ATTENTION-START/END` | Exception: the Attention block *is* tool-written by drift-check, under an older marker naming scheme predating the `MANAGED:` convention. Reconciling the two names requires updating `drift_check.py` in the same change. |

Keep this table current when the plugin gains or drops a managed file — it is what makes "who owns this line" answerable without opening every file.

## Writer-managed (added as project develops)

Rows for substantive writing artifacts (drafts, deliverables, analysis files, graphics, subprojects) are added by the librarian as the writer produces them. Initial table covers only the setup-time scaffold.

---

## Drift-check footer

This footer is written by `${CLAUDE_PLUGIN_ROOT}/tools/drift_check.py` (bundled with the writing-cowork plugin) on each run. Each run writes a status line below; a `DRIFT` line points at a detailed report under `drift_reports/`.

<!-- DRIFT-FOOTER-START -->
- Last drift check: **(not yet run)**
<!-- DRIFT-FOOTER-END -->

**Operation.** Scans vault for files not listed in this table; validates cross-references in core docs; compares source-markdown mtimes against built deliverable mtimes (if `build:` enabled in `drift_check.yaml`); counts inbox items (flags those past `overdue_days` as overdue); surfaces gitignored generated artifacts present in vault. Silent if clean. On drift: writes detailed report to `drift_reports/<date>T<time>.md`, sets `.drift_flag` marker file, populates the hub `## Attention` block. Resolving the underlying drift causes the next run to clear all three.
