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
     or overwrites it. Put anything repo-specific there.

     Block-level HTML comments are stripped before this file enters the
     model's context, so these markers cost no tokens at runtime. That
     also means the model never sees this notice — hence the short visible
     line at the top of the PROJECT-OWNED section.

     Provenance: writing-cowork v0.1.15 · router block rev 1 · 2026-07-25
     Prototype status: this file is the memory-management prototype's
     Tier-1 router (spine doc section 5). Not yet ported to the plugin.
     ===================================================================== -->

# writing-cowork — router

<!-- BEGIN WRITING-COWORK MANAGED: router-orientation -->

**This file is a router, not a manual.** It loads on every turn, so it holds pointers and invariants only. Content belongs in the documents it points at.

## Orient — read in this order, stop when oriented

1. `1_Project/Decisions.md` — current resting state of every decision. **Start here.**
2. `1_Project/Memory/INDEX.md` — memory manifest; pull topic files on demand, don't read them all.
3. `1_Project/Process/README.md` — how we work: dev cycle, release procedure, tool lanes.
4. `2_Development/RoadMap/Roadmap.md` — version status.
5. `1_Project/Todos.md` — the work list: what is open, who owns it, what blocks it.

That is the whole orientation set. It is fixed-size and does not grow with project age. Do **not** reconstruct project state by reading `1_Project/Handoff/` or `1_Project/History/` — those are ephemeral and historical respectively, never sources of truth.

## Invariants

- **Memory is the vault.** `1_Project/Memory/` is authoritative — visible, git-tracked, diffable. Do not write to the hidden session-managed memory store. See `1_Project/Memory/feedback_visible_memory_only.md`.
- **Git goes through osascript — including `git status`.** Anything that touches `.git/` runs via the host, not a mounted-view bash. That is *not* only add/commit/push/tag: `git status` refreshes the index, so it creates `.git/index.lock`, and from the mount the create succeeds while the unlink fails with EPERM. The output looks correct; the zero-byte orphan it leaves blocks your next host-side commit. Only `git log`, `git show`, and `git diff` are safe from the mount. See `1_Project/Memory/feedback_git_status_creates_index_lock.md`.
- **Stage a file once.** A file copied into the sandbox is pinned to its first stage for the whole session — re-staging does **not** refresh it, and reports the device's real size regardless. After writing a file back, make further edits on the host, never from a re-stage. See `1_Project/Memory/feedback_restaged_files_can_be_stale.md`.
- **Review `git diff`, not just `git status`, before committing.** Names tell you which files changed; only content tells you whether a change silently reverted something. This is the detector for stale-copy edits — the one failure mode the lane rules above can still let through.
- **Every record is one of four kinds** — State (overwrite in place, kept small), Log (append-only), Queue (`inbox/`, process then archive), Ephemeral (handoffs, scratch — never a source of truth). One home per fact.
- **A version bump touches three places** — `plugin.json`, the `pm-version` EXPECTED VERSION marker, and the `(vX.Y.Z)` tag in both plugin and marketplace catalog descriptions.

<!-- END WRITING-COWORK MANAGED: router-orientation -->

<!-- BEGIN WRITING-COWORK MANAGED: router-skills -->

## Skill routing

This repo is the **plugin source**, not a writing vault: it has no `process/active/` layout, so most `pm-*` skills do not apply here. They are for consumer vaults scaffolded by `pm-setup-project`.

| To do this | Use |
|---|---|
| Check which plugin version is loaded | `pm-version` |
| Close out a working session | `pm-close-session` — promotes durable content, logs, sweeps for anything hidden or uncommitted |
| Everything else in this repo | Plain file edits + the release procedure in `1_Project/Process/dev-workflow-and-release.md` |

<!-- END WRITING-COWORK MANAGED: router-skills -->

<!-- =====================================================================
     Everything below is PROJECT-OWNED. The plugin will never touch it.
     Add repo-specific instructions, current focus, or temporary notes.
     ===================================================================== -->
<!-- BEGIN PROJECT-OWNED -->

## Project-specific

*Sections above this line are plugin-managed and are overwritten on plugin sync — put repo-specific instructions here instead.*

- **Active prototype (2026-07-25):** memory management is being prototyped in this repo before being ported to the plugin. If a memory-related setting or file looks unusual, read `1_Project/Documents/memory_gating_test_2026-07-25.md` before changing it — an experiment may be in flight.
- `10_DeveloperSpace/` is Jamie's personal space, excluded from reads via `.claudeignore`. Do not read it.
- **No `writing-cowork:pm-*` / `voice-*` skill runs without asking first (2026-08-11).** This repo is the plugin's own dev vault — those skills are built here for consumer vaults, not meant to operate on the repo itself. `router-skills` above already names the two exceptions (`pm-version`, `pm-close-session`); those two are pre-approved and don't need to ask each time. Every other `pm-*` / `voice-*` skill, even one that looks like an exact match for the request (e.g. "add a task" matching `pm-add-task`), requires a plain-language check with Jamie before it runs — name the skill and what it would do, and wait for a yes. Plain file edits and git operations are unaffected; this is about the packaged skills only.

<!-- END PROJECT-OWNED -->
