<!-- =====================================================================
     WRITING-COWORK PLUGIN — MANAGED FILE
     ---------------------------------------------------------------------
     MARKER CONVENTION (applies to every plugin-managed markdown file):

       <!== BEGIN WRITING-COWORK MANAGED: <block-name> ==>   plugin-owned
       <!== END   WRITING-COWORK MANAGED: <block-name> ==>
       <!== BEGIN PROJECT-OWNED ==> ... <!== END PROJECT-OWNED ==>

     (Real markers below use standard HTML comment syntax; the forms above
     are written with `==` only so they don't terminate this comment.)

     Content inside a MANAGED block is owned by the writing-cowork plugin
     and is REGENERATED on sync. Hand edits inside a managed block are
     silently lost the next time the plugin updates it.

     Content inside PROJECT-OWNED is yours. The plugin never reads, edits,
     or overwrites it. Put anything project-specific there.

     Block-level HTML comments are stripped before this file enters the
     model's context, so these markers cost no tokens at runtime. That
     also means the model never sees this notice — hence the short visible
     line at the top of the PROJECT-OWNED section.

     Provenance: writing-cowork {{plugin_version}} · router block rev 1
     Installed: {{date_iso}} by pm-install-router
     ===================================================================== -->

# {{title}} — router

<!-- BEGIN WRITING-COWORK MANAGED: router-orientation -->

**This file is a router, not a manual.** It loads on every turn, so it holds pointers and invariants only. Content belongs in the documents it points at.

## Orient — read in this order, stop when oriented

1. `project_hub.md` — where-am-I: current state, navigation, work threads. **Start here.**
2. `process/data_management/charter.md` — how this project is run; the operating rules.
3. `process/memory/INDEX.md` — memory manifest. Pull topic files on demand, don't read them all.
4. `process/active/roadmap.md` and `process/active/todos.md` — what's planned and what's open.

That is the whole orientation set. It is fixed-size and does not grow with project age. Do **not** reconstruct project state by reading handoffs or history — those are ephemeral and historical respectively, never sources of truth.

## Invariants

- **Memory is the vault.** `process/memory/` is authoritative — visible, git-tracked, diffable. Do not write to hidden session-managed memory. If a durable fact is worth keeping, it goes in a file the writer can see and delete.
- **Knowledge routing — where a durable fact goes:**
  - a repeatable **operating procedure** → `process/` (the relevant process doc)
  - a raw **observation or correction** → `process/memory/`
  - a **commitment or choice** → the project's decisions record
  - a **standing constraint** on how work is done → `process/data_management/charter.md`
- **One home per fact.** No fact lives in two places. If it belongs in two, one of them is a pointer.
- **Every record is one of four kinds** — State (overwrite in place, kept small), Log (append-only), Queue (`inbox/`, process then archive), Ephemeral (handoffs, scratch — never a source of truth).
- **Claim before editing.** Files are claimed in `process/data_management/file_ownership.md` before edits and released on commit.

<!-- END WRITING-COWORK MANAGED: router-orientation -->

<!-- BEGIN WRITING-COWORK MANAGED: router-skills -->

## Skill routing

| To do this | Use |
|---|---|
| See project status / what's now and next | `pm-show-status`, `pm-show-roadmap` |
| Add or update a task | `pm-add-task`, `pm-update-task`, `pm-list-tasks` |
| Add or update a milestone | `pm-add-milestone`, `pm-update-milestone` |
| Claim or release a file | `pm-claim-file`, `pm-release-file`, `pm-show-claims` |
| Hand an artifact to the librarian | `pm-create-promotion-request` |
| Flag a process or plugin problem | `pm-create-issue-report` |
| Process anything sitting in `inbox/` | `pm-process-inbox-item` |
| Check vault integrity | `pm-run-drift-check` |
| Voice and terminology work | the `voice-*` skills |

<!-- END WRITING-COWORK MANAGED: router-skills -->

<!-- =====================================================================
     Everything below is PROJECT-OWNED. The plugin will never touch it.
     Add project-specific instructions, current focus, or temporary notes.
     ===================================================================== -->
<!-- BEGIN PROJECT-OWNED -->

## Project-specific

*Sections above this line are plugin-managed and are overwritten on plugin sync — put project-specific instructions here instead.*

(Nothing yet. Add instructions that apply to this project only — subject-matter conventions, people and sources, things a new session should know that aren't true of every writing-cowork project.)

<!-- END PROJECT-OWNED -->
