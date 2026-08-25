# Release checklist

1. Confirm the release changes only the reusable topic-video method and contains no private production or brand data.
2. Run the official Skill validator against the repository root.
3. Parse `agents/openai.yaml` and every JSON example.
4. Verify local Markdown links and render both SVG assets.
5. Review `git diff` and scan tracked files for secrets, personal paths, account data, client information, and copyrighted material.
6. Update `CHANGELOG.md` with the release date and migration notes.
7. Commit with the public no-reply author, create an annotated `vX.Y.Z` tag, and publish release notes from the changelog.
8. Install from a fresh clone and verify that Codex discovers the Skill.
