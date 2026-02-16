# Claude Code Instructions

**CRITICAL**: Before doing ANY task, you MUST follow the agentic workflow defined in this repository.

## Mandatory First Steps

1. **READ `AI-WORKFLOW.md`** - This is your primary reference for the complete workflow, protocols, and reading order
2. **Follow the reading order defined in AI-WORKFLOW.md** - It tells you which agent file to read at each step

## Agentic Workflow (ALWAYS FOLLOW)

When a user gives you ANY task (feature, bug fix, question, etc.), follow the steps in `AI-WORKFLOW.md`. Summary:

1. **IT Agent** (FIRST) → Verify & install `git` and `gh` CLI, authenticate `gh`
2. **Product Owner** → Clarify requirements, create user story
3. **Cost Analyst** → Estimate total task cost, warn if expensive (advisory)
4. **Architect** → Technical design, choose tech stack
5. **IT Agent** (Setup) → Install prerequisites + project dependencies, set up scripts/
6. **Developer** → Implement in modules/
7. **Tester** → Validate implementation
8. **IT Agent** (Release) → Build artifacts
9. **Product Owner** (Acceptance) → Review and present to user

### MANDATORY HANDOVER PROTOCOL (CRITICAL - DO NOT SKIP)

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

See `AI-WORKFLOW.md` for the full Handover Protocol, PR Creation Process, and Common Agent Protocols.

## Git Workflow (ALWAYS FOLLOW)

### Task-Based Branching Strategy

When user gives ANY new task, Product Owner MUST:

1. **Create a task master branch** from `template/agentic-workflow`:
   ```bash
   git checkout template/agentic-workflow
   git checkout -b master_{task_name}
   git push -u origin master_{task_name}
   ```

2. **All agents branch from the task master branch** (NOT main/master):
   ```bash
   git checkout master_{task_name}
   git checkout -b claude/{agent}-{task_name}-{sessionID}
   ```

3. **All PRs go to the task master branch** (NOT main/master)

### Branch Naming Convention

- **Task master branch**: `master_{task_name}`
- **Agent branches**: `claude/{agent}-{task_name}-{sessionID}`

## Agent Role Files

Read these files to understand each role:
- `ai-assistants/agents/product-owner-agent.md` - Requirements & coordination
- `ai-assistants/agents/architect-agent.md` - Design & architecture
- `ai-assistants/agents/developer-agent.md` - Implementation
- `ai-assistants/agents/tester-agent.md` - Quality assurance
- `ai-assistants/agents/it-agent.md` - Infrastructure & releases
- `ai-assistants/agents/cost-analyst-agent.md` - Cost estimation

## Output Locations

- User stories: `project-management/tasks/backlog/`
- Technical designs: `project-management/designs/`
- Code: `modules/[module-name]/`
- Tests: `modules/[module-name]/test/`
- Build output: `output/`

## REMEMBER

- **IT Agent runs FIRST** - Verify git & gh CLI before anything else
- **NEVER skip Product Owner** - After IT Agent, always go to Product Owner
- **NEVER code without design** - Architect designs first
- **ALWAYS follow the Handover Protocol** - At every agent transition
- **ALWAYS update domain info** - Keep template customized for the project
- **ALWAYS read `AI-WORKFLOW.md`** - It is the source of truth for all protocols
