---
name: pm-init-roadmap
description: >
  This skill should be used when the user asks to "initialize the roadmap",
  "create the project roadmap", "set up roadmap.md", or any variant of
  creating the writing-cowork roadmap document. Supports two shapes:
  phase-based (the Reconciliation pattern) and now-next-later (lighter,
  for newer projects). Invoked by pm-setup-project; also usable standalone.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-init-roadmap

Create the project roadmap at `<vault>/process/active/roadmap.md`. Two
shapes are supported via `--shape`:

- **`phase`** — phase-based milestones with explicit gates (the
  Reconciliation pattern). Use for projects with distinct phases that
  must close in sequence.
- **`now-next-later`** — three-bucket view of work (Now / Next / Later).
  Use for lighter projects where phase discipline would be overkill.

The shape is fixed at setup; switching shapes later means rewriting the
roadmap manually (or via a future `pm-convert-roadmap-shape` skill not in
v1 scope).

## Arguments

- **`<vault-path>`** (required) — absolute path to the vault.
- **`<name>`** (required) — project slug.
- **`--shape=<phase|now-next-later>`** (optional, default `now-next-later`)
  — roadmap shape. Choose `phase` if the project's structure justifies it.
- **`--title=<title>`** (optional) — human-readable title.

## Preconditions

1. Verify `<vault-path>` exists and is a directory.
2. Verify `<vault-path>/process/active/` exists.
3. Verify `<vault-path>/process/active/roadmap.md` does NOT already exist.
4. Verify the appropriate template exists:
   - `--shape=phase` → `templates/roadmap_phase.md`
   - `--shape=now-next-later` → `templates/roadmap_now_next_later.md`

## Execution

1. Read the shape-appropriate template.
2. Substitute `{{name}}`, `{{title}}`, `{{date_iso}}`, `{{vault_path}}`.
3. Atomic-write to `<vault-path>/process/active/roadmap.md`.

The two templates differ in initial structure; both include a header,
explanation of how to use the roadmap, and an empty starter section ready
for `pm-add-milestone` to append into.

## Output on success

```
Initialized roadmap.md at <vault-path>/process/active/roadmap.md
  Shape: <phase | now-next-later>
```

## Output on failure

- `process/active directory missing; run pm-init-vault first`
- `roadmap.md already exists at <path>; remove it first or skip this step`
- `templates/roadmap_<shape>.md not found in plugin install`
- `invalid --shape value: <value>. Accepted: phase, now-next-later`

## Standalone use

Same preconditions. Useful for adding a roadmap to a project that was set
up without one.
