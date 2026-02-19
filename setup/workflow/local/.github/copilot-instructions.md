# GitHub Copilot Instructions (Local Mode)

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

1. **Product Owner** (FIRST) → Clarify requirements, create user story
2. **Cost Analyst** → Estimate total task cost, warn if expensive (advisory)
3. **Architect** → Technical design, choose tech stack
4. **IT Agent** (Setup) → Install prerequisites + project dependencies, set up scripts/
5. **Developer** → Implement in modules/
6. **Tester** → Validate implementation
7. **IT Agent** (Release) → Build artifacts
8. **Product Owner** (Acceptance) → Review and present to user

---

## MANDATORY HANDOVER PROTOCOL (CRITICAL - DO NOT SKIP)

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

### Prompting Copilot for Agent Roles

- "Act as the Product Owner agent and create a user story for [feature]"
- "Act as the Architect agent and design the technical solution for [user story]"
- "Act as the IT Agent and set up the project dependencies (DO NOT write application code)"
- "Act as the Developer agent and implement [feature] according to the architect's design"
- "Act as the Tester agent and validate the implementation"

---

## CRITICAL RULES - NEVER VIOLATE

1. **Product Owner runs FIRST** - For ANY new user request
2. **ALWAYS follow the Handover Protocol** - At every agent transition
3. **ALWAYS read `AI-WORKFLOW.md`** - It is the source of truth for all protocols
4. **NEVER let IT Agent write application code** - Only infrastructure!
5. **NEVER skip an agent** - Follow the complete workflow

---

**For complete workflow details, protocols, and processes, see `AI-WORKFLOW.md`**
