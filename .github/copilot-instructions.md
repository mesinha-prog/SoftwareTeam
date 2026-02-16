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

**At EVERY handover between agents, you MUST:**

1. **STOP** - Do not silently continue to the next agent
2. **Commit and push** all work to the branch
3. **Ask the user**:
   > "My work as [Agent Name] is complete. Before handing over to [Next Agent]:
   > - Would you like me to **create a PR** for review?
   > - Or should I **continue directly** to [Next Agent]?"
4. **Wait for user response** - Do NOT assume the answer
5. **If user wants PR**: Create it using `gh pr create`, then wait for approval
6. **If user says continue**: Proceed to next agent

**NEVER skip this step. This is the #1 failure mode observed during testing.**

**NEVER ask the user to create a PR manually.** You MUST create it yourself using `gh pr create`. If it fails, troubleshoot in this order: (1) `gh auth status` — fix auth, (2) `gh repo set-default OWNER/REPO` — set repo context, (3) `git remote -v` — verify remotes. Do NOT give up and ask the user to do it.

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
