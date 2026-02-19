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
