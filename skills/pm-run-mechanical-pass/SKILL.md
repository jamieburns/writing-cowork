---
name: pm-run-mechanical-pass
description: >
  This skill should be used when the user asks to "run a mechanical pass",
  "do a typo / punctuation / grammar sweep", "mechanical voice pass",
  "fix typos and citation format", or any variant of a voice-pass scoped to
  mechanical issues (spelling, punctuation, grammar, capitalization,
  citation format). Inline summary + accept-prompt protocol; respects
  voice_exceptions.md.
metadata:
  version: "0.1.0"
  role: voice
  subset: voice
---

# pm-run-mechanical-pass

Run a mechanical voice pass over a scope of the vault. Catches: typos,
punctuation issues, grammar errors, citation format drift, capitalization
inconsistencies (including capitalization-after-period that isn't
paragraph-start). With `--strict`, also catches hyphenation-consistency
drift (which produces a lot of noise; opt-in only).

This is the "no judgment" pass — purely mechanical. Tone / register /
substantive wording stays for `pm-recommend-wording` (separate skill).

## Arguments

- **`<scope>`** (required) — vault-relative path to the file, directory,
  or glob to scan. Examples: `part1_draft.md`,
  `process/active/voice_handoff.md`, `analysis/*.md`.
- **`--ignore-exceptions`** (optional, flag) — skip the
  `voice_exceptions.md` consultation step. Default: respect exceptions.
- **`--strict`** (optional, flag) — also catch hyphenation drift. Off by
  default (noisy; producing many minor diffs).
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Verify the resolved `<scope>` matches at least one existing file.
3. Verify `process/active/voice_exceptions.md` exists (it should, per
   pm-init-voice-exceptions). If absent and `--ignore-exceptions` not
   set, warn and proceed without exception filtering.

## Execution

For each file in scope:

1. Scan the file for the issue classes listed above.
2. Cross-reference each candidate finding against
   `voice_exceptions.md`: drop findings whose term is exception-listed
   for this file/section/project scope.
3. Also respect inline markers: `<!-- exception -->` adjacent to a
   passage suppresses findings within that passage.
4. Also respect `::: passthrough` fenced divs and standard markdown
   blockquotes — don't flag content inside (those are quotes from
   external sources; not subject to the project's voice).
5. Group findings by issue class.

Then present an **inline summary** to the user — counts per class, top
N examples per class — and prompt: `Apply <class>? [y/n/each]`. Per
locked decision pattern: writer adjudicates each class.

- `y` → apply all findings in that class.
- `n` → skip the class entirely (no changes).
- `each` → cycle through each finding individually, writer accepts or
  rejects per finding.

Atomic-write each modified file. Commit with prefix `[voice]` if the
project is git-tracked. The skill commits per-file (one commit per
modified file), making it easy to revert specific changes.

## Output on success

```
Mechanical pass complete on <scope>:
  Files scanned: <N>
  Files modified: <M>
  Issue classes found:
    - Typos: <count> found, <accepted> accepted
    - Punctuation: <count>/<accepted>
    - Citation format: <count>/<accepted>
    - Capitalization: <count>/<accepted>
    - Hyphenation (strict only): <count>/<accepted>
  Commits: <list of commit hashes with [voice] prefix>
```

## Output on failure

- `scope <path> matches no files; refine the path or glob`
- `voice_exceptions.md not found at <vault>/process/active/; run pm-init-voice-exceptions or use --ignore-exceptions`
- `permission denied writing to <file>`

## Standalone use

Common standalone invocation: the voice context running a sweep over a
fresh draft section. Writer accepts/rejects per class in real time.
