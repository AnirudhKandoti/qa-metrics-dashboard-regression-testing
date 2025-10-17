# QA Metrics Dashboard for Regression Testing

An interactive observability dashboard to visualize regression and operational metrics across CI pipelines. Includes anomaly detection for early fault prediction and fine‑grained access control for secure metric visualization.

## Quick Start (Docker)

```bash
# 1) Clone and cd
# git clone <your-repo-url>
cd qa-metrics-dashboard

# 2) Create env
cp .env.example .env
# (optional) edit .env values

# 3) Build & run
docker compose up --build

# Backend: http://localhost:8000/docs
# Frontend: http://localhost:5173
```

## Manual (local, no Docker)

Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm i
npm run dev
```

## Seed data

```bash
docker compose exec backend python scripts/seed.py
# or locally: python scripts/seed.py
```

## Tech Stack
- FastAPI, SQLAlchemy, Alembic, PostgreSQL
- JWT (PyJWT) with role‑based access
- Scikit‑learn IsolationForest for anomalies
- React (Vite + TS), Recharts
- Docker Compose, GitHub Actions CI

## Default users (from .env)
- Admin: `admin@example.com` / password from `ADMIN_PASSWORD`
- Viewer: `viewer@example.com` / password from `VIEWER_PASSWORD`
