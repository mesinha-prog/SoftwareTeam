# Technical Tasks: Startup Idea Roaster MVP

## Task 1: Project Scaffold & Configuration

**Objective**: Set up the monorepo structure with React frontend (Vite) and Express backend.

**Implementation Details**:
- Create `modules/startup-roaster/` directory
- Init frontend: `npm create vite@latest frontend -- --template react`
- Init backend: `npm init` in `server/` folder
- Configure TailwindCSS for frontend
- Configure Vite proxy: forward `/api/*` to Express during dev
- Set up `.env` with `ANTHROPIC_API_KEY` placeholder
- Add `.env` to `.gitignore`

**Acceptance Criteria**:
- [ ] `npm run dev` starts both frontend (Vite) and backend (Express) together
- [ ] Frontend renders at localhost
- [ ] `/api/` requests proxy correctly to Express
- [ ] `.env` is gitignored

---

## Task 2: Backend — Result Store

**Objective**: Implement in-memory result storage.

**File**: `server/store/resultStore.js`

**Implementation Details**:
- Use a `Map<string, RoastResult>` keyed by UUID
- Export `save(result)` → stores and returns id
- Export `get(id)` → returns result or null

**Acceptance Criteria**:
- [ ] `save()` generates UUID, stores result, returns id
- [ ] `get()` returns correct result for valid id
- [ ] `get()` returns null for unknown id

---

## Task 3: Backend — Claude Service

**Objective**: Implement the Anthropic API integration.

**File**: `server/services/claudeService.js`

**Implementation Details**:
- Use `@anthropic-ai/sdk`
- Load `ANTHROPIC_API_KEY` from environment
- Build system prompt with 5-label scale and JSON-only instruction
- Send `messages.create()` with `model: "claude-sonnet-4-6"`, `max_tokens: 1024`
- Parse response text as JSON
- Validate score (1–5) and scoreLabel against allowed values
- Throw descriptive error if parsing or validation fails

**Acceptance Criteria**:
- [ ] Returns valid `{ score, scoreLabel, feedback, suggestions }` for a real pitch
- [ ] Throws error if Claude returns non-JSON
- [ ] Throws error if score is out of range

---

## Task 4: Backend — API Routes

**Objective**: Implement POST /api/roast and GET /api/roast/:id.

**File**: `server/routes/roast.js`

**Implementation Details**:
- `POST /api/roast`: validate pitch (required, string, ≤300 chars), call claudeService, save to store, return 201 + full result with id
- `GET /api/roast/:id`: look up in store, return 200 or 404
- Wrap Claude call in try/catch, return 500 with error message on failure
- Mount routes in `server/index.js`
- Auto-detect available port starting from 3000

**Acceptance Criteria**:
- [ ] POST with valid pitch returns 201 + result with id
- [ ] POST with missing pitch returns 400
- [ ] POST with pitch >300 chars returns 400
- [ ] GET with valid id returns 200 + result
- [ ] GET with unknown id returns 404
- [ ] Server starts on available port (not hardcoded 3000)

---

## Task 5: Frontend — Home Page

**Objective**: Build the pitch submission UI.

**Files**: `src/pages/HomePage.jsx`, `src/components/PitchForm.jsx`

**Implementation Details**:
- Text area with placeholder "Describe your startup idea in 1-3 sentences..."
- Character counter showing X/300
- Disable submit button when pitch is empty or >300 chars
- On submit: call `submitRoast(pitch)`, show `LoadingSpinner`, navigate to `/roast/{id}` on success
- Show error message if API call fails

**Acceptance Criteria**:
- [ ] Text area visible on load
- [ ] Character counter updates live
- [ ] Button disabled when empty or over limit
- [ ] Loading state shown during API call
- [ ] Navigates to result page on success
- [ ] Error message shown on API failure

---

## Task 6: Frontend — Result Page

**Objective**: Build the roast result display UI.

**Files**: `src/pages/ResultPage.jsx`, `src/components/RoastScore.jsx`, `src/components/FeedbackSection.jsx`, `src/components/SuggestionsSection.jsx`, `src/components/ShareButton.jsx`

**Implementation Details**:
- On mount: fetch `GET /api/roast/:id` using id from URL params
- Display: pitch text, score badge (label + emoji per score level), feedback paragraphs, suggestions as bullet list
- Score emoji mapping: 1=💀, 2=🔥, 3=😐, 4=💎, 5=🦄
- ShareButton: uses `navigator.clipboard.writeText(window.location.href)`; fallback to `prompt()` with URL
- "Roast Another Idea" link → `/`
- Show 404 message if result not found

**Acceptance Criteria**:
- [ ] All result fields displayed correctly
- [ ] Score badge shows correct label and emoji
- [ ] Share button copies URL to clipboard
- [ ] "Roast Another Idea" returns to home
- [ ] 404 handled gracefully

---

## Task 7: Frontend — Router & App Shell

**Objective**: Wire up React Router and overall app layout.

**Files**: `src/App.jsx`, `src/main.jsx`

**Implementation Details**:
- `BrowserRouter` with routes: `/` → HomePage, `/roast/:id` → ResultPage
- App shell: title bar "Startup Roaster" + tagline
- Tailwind base styles applied globally

**Acceptance Criteria**:
- [ ] `/` renders HomePage
- [ ] `/roast/{id}` renders ResultPage
- [ ] Browser back/forward navigation works
- [ ] Express serves `index.html` for all non-API routes (SPA fallback)

---

## Task 8: API Integration Module

**Objective**: Centralize all frontend→backend API calls.

**File**: `src/api/roastApi.js`

**Implementation Details**:
- `submitRoast(pitch)`: POST `/api/roast`, returns result or throws error
- `getRoast(id)`: GET `/api/roast/{id}`, returns result or throws 404 error

**Acceptance Criteria**:
- [ ] `submitRoast` returns full result with id on success
- [ ] `getRoast` returns result for valid id
- [ ] Both functions throw meaningful errors on failure
