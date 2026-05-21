---
name: pm-escalate-issue
description: >
  This skill should be used when the librarian asks to "escalate an
  issue", "file this as a GitHub issue", "send <issue-file> to the
  writing-cowork repo", or any variant of taking a cover-note from
  inbox/issues/ and creating a corresponding GitHub Issue on the
  writing-cowork plugin repository. Librarian-side counterpart to
  pm-create-issue-report. Uses the `gh` CLI and existing gh auth.
metadata:
  version: "0.1.0"
  role: pm
  subset: mvp-foundation
---

# pm-escalate-issue

Read an issue-report cover-note from `<vault>/inbox/issues/`, create a
GitHub Issue on the writing-cowork plugin repository, append the
returned issue URL back to the cover-note, then archive the cover-note
to `<vault>/process/history/`.

This is the librarian's promote-to-GitHub action. Issues that the
librarian decides to handle in-vault (no plugin-level component) should
NOT use this skill; they're archived to history directly via
pm-archive-to-history with a brief disposition note.

## Arguments

- **`<issue-file>`** (required) — path to a cover-note in
  `<vault>/inbox/issues/`. May be absolute or vault-relative.
- **`--repo=<owner/repo>`** (optional, default
  `jamieburns/writing-cowork`) — the GitHub repo to file against. Most
  issues go to the plugin repo; vault-specific ones with an external
  source could go elsewhere.
- **`--label=<label>`** (optional, repeatable) — additional labels
  beyond the auto-derived ones (`severity:<level>`, `from-vault`).
- **`--dry-run`** (optional, flag) — assemble the `gh issue create`
  command and print it without running. Useful for previewing the body.
- **`--vault=<path>`** (optional) — vault root. Default: inferred from
  the issue-file path.

## Preconditions

1. Verify `gh` is available on PATH (`which gh`). If not, abort with
   `gh CLI not found; install it from https://cli.github.com/`.
2. Verify gh authentication: `gh auth status` should report a logged-in
   account. If not, abort with `gh not authenticated; run gh auth login`.
3. Verify the cover-note exists at `<issue-file>` and parses as the
   expected schema (frontmatter-style key/value lines plus a markdown
   body).
4. Refuse to escalate if the cover-note has `Scope: vault` — log a
   message saying the issue should be handled locally via
   pm-archive-to-history, not escalated. The user can override by
   manually editing the cover-note's Scope before re-invoking.
5. Generate the issue title and body (see Execution).

## Execution

1. Parse the cover-note. Extract:
   - Title (the H1 heading or the `## <title>` heading depending on
     where the meaningful title lives — pm-create-issue-report puts it
     in `## <title>` under the `# Issue report` header)
   - Description (the body following the title heading)
   - Metadata: From, Date, Severity, Scope, Plugin version
2. Compose the GitHub Issue body:

   ```markdown
   **Observed in vault:** <vault-name>
   **Plugin version:** <X.Y.Z>
   **Severity:** <severity>
   **Requester context:** <from>
   **Date observed:** <date>

   ## Description

   <description-from-cover-note>

   ---

   *Filed via pm-escalate-issue from a writing-cowork vault.*
   ```

3. Compose labels: `severity:<low|medium|high>`, `from-vault`, plus any
   `--label` values supplied.
4. If `--dry-run`, print the assembled `gh issue create` command and
   stop. Otherwise:
5. Run `gh issue create --repo <repo> --title "<title>" --body "<body>"
   --label "<labels>"`. Capture stdout (the issue URL).
6. Append the issue URL back to the cover-note as a new last-line
   metadata entry: `**Escalated:** <URL>`.
7. Archive the cover-note to `<vault>/process/history/` via
   pm-archive-to-history (with date prefix preserved). The archived
   file name retains the original slug so it's still findable.

## Output on success

```
Escalated issue to <repo>:
  Title:        <title>
  URL:          <returned-issue-url>
  Labels:       <labels-list>
  Archived to:  <vault>/process/history/<archived-name>

The cover-note's local copy was updated with the issue URL before
archiving, so the link from vault to GitHub is recorded.
```

## Output on failure

- `gh CLI not found; install it from https://cli.github.com/`
- `gh not authenticated; run gh auth login`
- `<issue-file> not found`
- `cover-note has Scope: vault; this is not a plugin-level issue. Handle locally via pm-archive-to-history with a disposition note, or update Scope to plugin and re-invoke.`
- `gh issue create failed: <stderr from gh>`
- `permission denied archiving cover-note to process/history/`

If `gh issue create` succeeds but the post-archive step fails, the
issue URL is still printed and the cover-note is updated in-place —
the archive step can be retried manually.

## Standalone use

The librarian invokes this directly after reviewing an
`inbox/issues/<file>` and deciding it's plugin-scope. The skill is
idempotent in the dry-run sense (re-running --dry-run is fine), but
once `gh issue create` runs successfully the issue exists in GitHub
and cannot be un-filed (only closed). Use --dry-run first if unsure.

## Why this skill exists

Process observations (skill description gaps, missing docs, behavior
that surprised a specialist) used to live in chat scrollback and were
lost between sessions. The inbox/issues/ + pm-escalate-issue pair
gives those observations a durable home: low-friction capture
in-vault, structured tracking on the plugin repo. The threshold for
filing is intentionally low; closing noise is cheaper than missing
signal.
