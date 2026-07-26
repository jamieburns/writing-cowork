# Memory Index — {{title}}

Visible, user-manageable memory for this project. **Authoritative** — memory lives here as plain markdown you can read, edit, and delete, not in hidden session-managed storage.

Reached from the repo-root `CLAUDE.md` router. Pull topic files on demand; don't read them all.

**Created:** {{date_iso}} by `pm-init-memory` (writing-cowork {{plugin_version}}).

---

## What belongs here

A **raw observation or correction** — something learned about how this project works, captured so it isn't re-learned next session.

What does *not* belong here (see the routing rule in `process/data_management/charter.md`):

| If it is… | It goes… |
|---|---|
| a repeatable operating procedure | a `process/` doc — memory is the raw log, process is the manual |
| a commitment or choice | the project's decisions record |
| a standing constraint on how work is done | `process/data_management/charter.md` |

When a memory matures into a repeatable procedure, write the process doc and keep the memory file as its origin record.

## File convention

One topic per file, named `<type>_<slug>.md` where type is `feedback`, `project`, or `reference`. Each file opens with frontmatter:

```yaml
---
name: short-name
description: one line — used to judge relevance without opening the file
type: feedback | project | reference
---
```

Then the rule or fact, followed by **Why:** and **How to apply:** lines. Keep each file short enough to read in full.

## Index

(One line per memory file. Add a row when you add a file; this index is how a session decides what to open.)

- *(no memories recorded yet)*

---

## Review

This directory is git-tracked, so an unreviewed memory write shows up in `git status` before it is committed. That is the consent mechanism: review the diff, keep what's right, `git checkout` what isn't. Periodically check that nothing here has gone stale — a memory that contradicts current practice is worse than no memory.
