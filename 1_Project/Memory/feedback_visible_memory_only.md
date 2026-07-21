---
name: visible-memory-only
description: "All writing-cowork project memory lives in 1_Project/Memory/ as visible markdown files. No new hidden/session-managed memory files without explicit user consent."
type: feedback
originSessionId: housekeeping-2026-07-21
---

**Rule:** Do not call the hidden session-memory write tool for this project. All memory lives in `1_Project/Memory/` as plain markdown the user can read, edit, and delete directly.

**Why:** The user does not want memories accumulating somewhere they can't inspect or manage. This was raised explicitly during the 2026-07-21 housekeeping pass — prior sessions had written 7 memory files to hidden session storage the user had no visibility into.

**How to apply:**
1. Check `1_Project/Memory/INDEX.md` and the files it links before assuming something isn't recorded.
2. To add a memory: write a new file in `1_Project/Memory/` (or edit an existing one), then update `INDEX.md`.
3. If genuinely uncertain whether something belongs in memory at all, ask the user rather than writing it — this rule exists because unasked-for memory writes were the problem in the first place.
4. `1_Project/Process/` holds polished, current "how we do it" procedures distilled from memory entries — memory is the raw log, Process is the manual. When a memory matures into a repeatable procedure, add/update the Process doc and keep the memory file as its origin record.
