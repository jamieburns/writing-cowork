# Information Architecture Spine — Design Draft

**Status:** **LOCKED 2026-07-24.** Jamie concurred; resting-state summary lives in `1_Project/Decisions.md` → "Information Architecture Spine (2026-07-24)". The two `[QUESTION]` markers (§4 log length, §8 handoff cleanup) are resolved inline. §6 (memory) remains the **sole open item** — deliberately unsolved, tracked as OPEN. History of markup: Jamie added [CONCURRED] where he agreed and [QUESTION] where he wanted clarity; those questions are now answered.
**Date:** 2026-07-24
**Author:** Claude (Cowork), cloud session, with Jamie
**Scope:** The writing-cowork plugin's records/information architecture — applies to this dev repo **and** every consumer vault the plugin scaffolds. Product content is out of scope by design; this is the process skeleton the product sits inside.

---

## 0. Problem this solves [CONCURRED]

On a long-running project, knowledge that drives the AI's behavior ends up scattered across dozens of files — handoffs, roadmap working-notes, drift reports, memory files — with no single place any given kind of fact is *supposed* to live. The human can't reconstruct **why** the AI did something or **what inputs** it worked from, and every new session re-derives project state by spelunking prior handoffs, which grows without bound as the project ages.

The failure is not "handoffs are bad." It is the absence of two disciplines:

1. **Promotion** — nothing forces durable knowledge *out* of whatever transient doc it was written in and *into* one predictable home.
2. **A why-record** — nothing captures, in one place, what was done, why, and from what inputs.

Handoffs are just the puddle the knowledge collects in because nothing else claims it. Delete handoffs without fixing these two, and the nuggets relocate to the next transient doc.

## 1. Goals (the bar every decision below is measured against) [CONCURRED]

- **Consistent execution across projects** — the same skeleton, homes, and read-contract in every vault.
- **Clarity for both human and AI** — every fact has one predictable home; a single map tells you which.
- **Traceability** — the human can see why the AI did something and what it read to decide.
- **Bounded context** — the set a session must read to be oriented is small and does *not* grow with project age.

---

## 2. The taxonomy — four kinds of record **[CONCURRED]**

Every piece of project knowledge is exactly one of these. The *kind* determines both its home and its update rule. This taxonomy is identical in every vault — that is the consistency lever.

| Kind | Question it answers | Lifecycle rule | Homes |
|------|--------------------|----------------|-------|
| **State** | "What is true *now*?" | Overwrite in place. No history kept inside. Kept small. | `project_hub.md`, `roadmap.md`, `todos.md`, **decisions ledger (new for consumer vaults)**, `file_ownership.md`, `charter.md`, voice docs |
| **Log** | "What happened, *why*, and from what inputs?" | Append-only, chronological. Rolled to `history/` per version. | **one shared activity log (new)** |
| **Queue** | "What's waiting to be routed?" | Process, then archive. | `inbox/*` |
| **Ephemeral** | disposable working aids | Not saved / gitignored / cache. Readable by the immediate next step only; never a source of truth. | session-close handoffs, `drift_reports/`, scratch |

**Reference** (`resources/`, citation ledger, `background/`, and — see §6 — memory) is a read-only sub-case of **State**: durable knowledge the AI works *from*. It is called out separately because "what inputs did the AI use" is half of traceability.

The pattern already exists and is correct in one place: `Decisions.md`'s own rule — *current resting state only, update the row in place, rationale and history live in the versioned detail file*. The whole spine is that rule generalized to every kind.

---

## 3. State documents — the focus **[CONCURRED]**

State docs are the small, canonical set that answers "where does the project stand." Rules:

- **Latest answer only.** A State doc never accumulates history; when something changes, the row/section is overwritten. The prior value's rationale goes to the **Log** (or a versioned detail file), not into the State doc.
- **Small and bounded.** If a State doc grows without limit, it has stopped being State and is leaking Log/Reference content.
- **One home per fact.** No fact lives in two State docs.

**Gap to close:** consumer vaults currently get `charter.md` (operating rules) but **no decisions ledger**. The dev repo has `Decisions.md` and it works well. A consumer-vault decisions ledger (same "current resting state" shape) should ship in the template set.

---

## 4. The activity log **[LOCKED 2026-07-24]**

