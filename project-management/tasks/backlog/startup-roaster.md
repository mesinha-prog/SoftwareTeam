# User Story: Startup Idea Roaster

**As a** entrepreneur or aspiring founder
**I want to** submit my startup idea as a short pitch and receive brutally honest AI-generated feedback
**So that** I can quickly understand the weaknesses in my idea, get a fun roast score, and learn actionable ways to improve it

## Acceptance Criteria

- [ ] User can enter a short startup pitch (1–3 sentences) in a text input field
- [ ] On submission, the app calls an AI model and returns:
  - A **roast score** using a fun, creative scale (e.g., "Certified Dumpster Fire", "Pivot Needed", "Meh But Possible", "Hidden Gem", "Future Unicorn")
  - **Brutally honest feedback** — a mix of hard truths and constructive criticism about why the idea may or may not work
  - **Fix-it suggestions** — both specific action items (e.g., "narrow your target market to X") and strategic advice (e.g., "validate demand before building")
- [ ] Results are displayed clearly on the page after submission
- [ ] User can share their roast result via a shareable link or social share button
- [ ] No login or authentication required — fully anonymous
- [ ] App runs with a single command

## Roast Score Scale

| Score Label | Meaning |
|---|---|
| Certified Dumpster Fire | Fundamentally broken idea |
| Pivot Needed ASAP | Core issues, salvageable with major changes |
| Meh But Possible | Average idea, needs differentiation |
| Hidden Gem | Strong potential, needs polish |
| Future Unicorn | Exceptional idea, strong execution path |

## Priority
High

## Scope (MVP)
- **In scope**: Short pitch input, AI roast + score + suggestions, anonymous, shareable result link
- **Out of scope**: User accounts, pitch history, long-form structured input, mobile app

## Notes
- "Brutally honest" means a mix of savage/sarcastic roast tone AND real constructive advice — not just one or the other
- Fix-it suggestions should include both tactical action items AND strategic direction
- The roast score label should feel fun and memorable, not just a number

## Status
- [ ] Assigned to Architect
- [ ] Technical design complete
- [ ] Implementation in progress
- [ ] Testing
- [ ] Ready for acceptance
- [ ] Accepted
