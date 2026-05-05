# Conventional Commits

Reference: <https://www.conventionalcommits.org/en/v1.0.0/>

## Estructura

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Tipos

| Tipo       | Cuándo usarlo                                           |
| ---------- | ------------------------------------------------------- |
| `feat`     | Nueva funcionalidad (MINOR en SemVer)                   |
| `fix`      | Corrección de bug (PATCH en SemVer)                     |
| `docs`     | Solo documentación                                      |
| `style`    | Formato, espacios, puntos y comas; sin cambio de lógica |
| `refactor` | Cambio que no es feat ni fix                            |
| `perf`     | Mejora de rendimiento                                   |
| `test`     | Agregar o corregir tests                                |
| `build`    | Sistema de build o dependencias externas                |
| `ci`       | Configuración de CI/CD                                  |
| `chore`    | Otros cambios que no tocan src ni tests                 |
| `revert`   | Revierte un commit anterior                             |

## Reglas esenciales

- La **descripción** va inmediatamente después del `:` y un espacio — modo imperativo, sin punto final.
- El **scope** es opcional: un sustantivo entre paréntesis que indica el área afectada, ej. `fix(auth):`.
- El **body** comienza con una línea en blanco después de la descripción; explica el *por qué*.
- Los **footers** van después de otra línea en blanco; formato `Token: valor` o `Token #valor`.

## Breaking changes

Dos formas equivalentes:

```text
feat!: eliminar soporte para Node 6
```

```text
feat: eliminar soporte para Node 6

BREAKING CHANGE: se usan APIs no disponibles en Node 6.
```

- `!` después del tipo/scope señala el breaking change en el título.
- `BREAKING CHANGE:` en el footer lo documenta explícitamente (DEBE ser mayúsculas).
- Ambas formas correlacionan con MAJOR en SemVer.

## Ejemplos

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
