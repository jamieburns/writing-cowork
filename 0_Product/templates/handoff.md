# Data-management handoff — {{title}}

Where things stand for the librarian / data-management context. Read this first when picking up the role in any new chat. Living doc — kept current by the librarian.

**Last updated:** {{date_iso}} (initial setup).

---

## Quick start

For any new chat opening into librarian mode, read in this order:

1. `charter.md` — role definition, scope, mode boundary, operating rules.
2. `file_hierarchy.md` — vault layout and navigation-by-task.
3. `file_ownership.md` — who owns what; what's currently claimed; drift footer.
4. This file's "Current state" section below.

Reference docs as needed: `claim_dispute_protocol.md`, `tagging_conventions.md`.

**If you are NOT the librarian** (substance, voice, reader-review, etc.) — read `for_other_contexts.md` instead. That doc explains what to ask the librarian for, how to claim files, how to hand off new artifacts, and how to request hub updates.

---

## Current state ({{date_iso}})

### Vault structure

- Vault scaffolded {{date_iso}} via `pm-setup-project` (writing-cowork plugin v0.1).
- Source of truth: `{{vault_path}}`
- Substantive folders (`analysis/`, `background/`, `graphics/`, `subprojects/`, etc.) created organically by the writer as the project develops.

### Git / GitHub

- (populated as the project's git config is finalized — see `git remote -v`)
- Push happens from the writer's primary Mac. Credentials via `gh auth login` (HTTPS credential helper).

### Active automation

- **Drift check** — `~/code/cowork-tools/drift_check.py` runs against this project's `process/data_management/drift_check.yaml` on the shared schedule (per machine's launchd / cron). Output: Attention block at top of `project_hub.md`, footer in `file_ownership.md`. Detailed report on drift only: `drift_reports/<date>.md` (gitignored).

### Ownership default

- **`data-mgmt` is the default Owner for every file in the table.** The writer authors content; the librarian owns operational care (placement, drift, versioning, build artifacts, external packaging).
- Other Owner values (`writer`, `substance`, `voice`, `reader-review`) are used only when that context has actively claimed the file or is mid-edit. Released on commit.
- Mode boundary still applies — `data-mgmt` ownership of a file does not authorize substance edits to its content.

---

## Operating tools

| Tool | What it does | Where |
|------|---|-------|
| `drift_check.py` | Inventory / xref / build-freshness / inbox check | `~/code/cowork-tools/drift_check.py` (shared) |
| osascript MCP | Executes shell commands on writer's Mac (git, builds, file moves) | Loaded via ToolSearch |
| Build pipeline | (populated when a build pipeline is established) | (path) |

---

## Mode boundary (reminder)

**In scope** for this context:

- File placement, organization, drift, integrity, hygiene.
- Versioning operations — stage, commit, push, tag, branch.
- Build operations.
- Inbox routing — surface arrivals; placement decisions adjudicated with writer.
- External artifact generation — reader bundles, release packages, ad-hoc shares.

**Out of scope — escalate to writer or substance context:**

- Substance changes (claim strength, framing, scope, voice).
- Decisions about what documents should say.

Charter §"Mode boundary" has the full rule. When in doubt, escalate.

---

## Open / deferred

Tracked as the project develops. Initial items:

- (placeholder — replace with project-specific deferred items as they accrue)

---

## Origin

This context was established {{date_iso}} via `pm-setup-project` from the writing-cowork plugin. That plugin lifted the pattern from Reconciliation Hypothesis (the canary project). See plugin's HANDOFF.md and v1 design doc for the source pattern.
