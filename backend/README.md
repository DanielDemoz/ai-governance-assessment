# Backend

Python FastAPI service for the AI Governance Readiness Assessment.

## Phase 2 Status

Architecture, database schema, models, seed data, scoring engine, API endpoints, and assessment workflow are in place.

## Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI entry point
│   ├── config.py         # Environment configuration
│   ├── api/              # REST API routes
│   ├── schemas/          # Pydantic request/response models
│   ├── services/         # Business logic and scoring engine
│   ├── db/               # Database session, schema, and seed
│   └── models/           # SQLAlchemy ORM models
├── tests/                # pytest unit and integration tests
├── data/                 # SQLite database (gitignored)
└── requirements.txt
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/categories` | List categories with questions |
| POST | `/assessments` | Create new assessment |
| GET | `/assessments/{id}` | Get assessment |
| PUT | `/assessments/{id}/profile` | Update org/AI system profile |
| PUT | `/assessments/{id}/responses` | Submit questionnaire responses |
| POST | `/assessments/{id}/calculate` | Run deterministic scoring |
| GET | `/assessments/{id}/results` | Get computed results |
| GET | `/assessments/{id}/recommendations` | Get rule-based recommendations |
| GET | `/assessments/{id}/roadmap` | Get improvement roadmap by timeframe |
| GET | `/assessments/{id}/risk-matrix` | Get 5x5 matrix, risks, and AI system risk profile |
| POST | `/assessments/{id}/risks` | Add a governance risk entry |
| DELETE | `/assessments/{id}/risks/{id}` | Remove a risk entry |

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Initialize Database

```python
from app.db import init_db
init_db()
```

Or run the seed script (Phase 2):

```bash
python -m app.db.seed
```
