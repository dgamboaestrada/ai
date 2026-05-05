# Conventional Commits

Reference: <https://www.conventionalcommits.org/en/v1.0.0/>

## Structure

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

| Type       | When to use                                               |
| ---------- | --------------------------------------------------------- |
| `feat`     | New feature (MINOR in SemVer)                             |
| `fix`      | Bug fix (PATCH in SemVer)                                 |
| `docs`     | Documentation changes only                               |
| `style`    | Formatting, whitespace, semicolons; no logic change       |
| `refactor` | Code change that is neither a feat nor a fix              |
| `perf`     | Performance improvement                                   |
| `test`     | Adding or correcting tests                                |
| `build`    | Build system or external dependency changes               |
| `ci`       | CI/CD configuration and scripts                           |
| `chore`    | Other changes that don't touch src or test files          |
| `revert`   | Reverts a previous commit                                 |

## Essential rules

- The **description** immediately follows the `:` and a space — imperative mood, no trailing period.
- **Scope** is optional: a noun in parentheses indicating the affected area, e.g. `fix(auth):`.
- The **body** starts with a blank line after the description; explains the *why*.
- **Footers** follow another blank line; format `Token: value` or `Token #value`.

## Breaking changes

Two equivalent forms:

```text
feat!: drop support for Node 6
```

```text
feat: drop support for Node 6

BREAKING CHANGE: uses JavaScript features not available in Node 6.
```

- `!` after the type/scope signals the breaking change in the title.
- `BREAKING CHANGE:` in the footer documents it explicitly (MUST be uppercase).
- Both forms correlate with MAJOR in SemVer.

## Examples

```text
feat(lang): add Polish language
```

```text
fix: prevent racing of requests

Introduce a request id and dismiss responses from outdated requests.

Reviewed-by: Z
Refs: #123
```

```text
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```
