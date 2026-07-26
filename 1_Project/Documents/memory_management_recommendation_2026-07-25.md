# Memory Management — Recommendation for Prototyping in This Repo

**Status:** Recommendation for Jamie's review. Nothing executed. Not a decision.
**Date:** 2026-07-25
**Author:** Claude (Cowork), with Jamie
**Inputs:** `information_architecture_spine_2026-07-24.md` §6/§6e, `Decisions.md`, research findings 2026-07-25, plus live inspection of this repo's two memory stores.
**Follows:** the §6e research task (now complete).

---

## 0. The plan, as I understand it

Three stages, with a review gate between each. We are at the end of stage 1.

1. **Recommend** (this document) — take the research and propose how to apply it *to this repo specifically*. You review and red-line.
2. **Execute + test in this repo** — `writing-cowork` the dev repo is the prototyping ground. Real changes, real verification, in a repo where breakage is cheap and observable.
3. **Port to the plugin** — once the approach is proven here, generalize it into `0_Product/` (templates, skills, drift-check) so consumer vaults get it via `pm-setup-project`.

The reason this ordering is right: the single biggest unknown is whether the platform's memory controls even *apply* in Cowork, and that can only be settled by trying it somewhere real. Prototyping in the dev repo answers it before it's baked into the product other vaults depend on.

---

## 1. What I found — the two stores have already diverged, live, in this repo

This is the most useful result of the pass, and it is empirical rather than theoretical.

**Platform store** (via `project_memory_read`) — 7 content files + `MEMORY.md`.
**Vault store** (`1_Project/Memory/`) — 8 content files + `INDEX.md`.

They overlap on 5 files and disagree on the rest:

| File | Platform | Vault | Note |
|---|:--:|:--:|---|
| `feedback_sandbox_host_lanes.md` | ✅ | ✅ | vault copy has a 2026-07-21 addendum the platform copy lacks |
| `feedback_self_contained_quit_scripts.md` | ✅ | ✅ | |
| `feedback_verify_agent_citations.md` | ✅ | ✅ | |
| `feedback_workarounds_warrant_doc_check.md` | ✅ | ✅ | |
| `reference_personal_plugin_marketplace.md` | ✅ | ✅ | |
| `feedback_release_includes_version_in_description.md` | ✅ | ❌ | platform-only |
| `project_writing_cowork_v013_state.md` | ✅ | renamed `_HISTORICAL` | **stale in platform store** |
| `feedback_visible_memory_only.md` | ❌ | ✅ | **the governing rule — vault-only** |
| `feedback_no_sync_capability.md` | ❌ | ✅ | vault-only, and cited by `Decisions.md` |

### The three failures this demonstrates

**(a) The rule is invisible to the mechanism it governs.** `feedback_visible_memory_only.md` says, in as many words, *"Do not call the hidden session-memory write tool for this project."* It exists **only in the vault**. At the start of this session I was handed the platform `MEMORY.md` index, which does not contain it. The rule intended to control memory behavior lives in the one place the memory system never loads. That is a structural failure, not an obedience failure — and it is the cleanest possible confirmation of §6e's claim that a guideline only binds if it sits somewhere always-loaded.

**(b) The stale copy actively misinformed me.** The platform store's `project_writing_cowork_v013_state.md` says the plugin is at v0.1.13. The vault correctly renamed its copy to `_HISTORICAL` and annotated it as superseded; `Decisions.md` records v0.1.14 released and a v0.1.15 restructure. I began this session having been told v0.1.13 as apparently-current fact. The vault store got curated on 2026-07-21; the platform store did not, and nothing reconciled them. **Divergence is not a hypothetical future risk here — it already produced a wrong belief in a live session.**

**(c) Curation only happened on the side nobody reads first.** All vault files carry near-identical 2026-07-21 mtimes — one migration batch, untouched since. The platform store meanwhile stayed live. So the 2026-07-21 "visible memory only" decision produced a *snapshot copy* into the vault, while the actual writing continued into the platform store. Exactly the §6e prediction: the guideline lowered the rate, it did not close the hole.

### One thing I checked before overclaiming

I was going to say the platform-only `feedback_release_includes_version_in_description.md` represents knowledge that exists nowhere else. **That's wrong** — its content is fully captured in `1_Project/Process/dev-workflow-and-release.md` §"Release checklist". So: no unique irreplaceable knowledge is trapped in the platform store. The problem is *duplication that can drift*, plus the stale file, plus the missing rule — not data loss. Worth stating precisely, because it changes the urgency (this is a correctness-and-control problem, not a recovery problem).

### Two structural gaps, also confirmed

- **There is no `CLAUDE.md` at the repo root.** The spine's §5 Tier-1 router does not exist yet. This is the direct cause of failure (a).
- **`.claude/settings.json` contains only `enabledPlugins`.** No memory-related setting is set. Auto memory is on by default, so nothing is currently restraining it.

---

## 2. What this changes about the spine's assumptions

