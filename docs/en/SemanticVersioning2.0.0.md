# Semantic Versioning 2.0.0

Reference: <https://semver.org/spec/v2.0.0.html>

## Format

```text
MAJOR.MINOR.PATCH
```

## Increment rules

| Segment  | When to increment                              | Reset on increment  |
| -------- | ---------------------------------------------- | ------------------- |
| `MAJOR`  | Incompatible public API changes                | MINOR and PATCH → 0 |
| `MINOR`  | New backward-compatible functionality          | PATCH → 0           |
| `PATCH`  | Backward-compatible bug fixes                  | —                   |

## Essential rules

- Version `0.y.z` is initial development — anything may change, the API is not stable.
- Version `1.0.0` defines the stable public API.
- Once a version is released, its content **must not be modified** — any change requires a new version.
- No leading zeroes in version numbers: `1.9.0 → 1.10.0`, not `1.09.0`.

## Pre-releases and build metadata

```text
1.0.0-alpha
1.0.0-alpha.1
1.0.0-rc.1
1.0.0-beta+exp.sha.5114f85
```

- Pre-release: appended with `-` after the patch → has lower precedence than the normal version.
- Build metadata: appended with `+` → ignored when comparing versions.

## Version precedence

```text
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-rc.1 < 1.0.0
```

## Relationship with Conventional Commits

| Commit type       | SemVer increment |
| ----------------- | ---------------- |
| `fix`             | PATCH            |
| `feat`            | MINOR            |
| `BREAKING CHANGE` | MAJOR            |
