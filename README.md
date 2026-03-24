# أثر (ATHAR) — Digital Observatory for Gig Economy Activity

A digital observatory for estimating gig/platform economy activity in Saudi Arabia using multiple digital signals.

## Features

- **Gig Activity Index** — composite 0–100 indicator weighted across 5 data sources
- **Interactive Dashboard** — KPI cards, time-series, regional comparison, source contribution charts
- **Geographic Map** — Leaflet-powered map of Saudi cities with activity overlays
- **Arabic RTL UI** — full Arabic interface with Tailwind + Tajawal font
- **Demo Mode** — stable cached datasets for hackathon demos
- **Data Pipeline** — 10-step pandas pipeline (validate → clean → normalize → merge)

## Tech Stack

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Backend   | FastAPI · Python 3.11 · pandas · numpy  |
| Frontend  | Next.js 14 · TypeScript · Tailwind CSS  |
| Charts    | Recharts                                |
| Map       | Leaflet / react-leaflet                 |
| Container | Docker Compose                          |

## Project Structure

```
athar/
├── docker-compose.yml
├── README.md
├── backend/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── app/
│       ├── main.py              ← FastAPI entry point
│       ├── api/                 ← Route handlers
│       ├── services/            ← Pipeline, index calc, demo service
│       ├── schemas/             ← Pydantic models & constants
│       ├── utils/
│       └── data/
│           ├── raw/             ← JSON source datasets
│           └── processed/       ← Pipeline output (CSV)
└── frontend/
    ├── package.json
    ├── app/                     ← Next.js App Router pages
    ├── components/              ← React components
    ├── lib/                     ← API client
    └── types/                   ← TypeScript interfaces
```

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard: http://localhost:3000/dashboard

### Docker (full stack)

```bash
docker compose up --build
```

## API Endpoints

| Method | Endpoint           | Description                        |
|--------|--------------------|------------------------------------|
| GET    | /health            | Health check                       |
| GET    | /regions           | List of supported regions          |
| GET    | /sectors           | List of supported sectors          |
| GET    | /sources           | Data sources & weights             |
| POST   | /ingest            | Load raw datasets                  |
| POST   | /process           | Run data pipeline                  |
| POST   | /calculate-index   | Compute Gig Activity Index         |
| GET    | /dashboard-data    | Full dashboard payload             |

### Dashboard query params
- `period` — `30` | `90` | `180` | `365` (days)
- `region` — `Riyadh` | `Jeddah` | `Dammam` | `Makkah` | `Madinah`

## Gig Activity Index Methodology

The index is a weighted composite of 5 digital signals:

| Source                | Weight |
|-----------------------|--------|
| Google Trends         | 25%    |
| App Ecosystem Signals | 20%    |
| Food Delivery Signals | 20%    |
| Freelance Platforms   | 20%    |
| Benchmark Dataset     | 15%    |

Each source is normalized to 0–100 before weighting.

## Supported Regions (MVP)

Riyadh · Jeddah · Dammam · Makkah · Madinah

## Environment Variables

### Backend (`backend/.env`)
```
DEMO_MODE=true
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### Frontend (`frontend/.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Demo Mode

Set `DEMO_MODE=true` (default) to use cached datasets and disable external API calls.
The system remains fully stable during live demos.
