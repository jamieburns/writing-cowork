---
name: voice-recommend-wording
description: >
  This skill should be used when the user asks to "recommend wording",
  "suggest alternatives for this paragraph", "give me N voice options
  for this passage", or any variant of generating wording alternatives
  for a paragraph or passage with a specific voice target. Returns N
  variants, each labeled with its voice-mode targeting.
metadata:
  version: "0.1.0"
  role: voice
  subset: voice
---

# voice-recommend-wording

Generate N wording alternatives for a paragraph or passage, each
explicitly labeled with the voice mode it targets (Connect / Convince /
Convey). Anchored to the project's voice sample as the baseline.

This is the substance-light side of voice work: the input passage's
meaning stays; only the register / sentence structure / rhythm shifts.
For meaning-changing recommendations, escalate to substance context.

## Arguments

- **`<paragraph>`** (required) — the passage to rewrite. Can be passed
  inline (text) or as a path-and-range reference
  (`<file>:<line-start>-<line-end>`).
- **`--variants=<N>`** (optional, default 3) — how many alternatives to
  produce. Reasonable range: 2-5.
- **`--voice-target=<mode>`** (optional) — which mode the alternatives
  should target. Default: produce one variant per mode (`connect`,
  `convince`, `convey`).
- **`--sample=<path>`** (optional, default
  `process/active/writer_voice_sample.md`) — voice sample to anchor
  recommendations.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Resolve sample path. Verify the sample file exists.
3. If `<paragraph>` is a path-range reference, verify the file and
   range exist.

## Execution

1. Read the voice sample to anchor register.
2. Read the source paragraph (inline or from file).
3. Generate `<N>` variants. Each variant:
   - Preserves the passage's substantive meaning (same claims, same
     entities, same logical structure).
   - Shifts register per `<voice-target>` (or rotates through modes if
     no target specified).
   - Stays in the writer's voice as exemplified by the sample.
4. Present variants inline, each labeled with its mode and a
   one-sentence "what's different" annotation:
   ```
   Variant 1 — Convince mode (more direct, leading with claim):
     [text]

   Variant 2 — Connect mode (warmer, frames reader-first):
     [text]

   Variant 3 — Convey mode (neutral / technical):
     [text]
   ```
5. **Do not modify the source file.** Recommendation only; the writer
   chooses which variant (if any) to adopt. Adoption is a separate
   manual or `pm-claim-file`-mediated edit.

## Output on success

The variants themselves are the output, formatted as above. Plus a
trailing summary:

```
Generated <N> variants for the passage. Pick one, mix-and-match, or
reject all. Use pm-claim-file to claim the source file before editing
if you want voice-pass tracking.
```

## Output on failure

- `voice sample not found at <path>; capture one first via voice-capture-sample`
- `paragraph reference invalid: <file>:<range> does not match anything`
- `--variants=<N> out of range; expected 2-5`

## Standalone use

The voice context's primary work tool. Writers paste passages they're
unhappy with; the skill returns alternatives. Writers pick or reject.
