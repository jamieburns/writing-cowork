---
name: pm-create-promotion-request
description: >
  This skill should be used when a specialist context (substance, voice,
  reader-review, etc.) asks to "create a promotion request", "hand off this
  artifact to the librarian", "send <file> to inbox/promotion", or any
  variant of producing a properly-formatted inbox/promotion/ cover-note
  and dropping the artifact alongside.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-create-promotion-request

Sender-side counterpart to pm-process-inbox-item. Drops a new artifact
into `<vault>/inbox/promotion/` alongside a cover-note describing it,
where to place it, and who sent it. The librarian later processes the
inbox via pm-process-inbox-item.

## Arguments

- **`<artifact-path>`** (required) — absolute or vault-relative path to
  the artifact being handed off.
- **`--placement=<vault-relative-path>`** (optional) — proposed canonical
  destination. The librarian may override; this is a suggestion.
- **`--from=<context>`** (optional, default `substance`) — the requesting
  context.
- **`--notes=<text>`** (optional) — caveats, dependencies, anything the
  librarian or writer should know.
- **`--vault=<path>`** (optional) — vault root. Default: inferred from
  `<artifact-path>` or current directory.

## Preconditions

1. Resolve vault root.
2. Verify `<vault>/inbox/promotion/` exists.
3. Verify `<artifact-path>` exists and is a regular file.
4. Verify the cover-note destination doesn't collide:
   `<vault>/inbox/promotion/<artifact-basename>_promotion.md` must not
   already exist.

## Execution

1. Determine the artifact destination filename:
   `<vault>/inbox/promotion/<artifact-basename>` (preserve original name).
   If a file by that name already exists in the inbox, append a short
   timestamp suffix.
2. Copy (not move — preserve the source) `<artifact-path>` to the inbox.
3. Write the cover-note at
   `<vault>/inbox/promotion/<artifact-basename>_promotion.md`:

   ```markdown
   # Promotion request

   **From:** <from>
   **Date:** YYYY-MM-DD

   **Artifact:** `<artifact-basename>` (in this dir)
   **Proposed placement:** `<placement-or-defer>`
   **Summary:** <short summary; ask the user if not provided>
   **Notes:** <notes-or-"none">
   ```

   `<placement-or-defer>` is the `--placement=` value if provided,
   otherwise `defer to writer / librarian`.

4. Atomic-write the cover-note.

## Output on success

```
Created promotion request at <vault>/inbox/promotion/:
  Artifact: <artifact-basename>
  Cover-note: <artifact-basename>_promotion.md
  From: <from>
  Proposed placement: <placement-or-defer>

Librarian will process via pm-process-inbox-item on next pass.
```

## Output on failure

- `<vault>/inbox/promotion/ not found; run pm-init-vault or check the path`
- `artifact not found at <path>`
- `cover-note destination already exists; remove or rename first`
- `permission denied writing to inbox/promotion/`

## Standalone use

Specialist contexts call this directly. Useful when the specialist has
produced output (analysis, draft, log) that needs canonical placement but
the specialist isn't authorized to write to canonical paths.
