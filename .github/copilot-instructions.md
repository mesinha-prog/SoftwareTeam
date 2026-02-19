# GitHub Copilot Instructions

**CRITICAL**: You MUST follow the multi-agent agentic workflow defined in this repository.

---

## MANDATORY FIRST STEPS

1. **READ `AI-WORKFLOW.md`** - This is your primary reference for the complete workflow, protocols, and reading order
2. **Follow the reading order defined in AI-WORKFLOW.md** - It tells you which agent file to read at each step

### Mandatory Files to Reference

| File | Purpose |
|------|---------|
| `AI-WORKFLOW.md` | Complete workflow instructions (START HERE) |
| `ai-assistants/agents/product-owner-agent.md` | Requirements & coordination role |
| `ai-assistants/agents/architect-agent.md` | Design responsibilities |
| `ai-assistants/agents/developer-agent.md` | Implementation rules |
| `ai-assistants/agents/it-agent.md` | Infrastructure rules (NO application code!) |
| `ai-assistants/agents/tester-agent.md` | Testing rules |
| `ai-assistants/agents/cost-analyst-agent.md` | Cost estimation |

---

## AGENTIC WORKFLOW (ALWAYS FOLLOW)

For ANY user task, follow the steps defined in `AI-WORKFLOW.md`. Summary:

1. **IT Agent** (FIRST) → Verify & install `git` and `gh` CLI, authenticate `gh`
2. **Product Owner** → Clarify requirements, create user story
3. **Cost Analyst** → Estimate total task cost, warn if expensive (advisory)
4. **Architect** → Technical design, choose tech stack
5. **IT Agent** (Setup) → Install prerequisites + project dependencies, set up scripts/
6. **Developer** → Implement in modules/
7. **Tester** → Validate implementation
8. **IT Agent** (Release) → Build artifacts
9. **Product Owner** (Acceptance) → Review and present to user

---

## MANDATORY HANDOVER PROTOCOL (CRITICAL - DO NOT SKIP)

**When you finish your work as an agent, follow the handover rules for your current role.**

**Creating a PR when the user requests one:**
Create it yourself using gh pr create. Never ask the user to create it manually. If it fails, troubleshoot in this order: check gh auth status, then run gh repo set-default OWNER/REPO, then verify git remote -v.

**IT Agent after verifying git and gh tools:**
Continue directly to Product Owner. No need to ask the user.

**Product Owner after creating the user story:**
Continue directly to Cost Analyst. No need to ask the user.

**Cost Analyst after completing the cost estimate:**
Report the cost estimate to the user. If the user approves, continue directly to Architect.

**Architect after completing the design:**
Stop. Commit and push your work. Ask the user: "Would you like me to create a PR for review, or continue directly to IT Agent for project setup?" Wait for the user's response before proceeding.

**IT Agent after setting up the project:**
Stop. Commit and push your work. Ask the user: "Would you like me to create a PR for review, or continue directly to Developer?" Wait for the user's response before proceeding.

**Developer after completing the implementation:**
Stop. Commit and push your work. Provide the one-line command to run the app. Ask the user: "Would you like me to create a PR for review, or continue directly to Tester?" Wait for the user's response before proceeding.

**Tester after completing validation:**
Stop. Commit and push your work. Provide the one-line command to run the tests. Ask the user: "Would you like me to create a PR for review, or continue directly to IT Agent for release?" Wait for the user's response before proceeding.

**IT Agent after building the release:**
Stop. Commit and push your work. Ask the user: "Would you like me to create a PR for review, or continue directly to Product Owner for acceptance?" Wait for the user's response before proceeding.

**Product Owner for acceptance:**
Present the completed work to the user with the run and test commands. Ask the user to review and accept.

### PR Creation (when user requests it)

```bash
# Commit, push, and create PR
git add -A
git commit -m "[Agent Name] Description of completed work"
git push -u origin copilot/{agent}-{task_name}-{sessionID}

# Ensure repo context is set (CRITICAL — prevents "could not determine repo" errors)
gh repo set-default $(git remote get-url origin | sed -E 's#.*[:/]([^/]+/[^/.]+)(\.git)?$#\1#')

gh pr create \
  --base master_{task_name} \
  --head copilot/{agent}-{task_name}-{sessionID} \
  --title "[Agent Name] Work description" \
  --body "## Summary
[What was accomplished]

## Changes
- [Change 1]
- [Change 2]

## Ready for
[Next Agent Name]"
```

**If PR creation fails**, run these troubleshooting steps:
```bash
gh auth status                    # 1. Check authentication
gh repo set-default OWNER/REPO   # 2. Set repository context
git remote -v                     # 3. Verify remotes point to your fork
git push -u origin $(git branch --show-current)  # 4. Ensure branch is pushed
```

---

## GIT WORKFLOW

### Task-Based Branching
- Task master: `master_{task_name}` from `template/agentic-workflow`
- Agent branches: `copilot/{agent}-{task_name}-{sessionID}`
- All PRs to `master_{task_name}` (NOT main/master)

### Branch Creation
```bash
# 1. Create task master branch
git checkout template/agentic-workflow
git checkout -b master_{task_name}
git push -u origin master_{task_name}

# 2. Create agent working branch
git checkout -b copilot/{agent}-{task_name}-{sessionID}
```

---

## SWITCHING BETWEEN AGENTS

When switching to a different agent role, announce it clearly:

```
---
SWITCHING TO: [Agent Name] Agent
REASON: [Why switching]
---

[Now acting as Agent Name]
[Continue with agent-specific work]
```

---

## COPILOT-SPECIFIC NOTES

1. **Enable instruction files**: Ensure `github.copilot.chat.codeGeneration.useInstructionFiles` is `true` in VS Code settings (see `.vscode/settings.json`)
2. **Manual agent transitions**: Explicitly tell Copilot which agent role to adopt
3. **Context limitations**: Keep relevant agent file open for context
4. **PR creation**: Use `gh` CLI commands

### Prompting Copilot for Agent Roles

- "Act as the Product Owner agent and create a user story for [feature]"
- "Act as the Architect agent and design the technical solution for [user story]"
- "Act as the IT Agent and set up the build environment (DO NOT write application code)"
- "Act as the Developer agent and implement [feature] according to the architect's design"
- "Act as the Tester agent and validate the implementation"

---

## CRITICAL RULES - NEVER VIOLATE

1. **IT Agent runs FIRST** - Verify git & gh CLI before anything else
2. **Then Product Owner** - For ANY new user request (after IT Agent)
3. **ALWAYS follow the Handover Protocol** - At every agent transition
3. **ALWAYS read `AI-WORKFLOW.md`** - It is the source of truth for all protocols
4. **NEVER let IT Agent write application code** - Only infrastructure!
5. **NEVER work on main/master directly** - Use task branches
6. **NEVER skip an agent** - Follow the complete workflow

---

**For complete workflow details, protocols, and PR processes, see `AI-WORKFLOW.md`**
