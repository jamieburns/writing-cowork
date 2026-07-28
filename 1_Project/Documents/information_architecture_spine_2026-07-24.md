# Information Architecture Spine — Design Draft

**Status:** Draft for review. Not locked. Sections are marked **[DECIDED]**, **[PROPOSED]**, or **[OPEN]** so you can red-line each independently.  Jamie added [CONCURRED] for where I agree and [QUESTION] where I would like additional clarity or thought
**Date:** 2026-07-24 · **revised 2026-07-26** (memory pass)
**Author:** Claude (Cowork), cloud session, with Jamie
**Scope:** The writing-cowork plugin's records/information architecture — applies to this dev repo **and** every consumer vault the plugin scaffolds. Product content is out of scope by design; this is the process skeleton the product sits inside.

**Revision 2026-07-26 — memory pass.** §6 moved from `[OPEN — not solved]` to `[DECIDED — model; PROTOTYPED — mechanism]`; §5 gained §5a (ownership markers in plugin-managed files); §10 gained items 6–11, the decisions that gate the plugin port. The rest of the document is unchanged from the 2026-07-24 lock.

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

## 4. The activity log **[DECIDED — form; PROPOSED — mechanics]**

[QUESTION] what keeps this from getting to long, do we start a new on at each phase or subphase or something else?

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

### 5a. Ownership markers in plugin-managed files **[PROTOTYPED 2026-07-25]**

Once the plugin writes files into a vault that the user also edits, "who owns this line" becomes a real question — and a silent-overwrite risk on the next sync. Plugin-managed markdown therefore delimits ownership with **block-level HTML comments**:

```
<!-- BEGIN WRITING-COWORK MANAGED: <block-name> -->   plugin-owned, regenerated on sync
<!-- END   WRITING-COWORK MANAGED: <block-name> -->
<!-- BEGIN PROJECT-OWNED --> ... <!-- END PROJECT-OWNED -->
```

Blocks are **named** so a sync can regenerate one without disturbing others, and the opening comment carries provenance (plugin version, block revision, date).

Three properties worth recording, because they shaped the design:

- **Free at runtime.** Block-level HTML comments are stripped before a file enters model context, so markers cost no tokens on a file that loads every turn. (Documented for Claude Code CLI; Cowork behaviour is on the test plan.)
- **Invisible to the agent, therefore insufficient alone.** Because they are stripped, the model never sees "do not edit this." Every managed file must also carry **one short visible line** stating the boundary — otherwise an agent asked to "add something to `CLAUDE.md`" writes into a managed block and loses it on the next sync.
- **Markdown only.** JSON has no comment syntax, so `.claude/settings.json` cannot carry markers; its provenance has to be documented elsewhere. YAML (e.g. `drift_check.yaml`) can. **Which plugin-managed files get markers, and what substitutes for JSON, is open — see §10.**

Port target: a `--target=router` mode on `pm-sync-project-to-plugin`, per the one-mechanism-per-job precedent in `Decisions.md`.

---

## 6. Memory management — **[DECIDED — model; PROTOTYPED — mechanism]**

Was `[OPEN — not solved]` in the 2026-07-24 draft. Researched and prototyped 2026-07-25/26: the **model below is settled**; the **mechanism is under test in this repo** before anything ships to consumer vaults. Detail records: `memory_control_research_2026-07-25.md` (what the platform offers), `memory_management_recommendation_2026-07-25.md` (what to do about it), `memory_prototype_test_plan_2026-07-25.md` (how we know it works).

### 6a. Where memory sits — unchanged from the draft

Memory is the **Reference** layer of §2: durable knowledge the AI works *from*, a read-only sub-case of State. Two things share the name — **platform memory** (session-managed, outside the vault, outside git, invisible in Obsidian) and **vault memory** (`1_Project/Memory/` + `INDEX.md`, diffable and git-tracked). **Vault memory is authoritative**, and `Memory/INDEX.md` is a Tier-2 manifest reached from the §5 router.

### 6b. What we actually found — the stores had already diverged

The 2026-07-24 draft treated silent accumulation as a *future* risk. Inspection on 2026-07-25 found it had **already happened in this repo**, in three distinct ways:

1. **The governing rule was invisible to the mechanism it governed.** `feedback_visible_memory_only.md` — the rule saying "do not write to the hidden store" — existed *only* in the vault, which the platform store never loads. Sessions were handed the platform index without it.
2. **A stale copy actively misinformed a live session.** The platform store's project-state file still claimed v0.1.13 when the truth was v0.1.15, and a session began believing it.
3. **A memory lived only in the platform store** — the release-checklist entry, missed by the 2026-07-21 migration and invisible in Obsidian for four days.

All three are now reconciled. The lesson generalizes well past memory:

> **An instruction only binds if it lives somewhere the governed mechanism actually loads.**

That is the same principle §5's router encodes, reached from the opposite direction — which is why the router and the memory fix are one piece of work, not two.

### 6c. The control model — **git is the consent mechanism**

