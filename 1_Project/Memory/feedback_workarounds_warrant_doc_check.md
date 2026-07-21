---
name: when-workarounds-pile-up-stop-and-check-the-docs
description: "If a workaround sequence is accumulating and the tool has UI affordances that imply a supported flow, pause and read the canonical docs before adding more workarounds."
type: feedback
originSessionId: 988852c3-1715-4f55-8d1f-6cfeedc2a4a6
---
When you find yourself building a third or fourth workaround for the same problem, stop and ask whether the supported workflow exists somewhere you haven't looked yet.

**Why:** During the writing-cowork plugin dev arc (May 2026), six refresh scripts, several side-load attempts, multiple manifest backup files, and a temporary verification skill accumulated — all working around what turned out to be the wrong choice of dev tooling. The supported flow was `claude plugin marketplace update` + `claude plugin update` in Claude Code CLI. The Cowork UI's "Save plugin"/"Update plugin" buttons were evidence a supported workflow existed; they were treated as broken and routed around instead.

**How to apply:** When workaround #3 is being considered for the same root issue:
1. List the workarounds so far — are they all attacking the symptom of one underlying gap?
2. Identify UI elements the user has mentioned that haven't been explained. Those are evidence of an intended workflow.
3. Read the canonical docs (fetch primary sources, don't trust a summary).
4. If the docs describe a workflow that bypasses the problem entirely, migrate — don't add another workaround.
5. After migration, clean up the old workarounds aggressively.

**2026-07-21 note:** this same instinct applied directly to the folder-access confusion earlier in this session — instead of guessing at an app "toggle" that might not exist, the fix was to actually test the tool (`device_stage_files`) and get a definitive answer.
