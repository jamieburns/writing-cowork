# refresh-probe

**Throwaway plugin. Not a real tool.** Exists solely to test whether Cowork's
plugin/marketplace refresh mechanism actually picks up a version bump —
writing-cowork task `7c1b9e04`.

## Why this exists

writing-cowork itself hit a suspected Cowork-side caching bug: after a
version bump, commit, push, and marketplace update, Cowork kept serving an
old cached version. Testing the fix directly on writing-cowork risks leaving
the real plugin in a broken or half-updated state, and any test session has
to sit inside the writing-cowork project folder to be realistic — which
would also load 60+ real skills as a side effect. `refresh-probe` isolates
the test: one plugin, one skill, one version field to watch.

## Test cycle

1. Bump `version` in `.claude-plugin/plugin.json` (e.g. `0.0.1` → `0.0.2`).
2. Also bump the `EXPECTED VERSION` marker in
   `skills/test-version/SKILL.md`'s description frontmatter, so the loaded
   skill listing shows the expected version at a glance.
3. Commit and push to this plugin's own source repo.
4. Update the throwaway marketplace catalog entry if the version is recorded
   there too (depends on marketplace source type — see the marketplace
   repo's own README).
5. In Cowork, attempt the refresh — try the plain **Update plugin** button
   first. If that doesn't work, fall back to the full procedure in
   `writing-cowork`'s `1_Project/Process/dev-workflow-and-release.md`.
6. Open a new context/session. Ask for `test-version` (or just ask "what
   version is refresh-probe"). Compare the reported version against what you
   just bumped to.
7. Record the result (which refresh method was tried, whether it worked) —
   this is the evidence for `7c1b9e04`.

## Cleanup

Once `7c1b9e04` is resolved (or abandoned), delete:
- This folder.
- The throwaway marketplace repo/catalog entry.
- The plugin install itself, via Customize → Plugins → uninstall.

None of this should outlive the question it exists to answer.
