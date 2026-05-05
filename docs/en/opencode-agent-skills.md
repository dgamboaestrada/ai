# OpenCode Agent Skills

Reference: <https://opencode.ai/docs/skills/>

## What is a skill

A skill is a `SKILL.md` file that defines reusable behavior for agents. Agents discover them automatically and load them on demand.

## Where to place files

| Scope   | Path                                        |
| ------- | ------------------------------------------- |
| Project | `.opencode/skills/<name>/SKILL.md`          |
| Project | `.claude/skills/<name>/SKILL.md`            |
| Project | `.agents/skills/<name>/SKILL.md`            |
| Global  | `~/.config/opencode/skills/<name>/SKILL.md` |
| Global  | `~/.claude/skills/<name>/SKILL.md`          |
| Global  | `~/.agents/skills/<name>/SKILL.md`          |

## Frontmatter structure

```yaml
---
name: git-release          # required
description: "..."         # required, 1-1024 characters
license: MIT               # optional
compatibility: opencode    # optional
metadata:                  # optional, string-to-string map
  author: name
---
```

## Name rules

- Lowercase letters, digits, and single hyphens (`-`) only
- Cannot start or end with `-`, no consecutive `--`
- 1–64 characters
- Must match exactly the name of the directory containing `SKILL.md`
- Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`

## Permissions (`opencode.json`)

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

| Value   | Behavior                                    |
| ------- | ------------------------------------------- |
| `allow` | Skill loads immediately                     |
| `deny`  | Skill is hidden from the agent              |
| `ask`   | User is prompted for approval before use    |

## Troubleshooting if a skill does not appear

1. The file is named `SKILL.md` in all caps.
2. The frontmatter includes both `name` and `description`.
3. The skill name is unique across all search paths.
4. The permission is not set to `deny`.
