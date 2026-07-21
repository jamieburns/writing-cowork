# For other contexts — how to interact with the librarian (in {{title}})

If you're working in a non-librarian role — substance-execution, voice/tone advisory, reader-review triage, or any future workstream — this doc tells you what to ask the librarian to do, how to hand it work, and what conventions to follow.

If you ARE the librarian, read `handoff.md` instead.

---

## What the librarian does

Owns operational care of the vault:

- File placement, organization, naming, drift
- Versioning operations — stage / commit / push / tag / branch
- Build operations — freshness checks, deliverable packaging
- External artifact generation — reader bundles, release packages, ad-hoc shares
- Inbox routing — surface arrivals, adjudicate placement with writer
- Cross-path collaboration — claim/release across parallel chats

Does **not** make substance decisions. Substance escalates to the writer.

---

## When to ask the librarian

| You want to... | Ask the librarian to... |
|---|---|
| Move or rename a file | "Move `X` to `Y`" — librarian does it, updates ownership table, commits. |
| Run the build | "Run the build" — librarian invokes whatever build pipeline the project has. |
| Commit and push work | "Save point: commit and push as `[<your-context>] <message>`" |
| Tag a release / lock | "Tag this as `release/v1.0-reviewer-r1`" — librarian uses the tagging conventions, attaches artifacts to a GitHub Release. |
| Surface what's stale | "Run the drift check" — librarian runs it ad-hoc and reports. |
| Get the current state | Read `project_hub.md`. |
| Place a new artifact you produced | See "Handing a new file to the librarian" below. |
| Update the hub | See "Updating the project hub" below. |

When in doubt: operational / mechanical / hygiene → librarian. "What should this say?" → writer.

---

## Claiming a file before editing

If you're going to make non-trivial edits to a file, claim it first so parallel work doesn't conflict.

1. In `file_ownership.md`, find the row for the file. Set its Status to `claimed:<your-context>` — for example, `claimed:substance` or `claimed:voice`.
2. Make your edits.
3. On commit, release the claim — Status returns to the canonical value, Owner returns to `data-mgmt`.

If you find a file already claimed by another context, follow `claim_dispute_protocol.md`. Default route is "proceed in scratch, merge later."

Out-of-band edits the writer makes in Obsidian (Mac / iPad / iPhone) override any claim — the librarian surfaces a drift report at next op, and writer adjudicates the merge.

---

## Handing a new file to the librarian for placement

If you produce a new artifact (analysis, draft, log, image) and want it placed in the canonical vault structure:

1. Drop a copy in `inbox/promotion/`.
2. Add a short cover-note markdown file describing what it is, where you think it should go, and any caveats.

Cover-note format:

```markdown
# Promotion request

**From:** <your-context>
**Date:** YYYY-MM-DD

**Artifact:** `<filename(s)>` (in this dir)
**Proposed placement:** `<path>` — but defer to writer / librarian.
**Summary:** <one or two sentences>
**Notes:** <anything the librarian or writer should know — caveats, deps>
```

The librarian surfaces inbox arrivals in the project hub's Attention block (via drift check) and routes them in collaboration with the writer.

---

## Updating the project hub

**The hub is solely librarian-edited** — except for the `## Attention` block, which is tool-managed.

If you want to add or change something in the hub — typically the "Current work threads" or "Recently completed" sections — drop a hub-update request in `inbox/promotion/` (or `inbox/hub-updates/` if the project uses that separation).

Hub-update request format:

```markdown
# Hub update request

**From:** <your-context>
**Date:** YYYY-MM-DD

## Add to "Recently completed"
- **YYYY-MM-DD** — <terse description>

## Update in "Current work threads"
Replace the "<thread-name>" bullet with:
"<new bullet text>"

## Remove from "Current work threads" (if applicable)
"<bullet text to remove>"
```

The librarian integrates on its next pass, then archives the request to `process/history/`.

**Why route through inbox instead of editing the hub directly:** single writer prevents drift, keeps tone consistent, and gives a clean audit trail.

---

## Posting to the Attention block (tool integrations only)

If you're building a tool that needs to surface status on every session entry, you can write your own block into the hub's `## Attention` section, bracketed by HTML comment markers:

```
<!-- YOUR-TOOL-START -->
... your status / alert ...
<!-- YOUR-TOOL-END -->
```

Your tool owns its block: rewrite on each run, clear to a benign state when the condition resolves. The drift check is the reference implementation (`<!-- DRIFT-ATTENTION-START/END -->`).

This is for *tools*, not for chats. A chat updating the hub should go through the inbox flow above.

---

## Commit message prefixes

When committing work, prefix the commit message:

- `[substance]` — substance-execution work
- `[voice]` — voice/tone advisory work
- `[reader-review]` — reader-review triage
- `[writer]` or `[obsidian]` — writer's direct edits
- `[data-mgmt]` — librarian's own mechanical work
- `[promotion]` — inbox-promotion arrivals integrated into canonical structure

---

## Conventions

- **Scratch.** Any filename prefixed with `_`, any `_scratch/` or `scratch/` folder at any depth, or any `.scratch.md` file — ignored by drift checks and gitignored.
- **Dates.** ISO `YYYY-MM-DD` throughout.
- **Cross-references.** Bare filenames typical in prose; full paths when in navigational tables or when location is non-obvious.
- **Tagging.** Three namespaces — `release/`, `lock/`, `snapshot/`. See `tagging_conventions.md`.