**§6e's "split by kind" hypothesis needs adjusting.** It proposed durable *cross-project user facts* live in the platform store (where auto-load earns its keep), and project-specific content lives in the vault. But inspecting the actual contents: **all 7 platform files are project-specific `writing-cowork` content.** Zero cross-project user facts. The platform store is not being used for the thing it's good at — it's serving as a redundant, drifting mirror of vault memory. So for this project the split isn't "divide the contents"; it's closer to "**the platform store has no legitimate resident here and should be near-empty.**" The split-by-kind idea may still be right at the *user* scope; it isn't doing any work at the *project* scope.

**§6b's "hidden / invisible" framing is half right.** In Claude Code CLI the store is plain markdown one `/memory` command away — inspectable, just not *proactively surfaced*. The accurate problem statement is "unsurfaced and unreconciled," not "hidden." That matters because it makes the fix smaller: you need a *diff*, not a *decoder*.

**The most important new constraint: controls that work in the CLI may not exist in Cowork.** Everything the research found — `autoMemoryEnabled`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY`, `autoMemoryDirectory`, `/memory`, `PreToolUse` hooks — is documented for **Claude Code CLI**. This session's memory runs through `mcp__remote-devices__project_memory_read/write`, an MCP tool on the desktop bridge. Whether CLI settings bind it is **unverified**. And note that a `PreToolUse` hook matched on `Write|Edit` would *not* catch an MCP tool call at all — it would need to match `mcp__remote-devices__project_memory_write` — assuming Cowork runs hooks, which is itself unverified.

**This drives the central design conclusion:**

> You develop in Claude Code CLI and run in Cowork. Consumer vaults run in **Cowork**. So a control built on Claude Code settings or hooks may protect your dev loop and protect nothing in the product. A control built on **files plus git** works in both runtimes, because it doesn't depend on the runtime at all.

Design for the runtime-independent control first; treat CLI settings as a bonus belt-and-braces layer where they happen to apply.

---

## 3. Recommendation

### The core move: make git the consent mechanism

The unsolved problem in §6b is *consent* — writes happening without approval. There is no built-in "ask before saving." But you already run a review-before-commit discipline on everything else in this repo, and you're a retired engineer with decades of muscle memory for exactly that loop.

So: **put memory where an unapproved write shows up as an uncommitted change.** `git status` becomes the surfacing mechanism 6c-3 asks for; `git diff` becomes the review; `git checkout` becomes the reject. Consent-on-write becomes consent-on-commit — which is weaker in theory (the write already landed on disk) but is *actually achievable today, in both runtimes, with zero new machinery*. That trade is the whole recommendation.

### Three options for how to get there

**Option A — Disable platform memory; vault is the only store.**
Set `autoMemoryEnabled: false`; all memory written by hand to `1_Project/Memory/`, router points at `INDEX.md`.
*Pros:* maximum control, single store, no divergence possible, conceptually clean.
*Cons:* loses auto-load entirely (the one genuine advantage §6e identified) — memory only loads if the router routes to it; depends on a CLI setting that may not bind Cowork; relies on the agent choosing to write to the vault, which is the discipline that already failed once here.

**Option B — Redirect the platform store into the vault (recommended).**
Point `autoMemoryDirectory` at `1_Project/Memory/` so the auto-memory mechanism writes *into the git-tracked, Obsidian-visible directory*. One store, not two.
*Pros:* keeps auto-load; divergence becomes structurally impossible (there's only one pile); every unconsented write appears in `git status` for review; works with the grain of the mechanism instead of fighting it; and it fixes the actual observed failure (drift) rather than the imagined one (invisibility).
*Cons:* writes are still unconsented at the moment they happen — you review after, not before; `MEMORY.md` vs your existing `INDEX.md` is a naming collision that needs resolving; the agent will rewrite files you hand-curated; the per-project setting is only honored after accepting the workspace-trust dialog; **and if Cowork ignores `autoMemoryDirectory`, this fails silently into a worse state than A** (you believe it's redirected; it isn't).

**Option C — Keep both stores, add reconciliation tooling.**
A drift-check step that diffs the two and flags divergence.
*Pros:* no reliance on unverified settings; works regardless of runtime.
*Cons:* institutionalizes the two-pile problem instead of fixing it; most ongoing work; you'd be maintaining a sync you didn't want.

**My recommendation: B, with A as the fallback, and C's diff kept as the audit layer either way.** B is the only option that makes divergence structurally impossible rather than merely detected-and-corrected. But B is entirely contingent on a setting whose Cowork behavior is unknown — which is why the first thing to do is not to choose, but to test.

### The gating experiment (do this before choosing)

**Does a `.claude/settings.json` memory setting bind Cowork's `project_memory_write` tool at all?**

Everything downstream branches on this one answer, and it takes one session to settle:

1. Set `autoMemoryEnabled: false` in `.claude/settings.json`.
2. Start a fresh Cowork session in this repo. Check whether a platform `MEMORY.md` index is still injected at session start, and whether `project_memory_read` still returns content.
3. Deliberately provoke a memory-worthy moment (correct me on something durable) and see whether a write lands.

- **Binds** → Option B is viable; proceed to test `autoMemoryDirectory` redirection.
- **Doesn't bind** → Cowork has diverged again (consistent with the marketplace-cache and `extraKnownMarketplaces` precedents already in `Decisions.md`). Fall back to Option A's discipline *plus* C's diff, and record the divergence as a plugin-level constraint — because it means **no consumer vault can rely on settings-based memory control either.** That is a load-bearing finding for stage 3.

Either outcome is a real result. There is no wasted branch here.

---

## 4. Proposed execution sequence for the prototype

Ordered so each step is independently useful and reversible, and so nothing depends on an unverified assumption before it's verified.

**Step 0 — Reconcile the two stores (do first, regardless of option chosen).**
You cannot prototype control over a store whose current contents are unreconciled. Concretely: fix the stale `project_writing_cowork_v013_state.md` (it's telling every new session the wrong version); decide whether `feedback_release_includes_version_in_description.md` should exist as a memory at all given its content already lives in `Process/dev-workflow-and-release.md`; and get `feedback_visible_memory_only.md` into whatever store is actually loaded at session start. Low risk, immediate value, and it stops the active misinformation today.

**Step 1 — Write the Tier-1 `CLAUDE.md` router.**
This is the fix for failure (a) and it's already a locked spine decision (§5), so it costs no new decision. Memory is its first payload: point at the authoritative memory location and state the write rule. Tiny — pointers and invariants only. **This step is worth doing even if every other step fails**, because it's the piece that puts the rule where the agent actually reads it, and it's runtime-independent.

**Step 2 — Run the gating experiment** (§3 above). Record the result in `Decisions.md` either way.

**Step 3 — Apply the chosen option** (B if the setting binds, A if not), including resolving the `MEMORY.md`/`INDEX.md` naming collision if B.

**Step 4 — Add the audit diff.**
A drift-check step that compares the platform store against the vault and raises an Attention flag on divergence — the "periodic surfacing" the research confirmed is *not* built in. Under B this should almost always be a no-op, which is precisely what makes it a good alarm: it fires only when the model you chose has stopped holding.

**Step 5 — Live with it for a few sessions before porting.** The failure mode this whole exercise targets is *slow accumulation over months*. A control that looks fine on day one and quietly stops binding on day thirty is the exact thing you're trying to catch, and you can't detect that from a single test session.

### One thing I'd explicitly *not* do yet

Don't build a `PreToolUse` consent-gate hook. It's the most technically interesting answer to 6c-1, but it depends on two unverified things at once (that Cowork runs hooks, and that hook matchers catch MCP tool calls), and Step 4's diff gets you most of the practical benefit with none of that risk. Revisit it only if the diff proves insufficient in practice.

---

## 5. What ports to the plugin later (stage 3)

Flagging now because it should shape how stage 2 is built, not be retrofitted after:

- **`CLAUDE.md` router → a template**, with the memory rule as standard content. Highest-value, lowest-risk port.
- **Memory-store audit → a drift-check rule** in the existing `drift_check.yaml` mechanism. Slots into infrastructure that already exists.
- **The chosen memory model → `pm-setup-project`**, so new vaults are born with it rather than migrated onto it.
- **The Cowork-vs-CLI finding → a documented constraint.** If settings don't bind Cowork, every consumer vault is in that boat, and the plugin must not ship advice premised on a control that doesn't work there.
- **Per the existing skill-consolidation precedent in `Decisions.md`** (`pm-migrate-to-shared-tool` → `pm-sync-project-to-plugin`): memory-layout migration for existing vaults should be a `--target=memory` mode on `pm-sync-project-to-plugin`, **not** a new sibling skill.

---

## 6. Facts / assumptions / uncertainties

**Facts — verified this session by direct inspection:**
- The two stores exist and diverge exactly as tabulated in §1.
- `feedback_visible_memory_only.md` (the governing rule) is vault-only.
- The platform store's project-state file is stale and was served to me at session start.
- No `CLAUDE.md` exists at repo root; `.claude/settings.json` contains only `enabledPlugins`.
- The platform-only release-checklist content is duplicated in `Process/dev-workflow-and-release.md` — nothing unique is trapped.
- CLI docs document `autoMemoryEnabled`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY`, `autoMemoryDirectory`, `/memory`, and `PreToolUse` blocking.

**Assumptions — reasonable, not verified:**
- The platform store is project-scoped (implied by the tool name and by its contents matching this repo).
- Vault files sharing a 2026-07-21 mtime indicates one migration batch rather than coincidence.

**Uncertainties — genuinely unknown, and the plan is built to resolve rather than assume them:**
- Whether *any* `.claude/settings.json` memory setting binds Cowork's MCP memory tool. **The gating experiment.**
- Whether `autoMemoryDirectory` works in Cowork specifically — Option B lives or dies here.
- Whether Cowork runs hooks at all, and whether hook matchers catch `mcp__*` tool calls.
- Whether `feedback_release_includes_version_in_description.md` was written *after* the 2026-07-21 rule (rule ignored) or *before* and missed in migration (migration incomplete). Can't distinguish from available evidence; both indict the mechanism, differently.
