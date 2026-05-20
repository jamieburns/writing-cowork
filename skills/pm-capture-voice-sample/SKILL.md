---
name: pm-capture-voice-sample
description: >
  This skill should be used when the user asks to "capture a voice
  sample", "set a voice baseline", "elicit a writing sample for voice
  reference", or any variant of capturing a fresh writer sample as the
  voice baseline for a project. Default location:
  process/active/writer_voice_sample.md.
metadata:
  version: "0.1.0"
  role: voice
  subset: voice
---

# pm-capture-voice-sample

Elicit a fresh writing sample from the writer, save it as the project's
voice baseline. The sample anchors future voice work — voice context
references it when making recommendations, and writers can use it as a
sanity check for their own register drift.

For projects that already have a sample (e.g., lifted from another
project), use `pm-confirm-voice-sample` instead.

## Arguments

- **`--sample=<path>`** (optional, default
  `process/active/writer_voice_sample.md`) — where to save the captured
  sample. Future cross-project voice catalog work would supply a
  different path here.
- **`--prompt=<text>`** (optional) — custom elicitation prompt. Default
  prompt asks the writer for a representative paragraph or two of their
  voice across a chosen mode (Connect / Convince / Convey).
- **`--mode=connect|convince|convey`** (optional) — which voice mode the
  sample exemplifies. Default: ask the writer.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root.
2. Resolve the sample path (default or `--sample=`). Verify the parent
   directory exists.
3. Verify the resolved sample path does NOT already exist. If it does,
   abort with `voice sample already exists at <path>; use
   pm-confirm-voice-sample to confirm/refresh, or remove the existing
   file first`. Do not overwrite.

## Execution

1. Prompt the writer:
   > "Please write or paste a representative paragraph (one to three
   > paragraphs) of your voice for <mode> mode in this project. This
   > sample will anchor the voice context's recommendations and future
   > voice passes. Aim for prose that's natural for you, not
   > self-conscious — register, sentence structure, rhythm matters more
   > than polished content."

2. Wait for the writer's input. If they paste / type a sample, proceed.
   If they say "skip" or "later", abort without writing.

3. Write the sample to `<resolved-path>` with this format:

   ```markdown
   # Writer voice sample — <project-title>

   **Captured:** <date>
   **Mode:** <connect|convince|convey>
   **Path:** <resolved-path>

   ---

   <writer's text verbatim>

   ---

   ## Notes

   (Writer can add notes about this sample's context, what it exemplifies,
   when to use it as reference.)
   ```

4. Atomic-write.

## Output on success

```
Captured voice sample at <path>:
  Mode: <mode>
  Words: <count>
  Date: <date>

The voice context will reference this when making recommendations. Use
pm-recommend-wording with --sample=<path> to anchor a recommendation to
this voice baseline.
```

## Output on failure

- `voice sample already exists at <path>; use pm-confirm-voice-sample or remove first`
- `parent directory missing at <path>; create it or use --sample= with a valid path`
- `writer declined to provide a sample (skip / later); no file written`
- `permission denied writing to <path>`

## Standalone use

The first voice-context invocation in a new project typically calls
this skill to establish a baseline. Subsequent voice work references
the baseline implicitly.
