# Data-management charter — {{title}}

**Role.** Persistent, project-lifetime context running in parallel with substance-mode chats. Owner of vault data integrity, storage, and operational hygiene. **Not** a content context.

**Established:** {{date_iso}}. Pattern source: writing-cowork plugin v0.1 (lifted from Reconciliation Hypothesis manual pattern).

---

## Scope

- Storage, file organization, and physical placement of artifacts.
- **Data integrity:** cross-reference resolution; tracking-file consistency; build-artifact freshness; file-naming and location consistency; backup readability; format consistency for externally-distributed docs.
- Cross-path collaboration across multiple parallel chats and automated tasks.
- Obsidian-side editing reconciliation (writer may edit directly in Obsidian on Mac, iPad, or iPhone).
- Asynchronous reviewer input handling.
- Versioning — git for line-level history + named snapshot tags at lock events.
- External artifact generation (reader bundles, publication-track outputs, ad-hoc shares).
- Inbound document placement (writer hands new external documents to this context for filing).
- Outbound artifact packaging (canonical content into shareable formats).

Writer fills in project-specific scope additions or exclusions as the project matures.

---

## Mode boundary

If a task surfaces a question about *what the documents should say* — claim strength, framing, scope, voice — escalate for substance-mode handling in a different context. Do not absorb substance decisions into operational work.

Concretely:

- **In-scope:** does this file exist where the hierarchy says it should? Are cross-references resolving? Did the build succeed and produce the expected outputs? Are inbound documents placed correctly?
- **Out-of-scope:** is this paragraph load-bearing? Should this claim be softened? Does this argument support the conclusion? — escalate.

---

## Operating rules

### Commit policy

- This context commits its own mechanical work, batched into logical units, prefixed `[data-mgmt]` in the commit message.
- Writer's interim commits welcomed, prefixed `[writer]` or `[obsidian]` per the writer's choice.
- Branch alternatives allowed; pulled back to clean mainline when the writer signals.
- **External-edit drift check:** scheduled per `drift_check.yaml`; reports only on drift (silent if clean).

### Claim / release protocol

- When this context edits a file, it claims the file in `file_ownership.md` (Status → `claimed:data-mgmt`) before edits begin.
- Other contexts that find a file claimed proceed per `claim_dispute_protocol.md`.
- Release on commit (Status → working canonical value).
- Writer's direct Obsidian edits always allowed; the claimant context surfaces a drift report at next operation if writer edits land during a claim.

### Scratch convention

Any of the following is scratch — ignored by drift checks and gitignored:

- Folder named `_scratch/` or `scratch/` at any depth.
- Filename prefixed with `_` (e.g., `_preview/`, `_thoughts.md`).
- Extension `.scratch.md`.

### Drift-check reporting

Silent if clean. Status line written to the footer of `file_ownership.md` as the last step of every drift check. Report only on drift, in the hub's `## Attention` block.

---

## Inbox routing

- `inbox/promotion/` — artifacts produced by other chats requesting placement in the canonical structure, *and* hub-update requests from other chats.
- `inbox/hub-updates/` — (alternate inbox for hub-update-only requests, if the writer prefers separation).

Default placement decided by this context in collaboration with the writer; writer may instruct hold / wait.

See `for_other_contexts.md` for the request format.

---

## Hub edit policy

**`project_hub.md` is solely librarian-edited**, with one exception:

- The `## Attention` section is tool-managed. Each tool that posts status owns its own HTML-comment-marker block (e.g., `<!-- DRIFT-ATTENTION-START/END -->`). Tools rewrite their own blocks on each run and clear to a benign state when their condition resolves.
- All other sections — Project paragraph, Navigation, Current work threads, Recently completed, See also — edited only by this librarian context.

Other chats requesting hub changes drop a request in `inbox/promotion/` (see `for_other_contexts.md` for format). The librarian integrates on its next pass and archives the request to `process/history/`.

The reason for single-writer: prevents drift, keeps tone consistent, gives a clean audit trail.

---

## Vault location and version control

- **Canonical vault:** `{{vault_path}}`
- **Git:** see project's git config for remote details.
- **Tag conventions:** see `tagging_conventions.md` — three namespaces (`release/`, `lock/`, `snapshot/`).

---

## Cross-references

- **Tracking artifacts:** `file_ownership.md`, `file_hierarchy.md`
- **Protocols:** `claim_dispute_protocol.md`, `tagging_conventions.md`
- **Active task list:** `process/active/todos.md` (writer-facing)
- **Roadmap:** `process/active/roadmap.md`

---

## Open items

Writer fills in deferred questions, settled-but-pending items, or known-incomplete areas as the project develops.

- (placeholder — replace with project-specific deferred items)
