---
name: github-terraform-publish-plan
description: |
  Invoke when the user wants to add Terraform or Terragrunt plan output as a formatted comment on an existing GitHub pull request. The trigger is two signals together: (1) user already has plan output — a file path, a /tmp location, or pasted text — and (2) wants it posted as a PR comment so reviewers can see the changes.

  Covers phrasings like: "post the plan to the PR", "add a terraform plan comment on PR #N", "drop the plan output on the open PR", "publish the terraform plan to GitHub", "comment the plan on this branch's PR".

  Skip when: running terraform plan, explaining or analyzing what a plan will change, reviewing whether a plan is safe to apply, fixing deprecation warnings, or creating a new PR.
license: MIT
metadata:
  author: Daniel Gamboa Estrada
  version: "1.2.0"
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
- **Target command**: last `[INFO]` line at the bottom, e.g. `[INFO] terraform plan -var-file=env.tfvars -target='...'`. Note: `[INFO]` lines are produced by Terragrunt or CI wrappers — plain `terraform plan` output won't have them. If no `[INFO]` line is found, look for a `terraform plan ...` invocation line or leave the field blank.
- **Module-service**: first-level module from the target (e.g. `module.myservice`, not `module.myservice.module.sub`)
- **Summary line**: pattern `Plan: X to add, Y to change, Z to destroy`
- **Resource changes**: all `# module... will be...` blocks with their diffs
- **No-changes case**: if the plan contains `No changes.` and no `Plan:` line exists, set the summary to `No changes. Infrastructure matches the configuration.` and skip the Plan output section entirely.
- **Warnings**: strip by default; include only if the user explicitly requests them (e.g. "include warnings")

### Step 4 — Write comment to temp file

Build the Changes bullet list from the resources parsed in Step 3, then write the full comment to a temp file. Extract the COMPLETE terraform plan output verbatim (lines 1 through the "Plan: X to add..." summary line) for the Plan output section — do not summarize, truncate, or edit any resource block.

```bash
# Extract the complete plan (from line 1 to and including the summary line)
PLAN_LINES=$(grep -n "^Plan:" <plan-file-path> | head -1 | cut -d: -f1)
sed -n "1,${PLAN_LINES}p" <plan-file-path> > /tmp/plan_output.txt

# Write the formatted comment — substitute the real Changes bullets and metadata before running
cat > /tmp/pr_comment.txt << 'EOF'
Terraform plan for <module-service>
---
Target plan: `<target-command>`
Terraform path: `<relativ-path-of-the-terraform-root-module>`
Summary: `<plan-summary>`

<details><summary>Changes</summary>

- <resource_type> (<resource_name>)
  <what changed>

</details>

<details><summary>Plan output</summary>
<p>

```hcl
EOF

# Append the COMPLETE plan output (unmodified, verbatim)
cat /tmp/plan_output.txt >> /tmp/pr_comment.txt

# Close the markdown block
cat >> /tmp/pr_comment.txt << 'EOF'
```

</p>
</details>
EOF
```

### Step 4b — Add destroy warning (if applicable)

If the plan contains `terraform destroy` or `-destroy`, append this warning section to the end of the comment:

```markdown
---

## Important Note

**The terraform destroy must be executed from the `master` branch, not from the [CURRENT_BRANCH_NAME] branch.** If applied from the current branch, it will fail with:

```
Error: Provider configuration not present
```

This occurs because [REASON_PLACEHOLDER].

**Steps to apply:**
1. Checkout `master` branch
2. Run: [TERRAFORM_COMMAND_PLACEHOLDER]
3. Merge this PR to `master`.
```

Append this section at the very end of the comment (after the "Plan output" collapsible), replacing only [CURRENT_BRANCH_NAME], [REASON_PLACEHOLDER], and [TERRAFORM_COMMAND_PLACEHOLDER] with actual values derived from the plan context.

### Step 5 — Preview the comment

Display the temp file so the user can review before publishing:

```bash
cat /tmp/pr_comment.txt
```

Ask the user for explicit confirmation (e.g. "yes", "si", "proceed") before continuing.

