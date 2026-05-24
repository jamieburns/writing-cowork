# Writing-Cowork Lift Procedure

This guide documents the staged setup process for initializing a new writing-cowork project. The lift procedure orchestrates skill invocations in the correct order, with clear stage boundaries.

## Lift Stages

### Stage 1: Infrastructure Setup

Initialize the core vault structure and version control.

**Skills invoked (in order):**

1. `pm-init-vault` — Create the directory skeleton (process/, inbox/, .gitignore)
2. `pm-init-project-cowork-settings` — Write `.claude/settings.json` to enable writing-cowork for this project
3. `pm-init-git` — Initialize local git repository on main branch
4. `pm-init-github` — Create remote GitHub repository (if `--git=new-github`)
5. `pm-install-charter` — Install data-management charter
6. `pm-finalize-scaffold-commit` — Stage and commit the infrastructure

**Outputs:** A functional vault with git history, ready for operational documents.

**Blockers:** None — stage 1 is self-contained.

---

### Stage 2: Operational Documents & Planning

Create the tracking and planning infrastructure.

**Skills invoked (in order):**

1. `pm-init-roadmap` — Create roadmap (phase-based or now-next-later)
2. `pm-init-todos` — Create todos tracking with example tasks
3. `pm-init-voice-handoff` — Install voice/tone briefing document
4. `pm-init-reader-review-tracking` — Create reviewer tracking document
5. `pm-init-voice-exceptions` — Create voice exceptions tracking
6. `pm-install-hierarchy-and-ownership` — Install file hierarchy and ownership tables
7. `pm-install-project-hub` — Install project hub document

**Outputs:** A complete operational structure with tracking documents and planning views.

**Blockers:** Requires stage 1 to be complete.

---

### Stage 3: Data-Management Governance

Install the remaining governance documents.

**Skills invoked:**

1. `pm-install-handoff` — Install librarian handoff document (`handoff.md`)
2. `pm-install-for-other-contexts` — Install cross-context coordination guide
3. `pm-install-drift-check-config` — Install drift check configuration
4. `pm-install-claim-dispute-protocol` — Install claim/release protocol reference
5. `pm-install-tagging-conventions` — Install git tag conventions
6. `pm-register-project` — Register project in cowork registry

**Outputs:** A fully governed vault with all reference documents and operational policies in place.

**Blockers:** Requires stage 2 to be complete.

---

## Optional: Pre-Lift Decisions

Before starting the lift, the user may supply:

- `--decisions=<file>` — A pre-prepared decisions document from a planning phase. This is installed as `decisions.md` at vault root during stage 2.

---

## Resuming Interrupted Lifts

If a lift is interrupted (a skill fails), use `pm-resume-setup` to continue from the failed step. The orchestrator maintains state in `~/.config/cowork/writing-cowork/setup_state/<project-name>_setup_state.json`.

```bash
pm-resume-setup --project=<project-name>
```

This picks up where the previous run left off — no need to restart from stage 1.

---

## Vault Readiness Checklist

After lift completion, verify:

- [ ] Git repo initialized and remote configured
- [ ] `project_hub.md` exists and is readable
- [ ] `roadmap.md` exists with project phases/timeline
- [ ] `todos.md` exists with schema and example tasks
- [ ] `charter.md` documents scope and operating rules
- [ ] `process/data_management/file_ownership.md` exists
- [ ] `.gitignore` covers scratch conventions
- [ ] `drift_check.yaml` is configured for this project
- [ ] Project is registered in cowork registry (`pm-list-projects` includes it)

Once all items pass, the vault is ready for substance-execution work to begin.
