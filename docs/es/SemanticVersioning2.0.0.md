# Semantic Versioning 2.0.0

Reference: <https://semver.org/spec/v2.0.0.html>

## Formato

```text
MAJOR.MINOR.PATCH
```

## Reglas de incremento

| Segmento | Cuándo incrementar                                      | Reset al incrementar |
| -------- | ------------------------------------------------------- | -------------------- |
| `MAJOR`  | Cambios incompatibles con la API pública                | MINOR y PATCH → 0    |
| `MINOR`  | Nueva funcionalidad compatible con versiones anteriores | PATCH → 0            |
| `PATCH`  | Bug fixes compatibles con versiones anteriores          | —                    |

## Reglas esenciales

- Versión `0.y.z` es desarrollo inicial — cualquier cosa puede cambiar, la API no es estable.
- La versión `1.0.0` define la API pública estable.
- Una vez publicada una versión, su contenido **no debe modificarse** — cualquier cambio requiere una versión nueva.
- Los números no llevan ceros a la izquierda: `1.9.0 → 1.10.0`, no `1.09.0`.

## Pre-releases y build metadata

```text
1.0.0-alpha
1.0.0-alpha.1
1.0.0-rc.1
1.0.0-beta+exp.sha.5114f85
```

- Pre-release: se agrega con `-` después del patch → tiene menor precedencia que la versión normal.
- Build metadata: se agrega con `+` → se ignora al comparar versiones.

## Precedencia entre versiones

```text
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-rc.1 < 1.0.0
```

## Relación con Conventional Commits

| Tipo de commit    | Incremento SemVer |
| ----------------- | ----------------- |
| `fix`             | PATCH             |
| `feat`            | MINOR             |
| `BREAKING CHANGE` | MAJOR             |
