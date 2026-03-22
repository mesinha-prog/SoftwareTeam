# Cost Estimate: Startup Idea Roaster MVP

**Date**: 2026-03-22
**Task**: Build a web app where users submit startup ideas and get brutally honest AI feedback, a roast score, and suggestions to fix it.
**Model assumed for runtime**: Claude claude-sonnet-4-6 (input $3/1M tokens, output $15/1M tokens)
**Model used for development**: Claude claude-sonnet-4-6

---

## Development Phase Estimates (AI agent token usage)

| Agent | Role | Est. Input Tokens | Est. Output Tokens | Est. Cost |
|-------|------|------------------|--------------------|-----------|
| Product Owner | Requirements & user story | 8,000 | 2,000 | $0.05 |
| Cost Analyst | This estimate | 5,000 | 1,500 | $0.04 |
| Architect | System design, tech stack, interfaces | 12,000 | 6,000 | $0.13 |
| IT Agent (Setup) | Dependency install, scripts | 10,000 | 4,000 | $0.09 |
| Developer | Full app implementation (frontend + backend + API integration) | 30,000 | 20,000 | $0.39 |
| Tester | Test plan, test execution, test report | 15,000 | 6,000 | $0.14 |
| IT Agent (Release) | Release packaging, versioning | 8,000 | 3,000 | $0.07 |
| Product Owner | Acceptance review | 8,000 | 2,000 | $0.05 |
| **TOTAL** | | **96,000** | **44,500** | **$0.96** |

---

## Runtime Cost Estimate (per user interaction)

Each user submits a startup pitch and receives a roast. Estimated per-request token usage:

| Component | Input Tokens | Output Tokens | Cost per Request |
|-----------|-------------|---------------|-----------------|
| System prompt (roast persona + instructions) | ~500 | — | — |
| User pitch (short, ~50 words) | ~70 | — | — |
| AI response (score + feedback + suggestions) | — | ~400 | — |
| **Per request total** | **~570** | **~400** | **~$0.008** |

At 100 requests/day: ~$0.80/day | At 1,000 requests/day: ~$8.00/day

---

## Summary

| Category | Estimated Cost |
|----------|---------------|
| Development (all agents) | $0.96 |
| Runtime (per 100 requests) | ~$0.80 |
| **Total development cost** | **$0.96** |

**Threshold**: MEDIUM (development) — no approval required.
**Runtime cost** scales with usage; no upfront concern for MVP.

---

## Assumptions

- Developer phase is the most token-intensive due to full-stack implementation (frontend UI, backend API handler, Claude API integration, shareable link generation)
- Architect phase includes designing the share-link mechanism and AI prompt engineering
- Runtime prompt is kept concise to minimize per-request cost
- No database required for MVP (anonymous, stateless), which simplifies implementation and reduces cost

---

## Recommendation

Proceed. Total development cost is under $1.00 (MEDIUM threshold). Runtime cost is negligible at MVP scale. No user approval required.
