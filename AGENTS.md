# AGENTS.md

Project-level instructions for AI coding agents working in this repository.

## Git & commits

- **Never use an agent, assistant, or AI name anywhere in git activity.** Do not add
  "Co-authored-by" trailers, "Generated with ..." lines, or any mention of Cursor,
  Claude, an AI, or an agent in commit messages, commit authors, PR titles, or PR
  descriptions.
- Always commit and push using the repository owner's configured git identity
  (`user.name` / `user.email`). Do not override the author or committer.
- Keep commit messages plain and factual, describing only the change itself.

### Required workaround for the auto-injected co-author trailer

Cursor's agent commit path hard-codes a `Co-authored-by: Cursor <cursoragent@cursor.com>`
trailer onto every `git commit` (including `git commit --amend`). There is no settings
toggle for this. To produce a clean commit, bypass the `git commit` porcelain with a raw
commit object:

```sh
git add <paths>
TREE=$(git write-tree)
PARENT=$(git rev-parse HEAD)
NEW=$(git commit-tree "$TREE" -p "$PARENT" -m "Your plain message")
git reset --hard "$NEW"
```

`git commit-tree` does not inject the trailer. Verify with
`git log -1 --pretty='%an <%ae>%n%B'` before pushing.
