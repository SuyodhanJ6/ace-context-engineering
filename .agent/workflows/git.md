---
description: Check git status, diff, and commit changes using standard formats
---
1. Check the git status to identify changed and untracked files.
2. Use `git diff` to review changes if you are unsure of the modifications.
3. Add files and commit using the standard format:
   - `git add <file> && git commit -m "feat: <description>"`
   - `git add <file> && git commit -m "fix: <description>"`
   - `git add <file> && git commit -m "refactor: <description>"`
   - `git add <file> && git commit -m "docs: <description>"`
4. Ensure files in `.cursor/commands` or `.agent/workflows` are also added if they are untracked (use force add `git add -f` if necessary).
5. **CRITICAL**: Never add API keys or secrets to the repository.
