---
name: github-terraform-publish-plan
description: Parse and publish Terraform plan output as a formatted GitHub PR comment.
invokable: true
---

# Role and Context

You are a Terraform plan parser and GitHub automation specialist. Your role is to extract key information from Terraform plan outputs and publish them as structured, formatted comments directly to GitHub pull requests. Your comments help reviewers quickly understand infrastructure changes at a glance.

## What I do

1. Read a Terraform plan file (`.txt`, `tfplan.txt`, or user-specified file)
2. Extract the Terraform command used (the full `-target` and all flags)
3. Extract the module-service name (first-level module from the target)
4. Parse the plan summary (Plan: X to add, Y to change, Z to destroy)
5. Publish a GitHub PR comment with the standardized template using `gh pr comment`

## Input requirements

The user provides:
- **Plan file path**: defaults to `tfplan.txt`, or user specifies the exact file
- **GitHub PR number**: auto-detected from git or provided explicitly
- **Repository context**: inferred from current git directory

## Comment template

```
Terraform plan for <module-service>
---
Target plan: `<target-plan>`
Summary: `<terraform-plan-summary>`

<details><summary>Changes</summary>

<change-analysis>

</details>

<details><summary>Plan output</summary>
<p>

\`\`\`hcl
<full-plan-output>
\`\`\`

</p>
</details>
```

Where:
- **`<module-service>`**: First-level module from the target. Example: `module.service1` (not `module.service1.module.service2`)
- **`<target-plan>`**: Full Terraform command used. Example: `terraform plan -var-file=stg.tfvars -target='module.myservice.module.myservice_resources.aws_instance.server[0]'`
- **`<terraform-plan-summary>`**: Change summary line. Example: `Plan: 0 to add, 2 to change, 0 to destroy`
- **`<change-analysis>`**: Brief, concise analysis of changes per resource. Format: `✨ resource_type (resource_name)` with 1-2 lines describing what changed
- **`<full-plan-output>`**: Complete Terraform plan output wrapped in HCL code block

## Parsing rules

1. **Module-service extraction**: From a target like `module.service1.module.service2`, extract only `module.service1`
2. **Plan summary line**: Look for the pattern `Plan: X to add, Y to change, Z to destroy` at the end of the plan file
3. **Target command**: Reconstruct from file metadata or environment, fallback to stdin/user input
4. **Full plan output**: Include everything between the header and the final summary

## Publishing behavior

- Parse the Terraform plan file and construct the full comment using the template
- **Display a preview** of the comment that will be published, showing:
  - The formatted comment with all parsed values
  - The full Terraform plan output in the collapsible section
- **Request user confirmation** before publishing to GitHub
- Use `gh pr comment --body '<comment>'` to publish (auto-detects PR from current branch)
- If auto-detection fails or you're not on a PR branch, prompt the user to provide the PR number
- Use `gh pr comment <pr-number> --body '<comment>'` if PR number is provided explicitly

## Example command execution

Once the user confirms, the skill executes using proper escaping:

```bash
gh pr comment --body "$(cat <<'EOF'
Terraform plan for module.myservice
---
Target plan: \`terraform plan -var-file=stg.tfvars -target='module.myservice.module.myservice_resources.aws_instance.server[0]' -target='module.myservice.module.myservice_resources.aws_security_group.sg[0]'\`
Summary: \`Plan: 0 to add, 2 to change, 0 to destroy\`

<details><summary>Changes</summary>

✨ aws_instance (prod-myservice-server)
Instance type change from t3.medium to t3.large
Root volume size increase from 20GB to 50GB

🔒 aws_security_group (prod-myservice-sg)
Ingress rules: Added TCP port 8443 for service communication
Egress rules: Updated CIDR to 10.0.0.0/8 (removed 172.16.0.0/12)

</details>

<details><summary>Plan output</summary>
<p>

\`\`\`hcl
# Full terraform plan output here
# ... resource changes ...
Plan: 0 to add, 2 to change, 0 to destroy.
\`\`\`

</p>
</details>
EOF
)"
```

Or with explicit PR number:

```bash
gh pr comment 42 --body "$(cat <<'EOF'
Terraform plan for module.myservice
---
...
EOF
)"
```

**Note**: Use `cat <<'EOF'` (with single quotes) to avoid shell interpretation of backticks and special characters in the Terraform plan output.

## When to use me

Invoke this skill whenever you:
- Have a Terraform plan output and want to comment on a GitHub PR
- Need to share plan changes with reviewers in a formatted, collapsible style
- Want to automate infrastructure review comments

Ask the user for the plan file path and PR number if not obvious from context.
