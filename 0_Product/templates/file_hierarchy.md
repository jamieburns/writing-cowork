<!-- =====================================================================
     WRITING-COWORK PLUGIN - MANAGED FILE
     This file is plugin-owned and is REGENERATED on plugin sync.
     Hand edits inside the MANAGED block are lost on the next sync.
     Ownership is recorded in process/data_management/file_ownership.md;
     the marker convention is documented in CLAUDE.md.
     ===================================================================== -->
<!-- BEGIN WRITING-COWORK MANAGED: file-hierarchy -->

# File hierarchy — {{title}}

Navigational map of the project. Layout, structure, and "where to find X" guidance. The librarian-facing exhaustive inventory with status and ownership is in `file_ownership.md`.

**Last updated:** {{date_iso}} (initial scaffold)

---

## Layout

Starter layout produced by `pm-setup-project` on {{date_iso}}. Substantive folders (`research_and_analysis/`, `resources/`, `background/`, `graphics/`, `subprojects/`, `production/`, etc.) are added organically by the writer as the project develops.

```
{{title}}/
│
├── project_hub.md               ← where-am-I navigation document
├── .gitignore
│
├── inbox/
│   ├── promotion/               ← artifacts from other chats requesting placement
│   └── hub-updates/             ← hub-update requests from other chats (optional separation)
│
└── process/
    ├── active/
    │   ├── voice_handoff.md     ← voice/tone briefing
    │   ├── voice_exceptions.md  ← intentional voice-rule exceptions
    │   ├── reviewer_tracking.md ← per-reviewer engagement status
    │   ├── roadmap.md           ← project roadmap
    │   └── todos.md             ← granular task list
    ├── data_management/
    │   ├── charter.md           ← librarian role + operating rules
    │   ├── handoff.md           ← living librarian handoff
    │   ├── for_other_contexts.md ← how non-librarian chats interact
    │   ├── file_hierarchy.md    ← this file
    │   ├── file_ownership.md    ← ownership table + drift footer
    │   ├── claim_dispute_protocol.md ← multi-context claim resolution
    │   ├── tagging_conventions.md ← git tag namespaces + workflows
    │   ├── drift_check.yaml     ← per-project drift-check config
    │   └── drift_reports/       ← per-run drift reports (gitignored)
    └── history/                 ← closed task prompts, batch logs, audits
```

Folders added by the writer as the project matures:

- `research_and_analysis/` — analytical working artifacts (per-step / per-section)
- `resources/` — read-only reference material, cached with provenance (see the resources & citation ledger convention below)
- `background/` — background, history, source lists
- `graphics/` — rendered deliverable graphics
- `subprojects/` — multi-track work (e.g., cover, separate deliverables)
- `production/` — final-deliverable build/output directory (epub, print PDF, Word, etc.). Standard name going forward; full production-pipeline tooling is separately planned (see `Next Version Goals.md`) — this folder convention lands ahead of that tooling.

---

## Navigation by task

| Task | Where |
|------|-------|
| Get project current state | `project_hub.md` |
| See active tasks | `process/active/todos.md` |
| See project roadmap | `process/active/roadmap.md` |
| Understand how the project is run | `process/data_management/charter.md` |
| Look up file ownership / status | `process/data_management/file_ownership.md` |
| Pick up the librarian role in a new chat | `process/data_management/handoff.md` |
| Interact with the librarian (non-librarian chat) | `process/data_management/for_other_contexts.md` |
| Tag a release or lock | `process/data_management/tagging_conventions.md` |
| Resolve a file-claim dispute | `process/data_management/claim_dispute_protocol.md` |

Additional rows added by the writer as project structure develops (e.g., "Brief a reviewer", "Verify a specific finding", "Build deliverables").

---

## Conventions

- Cross-references in markdown typically use bare filenames (`charter.md`) rather than full paths. The folder structure is for navigation; paths given when the reference is in a navigational table or when location is non-obvious.
- Status markers and last-updated dates at the top of each file.
- ISO date format (`YYYY-MM-DD`) throughout.
- **Scratch convention.** Any filename prefixed with `_`, any `_scratch/` or `scratch/` folder at any depth, or any `.scratch.md` file — ignored by drift checks and gitignored.
- **Attention block convention (`project_hub.md` § Attention).** Tools may post status into the hub's Attention section by writing their own HTML-comment-delimited block, e.g., `<!-- TOOL-NAME-START --> ... <!-- TOOL-NAME-END -->`. The tool owns its block — auto-rewrites it on each run and clears to a benign state when its condition resolves. Reference implementation: `drift_check.py` (`<!-- DRIFT-ATTENTION-START/END -->`).
- **Folder-naming consistency across projects.** `research_and_analysis/` and `production/` are the standard names — cross-project consistency is a deliberate design goal of this plugin, not a per-vault style choice. Vaults on the older `analysis/` naming (or ad hoc `BookDeliverables/`-style output folders) are expected to migrate onto the standard names via `pm-sync-project-to-plugin --target=layout`, not to keep the old names indefinitely. That case tags a rollback point (`pm-tag-snapshot`) before moving anything, runs with the vault owner concurrent (not unattended), and rewrites internal cross-references it can find — see the skill's own docs for what it catches automatically vs. what needs manual follow-up. Git history remains the safety net for anything the automated rewrite misses.

*Sections above are plugin-managed and regenerated on sync — record project-specific layout below instead.*

<!-- END   WRITING-COWORK MANAGED: file-hierarchy -->

<!-- BEGIN PROJECT-OWNED -->

## Project-specific layout

(Add folders and navigation notes particular to this project as it develops — `research_and_analysis/`, `resources/`, `graphics/`, `production/`, subprojects, and anything else the writer creates. The plugin never edits below this line.)

<!-- END PROJECT-OWNED -->
