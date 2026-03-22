# Engineering Design Specification: Startup Idea Roaster

## Architecture Overview

**Pattern**: Layered single-page web application with a lightweight Node.js/Express backend serving a React frontend. The backend handles AI API calls and short-term result storage (in-memory for MVP). No database required.

```
┌─────────────────────────────────┐
│         React Frontend          │  Single-page app (Vite + React)
│  Home Page │ Result Page        │
└──────────────┬──────────────────┘
               │ HTTP REST API
┌──────────────▼──────────────────┐
│       Express.js Backend        │  Node.js server
│  POST /api/roast                │  - Calls Claude API
│  GET  /api/roast/:id            │  - Stores results in-memory
└──────────────┬──────────────────┘
               │ HTTPS
┌──────────────▼──────────────────┐
│        Anthropic Claude API     │  claude-sonnet-4-6
│  Prompt → Structured JSON out   │
└─────────────────────────────────┘
```

## Technology Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| Frontend | React 18 + Vite | Fast dev server, minimal setup, component model |
| Styling | TailwindCSS | Utility-first, quick to build polished UI |
| Backend | Node.js + Express | Lightweight, same language as frontend |
| AI | Anthropic Claude API (claude-sonnet-4-6) | Best-in-class instruction following for structured output |
| Result storage | In-memory Map (MVP) | No DB needed; results expire on server restart |
| Share links | UUID-based route `/roast/:id` | Simple, stateless, no auth needed |
| Package manager | npm | Standard, widely supported |

## Component Design

### Frontend Components

```
src/
├── App.jsx                  # Router: / → HomePage, /roast/:id → ResultPage
├── pages/
│   ├── HomePage.jsx         # Pitch input form + submit handler
│   └── ResultPage.jsx       # Fetches and displays roast by ID
├── components/
│   ├── PitchForm.jsx        # Textarea + character counter + button
│   ├── RoastScore.jsx       # Score badge with label + emoji
│   ├── FeedbackSection.jsx  # "Brutal Truth" text display
│   ├── SuggestionsSection.jsx # "Fix It" bulleted list
│   ├── ShareButton.jsx      # Copy link / Web Share API
│   └── LoadingSpinner.jsx   # Shown during API call
└── api/
    └── roastApi.js          # fetch() wrappers for backend endpoints
```

### Backend Modules

```
server/
├── index.js                 # Express app entry point, port detection
├── routes/
│   └── roast.js             # POST /api/roast, GET /api/roast/:id
├── services/
│   └── claudeService.js     # Anthropic SDK call + prompt construction
└── store/
    └── resultStore.js       # In-memory Map: id → roast result
```

## Interface Specifications

### POST /api/roast
**Request**:
```json
{ "pitch": "string (max 300 chars)" }
```
**Response** (201):
```json
{
  "id": "uuid-v4",
  "pitch": "original pitch text",
  "score": 3,
  "scoreLabel": "Meh But Possible",
  "feedback": "string (2-4 paragraphs)",
  "suggestions": ["string", "string", "string"]
}
```
**Errors**: 400 (missing/invalid pitch), 500 (AI call failed)

### GET /api/roast/:id
**Response** (200): Same shape as POST response
**Errors**: 404 (id not found)

### Claude Prompt Contract

The backend sends Claude a system prompt + user message and requests a **structured JSON response**. Claude is instructed to respond ONLY with JSON in this exact shape:

```json
{
  "score": 1-5,
  "scoreLabel": "one of the 5 defined labels",
  "feedback": "2-4 paragraphs of brutal honest feedback",
  "suggestions": ["3-5 fix-it items"]
}
```

The system prompt defines:
- The 5 roast score labels and what each means
- Tone: "mix of savage sarcasm and real constructive criticism"
- Output format: strict JSON only, no markdown, no preamble

## Data Flow

```
1. User types pitch → clicks "Roast My Idea"
2. Frontend POST /api/roast { pitch }
3. Backend validates input (non-empty, ≤300 chars)
4. Backend calls Claude API with system prompt + pitch
5. Claude returns JSON { score, scoreLabel, feedback, suggestions }
6. Backend generates UUID, stores result in memory Map
7. Backend returns { id, ...result } to frontend
8. Frontend navigates to /roast/{id}
9. ResultPage renders score badge, feedback, suggestions, share button
10. Share button copies /roast/{id} URL to clipboard
11. Anyone visiting /roast/{id} → frontend fetches GET /api/roast/{id} → displays result
```

## Share Link Design

- Result ID: `uuid.v4()` — unguessable, no auth needed
- Share URL: `http://localhost:{PORT}/roast/{id}` (MVP; production would use real domain)
- Frontend uses React Router for client-side routing
- Backend serves `index.html` for all non-API routes (SPA fallback)

## Port Handling

Per user preference: check if default port (3000) is in use; if so, find the next available port automatically. Log the actual port used to console.

## Dependencies

**Frontend** (package.json):
- `react`, `react-dom`
- `react-router-dom`
- `tailwindcss`, `postcss`, `autoprefixer`
- `vite`, `@vitejs/plugin-react`

**Backend** (package.json):
- `express`
- `@anthropic-ai/sdk`
- `uuid`
- `cors`
- `dotenv`

## Constraints

- Claude API key required at runtime — stored in `.env` as `ANTHROPIC_API_KEY`
- In-memory storage: results lost on server restart (acceptable for MVP)
- Max pitch length: 300 characters (enforced client + server side)
- No persistent database for MVP
- Single-process: frontend served as static files by Express in production mode; Vite dev server proxies to Express in development

## Security Considerations

- `.env` must be in `.gitignore` — API key never committed
- Input validation on server (pitch length, type)
- CORS configured to allow only localhost in MVP
- No user data stored beyond the pitch text and AI output
