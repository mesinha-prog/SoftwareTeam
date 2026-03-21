# Setup Guide: Anthropic API Key for Automated Reviews

**Document**: Anthropic API Key Setup
**Project**: SoftwareTeam
**Owner**: IT Agent
**Date**: 2026-01-20

---

## Overview

The automated multi-agent peer review system uses **Claude API** (Anthropic) to perform intelligent code reviews as different agent roles. To enable this, you need to configure an `ANTHROPIC_API_KEY` in your GitHub repository.

---

## Step-by-Step Setup

### Step 1: Obtain Anthropic API Key

1. **Go to Anthropic Console**: https://console.anthropic.com/

2. **Sign In or Create Account**:
   - If you don't have an account, sign up
   - If you have an account, sign in

3. **Navigate to API Keys**:
   - Click on your profile/settings
   - Select "API Keys" or "Keys"

4. **Create New API Key**:
   - Click "Create Key" or "New API Key"
   - Give it a name: `SoftwareTeam-GitHub-Actions`
   - Copy the key (starts with `sk-ant-...`)
   - **⚠️ IMPORTANT**: Save this key securely - you won't be able to see it again!

5. **Verify API Access**:
   - Ensure your account has API access enabled
   - Check your usage limits and billing settings

---

### Step 2: Add API Key to GitHub Repository

1. **Navigate to Repository Settings**:
   - Go to your GitHub repository: https://github.com/{owner}/{repo}
   - Click "Settings" tab (requires admin/owner permissions)

2. **Go to Secrets Section**:
   - In left sidebar, expand "Secrets and variables"
   - Click "Actions"

3. **Create New Repository Secret**:
   - Click "New repository secret" button
   - **Name**: `ANTHROPIC_API_KEY` (exactly this, case-sensitive)
   - **Secret**: Paste your API key (`sk-ant-...`)
   - Click "Add secret"

4. **Verify Secret**:
   - You should see `ANTHROPIC_API_KEY` in the list of repository secrets
   - The value will be hidden (shows as `***`)

---

### Step 3: Configure GitHub Actions Permissions

1. **Still in Repository Settings**:
   - In left sidebar, click "Actions" → "General"

2. **Workflow Permissions**:
   - Scroll down to "Workflow permissions" section
   - Select: **"Read and write permissions"**
   - Check: **"Allow GitHub Actions to create and approve pull requests"**
   - Click "Save"

---

### Step 4: Verify Setup

#### Option A: Test with a Dummy PR

1. **Create a test branch**:
   ```bash
   git checkout -b agent/developer-test-12345
   echo "test" > test.txt
   git add test.txt
   git commit -m "Test: Automated review system"
   git push -u origin agent/developer-test-12345
   ```

2. **Create PR**:
   - Go to GitHub and create PR from `agent/developer-test-12345` to `master`

3. **Check Workflow**:
   - Go to "Actions" tab
   - You should see "Automated Multi-Agent Peer Review" workflow running
   - Wait for completion (2-5 minutes)

4. **Verify Reviews**:
   - Go back to PR
   - You should see 3 review comments:
     - Product Owner Agent Review
     - Architect Agent Review
     - Tester Agent Review
   - Each should have detailed feedback and a decision (APPROVED or CHANGES REQUESTED)

5. **Clean Up**:
   - Close the test PR
   - Delete the test branch

#### Option B: Check Workflow Manually

1. **Go to Actions Tab**:
   - Navigate to repository → Actions

2. **Find Workflow**:
   - Look for "Automated Multi-Agent Peer Review" in workflows list

3. **Run Manually** (if workflow dispatch enabled):
   - Click workflow
   - Click "Run workflow"
   - Select branch and run

4. **Check Logs**:
   - View workflow run logs
   - Should see "Calling Claude API as product-owner..." etc.
   - No API key errors should appear

---

## Troubleshooting

### Error: "ANTHROPIC_API_KEY environment variable is required"

**Cause**: Secret not configured or named incorrectly

**Solution**:
1. Verify secret exists: Settings → Secrets and variables → Actions
2. Verify name is exactly `ANTHROPIC_API_KEY` (case-sensitive)
3. If wrong name, delete and recreate with correct name

---

### Error: "401 Unauthorized" from Anthropic API

**Cause**: Invalid or expired API key

**Solution**:
1. Go to Anthropic Console: https://console.anthropic.com/
2. Verify API key is still valid
3. Create a new API key if needed
4. Update GitHub secret with new key
5. Re-run workflow

---

### Error: "429 Too Many Requests" from Anthropic API

**Cause**: API rate limit exceeded

**Solution**:
1. Wait a few minutes before trying again
2. Check your Anthropic account usage limits
3. Consider upgrading plan if hitting limits frequently

