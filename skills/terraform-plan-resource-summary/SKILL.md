---
name: terraform-plan-resource-summary
description: |
  Invoke whenever the user has a Terraform or Terragrunt plan (a plan text log, a saved plan file, or plan output pasted into the conversation) and wants a readable summary/documentation of what resources it will touch — create, change, or destroy. Trigger on phrases like "documentame los recursos que se van a crear", "summarize this terraform plan", "que recursos crea este plan", "list every resource this plan will add/change/destroy", "make a report of this plan", or when the user points at a plan log file and asks what it does. Also trigger when the user wants that summary saved to a file (any format they name — markdown, txt, etc.).

  Works on plans of any size, including huge ones (100+ resources) where scrolling through raw terraform output isn't practical — the goal is a structured, grouped-by-module report instead of a wall of `+`/`~`/`-` diffs.

  Do NOT invoke for: publishing/posting a plan as a GitHub PR comment (that's github-terraform-publish-plan), actually running `terraform plan`/`apply`/`destroy` (never execute terraform commands — always ask the user for the plan output per the user's global CLAUDE.md instructions), reviewing whether a plan is safe or correct from an architecture standpoint, or explaining a single specific resource diff in isolation.
license: MIT
metadata:
  author: Daniel Gamboa Estrada
  version: "0.1.0"
  category: infrastructure
  tags:
    - terraform
    - terragrunt
    - infrastructure
    - documentation
    - aws
---

# Terraform Plan Resource Summary

You are turning a raw `terraform plan` (or `terragrunt plan`) text log into a structured, human-readable Markdown report of every resource the plan will touch. Plans on real infrastructure are often hundreds of resources deep across nested modules — nobody wants to scroll a 10,000-line diff to answer "what is this actually going to do?". Your job is to answer that question clearly, grouped in a way a reviewer can actually scan.

**Important:** never run `terraform plan` yourself. Per the user's global instructions, terraform commands are always executed by the user — ask them for the plan output/file if you don't already have one.

## Step 1 — Locate the plan

The user will usually give you a file path (a saved plan log, a CI artifact download, something in `Downloads/`). If they instead paste plan output directly into the chat, save it to a temp file first (e.g. `/tmp/plan.txt`) so the script below can read it.

## Step 2 — Run the parser script

Use the bundled script — it does the regex/grouping work deterministically, which is both faster and more reliable than reading a huge file yourself token by token:

```bash
python3 <skill-dir>/scripts/parse_plan.py <plan-file> -o <output-file>.md
```

This produces a Markdown report with:
- A summary line (`X to add, Y to change, Z to destroy`, matching Terraform's own summary — sanity-check that your output totals agree with it)
- One section per action: **A crear**, **A reemplazar** (destroy+create, e.g. resources with `replace_triggered_by`), **A modificar (in-place)**, and **Se leera durante apply** (values not yet known — these show up when a plan depends on other unapplied changes)
- Within each section, resources grouped by top-level service/module, then by nested module path — this mirrors how the plan's own module tree is organized, so a reviewer can jump straight to "what changes in the API service" vs "what changes in the SSO service"
- A totals-by-resource-type table at the end (handy for spotting "oh, this plan creates 39 new secrets" at a glance)

If the script errors with "no se encontraron bloques de recursos", double check the file is actually plan output (has `# module... will be created` style comment lines and a `Plan: ... to add` summary) and not, say, an apply log or something unrelated.

## Step 3 — Decide where the output goes

- If the user named a specific destination file, write there — but if that file already contains something unrelated (e.g. it *is* the original plan log, not a report), stop and ask before overwriting; don't silently destroy their raw plan output.
- If they didn't name a destination, default to a `.md` file in the current working directory (e.g. `plan-resources-summary.md`), matching how this user's other documentation ends up saved.
- Never write the report back into the original plan log file itself unless the user explicitly confirms that's what they want.

## Step 4 — Sanity check and hand off

Before telling the user it's done:
- Compare the script's `to add`/`to change`/`to destroy` counts against the raw `Plan: ...` line in the source file — they should match exactly (the section counts inside "to change" split into replace + update in-place, so add those two together when checking).
- Skim a couple of module groups to make sure names look sensible (e.g. a nested module path shouldn't just say "module" — the script strips the literal `module.` keyword and keeps the actual module names).
- Report back concisely: totals, where the file was saved, and anything notable worth flagging (e.g. "this creates N new secrets", "3 resources will be destroyed and recreated because of X").

## Notes on the parser's scope

The script recognizes standard Terraform provider resource-type prefixes (`aws_*`, `random_*`, `mongodbatlas_*`, `ultradns_*`, `akamai_*`, `terraform_data`, `null_resource`, `time_*`). If a plan uses a provider not in that list, resource paths for that provider won't split into module/resource correctly — in that case, either add the prefix to `TYPE_RE` in the script (quick fix, one line) or fall back to summarizing that provider's resources manually by reading the relevant `# ... will be ...` lines directly.
