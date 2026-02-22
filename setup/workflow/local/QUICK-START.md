# Quick Start Guide (Local Mode)

Welcome! This guide will help you set up the AI-assisted workflow.

**No programming experience required.**
**No GitHub account or git installation required.**

Everything runs locally on your computer.

---

## Choose Your Path

Pick ONE path based on which AI tool you want to use:

| Path | AI Tool | Best For | Difficulty | Setup Guide |
|------|---------|----------|------------|-------------|
| **Path A** | Claude Code + Anthropic | Software projects | Easy (CLI) | [Setup Guide](quickstart/tools/claude-code-setup.md) |
| **Path B** | Cursor IDE | Beginners, visual | Easiest (GUI) | [Setup Guide](quickstart/tools/cursor-setup.md) |
| **Path C** | Windsurf IDE | Beginners, visual | Easiest (GUI) | [Setup Guide](quickstart/tools/windsurf-setup.md) |
| **Path D** | Aider + Gemini | Budget-conscious | Easy (CLI) | [Setup Guide](quickstart/tools/aider-gemini-setup.md) |
| **Path E** | Aider + OpenAI | GPT-4 users | Easy (CLI) | [Setup Guide](quickstart/tools/aider-openai-setup.md) |
| **Path F** | Continue + VS Code | VS Code users | Easy (Extension) | [Setup Guide](quickstart/tools/continue-setup.md) |
| **Path G** | GitHub Copilot | Copilot subscribers | Easiest (GUI) | [Setup Guide](quickstart/tools/github-copilot-setup.md) |

**Recommended**:
- **Path A** (Claude Code) for best software development experience
- **Path B** (Cursor) or **Path C** (Windsurf) for the easiest visual experience

**Click on your chosen setup guide above** for detailed installation and configuration instructions.

---

## LLM Provider Setup

Your AI tool needs an API key to work. Choose your provider:

| Provider | Cost | Best For |
|----------|------|----------|
| **Anthropic (Claude)** | Pay per use | Best for software projects (recommended) |
| **Google (Gemini)** | Pay per use | Google ecosystem, budget-friendly |
| **OpenAI (GPT-4)** | Pay per use | General coding |

### Get Your API Key

1. **Anthropic**: Go to https://console.anthropic.com/
2. **Google Gemini**: Go to https://aistudio.google.com/ --> Click "Get API Key"
3. **OpenAI**: Go to https://platform.openai.com/api-keys

### Save Your API Key

**On Mac/Linux:**
```bash
# For Anthropic:
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc

# For Google Gemini:
echo 'export GOOGLE_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc

# For OpenAI:
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**On Windows (PowerShell as Administrator):**
```powershell
# For Anthropic:
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "your-key-here", "User")

# For Google Gemini:
[Environment]::SetEnvironmentVariable("GOOGLE_API_KEY", "your-key-here", "User")

# For OpenAI:
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-key-here", "User")
```

---

## After Setup: How the Agentic Workflow Works

Once you are set up, the AI follows a structured workflow:

```
You describe what you want
         |
   Product Owner
   (Understands your request, creates plan)
         |
      Architect
   (Designs the solution)
         |
      Developer
   (Writes the code)
         |
       Tester
   (Validates it works)
         |
   Product Owner
   (Reviews and presents to you)
```

**Important**: The AI will automatically:
1. Start as **Product Owner** to understand your request
2. Update project documentation with your domain info
3. Follow the complete workflow for quality results
4. Save work and present for your review at each step

---

## Example Requests

Just describe what you want in plain English!

**Building something new:**
> "I want to create a simple todo list application where users can add, complete, and delete tasks"

**Adding a feature:**
> "Add a search feature so users can find items by name"

**Fixing a problem:**
> "Users are reporting that the save button doesn't work on mobile devices"

**Understanding the code:**
> "Explain how the login system works"

---

## Quick Reference

| What you want | What to say |
|---------------|-------------|
| Build new feature | "Create a [feature] that does [what]" |
| Fix a bug | "Fix the issue where [problem]" |
| Understand code | "Explain how [feature] works" |
| Improve something | "Make [feature] faster/better/simpler" |
| Add tests | "Add tests for [feature]" |

---

## Project Structure

```
your-project/
├── CLAUDE.md             <- AI workflow instructions (Claude Code)
├── .cursorrules          <- AI workflow instructions (Cursor)
├── .windsurfrules        <- AI workflow instructions (Windsurf)
├── .continuerules        <- AI workflow instructions (Continue)
├── .aider.conf.yml       <- AI workflow instructions (Aider)
│
├── ai-assistants/        <- AI configuration
├── project-management/   <- Documentation and tasks
│   └── tasks/backlog/    <- User stories go here
├── modules/              <- Your software code
├── scripts/              <- Build, test, run scripts
├── output/               <- Built software
```

---

## Troubleshooting

### "API key not found" error
- Make sure you saved the key correctly
- Close and reopen your terminal
- Check for extra spaces in the key

### "Command not found" error
- Make sure you installed the tool
- Close and reopen your terminal
- On Windows, run as Administrator

### AI doesn't follow the workflow
- The AI config files (CLAUDE.md, .cursorrules, etc.) instruct the AI
- If issues persist, tell the AI: "Please follow the workflow guide" (this is the provider file: CLAUDE.md, .cursorrules, etc.)

### AI gives wrong answers
- Be more specific in your request
- Provide examples of what you want
- Break big requests into smaller steps

### Need more help?
- See `ai-assistants/how-to-use.md` for detailed guide
- See your AI tool's workflow guide (CLAUDE.md, .cursorrules, etc.) for full workflow documentation

---

## Cost Awareness

Using AI APIs costs money per request.

**Approximate costs:**
- Simple question: ~$0.01
- Small feature: ~$0.10
- Large feature: ~$1.00+

The **Cost Analyst** agent will warn you before expensive operations.
