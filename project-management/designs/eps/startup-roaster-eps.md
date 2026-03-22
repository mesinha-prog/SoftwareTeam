# Engineering Product Specification: Startup Idea Roaster

## Overview

A single-page web application where users submit a short startup pitch and receive brutally honest AI-generated feedback including a fun roast score, mixed roast + constructive critique, and actionable fix-it suggestions. Results are shareable via a unique link. No login required.

## User Stories

**As an** entrepreneur or aspiring founder
**I want to** paste my startup pitch and get roasted by AI
**So that** I understand where my idea is weak and what I can do to strengthen it

## Functional Requirements

### FR-1: Pitch Submission
- User sees a single text area on the homepage
- User types or pastes a short startup pitch (1–3 sentences, max ~300 characters)
- User clicks a "Roast My Idea" button to submit
- App shows a loading state while AI processes the request

### FR-2: Roast Results Display
The result page displays three sections:

**FR-2a: Roast Score**
A fun categorical label from the scale below:
| Score | Label |
|-------|-------|
| 1 | Certified Dumpster Fire |
| 2 | Pivot Needed ASAP |
| 3 | Meh But Possible |
| 4 | Hidden Gem |
| 5 | Future Unicorn |

**FR-2b: Brutal Feedback**
2–4 paragraphs mixing sarcastic roast tone with real hard-truth critique about why the idea does or doesn't work.

**FR-2c: Fix-It Suggestions**
A list of 3–5 suggestions combining:
- Specific tactical action items (e.g., "Run 20 customer interviews before writing a line of code")
- Strategic directional advice (e.g., "Narrow your ICP to solo founders, not all SMBs")

### FR-3: Shareable Link
- Each result is accessible via a unique URL (e.g., `/roast/{id}`)
- A "Share Your Roast" button copies the link or opens a share dialog
- Visiting a shared link shows the same result (pitch + score + feedback + suggestions)

### FR-4: Anonymous & Stateless (MVP)
- No user accounts or login
- Results stored server-side temporarily to support share links
- No personal data collected

## User Interface

### Home Page
- App name and tagline ("Brutally Honest Startup Feedback")
- Large text area: "Describe your startup idea in 1-3 sentences..."
- Character counter (max 300)
- "Roast My Idea" CTA button
- Loading spinner/animation while waiting for AI

### Result Page
- Pitch text (shown back to user)
- Roast score badge with label and emoji
- "The Brutal Truth" section (AI feedback)
- "How to Fix It" section (bulleted suggestions)
- "Share Your Roast" button
- "Roast Another Idea" link back to home

## Success Criteria

- User can submit a pitch and receive a full roast result in under 10 seconds
- Shareable link works and shows correct result
- Score label is always one of the 5 defined categories
- App runs with a single command, opens browser automatically
- No login required at any point
