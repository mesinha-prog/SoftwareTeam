# Claude Code Instructions (Local-Only Mode)

**CRITICAL**: Before doing ANY task, you MUST follow the agentic workflow defined in this repository.

## Mandatory First Steps

1. **READ `AI-WORKFLOW.md`** - This is your primary reference for the complete workflow, protocols, and reading order
2. **Follow the reading order defined in AI-WORKFLOW.md** - It tells you which agent file to read at each step

## Agentic Workflow (ALWAYS FOLLOW)

When a user gives you ANY task (feature, bug fix, question, etc.), follow the steps in `AI-WORKFLOW.md`. Summary:

1. **Product Owner** (FIRST) -> Clarify requirements, create user story
2. **Cost Analyst** -> Estimate total task cost, warn if expensive (advisory)
3. **Architect** -> Technical design, choose tech stack
4. **IT Agent** (Setup) -> Install prerequisites + project dependencies, set up scripts/
5. **Developer** -> Implement in modules/
6. **Tester** -> Validate implementation
7. **IT Agent** (Release) -> Build artifacts
8. **Product Owner** (Acceptance) -> Review and present to user

### MANDATORY HANDOVER PROTOCOL (CRITICAL - DO NOT SKIP)

**When you finish your work as an agent, follow the handover rules for your current role.**

**IT Agent after verifying tools and dependencies:**
Continue directly to Product Owner. No need to ask the user.

**Product Owner after creating the user story:**
Continue directly to Cost Analyst. No need to ask the user.

**Cost Analyst after completing the cost estimate:**
Report the cost estimate to the user. If the user approves, continue directly to Architect.

**Architect after completing the design:**
Stop. Save all work. Ask the user: "Would you like to review my work, or continue directly to IT Agent for project setup?" Wait for the user's response before proceeding.

**IT Agent after setting up the project:**
Stop. Save all work. Ask the user: "Would you like to review my work, or continue directly to Developer?" Wait for the user's response before proceeding.

**Developer after completing the implementation:**
Stop. Save all work. Provide the one-line command to run the app. Ask the user: "Would you like to review my work, or continue directly to Tester?" Wait for the user's response before proceeding.

**Tester after completing validation:**
Stop. Save all work. Provide the one-line command to run the tests. Ask the user: "Would you like to review my work, or continue directly to IT Agent for release?" Wait for the user's response before proceeding.

**IT Agent after building the release:**
Stop. Save all work. Ask the user: "Would you like to review my work, or continue directly to Product Owner for acceptance?" Wait for the user's response before proceeding.

**Product Owner for acceptance:**
Present the completed work to the user with the run and test commands. Ask the user to review and accept.

See `AI-WORKFLOW.md` for the full Handover Protocol and Common Agent Protocols.

## Agent Role Files

Read these files to understand each role:
- `ai-assistants/agents/product-owner-agent.md` - Requirements & coordination
- `ai-assistants/agents/architect-agent.md` - Design & architecture
- `ai-assistants/agents/developer-agent.md` - Implementation
- `ai-assistants/agents/tester-agent.md` - Quality assurance
- `ai-assistants/agents/it-agent.md` - Project dependencies & releases
- `ai-assistants/agents/cost-analyst-agent.md` - Cost estimation

## Output Locations

- User stories: `project-management/tasks/backlog/`
- Technical designs: `project-management/designs/`
- Code: `modules/[module-name]/`
- Tests: `modules/[module-name]/test/`
- Build output: `output/`

## REMEMBER

- **Product Owner runs FIRST** - Gather requirements before anything else
- **NEVER code without design** - Architect designs first
- **ALWAYS follow the Handover Protocol** - At every agent transition
- **ALWAYS update domain info** - Keep template customized for the project
- **ALWAYS read `AI-WORKFLOW.md`** - It is the source of truth for all protocols