The unsolved problem in the draft was *consent*: writes happening without approval. The platform ships no "ask before saving." Rather than build one, put memory where an unapproved write **shows up as an uncommitted change**: `git status` is the surfacing the draft asked for, `git diff` is the review, `git checkout` is the reject. Consent-on-write becomes **consent-on-commit** — weaker in theory, available today in every runtime, and it needs no new machinery.

Two corollaries:
- It gates **undirected** agent writes. Work the user explicitly directed does not need the gate.
- It only works if the working tree is otherwise clean. Permanent untracked noise (stray handoffs, scratch) degrades the review surface, which is a second reason the §7 handoff cleanup matters.

### 6d. Runtime independence — the rule with the most reach

Every memory control the platform documents — `autoMemoryEnabled`, `autoMemoryDirectory`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY`, `/memory`, `PreToolUse` hooks — is documented for **Claude Code CLI**. Cowork's memory runs through a different mechanism entirely. Development happens in CLI; **consumer vaults run in Cowork**. Therefore:

> A control built on Claude Code settings or hooks may protect the dev loop and protect **nothing** in the shipped product. A control built on **files plus git** works in both, because it does not depend on the runtime.

Prefer runtime-independent controls; treat settings as belt-and-braces where they happen to bind. **This governs the whole plugin port, not just memory** — it is the strongest architectural constraint this pass produced.

### 6e. What the platform offers (research result, supersedes the draft's open questions 1–3)

- **Disable** — real and documented: `autoMemoryEnabled: false` (user or per-project scope), or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
- **Redirect** — `autoMemoryDirectory` relocates the store; honored only after the workspace-trust dialog.
- **Gate writes** — no dedicated hook. `PreToolUse` can *block*; `PostToolUse` can only *log*. Deliberately **not built**: it depends on two unverified things at once (that Cowork runs hooks, and that matchers catch `mcp__*` calls), and an audit diff gets most of the benefit at none of the risk.
- **Audit** — the store is plain markdown, inspectable via `/memory`. It is **unsurfaced, not hidden**; the missing piece is *proactive periodic surfacing*, i.e. a diff, not a decoder.

Correction to the draft's §6e hypothesis: the "split by kind" idea (cross-project user facts in the platform store, project content in the vault) **was doing no work here** — all seven platform files were project-specific. At *project* scope the platform store has no legitimate resident. The split may still hold at *user* scope; it is not load-bearing for this design.

### 6f. Ownership markers — see §5

Memory work drove the plugin-managed vs. project-owned marker convention, but it applies to every file the plugin writes, so it is recorded in §5 rather than here.

### 6g. First live evidence (2026-07-26)

Given a durable correction ("always run `claude plugin validate .` before committing a version bump"), a session routed it to **`Process/dev-workflow-and-release.md` plus an activity-log entry** — not to either memory store. The knowledge landed in two git-visible files and zero invisible ones. The model works; it also shows the routing instinct is *Process*, not *Memory*, which sharpens the open boundary question below rather than settling it.

### 6h. What remains open

1. ~~**The boundary — memory vs. decision vs. charter-rule vs. Process doc.**~~ **RESOLVED 2026-07-26** (Jamie confirmed). Every durable fact has one home, by kind: repeatable **operating procedure** → the relevant `process/` doc; raw **observation or correction** → `process/memory/`; **commitment or choice** → the decisions record; **standing constraint** on how work is done → `charter.md`. Memory is the raw log, a process doc is the manual; when a memory matures into a procedure, write the doc and keep the memory as its origin record rather than duplicating. Full statement in `Decisions.md` → "Knowledge routing rule"; shipped in `templates/charter.md` and the router's `router-orientation` block.
2. **Default model for consumer vaults** — disable the platform store outright, or redirect it into the vault. Pending the gating test.
3. **Fate of the platform store** — leave it as a reconciled, banner-carrying mirror, or empty it?
4. **Trust in unprovenanced memory** (draft question 5) — partly improved: writes now carry a `modified` timestamp, so there is a recency signal, but still no why/inputs provenance of the kind §4's log gives. Revisit once the log is real.

### 6i. Prototype status

Running in this dev repo (commits `953e588`, `c39f04d`): stores reconciled, §5 router in place, memory settings armed, test plan written. **Not yet ported.** Port only after the Tier-1 results are recorded and 6h-1 is decided.

## 7. Handoff lifecycle — **[DECIDED, see `Decisions.md`]**

Session-close handoffs are **Ephemeral**: fully gitignored, local + iCloud only, readable by the immediate next session but never a source of truth, cleaned up on a confirm-before-delete basis. The load-bearing rule: a kickoff session's **first** job is to promote any durable content into its State home *before* the handoff is discarded. Full decision recorded in `Decisions.md` → "Handoff lifecycle" (2026-07-23); implementation deferred to v0.16.

---

## 8. Enforcement — **[SPECIFIED 2026-07-27 — `pm-close-session` written]**

The earlier open question about cleaning up old handoffs is resolved: **single-slot**, gitignored. `pm-close-session` writes *the* handoff; the next kickoff reads it, promotes the durable bits, then deletes it. At most one live handoff exists at a time.

Folders enforce nothing. The spine rots the moment promote-and-log is skipped. So the real deliverable is a skill, and eventually a hook:

- **`pm-close-session` (skill, written 2026-07-27):** six steps in a fixed order — survey (including `git diff` *content*, not just status), promote durable content to its State home, sweep, append one author-stamped Log entry, commit, and write the handoff **last**. The order is load-bearing: the handoff is only written after promotion has committed, because ephemerality is safe *only* if durable content left first.

  The **sweep** is split by what each layer can reach. The session-managed memory store is checked by the skill itself — in some runtimes it sits behind a tool no script can call. Everything else (uncommitted durable content, stray untracked files, log entries stuck at `commit: uncommitted`, `autoMemoryDirectory` drift, unbalanced managed markers) delegates to `pm-run-drift-check` under a new `session_hygiene:` config block, so there is one implementation rather than two that can diverge.

  Red flags **block the close** by default; `--force` overrides and records the override in the log entry, since an override that leaves no trace is indistinguishable from the check never running.

  One wrinkle worth knowing: the log entry names the commit that carried the change, but the log is itself committed — and `--amend` cannot resolve that, since amending changes the hash the entry would name. Resolution is **two commits**: content first, then the log entry naming that hash. The log trails the work by one commit. Correct rather than elegant, but the hash is real and greppable.
- **Session-start orientation (convention now, hook later):** read the bounded set + log tail, then state back "here's what I read, the state as I understand it, and what I'm about to do and why" before acting.
- ~~**Session-start/-end hooks (v0.17)**~~ — **dropped 2026-07-27.** Claude Code hooks do not run in Cowork, and consumer vaults run in Cowork. Enforcement moved to a **git `post-commit` hook** (`pm-install-git-hooks`), which runs on the host in every runtime and fires at the moment consent actually happens — the commit. Orientation stays with the router plus the hub's Attention block; a periodic scheduled drift check is the third layer. Full record in `Decisions.md` → "Claude Code hooks — dropped entirely".

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
3. ~~**Memory boundary**~~ → **still open, now the critical path.** See item 6 below.
4. ~~**Memory consent/control**~~ → **RESOLVED 2026-07-25.** Model settled (§6c: git is the consent mechanism); mechanism prototyped and under test. No longer blocking.
5. **Consumer-vault decisions ledger** — confirm it should ship in the template set (§3). [CONFIRMED]

### Open before the plugin port (added 2026-07-25/26)

These are the decisions that gate stage 3 — porting the spine into `0_Product/` templates and skills. Ordered by how much else depends on them.

6. ~~**The routing boundary**~~ — **CONFIRMED 2026-07-26.** *Operating procedure → Process, raw observation → Memory, commitment → Decisions, standing constraint → charter.* Locked in `Decisions.md`, shipped in `templates/charter.md` §"Knowledge routing" and the router's `router-orientation` block. The port is unblocked; first slice landed (router + memory scaffold + orchestration wiring). Items 7–11 remain and gate the *remaining* slices, not the whole port.
7. **Default memory model for consumer vaults** — disable the platform store (Option A) or redirect it into the vault (Option B)? Pending the Tier-1 gating result. If neither setting binds Cowork, the answer is forced: router + discipline + audit diff, and the plugin must not promise settings-based control.
8. **Path portability.** `autoMemoryDirectory` currently holds a machine-specific absolute path in a **git-tracked** file. Fine for the prototype, disqualifying for a shipped template. Choose: gitignored `settings.local.json` (per-machine, not shared) or computed at install time by the sync skill.
9. **Marker coverage** (§5a) — which plugin-managed files get ownership markers? `CLAUDE.md` only, or also `charter.md`, `project_hub.md`, `file_hierarchy.md`, `drift_check.yaml`? And what substitutes for markers in JSON?
10. **Activity-log location and ordering** (§4) — `1_Project/Log.md` and newest-last were bootstrapped provisionally on 2026-07-26, ahead of the v0.16 build. Confirm or revise before the template ships, since consumer vaults will inherit whatever is chosen.
11. **Fate of the platform store** (§6h-3) — leave it as a reconciled, banner-carrying mirror, or empty it?

---

## 11. Status / next steps

This doc is itself the first artifact built the new way: a durable **State** design record, promoted out of a chat conversation before it evaporated.

**Where things stand (2026-07-26):** §6 has moved from `[OPEN — not solved]` to `[DECIDED — model; PROTOTYPED — mechanism]`, §5 gained the ownership-marker convention (§5a), and the prototype is running in this repo at commits `953e588` / `c39f04d`. The §4 activity log has been bootstrapped early as `1_Project/Log.md`.

**Next:** record the Tier-1 test results, decide §10 items 6–8, then port to `0_Product/`. `pm-close-session` (§8) remains the first build after that.
