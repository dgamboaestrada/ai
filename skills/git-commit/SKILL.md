---
name: git-commit
description: Git commit staged
license: MIT
metadata:
  author: Daniel Gamboa Estrada
  version: "0.1.1"
---

# Role and Context
You are a Git version control expert specializing in the **Conventional Commits** specification. Your goal is to ensure that every commit message provides a clear, machine-readable history that correlates with semantic versioning. Whenever you are asked to perform a commit using this skill, you must strictly follow the structured steps and rules defined here to maintain a standardized and professional project history.

## Steps to commit staged files in git

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

### 3. Compose the commit message using Conventional Commits

The commit message MUST follow this structure:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types

| Type       | When to use                                                  |
| ---------- | ------------------------------------------------------------ |
| `feat`     | Introduces a new feature (correlates with MINOR in SemVer)  |
| `fix`      | Patches a bug (correlates with PATCH in SemVer)             |
| `docs`     | Documentation changes only                                   |
| `style`    | Formatting, missing semicolons, etc.; no logic change        |
| `refactor` | Code change that neither fixes a bug nor adds a feature      |
| `perf`     | Performance improvement                                      |
| `test`     | Adding or correcting tests                                   |
| `build`    | Changes to build system or external dependencies             |
| `ci`       | Changes to CI/CD configuration and scripts                   |
| `chore`    | Other changes that don't modify src or test files            |
| `revert`   | Reverts a previous commit                                    |

#### Scope (optional)

A noun describing the section of the codebase in parentheses, e.g. `feat(parser):` or `fix(auth):`.

#### Breaking changes

- Append `!` after the type/scope to signal a breaking change: `feat!:` or `feat(api)!:`
- Optionally include a `BREAKING CHANGE: <description>` footer
- Breaking changes correlate with MAJOR in SemVer

#### Description rules

- Immediately follows the colon and space after the type/scope prefix
- Short summary of the code changes in imperative mood ("add", not "added" or "adds")
- No period at the end

#### Body (optional, use sparingly)

- Only add a body if the description alone doesn't explain the intent
- Begins one blank line after the description
- Keep it brief: 1-2 sentences max explaining the *why*, not the *what*
- The diff already shows what changed — body should explain why it was necessary

#### Footers (optional)

- Begin one blank line after the body
- Format: `token: value` or `token #value`
- Use `-` instead of spaces in token names (except `BREAKING CHANGE`)
- Examples: `Reviewed-by: Z`, `Refs: #123`, `BREAKING CHANGE: <description>`

#### Examples

Simple commit (no body needed):

```
feat(lang): add Polish language
```

```
docs: update installation guide
```

Commit with body (only when context is necessary):

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Reviewed-by: Z
Refs: #123
```

```
feat!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

### 4. Mandatory Confirmation

The agent **MUST** present the proposed commit message to the user and wait for explicit confirmation (e.g., "Yes", "Proceed", or "Approved") before executing the commit command.

### 5. Create the commit

Only include a body if the commit requires additional context beyond the description. If included, keep it brief (1-2 sentences explaining why).

```bash
git commit -m "$(cat <<'EOF'
<type>[optional scope]: <description>
EOF
)"
```

With body (only when necessary):

```bash
git commit -m "$(cat <<'EOF'
<type>[optional scope]: <description>

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

## Best Practices

- One logical change per commit — if a commit covers multiple types, split it
- Scope should be a noun describing the affected module or area
- Avoid redundancy: the type already conveys the nature of the change
- Use `git commit --amend` only to fix the last commit before pushing
- `BREAKING CHANGE` footer MUST be uppercase
