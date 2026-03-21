# OpenAI (GPT-4) Setup Guide

**Best for**: General purpose, most popular, wide ecosystem support

## Step 1: Get Your API Key

1. Go to https://platform.openai.com/api-keys
2. Create an account (or sign in)
3. Click **Create new secret key**
4. Give it a name (e.g., "SoftwareTeam")
5. Copy the key (starts with `sk-...`)

## Step 2: Set Environment Variables

**On Mac/Linux:**
```bash
echo 'export LLM_PROVIDER="openai"' >> ~/.bashrc
echo 'export LLM_API_KEY="your-openai-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**On Windows (PowerShell as Administrator):**
```powershell
[Environment]::SetEnvironmentVariable("LLM_PROVIDER", "openai", "User")
[Environment]::SetEnvironmentVariable("LLM_API_KEY", "your-openai-key-here", "User")
$env:LLM_PROVIDER = "openai"
$env:LLM_API_KEY = "your-openai-key-here"
```

## Step 3: Configure GitHub Secrets (for automated reviews)

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add these secrets:
   - Name: `LLM_PROVIDER`, Value: `openai`
   - Name: `LLM_API_KEY`, Value: your OpenAI API key

## Model Information

- **Model**: GPT-4o
- **Cost**: $$ (Moderate)
- **Strengths**: Fast, versatile, good for most tasks

## Verification

```bash
# Verify setup
echo "LLM_PROVIDER=$LLM_PROVIDER"
echo "LLM_API_KEY is set: $([ -n "$LLM_API_KEY" ] && echo 'Yes' || echo 'No')"
```

You're ready to use OpenAI! Return to [Quick Start Guide](../../QUICK-START.md).