**[RESOLVED — §4 question]** What keeps it from getting too long: roll at **phase/version close**, not per-subphase (too granular — you'd drown in tiny files). At a phase/version close, that segment archives to `history/` named for the phase/version and the live log starts fresh. Size safety-valve: a numbered continuation if one phase's log runs long. And length never drives context cost — a session reads only the **tail** (last N entries) to orient, so this is file hygiene, not a context concern.

The single missing organ. It is the audit trail and the answer to "why, and from what inputs."

**Decided this session:**
- **One shared log**, not per-role — the roles have interplay and read each other's entries.
- **Every entry is author-stamped** — which role, or the user.
- **Index-first**, not narrative-first — the log's primary reader is the *next session reloading state cheaply*, so entries are terse and scannable, optimized for fast orientation over prose readability.

**Proposed mechanics:**
- **Append-only markdown**, one file, entries newest-last (or newest-first — TBD, see open questions). Rolled to `history/` per version so the live file stays bounded.
- Each entry links to the git commit that carried the change, so the log is the *semantic* layer over git's *mechanical* layer.
- Entry schema (draft):

```
- <YYYY-MM-DD> · <author: role|user> · <action>
  why: <one line>
  inputs: <files / decisions read>
  changed: <files written>  · commit: <hash>
```

- Structured (JSONL/YAML) events with a rendered view are a **later** option once the markdown convention has proven itself and a session-start hook exists to consume them. Not now — that's machinery ahead of a proven shape.

---

## 5. Routing: the hub as manifest + a bounded read-contract **[CONCURRED]**

Three tiers, each small, each read only as far down as needed. Same descent path for human and AI.

**Tier 1 — `CLAUDE.md`: the router, loaded every turn.** Pointers and invariants only, never content — it's in context on *every message*, so it is the most expensive real estate and must stay tiny. It says, in effect: orient via `project_hub.md`; canonical State docs are [list]; the activity log is [path]; for memory read `Memory/INDEX.md` and pull topics on demand; for operation X use skill Y. It changes rarely. Keeping it tiny **is** the context lever — the agent knows where everything is without loading any of it.

**Tier 2 — the two manifests.** `project_hub.md` is the manifest for **State** (current snapshot + the explicit bounded read-set). `Memory/INDEX.md` is the manifest for **Reference/memory**. Both read when relevant, not always.

**Tier 3 — the topic files themselves.** Pulled only when a manifest says they're relevant.

**Bounded read-contract:** the hub names the exact short set a session reads to be oriented — hub, decisions, roadmap, todos, the tail of the log, charter. That set is fixed-size and does not grow with project age, because durable content is promoted into small canonical docs and old log entries roll off. This is what keeps context flat over a multi-month project.

**Skill routing:** with ~60 skills, choosing the right one is itself a search the agent does poorly. A compact "for operation X, use skill Y" map (in the router or a doc it references) cuts that search and makes skill choice *legible* — you can see why a skill was used because the router pointed at it.

---

## 6. Memory management — **[OPEN — not solved]**

This section is deliberately unfinished. We are moving in the right direction but do **not** yet have this managed the best way. Recording the open problem is the point.

### 6a. What we believe is right

Memory is the **Reference** layer of the taxonomy — durable knowledge the AI works from. Two distinct things share the name:

- **Platform memory** — the hidden, session-managed store the environment keeps (the `MEMORY.md` index handed to the agent at session start lives here). Cross-session, but **not** in the vault, **not** in git, **not** visible in Obsidian.
- **Vault memory** — the visible `Memory/*.md` files plus `INDEX.md`. Diffable, git-tracked, controllable. The locked `feedback_visible_memory_only.md` decision already favors this.

Direction we're fairly confident about: make **vault memory authoritative**, wire `Memory/INDEX.md` into the Tier-1 router so the agent finds what it needs without a grand search, and keep the `INDEX.md`-plus-topic-files shape (it's correct — it just isn't wired into an always-on router yet).

### 6b. The core unresolved risk — memory created without consent

**On a long-running project, Claude agents generate new files in the platform memory system without the user's consent, and that hidden store is where unexpected things pile up over time.** The user cannot see this accumulation in Obsidian, did not approve it, and has no natural moment where it surfaces for review. This is the single biggest unsolved problem in this whole design. Everything else here is arrangement; this is a control problem we do not yet have a clean answer for.

### 6c. Open questions (memory) — none of these are decided

1. **Consent on write.** Can memory creation be made consent-gated — the agent proposes a memory, the user approves before it persists — rather than written silently? Is that even controllable from inside a project, or is the platform store going to write regardless?
2. **Suppress or redirect the hidden store.** Can the project make the agent write learned knowledge to *visible vault memory* instead of the platform store? If the platform store still writes on its own, can its content at least be surfaced/mirrored into a place the user reviews?
3. **Audit and cleanup of what's already accumulated.** A long-running project already has a pile in the hidden store. Is there a periodic surfacing ("here is what has accumulated in platform memory — keep / promote to vault / delete") so it stops being a silent junk drawer? Possibly a drift-check-style Attention flag.
4. **The boundary problem.** A "feedback" memory ("always verify agent citations") is really a durable *operating rule* — is that memory, or does it belong with `charter.md`/process rules? A "we decided X" is a *decision*, not a memory. Without a crisp line between **memory / decision / charter-rule**, the memory layer becomes the new scatter. The platform's own typing (*user / feedback / project / reference*) is a starting cut but does not resolve the memory-vs-rule line.
5. **Cross-session trust.** How much should a fresh session trust hidden-store memory it can't show the user the provenance of? (Ties to §4 — the visible log has provenance; hidden memory does not.)

### 6d. What NOT to do yet

Do not build new memory machinery until 6b/6c have answers. The immediate, safe, reversible steps are: (a) the Tier-1 router pointing at visible vault memory, and (b) declaring vault memory authoritative in `charter.md`. Those improve targeting today without committing to a memory model we're not sure of.

---

## 7. Handoff lifecycle — **[DECIDED, see `Decisions.md`]**

Session-close handoffs are **Ephemeral**: fully gitignored, local + iCloud only, readable by the immediate next session but never a source of truth, cleaned up on a confirm-before-delete basis. The load-bearing rule: a kickoff session's **first** job is to promote any durable content into its State home *before* the handoff is discarded. Full decision recorded in `Decisions.md` → "Handoff lifecycle" (2026-07-23); implementation deferred to v0.16.

---

## 8. Enforcement — **[LOCKED 2026-07-24]**

**[RESOLVED — §8 question]** How old handoffs get cleaned up: the handoff is **single-slot**. `pm-close-session` writes *the* handoff; the next kickoff reads it, promotes the durable bits, then deletes it — so at most one live handoff exists at a time. They're gitignored, so deletion is trivial and prunes no git history. A drift-check Attention flag surfaces any straggler older than a short window (a session that closed but was never picked up) for confirm-before-delete. The existing dated pile in `1_Project/Handoff/` gets swept once — keep as frozen history or delete, Jamie's call — and new ones never accumulate.

Folders enforce nothing. The spine rots the moment promote-and-log is skipped. So the real deliverable is a skill, and eventually a hook:

- **`pm-close-session` (skill, build now):** atomically promote durable content → its State home, append one author-stamped Log entry with provenance, write the Ephemeral handoff. This is what makes ephemerality safe and the log reliable.
- **Session-start orientation (convention now, hook later):** read the bounded set + log tail, then state back "here's what I read, the state as I understand it, and what I'm about to do and why" before acting.
- **Session-start/-end hooks (v0.17):** move the above from convention to enforced. Already on the roadmap.

---

## 9. How this maps to the four goals

- **Consistency:** taxonomy + hub-manifest + router shipped identically by templates.
- **Clarity:** one predictable home per fact; the hub says which; the log is the single why-narrative.
- **Traceability:** each log entry = action + rationale + inputs-read + commit. (Memory provenance is the gap — §6.)
- **Bounded context:** fixed read-set that doesn't grow with age; `CLAUDE.md` stays a tiny router; log and history roll per version.

---

## 10. Decisions needed from Jamie

1. **Scope** — additive "impose the spine" (recommended), fuller data-management consolidation, or minimal first-cut on this dev repo only? [concur with imposed spine - Jamie]
2. **Log ordering** — newest-first or newest-last in the live file? [JAMIE - either]
3. **Memory boundary** (§6c-4) — where's the line between memory, decision, and charter-rule? *You own this call.*
4. **Memory consent/control** (§6b, §6c-1/2/3) — the open risk. No action until there's a direction here.
5. **Consumer-vault decisions ledger** — confirm it should ship in the template set (§3). [CONFIRMED]

---

## 11. Status / next steps

This doc is itself the first artifact built the new way: a durable **State** design record, promoted out of a chat conversation before it evaporated. Next, on your red-line: lock the **[PROPOSED]** sections you agree with into `Decisions.md`, then scope `pm-close-session` as the first build.