---

## Things you can read directly without asking

You don't need the librarian's help to:

- Read any file in the vault.
- See current state: `project_hub.md`.
- See layout: `file_hierarchy.md`.
- See who owns what: `file_ownership.md`.
- See conventions: this file, `charter.md`, `tagging_conventions.md`, `claim_dispute_protocol.md`.

You need the librarian when you want to *change* something operationally.

---

## Two-axis phase model

Some projects run both substance phases (artifact development) and process phases (research, review, voice refinement) in parallel. This creates a two-axis structure:

**Substance phases** (sequential): Phase 1–N focused on content artifact development (outline → first draft → revision → final).

**Process phases** (parallel): Analysis (research, background work), Review (quality gates), Voice (tone and polish).

Why two axes: different people own substance vs. process development, and their timelines don't align. Substance is heavily sequential; process can run alongside or slightly behind.

**Example structure:**

- **Phase 1–3:** Substance work (outline, first draft, revision)
- **Analysis phase:** Parallel to all substance phases (research, contextual findings feed into substance as needed)
- **Review phase:** Phase 3→4 boundary (quality gate before voice work proceeds)
- **Voice phase:** Phase 5 (final tone pass on completed substance)

The Epistemology project uses this model successfully. Your project may adopt a different structure — the point is: you can layer process phases across substance phases instead of strictly serializing everything.

Document your phase structure in `project_hub.md` so all contexts understand the timeline.

---

## Memory-file refresh at role-shift

When a role's memory files (e.g., `voice_handoff.md`, `voice_exceptions.md`) need updating because the person in that role has changed, how do you preserve history while signaling the transition?

**Protocol:**

- **Filename stays stable** (e.g., `voice_handoff.md` is always `voice_handoff.md` — don't rename it)
- **Frontmatter slug changes** (if the writer or voice lead identity changes, update the `name:` field in the file's frontmatter to reflect the new role owner)
- **HTML comments explain transitions** (add a comment like `<!-- Updated by [new role lead] on YYYY-MM-DD: reason for changes -->`)

This preserves git history (file name is constant across commits) while signaling to human readers that a role transition happened. When you inspect the file's git log, you'll see the continuous file, and the HTML comments mark where the handoff occurred.

**Do NOT delete and recreate the file** — that breaks git history and makes it hard to trace evolution. Edit in place, update the slug and metadata, and leave a comment.

---

## Cross-context workflows — promotion inbox pattern

How do roles hand off work to each other operationally?

**Mechanism:** `inbox/promotion/` folder + cover note describing what's being promoted and where it should go.

**What gets promoted:**
- Completed analysis or research (findings, background documentation)
- Review feedback or quality assessment
- Voice-edited sections or tone guidance
- Substance decisions ready for integration

**Who promotes:** the chat that completed the work.

**Who processes:** PM reads the cover note, decides on placement (with writer input if needed), integrates the artifact into the canonical structure, and moves the cover note to `process/history/`.

**Atomic promotion:** one finding or discrete piece of work per promotion request, not a dump of everything. This keeps decisions granular and auditable.

**Example flow:**

1. Analysis chat completes research on a chapter topic
2. Analysis creates `inbox/promotion/analysis-ch3-framing.md` (cover note)
3. Analysis drops the research artifact (markdown, image, spreadsheet) in the same folder
4. PM processes the request: integrates findings into the chapter workspace, updates `project_hub.md` if needed, archives cover note
5. If findings need substance response, PM creates a task in substance chat

---

## Cross-context workflows — lightweight handoff log pattern

Not all handoffs need full artifact promotion. Some projects prefer a lightweight log.

**Alternative mechanism:** `process/active/handoffs.md` as a timestamped log of inter-role coordination.

**Format:** Simple markdown table with columns: Date | From → To | Work Item | Status

**Example:**

```markdown
| Date | Flow | Work Item | Status |
|------|------|-----------|--------|
| 2026-05-20 | Analysis → Substance | Chapter 3 framing review | Complete |
| 2026-05-21 | Substance → Voice | Draft ch3 ready for tone pass | In progress |
| 2026-05-22 | Voice → PM | Tone edits committed, ready to merge | Complete |
```

**When to use:** Quick coordination, fewer artifacts, or when the team prefers a single handoff log over folder-based promotion.

**Reconciliation uses `inbox/promotion/`** for clear artifact routing. **Authority may prefer `handoffs.md`** for lighter overhead. Your charter can specify which pattern fits your project.

---

## Deferred sections

The following sections depend on Part 3 (role clarification) and Part 7 (implementation):

- § "Substance and Analysis Coordination" — depends on Part 3
- § "Chat-Managed Workstream Status Blocks" — depends on Drift implementation (Part 7)
- § "Reader-Bundle Generation Split" — depends on Review skills (Part 7)

These will be added in the next documentation cycle.

---

## When in doubt

- Operational, mechanical, or hygiene → librarian.
- "What should this document say?" → writer.
- Anything between → ask the writer; they'll route.

Charter §"Mode boundary" has the full rule.
