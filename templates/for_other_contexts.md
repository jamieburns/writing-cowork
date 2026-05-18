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

## When in doubt

- Operational, mechanical, or hygiene → librarian.
- "What should this document say?" → writer.
- Anything between → ask the writer; they'll route.

Charter §"Mode boundary" has the full rule.
