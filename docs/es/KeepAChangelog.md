# Keep a Changelog

Reference: <https://keepachangelog.com/en/1.1.0/>

## Estructura del archivo

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

- El archivo se llama `CHANGELOG.md`.
- La versión más reciente va primero.
- Cada versión incluye su fecha en formato `YYYY-MM-DD` (ISO 8601).
- Siempre hay una sección `[Unreleased]` al inicio para acumular cambios pendientes.

## Tipos de cambios

| Tipo         | Cuándo usarlo                         |
| ------------ | ------------------------------------- |
| `Added`      | Nuevas funcionalidades                |
| `Changed`    | Cambios en funcionalidad existente    |
| `Deprecated` | Funcionalidades próximas a eliminarse |
| `Removed`    | Funcionalidades eliminadas            |
| `Fixed`      | Corrección de bugs                    |
| `Security`   | Vulnerabilidades corregidas           |

## Reglas esenciales

- El changelog es para humanos, no para máquinas — redacta con claridad.
- Agrupa los cambios por tipo dentro de cada versión.
- Al publicar una versión, mueve el contenido de `[Unreleased]` a la nueva sección versionada.
- Documenta siempre deprecaciones, remociones y breaking changes.
- Las versiones yanked (retiradas) se marcan con `[YANKED]` y deben aparecer en el changelog.

## Qué evitar

- **No uses git log como changelog** — los commits tienen ruido (merges, typos, cambios menores).
- **No omitas deprecaciones** — los usuarios necesitan saber qué va a romperse antes de que ocurra.
- **No seas inconsistente** — un changelog incompleto genera más confusión que no tener uno.

## Versiones yanked

```text
## [0.0.5] - 2014-12-13 [YANKED]
```