---

### Workflow Doesn't Trigger

**Cause**: Multiple possible causes

**Solutions**:
1. **Check branch name**: Must match `agent/{agent}-{project}-{sessionID}`
2. **Check PR target**: Must target `master` or `main` branch
3. **Check GitHub Actions**: Ensure Actions are enabled (Settings → Actions)
4. **Check permissions**: Verify "Read and write permissions" are enabled

---

### Reviews Not Posting to PR

**Cause**: GitHub token permissions insufficient

**Solution**:
1. Go to: Settings → Actions → General → Workflow permissions
2. Select: "Read and write permissions"
3. Check: "Allow GitHub Actions to create and approve pull requests"
4. Save and re-run workflow

---

## Security Best Practices

### API Key Security

✅ **DO**:
- Store API key in GitHub Secrets (encrypted)
- Use separate API keys for different projects
- Rotate API keys periodically (every 3-6 months)
- Monitor API usage in Anthropic Console
- Revoke keys immediately if compromised

❌ **DON'T**:
- Commit API keys to git repository
- Share API keys in plain text (email, chat)
- Use the same key across multiple projects
- Log API keys in workflow output

### Access Control

- Limit repository admin access (who can view secrets)
- Enable branch protection on `master`
- Require PR reviews before merge
- Monitor Actions workflow runs

---

## Cost Management

### Understanding Costs

Claude API charges based on tokens used:
- **Input tokens**: PR details, prompts, context
- **Output tokens**: Review comments generated

**Typical PR Review**:
- Input: 2000-5000 tokens
- Output: 500-2000 tokens
- Cost per review: ~$0.01-$0.05
- Cost per PR (3 agents): ~$0.03-$0.15

**Monthly Estimate** (50 PRs):
- Total cost: ~$1.50-$7.50/month

### Cost Optimization

1. **Review Large PRs in Batches**:
   - Split large features into smaller PRs
   - Reduces tokens per review

2. **Use Lower-Cost Models** (if needed):
   - Current: `claude-sonnet-4-20250514`
   - Alternative: `claude-haiku-...` (faster, cheaper, less detailed)

3. **Monitor Usage**:
   - Check Anthropic Console regularly
   - Set up usage alerts
   - Review monthly bills

4. **Set Budget Limits**:
   - Configure spending limits in Anthropic Console
   - Receive alerts when approaching limit

---

## API Key Rotation

### When to Rotate

- **Scheduled**: Every 3-6 months
- **Compromised**: Immediately if key is leaked
- **Team Changes**: When team members leave
- **Security Audit**: As part of regular security reviews

### How to Rotate

1. **Create New API Key**:
   - Go to Anthropic Console
   - Create new key with different name

2. **Update GitHub Secret**:
   - Settings → Secrets and variables → Actions
   - Click `ANTHROPIC_API_KEY`
   - Click "Update secret"
   - Paste new key
   - Click "Update secret"

3. **Verify New Key Works**:
   - Trigger a test workflow
   - Check workflow completes successfully

4. **Revoke Old Key**:
   - Go to Anthropic Console
   - Delete/revoke old API key

5. **Document Rotation**:
   - Note rotation date
   - Schedule next rotation

---

## Support

### Anthropic Support

- **Documentation**: https://docs.anthropic.com/
- **Support**: https://console.anthropic.com/support
- **Status Page**: https://status.anthropic.com/

### GitHub Actions Support

- **Documentation**: https://docs.github.com/en/actions
- **Community Forum**: https://github.community/

### SoftwareTeam Support

- **Documentation**: `docs/it/automated-multi-agent-review.md`
- **Issues**: https://github.com/{owner}/{repo}/issues

---

## Checklist

Use this checklist to verify setup:

- [ ] Created Anthropic account
- [ ] Obtained API key from Anthropic Console
- [ ] Saved API key securely
- [ ] Added `ANTHROPIC_API_KEY` secret to GitHub repository
- [ ] Verified secret name is exact: `ANTHROPIC_API_KEY`
- [ ] Enabled "Read and write permissions" for GitHub Actions
- [ ] Enabled "Allow GitHub Actions to create and approve pull requests"
- [ ] Tested with a sample PR or workflow run
- [ ] Verified automated reviews are posting to PR
- [ ] Reviewed API usage and costs in Anthropic Console
- [ ] Set up billing alerts (optional but recommended)
- [ ] Scheduled API key rotation (3-6 months)

---

**Setup Complete!** 🎉

Your automated multi-agent peer review system is now ready to review Developer PRs automatically using Product Owner, Architect, and Tester agents powered by Claude API.

---

**Document Change History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-20 | IT Agent | Initial Anthropic API key setup guide |

---

**End of Setup Guide**
