# PharmaStock AI

Action-first inventory & compliance intelligence for pharmacies, hospital pharmacies, and distributors (SIH26179 — Team Pilluminati).

## Stack

- **Backend:** Python FastAPI, SQLAlchemy, PostgreSQL (SQLite supported for local MVP)
- **Frontend:** React + Vite PWA, Tailwind CSS, Lucide, Framer Motion
- **Auth:** HttpOnly cookie JWT session

## Quick start

### 1. Database

```bash
docker compose up -d
```

Or use SQLite by setting `DATABASE_URL=sqlite:///./pharmastock.db` in `backend/.env` (default in local `.env`).

### 2. Backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # if needed
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — API is proxied to port 8000 with credentials.

### Seed logins

| Email | Password | Role |
|-------|----------|------|
| admin@pharmastock.example | ChangeMeAdmin123! | SYSTEM_ADMIN |
| owner@retail.example | Password123! | PHARMACY_OWNER |
| manager@retail.example | Password123! | STORE_MANAGER |
| procurement@dist.example | Password123! | PROCUREMENT_MANAGER |
| hospital@hosp.example | Password123! | HOSPITAL_INCHARGE |
| warehouse@dist.example | Password123! | WAREHOUSE_BRANCH_MANAGER |
| chainhead@chain.example | Password123! | MULTI_OUTLET_INVENTORY_HEAD |

## Structure

```
backend/   FastAPI (api → services → repositories → models)
frontend/  React PWA (two-color design system)
```
