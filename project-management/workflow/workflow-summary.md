# Multi-Agent Workflow Summary

## Complete Workflow from Task to PR Review

### Step 1: Give Task to Product Owner

**You (User)**: Give a task in conversation

Example: "Implement a temperature monitoring feature"

### Step 2: Product Owner Assigns to Agent

**Product Owner Agent** (Claude Code acting as Product Owner):
- Analyzes the task
- Reviews agent capabilities
- Determines the best agent for the job
- Creates task specification in `docs/tasks/{agent}/`
- Assigns work to appropriate agent

Example assignment:
- "Design temperature monitoring" → **Architect Agent**
- "Implement temperature sensor class" → **Developer Agent**
- "Test temperature thresholds" → **Tester Agent**
- "Set up build for new module" → **IT Agent**

### Step 3: Agent Works on Task

**Assigned Agent** (Claude Code acting as that agent):
- Works in their git worktree (if using worktree workflow)
- Implements the solution
- Follows agent-specific best practices
- Documents their work

### Step 4: Agent Creates Pull Request

**Agent**:
- Commits all changes to their branch
- Branch MUST follow naming: `agent/{agent}-{project}-{sessionID}`
  - Example: `agent/developer-rtdcs-NxeRq`
  - This naming is CRITICAL for automated review to work
- Pushes branch to GitHub
- Creates PR using `gh pr create`

Example PR creation:
```bash
export GH_TOKEN=$(cat /home/user/SoftwareTeam/.github_token)

gh pr create --base master --head agent/developer-rtdcs-NxeRq \
  --title "Implement temperature monitoring" \
  --body "$(cat <<'EOF'
## Summary
- Implemented TemperatureSensor class
- Added unit tests

## Files Changed
- src/temperature/TemperatureSensor.cpp
- tests/unit/test_temperature_sensor.cpp

## Test Plan
- All unit tests pass
- Tested threshold detection
EOF
)"
```

### Step 5: You Manually Trigger Peer Review

**You (User)**:
1. Go to GitHub repository
2. Click "Actions" tab
3. Click "Automated Multi-Agent Peer Review" workflow
4. Click "Run workflow" button
5. Enter the PR number
6. Click "Run workflow"

### Step 6: Automated Multi-Agent Review Runs

**GitHub Actions Workflow**:
- Detects agent type from branch name (e.g., `developer` from `agent/developer-rtdcs-NxeRq`)
- Determines reviewers based on agent type:
  - **Developer PR** → Reviewed by: Architect + Tester (2 reviewers)
  - **Architect PR** → Reviewed by: Developer + Tester (2 reviewers)
  - **Tester PR** → Reviewed by: Developer + Product Owner (2 reviewers)
  - **IT PR** → Reviewed by: Architect (1 reviewer)
  - **Product Owner PR** → Reviewed by: Architect (1 reviewer)

- Each reviewer agent:
  1. Reviews code using Claude API
  2. Focuses on CRITICAL issues only:
     - **Design**: Architecture, patterns, SOLID violations
     - **Functionality**: Logic errors, broken features
     - **Consistency**: Project standards, conventions
     - **Clean Code**: Code smells, maintainability
  3. Provides **MAXIMUM 10 inline comments** per reviewer
  4. Posts review with ✅ **APPROVED** or 🔴 **CHANGES REQUESTED**

### Step 7: Review Comments Posted

**GitHub automatically posts**:
- Summary comment from each reviewer
- Inline comments on specific code lines (max 10 per reviewer)
- Overall decision: Approve or Request Changes

**Example review output**:
```
🤖 Architect Agent Review

### Summary
Implementation follows design patterns well, but found 3 SOLID violations.

### Decision
🔴 CHANGES REQUESTED - This PR requires changes before approval.

---
8 inline comment(s) posted on specific lines in the "Files changed" tab.
```

### Step 8: Check Approval Status

**Workflow automatically checks**:
- If all reviewers approve (2+ approvals) → Adds label `peer-review:approved`
- If any reviewer requests changes → Adds label `peer-review:changes-requested`
- Posts summary comment with approval status

### Step 9: Address Feedback (if needed)

**Agent** (if changes requested):
- Reviews feedback from peer agents
- Makes necessary changes
- Pushes new commits to same branch
- You re-run the peer review workflow (Step 5)

**🔄 RE-REVIEW MODE** (Automatic):
When you re-trigger the workflow on a PR that already has reviews:
- Agents automatically detect they've reviewed before
- They check ONLY if their previous concerns were addressed
- If addressed: They **resolve the conversation threads** and approve
- If not addressed: They explain why and keep requesting changes
- **No new comprehensive reviews** - focused re-review only
- More efficient iteration cycle

### Step 10: Final User Review

**You (User)**:
- Review the PR on GitHub
- Check peer review comments
- Verify approval status
- Merge if satisfied

---

## Key Points

✅ **Branch naming is CRITICAL**: Must be `agent/{agent}-{project}-{sessionID}`
✅ **Manual trigger only**: Saves API costs by running only when you click
✅ **Focused reviews**: Only critical issues (Design, Functionality, Consistency, Clean Code)
✅ **Limited comments**: Maximum 10 per reviewer - prioritizes most important issues
✅ **Sequential review**: Agents review one after another (not truly parallel, but automated)
✅ **2 reviewers minimum**: Most PRs get 2 agent reviews for thorough quality check
✅ **Re-review mode**: Agents automatically check only previous concerns and resolve threads when addressed

## Workflow Diagram

```
User Task
    ↓
Product Owner Analyzes → Assigns to Agent
    ↓
Agent Works → Commits → Creates PR (with correct branch naming)
    ↓
User Triggers "Run workflow" in GitHub Actions
    ↓
Workflow detects agent from branch name
    ↓
Assigns 2 reviewers based on agent type
    ↓
Reviewer 1 (Claude API) → Posts max 10 critical comments
    ↓
Reviewer 2 (Claude API) → Posts max 10 critical comments
    ↓
Workflow checks: 2+ approvals? → Label PR as approved
    ↓
User reviews → Merges (if approved)
```

## Important Files

- **Workflow**: `.github/workflows/automated-peer-review.yml`
- **Review Script**: `.github/scripts/automated-review.js`
- **Agent Definitions**: `.agent/agents/{agent}-agent.md`
- **GitHub Token**: `.github_token` (for creating PRs)

## Cost Optimization

The workflow is **manually triggered** to save API costs:
- Only runs when you explicitly click "Run workflow"
- Doesn't run automatically on every PR
- You control when peer review happens
- Typically 2 Claude API calls per PR (2 reviewers × 1 call each)

## Next Steps

Ready to try it! Here's what to do:
1. Give me a task
2. I'll act as Product Owner and assign to appropriate agent
3. Agent creates PR with correct branch naming
4. You manually trigger the peer review workflow on GitHub
5. Check the review comments
6. Merge when ready!
