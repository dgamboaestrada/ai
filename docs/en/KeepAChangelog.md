# Keep a Changelog

Reference: <https://keepachangelog.com/en/1.1.0/>

## File structure

```text
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.1.0] - 2023-03-05
### Added
- ...

### Changed
- ...
```

- The file is named `CHANGELOG.md`.
- The most recent version goes first.
- Each version includes its date in `YYYY-MM-DD` format (ISO 8601).
- Always keep an `[Unreleased]` section at the top to accumulate upcoming changes.

## Change types

| Type         | When to use                                    |
| ------------ | ---------------------------------------------- |
| `Added`      | New features                                   |
| `Changed`    | Changes to existing functionality              |
| `Deprecated` | Features soon to be removed                    |
| `Removed`    | Features that have been removed                |
| `Fixed`      | Bug fixes                                      |
| `Security`   | Security vulnerability fixes                   |

## Essential rules

- A changelog is for humans, not machines — write clearly.
- Group changes by type within each version.
- At release time, move `[Unreleased]` content into a new versioned section.
- Always document deprecations, removals, and breaking changes.
- Yanked releases must be marked with `[YANKED]` and still appear in the changelog.

## What to avoid

- **Don't use git log as a changelog** — commits are full of noise (merges, typos, minor changes).
- **Don't skip deprecations** — users need to know what will break before it does.
- **Don't be inconsistent** — an incomplete changelog creates more confusion than none at all.

## Yanked releases

```text
## [0.0.5] - 2014-12-13 [YANKED]
```
