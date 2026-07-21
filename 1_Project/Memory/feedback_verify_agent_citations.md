---
name: Verify agent-supplied citations before using them
description: Citations from research subagents (issue numbers, repo URLs, doc links) need direct verification — they're draft data, not facts.
type: feedback
originSessionId: 988852c3-1715-4f55-8d1f-6cfeedc2a4a6
---
When a research subagent (claude-code-guide, general-purpose, etc.) supplies specific identifiers — GitHub issue numbers, doc URLs, file paths, version numbers — treat them as draft data. Verify with a direct fetch (WebFetch on the URL or a shell check of the path) before quoting them in user-facing material like feedback letters, commit messages, or PRs.

**Why:** Subagents sometimes generate plausible-looking citations that don't map to real specific items. The user found this when chasing issue numbers cited in an Anthropic support feedback draft — some were real but wrong, some looked hallucinated. Created friction (rabbit-hole chase) and undermined credibility of the feedback.

**How to apply:** Before passing any specific identifier from an agent's output to the user, fetch/check it. If verification fails, either find the correct identifier or rephrase to omit the specifics (e.g., "several public GitHub issues describe variants" instead of "issue #38271").
