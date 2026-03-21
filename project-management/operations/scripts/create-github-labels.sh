#!/bin/bash

# Create GitHub Labels for Peer Review Workflow
#
# This script creates all the labels used by the automated peer review workflow.
# Run this script once after setting up the repository to create the necessary labels.
#
# Prerequisites:
# - GitHub CLI (gh) installed and authenticated
# - Repository access (owner or admin permissions)
#
# Usage:
#   ./create-github-labels.sh

set -e

REPO="meenusinha/SoftwareTeam"

echo "Creating GitHub labels for peer review workflow..."
echo "Repository: ${REPO}"
echo ""

# Function to create a label (idempotent - won't fail if label exists)
create_label() {
    local name="$1"
    local color="$2"
    local description="$3"

    echo "Creating label: ${name}"
    gh label create "${name}" \
        --repo "${REPO}" \
        --color "${color}" \
        --description "${description}" \
        --force 2>/dev/null || echo "  → Label '${name}' already exists, updating..."
}

echo "=== Peer Review Type Labels ==="
create_label "peer-review:developer" "0E8A16" "Pull request from Developer Agent (requires Product Owner, Architect, Tester review)"
create_label "peer-review:architect" "1D76DB" "Pull request from Architect Agent (requires Product Owner, Developer review)"
create_label "peer-review:tester" "FBCA04" "Pull request from Tester Agent (requires Product Owner, Developer review)"
create_label "peer-review:it" "D93F0B" "Pull request from IT Agent (requires Product Owner, Architect review)"
create_label "peer-review:product-owner" "5319E7" "Pull request from Product Owner Agent (requires Architect, Developer, Tester review)"

echo ""
echo "=== Review Status Labels ==="
create_label "awaiting-product-owner-review" "EDEDED" "Waiting for Product Owner Agent review"
create_label "awaiting-architect-review" "EDEDED" "Waiting for Architect Agent review"
create_label "awaiting-developer-review" "EDEDED" "Waiting for Developer Agent review"
create_label "awaiting-tester-review" "EDEDED" "Waiting for Tester Agent review"

echo ""
echo "=== Additional Quality Labels ==="
create_label "peer-review:approved" "0E8A16" "All required peer reviews have been approved"
create_label "peer-review:changes-requested" "D93F0B" "Peer reviewers have requested changes"
create_label "ready-for-user-review" "5319E7" "Peer reviews complete, ready for user review and merge"

echo ""
echo "✅ All labels created successfully!"
echo ""
echo "Next steps:"
echo "1. Verify labels in GitHub: https://github.com/${REPO}/labels"
echo "2. Test the workflow by creating a PR from a agent/{agent}-* branch"
echo ""
