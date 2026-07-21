# Roadmap — {{title}} (now / next / later)

Three-bucket roadmap. Less ceremony than phase-based; better for projects without rigid sequencing. Shape chosen at setup (alternative: phase, see `roadmap_phase.md` template).

**Last updated:** {{date_iso}} (initial scaffold)

---

## How to use

Three buckets:

- **Now** — what's actively in progress this week / sprint / iteration.
- **Next** — committed to soon (next 2–4 weeks-ish), but not started.
- **Later** — on the radar, not committed. May not happen; may be reshuffled.

Add a milestone via `pm-add-milestone --bucket=now|next|later` (MVP Planning sub-skill). Move items between buckets as priorities shift. View via `pm-show-status`.

Items are milestones, not tasks. Granular work lives in `todos.md`. Each milestone has a goal and (optionally) listed gates; close milestones via `pm-update-milestone --status=done`.

---

## Now

(Currently in flight. Aim for 1–3 items; more usually means too much WIP.)

- (none yet — writer / librarian populates as work starts)

---

## Next

(Coming up after the current Now items close.)

- (none yet)

---

## Later

(On the radar. May be reshuffled.)

- (none yet)

---

## Done

(Closed milestones, most recent first. Closed via `pm-update-milestone --status=done`. Optionally tagged with `lock/` when the closure is a substantive decision-lock.)

- (none yet)

---

## See also

- Granular tasks: `todos.md`
- Project hub: `project_hub.md` (current work threads)
- Tagging conventions: `process/data_management/tagging_conventions.md` (for `lock/` tags on milestone closures)
