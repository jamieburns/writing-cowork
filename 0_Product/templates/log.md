# Activity Log — {{title}}

The single **shared, append-only** activity log for this project — the semantic layer over git's mechanical layer. One entry per durable change: what, why, from what inputs, and the commit that carried it.

**Kind:** Log (append-only; never overwrite an entry). One log for the whole project, not one per role — the roles read each other's entries.

**Created:** {{date_iso}} by `pm-init-log` (writing-cowork {{plugin_version}}).

## Conventions

- **Append-only, newest-last.** Sessions orient by reading the *tail*, so the newest work is where the eye lands last and the file reads as a narrative forward in time.
- **Author-stamped** — the role, or `user`, responsible for the change.
- **Index-first** — terse and scannable. The primary reader is the next session reloading state cheaply, not a person reading prose. Optimize for fast orientation over readability.
- **Rolls at phase/version close** to `process/history/`, named for the phase or version, and this live file starts fresh. Size is hygiene, not context cost — sessions read only the tail.
- If one phase runs long, use a numbered continuation rather than letting a single file grow without bound.

## What earns an entry

A durable change: something promoted into a State document, a decision recorded, a milestone moved, an artifact accepted. Not every edit — a typo fix is not a log entry. The test is whether a future session would want to know *why* this happened and *what it was based on*.

## Entry schema

```
- <YYYY-MM-DD> · <author: role|user> · <action>
  why: <one line>
  inputs: <files / decisions read>
  changed: <files written>  · commit: <hash | uncommitted>
```

Fill `commit:` with the real hash once the change is committed. An entry left at `uncommitted` is a signal that durable content is sitting in a working tree where it can evaporate.

---

## Entries

*(none yet — the first entry is usually the project's setup-completion commit)*
