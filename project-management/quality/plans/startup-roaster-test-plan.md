# Test Plan: Startup Idea Roaster MVP

**Date**: 2026-03-22
**Version**: 1.0
**Tester**: Tester Agent

---

## Scope

Testing the Startup Idea Roaster MVP — a web app where users submit a startup pitch and receive AI-generated roast score, feedback, and suggestions.

## Test Strategy

| Level | Framework | Focus |
|-------|-----------|-------|
| Unit / Component | Vitest + React Testing Library | Individual modules and components |
| Integration | Vitest + Supertest | Backend API routes end-to-end (with Claude mocked) |
| System | Manual + checklist | Full app flow in browser |

## Test Scenarios

### Backend — resultStore
- TC-01: `save()` stores result and returns a UUID
- TC-02: `get()` returns stored result by valid id
- TC-03: `get()` returns null for unknown id

### Backend — API Routes (mocked Claude)
- TC-04: `POST /api/roast` with valid pitch returns 201 + full result with id
- TC-05: `POST /api/roast` with missing pitch returns 400
- TC-06: `POST /api/roast` with empty pitch returns 400
- TC-07: `POST /api/roast` with pitch > 300 chars returns 400
- TC-08: `GET /api/roast/:id` with valid id returns 200 + result
- TC-09: `GET /api/roast/:id` with unknown id returns 404

### Frontend — Component Tests
- TC-10: PitchForm renders textarea and button
- TC-11: PitchForm disables button when input is empty
- TC-12: PitchForm disables button when input exceeds 300 chars
- TC-13: PitchForm shows character counter
- TC-14: RoastScore renders correct emoji and label for each score (1-5)
- TC-15: ShareButton copies URL to clipboard on click

### System — Manual Checklist
- TC-16: Full happy path (submit pitch → see result page)
- TC-17: Share link works (visit /roast/:id directly)
- TC-18: "Roast Another Idea" returns to home
- TC-19: 404 shown for unknown roast id
- TC-20: App opens automatically in browser on `bash scripts/run.sh`

## Pass Criteria

- All automated tests pass (0 failures)
- No Critical or High severity bugs open
- All manual system checklist items verified
