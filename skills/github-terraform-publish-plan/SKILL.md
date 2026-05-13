---
name: github-terraform-publish-plan
description: Parse and publish Terraform plan output as a formatted GitHub PR comment with clean formatting, no warnings by default, and resource-focused analysis.
license: MIT
metadata:
  author: Daniel Gamboa Estrada
  version: "1.1.0"
---

# Role and Context

You are a Terraform plan parser and GitHub automation specialist. Your role is to extract key information from Terraform plan outputs and publish them as structured, formatted comments directly to GitHub pull requests.

## Execution workflow

### Step 1 — Resolve the plan file

Read the file path provided by the user. If none given, default to `tfplan.txt` in the current directory.

```bash
cat <plan-file-path>
```

### Step 2 — Detect the PR number

Auto-detect from the current branch:

```bash
gh pr list --state open --head $(git branch --show-current) --json number,title
```

If detection fails or returns no results, ask the user for the PR number explicitly.

### Step 3 — Parse the plan

Extract from the plan file:
- **Target command**: last `[INFO]` line at the bottom, e.g. `[INFO] terraform plan -var-file=env.tfvars -target='...'`
- **Module-service**: first-level module from the target (e.g. `module.myservice`, not `module.myservice.module.sub`)
- **Summary line**: pattern `Plan: X to add, Y to change, Z to destroy`
- **Resource changes**: all `# module... will be...` blocks with their diffs
- **Warnings**: strip by default; include only if the user explicitly requests them (e.g. "con warnings", "include warnings")

### Step 4 — Write comment to temp file

Build the formatted comment and write it to a temp file for preview and reuse:

```bash
cat > /tmp/pr_comment.txt << 'EOF'
Terraform plan for <module-service>
---
Target plan: `<target-command>`
Summary: `<plan-summary>`

<details><summary>Changes</summary>

- <resource_type> (<resource_name>)
  <what changed>

</details>

<details><summary>Plan output</summary>
<p>

```hcl
<resource-changes-only>
```

</p>
</details>
EOF
```

### Step 5 — Preview the comment

Display the temp file so the user can review before publishing:

```bash
cat /tmp/pr_comment.txt
```

Ask the user for explicit confirmation (e.g. "yes", "si", "proceed") before continuing.

### Step 6 — Publish to GitHub PR

```bash
gh pr comment <pr-number> --body "$(cat /tmp/pr_comment.txt)"
```

Use `cat /tmp/pr_comment.txt` to avoid shell escaping issues with backticks and special characters in the plan output.

---

## Comment template

```
Terraform plan for <module-service>
---
Target plan: `<target-command>`
Summary: `<plan-summary>`

<details><summary>Changes</summary>

- <resource_type> (<resource_name>)
  <1-2 lines describing what changed>

</details>

<details><summary>Plan output</summary>
<p>

```hcl
<resource-changes-only, no warnings>
```

</p>
</details>
```

### Formatting rules

- **Changes bullets**: use `-` (no emojis) with resource type and name, 1-2 lines per resource
- **Plan output**: include only resource change blocks and the summary line — strip warnings, deprecations, and variable declarations
- **Warnings (optional)**: only when explicitly requested, add a third collapsible section:

```markdown
<details><summary>Warnings</summary>

**Undeclared Variables:** my_variable (env.tfvars), another_variable (terraform.tfvars)
**Deprecated Syntax:** Quoted references in ignore_changes; interpolation-only expressions
**Resource Targeting:** Plan uses -target — may not represent all requested changes

</details>
```

---

## Full example

```bash
# Step 2 — detect PR
gh pr list --state open --head $(git branch --show-current) --json number,title
# → [{"number":42,"title":"feat: rotate TLS certificate for myservice"}]

# Step 4 — write comment to temp file
cat > /tmp/pr_comment.txt << 'EOF'
Terraform plan for module.myservice
---
Target plan: `terraform plan -var-file=env.tfvars -target='module.myservice.module.myservice_elb.aws_elb.public_elb[0]' -target='module.myservice.module.myservice_elb.aws_elb.elb[0]'`
Summary: `Plan: 0 to add, 4 to change, 0 to destroy`

<details><summary>Changes</summary>

- aws_elb (myservice-public-elb)
  Rotating SSL certificate: `old-cert-id` → `new-cert-id`
  External-facing ELB listener HTTPS update

- aws_security_group (public_elb_security_group)
  Ingress port 443: Adding new IPs, removing outdated ones

- aws_elb (myservice-elb)
  Rotating SSL certificate: `old-cert-id` → `new-cert-id`
  Tags: Migration metadata update

- aws_security_group (elb_security_group)
  Egress/Ingress: Consolidating CIDR blocks
  Tags: Migration metadata update

</details>

<details><summary>Plan output</summary>
<p>

```hcl
# module.myservice.module.myservice_elb.aws_elb.public_elb[0] will be updated in-place
~ resource "aws_elb" "public_elb" {
    + listener { ssl_certificate_id = "arn:aws:acm:us-east-1:123456789012:certificate/new-cert-id" }
    - listener { ssl_certificate_id = "arn:aws:acm:us-east-1:123456789012:certificate/old-cert-id" }
  }

Plan: 0 to add, 4 to change, 0 to destroy.
```

</p>
</details>
EOF

# Step 5 — preview
cat /tmp/pr_comment.txt

# Step 6 — publish (after user confirmation)
gh pr comment 42 --body "$(cat /tmp/pr_comment.txt)"
```
