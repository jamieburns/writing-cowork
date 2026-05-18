# Roadmap — {{title}} (phase-based)

Phase-based project roadmap. Each phase has a goal, gates that must close before moving on, and a status. Phase shape chosen at setup (alternative: now-next-later, see `roadmap_now_next_later.md` template).

**Last updated:** {{date_iso}} (initial scaffold)

---

## How to use

Each phase is a logical chunk of work with a defined endpoint. Phases close in sequence; the gating check is whether the phase's listed gates have been met.

Add a phase via `pm-add-milestone --phase=<n>` (MVP Planning sub-skill, ships with rest of MVP). Update phase status via `pm-update-milestone --status=planned|in-progress|done`. View the roadmap via `pm-show-roadmap` (phase view) or `pm-show-status` (Now/Next/Later-derived view).

---

## Phases

### Phase 1 — (name)

**Goal:** (one sentence — what does this phase accomplish?)

**Gates:**

- [ ] (gate 1 — concrete, testable)
- [ ] (gate 2)

**Status:** planned

**Notes:** (deferred items, dependencies, open questions)

---

### Phase 2 — (name)

**Goal:**

**Gates:**

- [ ] (gate 1)

**Status:** planned

---

(Add more phases as the project's structure becomes clear. A phase plan emerges; it isn't fully designed upfront.)

---

## Locked phases (closed)

(Phases moved here when their gates are met and they're tagged with a `lock/` tag. Format: phase name + date locked + summary.)

- (none yet)

---

## See also

- Granular tasks: `todos.md`
- Project hub: `project_hub.md` (current work threads)
- Tagging conventions: `process/data_management/tagging_conventions.md` (for `lock/` tags)
