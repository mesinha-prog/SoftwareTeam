# Environment Setup: Startup Idea Roaster

## Prerequisites

- Node.js 18+ and npm
- An Anthropic API key (sk-ant-...)

## Directory Structure

```
modules/startup-roaster/
├── .env                  # API key (gitignored)
├── .gitignore
├── package.json          # Root: runs frontend + backend together via concurrently
├── frontend/             # React 18 + Vite + TailwindCSS
│   ├── package.json
│   ├── vite.config.js    # Proxies /api/* → Express backend
│   └── src/
└── server/               # Express.js + Anthropic SDK
    ├── package.json
    └── index.js
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude claude-sonnet-4-6 |
| `PORT` | No | Backend port (auto-detected from 3001 if not set) |

Set in `modules/startup-roaster/.env` (never commit this file).

## Running the App

```bash
bash scripts/run.sh
```

This single command:
1. Loads `.env`
2. Auto-detects an available backend port (starting from 3001)
3. Updates Vite proxy config to match
4. Starts Express backend + Vite frontend concurrently
5. Opens browser at http://localhost:5173 automatically

## Dependencies Installed

**Frontend** (`modules/startup-roaster/frontend/`):
- react, react-dom, react-router-dom
- tailwindcss, @tailwindcss/vite
- vite, @vitejs/plugin-react

**Backend** (`modules/startup-roaster/server/`):
- express, cors, dotenv
- @anthropic-ai/sdk
- uuid

**Root** (`modules/startup-roaster/`):
- concurrently (runs frontend + backend in one command)
