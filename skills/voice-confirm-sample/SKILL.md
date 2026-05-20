---
name: voice-confirm-sample
description: >
  This skill should be used when the user asks to "confirm a voice
  sample", "verify the lifted voice sample matches", "check the voice
  baseline", or any variant of presenting an existing voice sample to
  the writer and asking confirm-or-refresh. Used when a sample was
  lifted from another project, or after substantive voice drift.
metadata:
  version: "0.1.0"
  role: voice
  subset: voice
---

# voice-confirm-sample

Present the project's current voice sample to the writer and ask
"does this still represent your voice for this project?" with options
to confirm-as-is or refresh with a new sample.

This is the lifecycle counterpart to `voice-capture-sample`. Capture
is for new samples; confirm is for revalidating existing ones.

## Arguments

- **`--sample=<path>`** (optional, default
  `process/active/writer_voice_sample.md`) — which sample to confirm.
  Future cross-project voice catalog work would supply a catalog path
  here.
- **`--vault=<path>`** (optional) — vault root. Default: cwd.

## Preconditions

1. Resolve vault root and sample path.
2. Verify the sample file exists at the resolved path. If absent, abort
   with `voice sample not found at <path>; run voice-capture-sample
   first or check --sample= path`.

## Execution

1. Read the existing sample file.
2. Present its contents to the writer in chat, with:
   - Header: when it was captured, what mode it exemplifies.
   - The sample text in full.
3. Ask the writer:
   > "Does this still represent your voice for this project today?
   > Options: (a) confirm as-is, (b) refresh with a new sample,
   > (c) annotate this one with notes but keep, (d) defer the question."
4. Based on response:
   - **(a) confirm:** update the sample file's "Captured" metadata line
     to add "Confirmed: <today>" alongside the original capture date.
     No content change.
   - **(b) refresh:** archive the existing sample to
     `<vault>/process/history/writer_voice_sample_<old-date>.md`, then
     invoke `voice-capture-sample` to capture a new one at the same
     path.
   - **(c) annotate:** prompt the writer for notes; append to the
     sample's `## Notes` section.
   - **(d) defer:** no changes; report deferred status.

5. For (a) and (c), atomic-write the modified file. For (b), the
   archive move and new capture are handled by the downstream skill.

## Output on success

Depends on the writer's choice:

```
Voice sample at <path> confirmed (option a):
  Original capture date: <date>
  Confirmed today: <today>
```

OR

```
Voice sample at <path> archived to process/history/; new sample captured.
  Old: <history path>
  New: <sample path> (from voice-capture-sample)
```

OR

```
Voice sample at <path> annotated:
  New notes appended to ## Notes section.
```

OR

```
Voice sample confirmation deferred. No changes made.
```

## Output on failure

- `voice sample not found at <path>; run voice-capture-sample first`
- `permission denied writing to <path>`

## Standalone use

Common invocation: at the start of a voice work session, run this to
make sure the baseline still feels right before applying it. Cheap
ritual that catches voice drift early.