### Step 6 — Publish to GitHub PR

Use `--body-file` to avoid shell expansion mangling backticks and `$` signs in the plan output:

```bash
gh pr comment <pr-number> --body-file /tmp/pr_comment.txt
```

---

## Comment template

**Standard plan:**
```
Terraform plan for <module-service>
---
Target plan: `<target-command>`
Terraform path: `<relativ-path-of-the-terraform-root-module>`
Summary: `<plan-summary>`

<details><summary>Changes</summary>

- <resource_type> (<resource_name>)
  <1-2 lines describing what changed>

</details>

<details><summary>Plan output</summary>
<p>

```hcl
<complete-terraform-plan-from-line-1-to-plan-summary>
```

</p>
</details>
```

**Destroy plan (append this warning at the end):**
```
<details><summary>Plan output</summary>
<p>

```hcl
<complete-terraform-plan-from-line-1-to-plan-summary>
```

</p>
</details>

---

## Important Note

**The terraform destroy must be executed from the `master` branch, not from the [CURRENT_BRANCH_NAME] branch.** If applied from the current branch, it will fail with:

```
Error: Provider configuration not present
```

This occurs because [REASON_PLACEHOLDER].

**Steps to apply:**
1. Checkout `master` branch
2. Run: [TERRAFORM_COMMAND_PLACEHOLDER]
3. Merge this PR to `master`.
```

### Formatting rules

- **Changes bullets**: use `-` (no emojis) with resource type and name, 1-2 lines per resource
- **Plan output section**: always include the complete raw terraform plan output (from line 1 through the `Plan: X to add, Y to change, Z to destroy` summary line). Do not summarize, truncate, or edit any resource block. Strip warnings, deprecation notices, and variable declaration warnings (lines after the summary line) by default; include them only if the user explicitly requests them.
- **No-changes case**: omit the Plan output section entirely and use `No changes. Infrastructure matches the configuration.` as the summary.
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
# → [{"number":42,"title":"feat: rotate TLS certificate for service"}]

# Step 4 — extract the complete plan output up to the summary line
PLAN_FILE="path/to/tfplan.txt"
PLAN_LINES=$(grep -n "^Plan:" "$PLAN_FILE" | head -1 | cut -d: -f1)
sed -n "1,${PLAN_LINES}p" "$PLAN_FILE" > /tmp/plan_output.txt

# Step 4 — write the comment to a temp file (Changes section built from Step 3 parsed resources)
cat > /tmp/pr_comment.txt << 'EOF'
Terraform plan for module.service
---
Target plan: `terraform destroy -var-file=env.tfvars -target='module.service'`
Terraform path: `/opt/terraform/infrastructure/env`
Summary: `Plan: 0 to add, 0 to change, 3 to destroy`

<details><summary>Changes</summary>

- aws_security_group (service_sg)
  Destroying security group and 2 ingress rules

- aws_iam_role (service_role)
  Removing IAM role for service

- aws_lambda_function (service_handler)
  Removing Lambda function deployment

</details>

<details><summary>Plan output</summary>
<p>

```hcl
EOF

# Append the complete plan output (verbatim, unmodified)
cat /tmp/plan_output.txt >> /tmp/pr_comment.txt

cat >> /tmp/pr_comment.txt << 'EOF'
```

</p>
</details>

---

## Important Note

**The terraform destroy must be executed from the `master` branch, not from the [CURRENT_BRANCH_NAME] branch.** If applied from the current branch, it will fail with:

```
Error: Provider configuration not present
```

This occurs because the [CURRENT_BRANCH_NAME] branch contains the changes that remove the module configuration, preventing Terraform from initializing the provider for that module.

**Steps to apply:**
1. Checkout `master` branch
2. Run: `terraform destroy -var-file=env.tfvars -target='module.service'` from the `environment/prd` directory
3. Merge this PR to `master`.
EOF

# Step 5 — preview
cat /tmp/pr_comment.txt

# Step 6 — publish (after user confirmation)
gh pr comment 42 --body-file /tmp/pr_comment.txt
```
