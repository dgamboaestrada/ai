# OpenCode Agent Skills

Reference: <https://opencode.ai/docs/skills/>

## Qué es un skill

Un skill es un archivo `SKILL.md` que define comportamiento reutilizable para agentes. Los agentes los descubren automáticamente y los cargan bajo demanda.

## Dónde colocar los archivos

| Scope    | Ruta                                        |
| -------- | ------------------------------------------- |
| Proyecto | `.opencode/skills/<name>/SKILL.md`          |
| Proyecto | `.claude/skills/<name>/SKILL.md`            |
| Proyecto | `.agents/skills/<name>/SKILL.md`            |
| Global   | `~/.config/opencode/skills/<name>/SKILL.md` |
| Global   | `~/.claude/skills/<name>/SKILL.md`          |
| Global   | `~/.agents/skills/<name>/SKILL.md`          |

## Estructura del frontmatter

```yaml
---
name: git-release          # requerido
description: "..."         # requerido, 1-1024 caracteres
license: MIT               # opcional
compatibility: opencode    # opcional
metadata:                  # opcional, mapa string → string
  author: nombre
---
```

## Reglas del nombre

- Solo letras minúsculas, números y guiones simples (`-`)
- No empieza ni termina con `-`, sin `--` consecutivos
- 1–64 caracteres
- Debe coincidir exactamente con el nombre del directorio que contiene el `SKILL.md`
- Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`

## Permisos (`opencode.json`)

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

| Valor   | Comportamiento                              |
| ------- | ------------------------------------------- |
| `allow` | El skill carga inmediatamente               |
| `deny`  | El skill está oculto para el agente         |
| `ask`   | Se pide aprobación al usuario antes de usar |

## Diagnóstico si el skill no aparece

1. El archivo se llama `SKILL.md` en mayúsculas.
2. El frontmatter incluye `name` y `description`.
3. El nombre del skill es único en todas las rutas de búsqueda.
4. El permiso no está en `deny`.
