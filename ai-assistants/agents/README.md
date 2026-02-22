# AI Agent System

This directory contains agent role definitions for the multi-agent workflow. These definitions work with **any LLM provider** and **any AI coding tool**.

## Supported AI Tools

| Tool | Provider(s) | Setup |
|------|-------------|-------|
| Claude Code | Anthropic | Reads `CLAUDE.md` automatically |
| GitHub Copilot | GitHub/OpenAI | Reads `.github/copilot-instructions.md` via `.vscode/settings.json` |
| Cursor | OpenAI, Anthropic | Reads `.cursorrules` automatically |
| Windsurf | Multiple | Reads `.windsurfrules` automatically |
| Continue | Multiple | Reads `.continuerules` automatically |
| Aider | OpenAI, Anthropic, Ollama | Configure in `.aider.conf.yml` |
| Any CLI | Any provider | Read these files as context |

## Agent Files

- **`product-owner-agent.md`**: Customer-Facing Requirements Lead - gathers requirements, creates user stories, coordinates agents
- **`architect-agent.md`**: Design Agent - creates technical specifications, designs, enriches tasks with details
- **`developer-agent.md`**: Implementation Agent - writes code and unit tests
- **`tester-agent.md`**: QA Agent - validates quality and reports bugs
- **`it-agent.md`**: Infrastructure Agent - manages builds, releases, CI/CD
- **`cost-analyst-agent.md`**: Resource Analyst - estimates token costs and warns before expensive operations

## How It Works

1. **AI reads agent definitions** from this directory
2. **Analyzes your request** to understand the task type
3. **Adopts the appropriate agent role** based on activation triggers
4. **Follows that role's responsibilities and workflow**
5. **Hands off to other agents** as needed

## Role Clarification

| Role | Primary Responsibility | Focus |
|------|------------------------|-------|
| **Product Owner** | User communication, requirements, user stories | WHAT to build |
| **Architect** | Technical design, specifications, enriches tasks | HOW to build |
| **Developer** | Code implementation, unit testing | Build it |
| **Tester** | Quality validation, test planning, bug reporting | Verify it |
| **IT** | Build systems, releases, infrastructure | Ship it |
| **Cost Analyst** | Token estimation, cost warnings, usage tracking | Cost awareness |

## Key Distinction: Product Owner vs Architect

| Aspect | Product Owner | Architect |
|--------|---------------|-----------|
| **Focus** | WHAT to build | HOW to build |
| **Language** | Business terms, user needs | Technical terms, patterns |
| **Tasks** | High-level user stories | Detailed technical specs |
| **Example** | "Users need to login" | "Use OAuth2 with IAuthService" |

## Example Workflows

### Creating a New Feature
1. **Product Owner**: Receives request → Creates user story with acceptance criteria
2. **Architect**: Enriches with technical design → Creates detailed tasks
3. **Product Owner**: Assigns implementation tasks to Developer
4. **Developer**: Implements code → Writes unit tests
5. **Tester**: Validates → Reports issues → Approves
6. **IT**: Creates release

### Fixing a Bug
1. **Product Owner**: Receives bug report → Documents issue
2. **Tester**: Investigates and documents details
3. **Developer**: Fixes code → Updates tests
4. **Tester**: Verifies fix → Approves

### Expensive Operation
1. **Cost Analyst**: Estimates token usage for task
2. **Cost Analyst**: Warns user if cost exceeds threshold
3. **User**: Approves or modifies scope
4. **Agents**: Proceed with work

## Agent Collaboration

Agents work together through handoffs:
- **Product Owner** gathers requirements and coordinates agents
- **Architect** enriches tasks with technical specifications
- **Developer** implements based on Architect's specs
- **Tester** validates Developer's work
- **IT** provides infrastructure to all
- **Cost Analyst** monitors resource usage across all agents

## Customizing for Your AI Tool

### For Aider
Add to `.aider.conf.yml`:
```yaml
read:
  - ai-assistants/agents/product-owner-agent.md
  - ai-assistants/agents/architect-agent.md
  - ai-assistants/agents/developer-agent.md
  - ai-assistants/agents/tester-agent.md
  - ai-assistants/agents/it-agent.md
  - ai-assistants/agents/cost-analyst-agent.md
```

### For Cursor
Add to `.cursorrules`:
```
Read and follow the agent role definitions in the ai-assistants/agents/ directory.
When working on tasks, adopt the appropriate agent role based on the task type.
```

### For Other Tools
Include agent files as context or system prompts.

## Modifying Agent Behavior

Edit the `.md` files to customize:
- **Role**: Agent's primary function
- **Domain Expertise**: Your project's domain knowledge (CUSTOMIZE THIS)
- **Responsibilities**: What the agent does
- **Output Locations**: Where work is stored
- **Handoffs**: How agents interact
- **Workflow**: Step-by-step processes
- **Activation Triggers**: When to use this agent

## Domain Customization

Each agent has a section marked:
```
**CUSTOMIZE THIS SECTION**
```

Replace with your project's domain expertise (healthcare, finance, e-commerce, etc.).

## Documentation

See your AI tool's workflow guide (CLAUDE.md, .cursorrules, etc.) for full workflow documentation.
