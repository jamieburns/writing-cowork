---
name: pm-init-memory
description: >
  This skill should be used when the user asks to "initialize memory",
  "set up the memory folder", "create the memory index", "add visible
  memory to this vault", or any variant of creating the visible,
  git-tracked project memory directory. Creates `process/memory/` with an
  `INDEX.md` manifest so durable knowledge lives in files the writer can
  read, diff, and delete rather than in hidden session-managed storage.
  Invoked by pm-setup-project; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: information-architecture
---

# pm-init-memory

Create `<vault>/process/memory/` and place `INDEX.md` from
`${CLAUDE_PLUGIN_ROOT}/templates/memory_index.md`.

Memory is the **Reference** layer of the record taxonomy: durable knowledge the
project works *from*, a read-only sub-case of State. `INDEX.md` is a **Tier-2
manifest** — the router points at it, and it points at topic files that are
pulled on demand.

## Why visible memory

Session-managed memory stores sit outside the vault, outside git, and invisible
in Obsidian. In practice they diverge from the vault silently: content written
to one is not seen by the other, stale entries keep being served to new
sessions, and — the failure that motivated this design — a rule written in the
vault to govern memory behaviour was never loaded by the memory system it was
meant to govern.

Putting memory in a **git-tracked directory** makes `git status` the review
surface: an unreviewed write shows up as an uncommitted change, `git diff` is
the review, and `git checkout` is the reject. Consent-on-write becomes
consent-on-commit. This works in every runtime because it depends on git, not
on any runtime's settings.

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--title=<title>`** (optional) — human-readable title; default
  title-cased `<name>`.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/` exists (created by `pm-init-vault`).
3. Verify `<vault-path>/process/memory/INDEX.md` does NOT already exist.
4. Verify `${CLAUDE_PLUGIN_ROOT}/templates/memory_index.md` exists.

## Execution

1. `mkdir -p <vault-path>/process/memory/`.
2. Read `${CLAUDE_PLUGIN_ROOT}/templates/memory_index.md`.
3. Substitute `{{title}}`, `{{date_iso}}`, `{{plugin_version}}` (the `version`
   field from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`).
4. Atomic-write to `<vault-path>/process/memory/INDEX.md` using the Write file
   tool.

The index ships with an empty memory list — a new project has nothing learned
yet, and a pre-populated index would be fiction.

## Output on success

```
Initialized memory at <vault-path>/process/memory/ (INDEX.md)
```

## Output on failure

- `process/ not found at <vault-path>; run pm-init-vault first`
- `memory INDEX.md already exists at <vault-path>/process/memory/INDEX.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/memory_index.md not found in plugin install`

## Standalone use

Retrofitting onto an existing vault is the common standalone case. If that
vault already accumulated knowledge in a session-managed store, reconcile
before or shortly after: read what is in the hidden store, promote anything
worth keeping into `process/memory/` as a topic file, and correct or tombstone
anything stale. Divergence found late is worse than divergence found early —
a stale entry will keep being served to new sessions as though current.

## Related skills

- `pm-install-router` — installs the `CLAUDE.md` that points at this index.
- `pm-install-charter` — the charter carries the knowledge-routing rule that
  decides what belongs here versus in a process doc, decisions record, or the
  charter itself.
