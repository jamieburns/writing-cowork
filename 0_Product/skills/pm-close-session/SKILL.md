---
name: pm-close-session
description: >
  This skill should be used when the user asks to "close the session",
  "wrap up", "end of session", "close out and hand off", "commit and write
  the handoff", or any variant of ending a working session cleanly. Promotes
  durable content into its State home, appends one author-stamped activity-log
  entry, sweeps for anything hidden or uncommitted, commits, and writes the
  single-slot ephemeral handoff. This is the skill that makes ephemeral
  handoffs safe — durable content is promoted BEFORE the handoff is written.
metadata:
  version: "0.1.0"
  role: pm
  subset: information-architecture
---

# pm-close-session

The enforcement organ of the information architecture. Folders enforce nothing;
this skill is what keeps the spine from rotting.

It exists because the two disciplines the architecture depends on — **promotion**
(durable knowledge leaves the transient doc it was written in) and **the
why-record** (what was done, why, from what inputs) — are exactly the steps a
session skips when it is running out of room. Automating them is the only way
they happen reliably.

## Order of operations — this order, not another

1. **Survey** — find out what actually happened this session.
2. **Promote** — move durable content into its State home.
3. **Sweep** — verify nothing is hidden, stale, or stranded.
4. **Log** — append one author-stamped entry.
5. **Commit** — land it.
6. **Handoff** — write the single-slot baton, last.

The handoff is written **last and only after promotion has committed.**
Ephemerality is safe *because* durable content was promoted first; reverse the
order and the handoff becomes a source of truth again, which is the failure the
whole design targets.

## 1. Survey

Gather, and show the user:

- `git status --porcelain` — modified, staged, untracked.
- `git diff` — **content, not just names.** A filename tells you a file changed;
  only the diff tells you whether a change silently reverted something. This is
  the detector for stale-copy edits and it is not optional.
- The tail of `process/Log.md` — what the last session recorded.
- Anything in `inbox/` still unprocessed.

## 2. Promote

For each piece of durable knowledge produced this session, route it by kind —
the routing rule from `charter.md` §"Knowledge routing":

| Kind | Home |
|---|---|
| repeatable operating procedure | the relevant `process/` doc |
| raw observation or correction | `process/memory/` + a row in `INDEX.md` |
| commitment or choice | the decisions record |
| standing constraint on how work is done | `charter.md` |

One home per fact. If something seems to belong in two, one of them is a
pointer. **Ask when genuinely ambiguous** rather than filing it twice — a
duplicate that drifts is worse than a question.

## 3. Sweep — "is anything hiding?"

Two halves, split by what each layer can actually reach.

**Agent-performed (must happen here):** check the session-managed memory store.
A script cannot reach it — in some runtimes it sits behind a tool only an agent
can call. List it; if it holds anything, review each entry against the vault and
either promote it to `process/memory/` or discard it. Report the disposition.
Do not assume entries are stale duplicates — verify. On this project's own
retirement pass, the assumption would have been wrong: one entry held content
that existed nowhere else.

**Delegated to `pm-run-drift-check`** — do not reimplement these:

| Check | Catches |
|---|---|
| nothing durable uncommitted | a decision lost when a working tree is reverted |
| untracked files that look durable | stray handoffs, orphaned drafts |
| log entries still at `commit: uncommitted` | work recorded but never landed |
| `autoMemoryDirectory` resolves inside this vault | silent path drift after a move or clone |
| managed markers balanced | a half-written sync that would corrupt on next run |

**Red flags block the close by default.** Report them and stop. `--force`
proceeds anyway and records the override in the log entry — an override that
leaves no trace is indistinguishable from the check never running.

## 4. Log

Append **one** entry to `process/Log.md`, newest-last:

```
- <YYYY-MM-DD> · <author: role|user> · <action>
  why: <one line>
  inputs: <files / decisions read>
  changed: <files written>  · commit: <hash>
```

One entry per session, not one per edit. If a session genuinely did two
unrelated things, two entries are fine — but resist narrating every file touch.
The reader is the next session orienting cheaply.

## 5. Commit — and the hash problem

The log entry names the commit that carried the change, but the log is itself a
file that must be committed. That is circular, and `--amend` does not solve it:
amending changes the hash the entry would name.

**Resolution — two commits, deliberately:**

1. Commit the promoted content. Capture its hash `H`.
2. Write the log entry naming `H`. Commit the log as a small second commit.

The log therefore trails the work by one commit. This is correct rather than
elegant: the hash in the entry is real and greppable, which a self-referential
placeholder would not be. Do not try to collapse it into one commit.

Follow the project's own git discipline for how commits are executed — on this
project, mutations run on the host rather than through a mounted view.

## 6. Handoff

Write **the** handoff — single-slot, gitignored, local disk only. Overwrite any
existing one; at most one live handoff exists at a time.

Keep it a **routing note, never a source of truth**: where the next session
should pick up, what was in flight, what to read first. Anything durable should
already be promoted by step 2 — if you find yourself writing durable content
into the handoff, that content belongs in a State home instead, and the promote
step missed it.

The next kickoff session reads it, acts on it, and deletes it.

## Arguments

- **`--dry-run`** — survey, sweep, and report the proposed promotions and log
  entry. Write nothing.
- **`--force`** — proceed despite red flags. The override is recorded in the log.
- **`--no-handoff`** — skip step 6 (work is genuinely finished; nothing to hand off).
- **`--author=<role|user>`** — stamp the log entry. Default: the acting role.

## Output

```
Session close — <project>

Surveyed:   <n> modified, <n> untracked, <n> inbox items
Promoted:   <file> → <home>   (per promotion)
Sweep:      hidden store: <empty | n entries dispositioned>
            drift-check: <clean | n flags>
Logged:     1 entry, author <role>
Committed:  <hash> (content) + <hash> (log)
Handoff:    <path>   (or: skipped)
```

On a red flag, stop after Sweep and report what blocked, with the command to
re-run once fixed.

## Standalone use

Perfectly reasonable mid-session when a natural boundary is reached — a phase
closing, a decision landing. Nothing about it requires the session to be ending;
`--no-handoff` covers that case.

## Related skills

- `pm-run-drift-check` — the delegated verification; this skill invokes it.
- `pm-archive-to-history` — rolls `Log.md` at phase close.
- `pm-process-inbox-item` — clear the inbox before closing if the survey finds items.
