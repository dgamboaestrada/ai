#!/usr/bin/env python3
"""Parse a `terraform plan` (or `terragrunt plan`) text log and emit a Markdown
summary of every resource that will be created, updated in-place, replaced,
or destroyed — grouped by module/service and by resource type.

Usage:
    python3 parse_plan.py <plan-log-file> [-o output.md]

If -o is omitted, the Markdown is printed to stdout.
"""
import argparse
import re
import sys
from collections import defaultdict

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

# Matches the resource header comment line, e.g.:
#   # module.a.module.b.aws_iam_role.execution will be created
#   # module.a.aws_ecs_task_definition.this will be replaced due to changes in replace_triggered_by
#   # module.a.aws_lb_listener.https will be updated in-place
#   # module.a.aws_secretsmanager_secret_version.x will be read during apply (config refers to values not yet known)
HEADER_RE = re.compile(
    r'^\s*#\s+(?P<path>.+?)\s+will\s+be\s+(?P<action>created|updated in-place|replaced|destroyed|read during apply)'
    r'(?P<rest>.*)$'
)

# Splits a fully-qualified resource path into (module_path, resource_type.resource_name)
# The resource type is always the last segment matching <provider>_<noun> (or a known
# non-aws type like random_password, ultradns_record, mongodbatlas_*, akamai_*, terraform_data),
# immediately followed by `.<name>`.
TYPE_RE = r'(aws_[a-z0-9_]+|random_[a-z0-9_]+|mongodbatlas_[a-z0-9_]+|ultradns_[a-z0-9_]+|akamai_[a-z0-9_]+|terraform_data|null_resource|time_[a-z0-9_]+)'
RESOURCE_RE = re.compile(r'^(?P<modpath>.*?)\.(?P<type>' + TYPE_RE + r')\.(?P<name>.*)$')

ACTION_LABELS = {
    'created': 'A crear',
    'updated in-place': 'A modificar (in-place)',
    'replaced': 'A reemplazar (destroy + create)',
    'destroyed': 'A destruir',
    'read during apply': 'Se leera durante apply (valor aun no conocido)',
}

ACTION_ORDER = ['created', 'replaced', 'updated in-place', 'destroyed', 'read during apply']


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub('', text)


def parse_resources(text: str):
    """Returns dict[action] -> list of (full_path, replace_reason_or_None)."""
    results = defaultdict(list)
    for line in text.splitlines():
        m = HEADER_RE.match(line)
        if not m:
            continue
        path = m.group('path').strip()
        action = m.group('action').strip()
        rest = m.group('rest').strip()
        reason = None
        if action == 'replaced' and rest:
            reason = rest.lstrip('due to ').strip()
        results[action].append((path, reason))
    return results


def split_module_and_resource(path: str):
    m = RESOURCE_RE.match(path)
    if not m:
        return None, path
    modpath = m.group('modpath')
    resource = f"{m.group('type')}.{m.group('name')}"
    return modpath, resource


def clean_modpath(mp: str) -> str:
    """Collapse `module.<name>.module.<name>...` into `<name>.<name>...` so the
    report groups by actual module names instead of the literal `module` keyword."""
    tokens = mp.split('.') if mp else []
    names = [t for t in tokens if t != 'module']
    return '.'.join(names)


def find_summary_line(text: str):
    m = re.search(r'Plan:\s*(\d+)\s*to add,\s*(\d+)\s*to change,\s*(\d+)\s*to destroy', text)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    if re.search(r'No changes\.', text):
        return 0, 0, 0
    return None


def build_markdown(source_file: str, resources_by_action, add_n, change_n, destroy_n) -> str:
    lines = []
    lines.append("# Resumen de recursos - Terraform Plan")
    lines.append("")
    lines.append(f"**Archivo origen:** `{source_file}`")
    lines.append("")
    lines.append("## Resumen del plan")
    lines.append("")
    lines.append(f"- **{add_n}** recursos a crear (`to add`)")
    lines.append(f"- **{change_n}** recursos a modificar (`to change`)")
    lines.append(f"- **{destroy_n}** recursos a destruir (`to destroy`)")
    lines.append("")

    grand_total = 0
    type_counts = defaultdict(int)

    for action in ACTION_ORDER:
        entries = resources_by_action.get(action, [])
        if not entries:
            continue
        label = ACTION_LABELS[action]
        lines.append(f"## {label} ({len(entries)})")
        lines.append("")

        by_module = defaultdict(list)
        for path, reason in entries:
            modpath, resource = split_module_and_resource(path)
            modpath = clean_modpath(modpath or '')
            by_module[modpath].append((resource, reason))
            rtype = resource.split('.')[0]
            type_counts[rtype] += 1
            grand_total += 1

        top_groups = defaultdict(dict)
        for modpath in by_module:
            top = modpath.split('.')[0] if modpath else '(root)'
            top_groups[top][modpath] = by_module[modpath]

        for top in sorted(top_groups.keys()):
            lines.append(f"### Servicio: `{top}`")
            lines.append("")
            for modpath in sorted(top_groups[top].keys()):
                sub = modpath[len(top):].lstrip('.')
                heading = f"**Modulo:** `{sub}`" if sub else "**(recursos directos del servicio)**"
                lines.append(f"- {heading}")
                for resource, reason in sorted(top_groups[top][modpath]):
                    if reason:
                        lines.append(f"  - `{resource}` — {reason}")
                    else:
                        lines.append(f"  - `{resource}`")
            lines.append("")

    lines.append("## Totales por tipo de recurso")
    lines.append("")
    lines.append("| Tipo | Cantidad |")
    lines.append("|---|---|")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| `{t}` | {c} |")
    lines.append(f"| **TOTAL** | **{grand_total}** |")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan_file', help='Path to the terraform/terragrunt plan text log')
    parser.add_argument('-o', '--output', help='Output Markdown file (default: stdout)')
    args = parser.parse_args()

    with open(args.plan_file, 'r', errors='replace') as f:
        raw = f.read()

    text = strip_ansi(raw)
    resources_by_action = parse_resources(text)
    summary = find_summary_line(text)

    if summary is None and not resources_by_action:
        print("No se encontraron bloques de recursos ni una linea 'Plan: ... to add, ... to change, ... to destroy'. "
              "¿Es realmente un archivo de salida de `terraform plan`?", file=sys.stderr)
        sys.exit(1)

    add_n, change_n, destroy_n = summary if summary else (
        len(resources_by_action.get('created', [])),
        len(resources_by_action.get('updated in-place', [])) + len(resources_by_action.get('replaced', [])),
        len(resources_by_action.get('destroyed', [])),
    )

    md = build_markdown(args.plan_file, resources_by_action, add_n, change_n, destroy_n)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(md)
        print(f"Resumen guardado en: {args.output}", file=sys.stderr)
    else:
        print(md)


if __name__ == '__main__':
    main()
