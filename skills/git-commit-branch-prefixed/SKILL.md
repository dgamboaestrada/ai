---
name: git-commit-branch-prefixed
description: Create commits with branch-prefixed format for automatic change tracking and issue correlation.
license: MIT
metadata:
  author: Daniel Gamboa Estrada
  version: "0.1.0"
---

# Role and Context
You are a Git version control expert specializing in creating clear, concise commit messages that adhere to rigorous standards. Whenever you are asked to perform a commit using the `branch-prefixed` format, you must strictly follow the steps and rules defined in this document to ensure traceability and automatic correlation of changes with the corresponding issues.

## Steps to commit staged files in git using branch-prefixed format (BRANCH-ID: description)

### 1. Check what files are staged

```bash
git status
```

or

```bash
git diff --cached --name-only
```

### 2. Review the changes

```bash
git diff --cached
```

### 3. Compose the commit message

The commit message MUST follow this structure:

```
<branch>: <description>

[optional body]

[optional footer(s)]
```

#### Branch reference

- Use the current Git branch name (e.g., `FEATURE-001`, `BUGFIX-042`, `TASK-789`)
- Extract from: `git rev-parse --abbrev-ref HEAD` or `git branch --show-current`
- Format: `PREFIX-NUMBER` where PREFIX is the ticket/feature identifier

#### Description rules

- Immediately follows the colon and space
- Short summary of the code changes in imperative mood ("add", not "added" or "adds")
- No period at the end
- Example: `FEATURE-001: add new language support`

#### Body (optional, use sparingly)

- Only add a body if the description alone doesn't explain the intent
- Begins one blank line after the description
- Keep it brief: 1-2 sentences max explaining the *why*, not the *what*
- The diff already shows what changed — body should explain why it was necessary

#### Footers (optional)

- Begin one blank line after the body
- Format: `token: value` or `token #value`
- Use `-` instead of spaces in token names
- Examples: `Reviewed-by: Z`, `Refs: #123`

#### Examples

Simple commit (no body needed):

```
FEATURE-001: add new language support
```

```
TASK-789: remove deprecated access rule
```

Commit with body (only when context is necessary):

```
BUGFIX-042: update service configuration

- Resource parameters adjusted for better performance under load.
```

```
FEATURE-015: add retry logic to API client

- Prevents cascading failures during transient network issues.
```

```
DOCS-089: update resource documentation

- Alphabetize resource links for better readability
- Add Gemini CLI documentation link
```

### 4. Mandatory Confirmation

The agent **MUST** present the proposed commit message to the user and wait for explicit confirmation (e.g., "Yes", "Proceed", or "Approved") before executing the commit command.

### 5. Create the commit

Only include a body if the commit requires additional context beyond the description. If included, keep it brief (1-2 sentences explaining why).

```bash
git commit -m "$(cat <<'EOF'
<branch>: <description>
EOF
)"
```

With body (only when necessary):

```bash
git commit -m "$(cat <<'EOF'
<branch>: <description>

<concise explanation of why>
EOF
)"
```

### 6. Verify the commit was created

```bash
git log -1
```

### 7. Push to remote repository (only if explicitly requested)

```bash
git push origin <branch-name>
```

### Best Practices

- Always prefix commits with the current branch identifier for automatic issue correlation
- One logical change per commit — split commits if they address multiple concerns
- Use imperative mood in descriptions ("add", "fix", "update", "remove")
- Keep the first line concise and descriptive (under 72 characters recommended)
- Use the body to explain the *why*, not the *what* — the diff shows what changed
- Include related issue references in footers when applicable
- Use `git commit --amend` only to fix the last commit before pushing
