# Goosemarket

Goosemarket is a full-stack prediction market web application. Users register and authenticate against Supabase, create and trade on polls (markets), and view positions, tags, and leaderboard data. The frontend is a Vite + React SPA, and the backend is a Flask API that proxies Supabase operations and enforces authentication via cookies.

## Architecture overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                               Browser                               │
│  React SPA (Vite)                                                    │
│  - Routes + UI                                                       │
│  - React Query for API calls                                         │
└───────────────▲───────────────────────────────────────┬──────────────┘
                │ HTTP (fetch /api/*)                   │ Static assets
                │                                       │
┌───────────────┴───────────────────────────────────────▼──────────────┐
│                             Flask API                                │
│  api/index.py                                                        │
│  - Auth (login/register/verify/logout)                               │
│  - Polls (create/edit/list/stats/price/estimate)                     │
│  - Trades (buy/sell)                                                 │
│  - Tags, Positions, User info                                        │
│  - Admin review/resolve flows                                        │
│  - Leaderboard                                                      │
└───────────────▲──────────────────────────────────────────────────────┘
                │ Supabase client (service role key)
┌───────────────┴──────────────────────────────────────────────────────┐
│                       Supabase (Postgres)                            │
│  - Schema in src/schema.sql                                          │
└──────────────────────────────────────────────────────────────────────┘
```

### Key backend modules
- `src/api/index.py`: Flask app and route definitions for the REST API.
- `src/api/database.py`: Supabase client bootstrap via `SUPABASE_URL` and `SUPABASE_SECRET_KEY`.
- `src/api/*`: Business logic for polls, trades, tags, admin review, leaderboard, etc.

### Frontend
- `src/src/`: React application built with Vite.
- Tailwind CSS is used for styling and layout.
- React Query manages client-side data fetching and caching.

## Tech stack
- **Frontend:** React 19, Vite 7, Tailwind CSS, React Router, React Query.
- **Backend:** Python 3.11+, Flask.
- **Database/Auth:** Supabase (Postgres + auth), accessed via the Supabase Python client.

## Running the project locally

### Prerequisites
- Node.js 18+ (Node 20 LTS recommended) and npm.
- Python 3.11+ and `pip`.
- A Supabase project with the schema applied (see below).

### 1) Install dependencies
From the repository root:

```bash
# (Optional) create a virtual environment
python -m venv .venv
# Activate it:
#   Windows PowerShell: .\.venv\Scripts\Activate.ps1
#   macOS/Linux: source .venv/bin/activate

# Backend deps
python -m pip install -r src/requirements.txt

# Frontend deps
cd src
npm install
```

### 2) Configure environment variables
The API expects Supabase credentials in environment variables.

```bash
cp .env.template .env   # Windows: copy .env.template .env
```

Populate `.env` with your Supabase credentials:

```
SUPABASE_URL=<your-project-url>
SUPABASE_SECRET_KEY=<your-service-role-key>
```

### 3) Initialize the database schema
Apply the schema in `src/schema.sql` to your Supabase Postgres database. You can do this via the Supabase SQL editor or by using your preferred Postgres client.

### 4) Run the application (development)
The default dev workflow runs both the Flask API and the Vite dev server concurrently.

```bash
cd src
npm run dev
```

- Frontend: http://localhost:5173
- API: http://localhost:5328

If you are on Windows and `python3` is not available, run the API and frontend in separate terminals from `src/`:

```bash
# Terminal 1
python api/index.py

# Terminal 2
npm run dev -- --host
```

### 5) Build and preview the frontend

```bash
cd src
npm run build
npm run preview
```

### 6) Run tests
From the repository root:

```bash
python -m pip install pytest
python -m pytest
```

> Note: tests that hit Supabase require valid environment variables.

## API surface (high level)
The Flask API exposes authenticated routes under `/api/*` for:
- Authentication: login, register, verify, logout.
- Polls/markets: create, list, edit, get, price, stats, estimate cost.
- Trading: buy/sell shares.
- Metadata: tags, positions, user info.
- Admin: approve/reject/update/resolve polls.
- Leaderboard: top users and total count.

These routes are defined in `src/api/index.py`, with supporting modules under `src/api/`.

## Repository layout
```
.
├── README.md           # Project overview and setup (this file)
├── .env.template       # Env var template
├── docs/               # Documentation artifacts
├── src/
│   ├── api/            # Flask API
│   ├── src/            # React app
│   ├── public/         # Frontend static assets
│   ├── schema.sql      # Supabase schema
│   ├── package.json    # Frontend scripts and deps
│   └── requirements.txt# Backend deps
└── tests/              # Pytest test suite
```
