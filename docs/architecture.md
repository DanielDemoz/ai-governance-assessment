# Architecture

## Overview

The AI Governance Readiness Assessment is a full-stack web application with clear separation between deterministic assessment logic and optional AI-generated narratives.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                       │
│  Landing │ Methodology │ Assessment Flow │ Dashboard │ Report   │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API
┌────────────────────────────▼────────────────────────────────────┐
│                      Backend (FastAPI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   API Layer  │  │   Services   │  │  Scoring Engine      │  │
│  │  (routes)    │──│  (business)  │──│  (deterministic)     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Recommend.   │  │ Risk Engine  │  │  Report Generator    │  │
│  │ Engine       │  │              │  │  (PDF)               │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Optional LLM Service (Phase 7)               │  │
│  │         Narratives only — never controls scores           │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ SQLAlchemy ORM
┌────────────────────────────▼────────────────────────────────────┐
│              Database (SQLite dev / PostgreSQL prod)            │
│  Assessment │ Organization │ AISystem │ Question │ Response    │
│  Category │ Risk │ Recommendation │ AssessmentResult │ Report │
└─────────────────────────────────────────────────────────────────┘
```

## Design Principles

1. **Deterministic scoring** — All numerical scores are calculated by rule-based engines, never by LLMs.
2. **Explainability** — Every score traces back to individual question responses.
3. **Separation of concerns** — Frontend displays; backend validates and computes.
4. **Normalized data model** — No hard-coded results in UI components.
5. **PostgreSQL-ready** — SQLite for local development; schema designed for PostgreSQL migration.

## Entity Relationships

```
Assessment (1) ──── (1) Organization
         (1) ──── (1) AISystem
         (1) ──── (*) Response ──── (1) Question ──── (1) Category
         (1) ──── (*) Risk
         (1) ──── (*) Recommendation
         (1) ──── (1) AssessmentResult
         (1) ──── (*) Report
```

## API Structure (planned)

| Endpoint | Purpose |
|----------|---------|
| `POST /assessments` | Create new assessment |
| `GET /assessments/{id}` | Retrieve assessment |
| `PUT /assessments/{id}/profile` | Update org/AI system profile |
| `PUT /assessments/{id}/responses` | Submit questionnaire responses |
| `POST /assessments/{id}/calculate` | Run deterministic scoring |
| `GET /assessments/{id}/results` | Get computed results |
| `POST /assessments/{id}/risks` | Add risk matrix entries |
| `GET /assessments/{id}/report` | Generate PDF report |
| `POST /assessments/demo` | Load demo assessment |

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS |
| Charts | Recharts |
| Backend | Python 3.11+, FastAPI, Pydantic |
| ORM | SQLAlchemy 2.x |
| Database | SQLite (dev), PostgreSQL (prod) |
| PDF | WeasyPrint (Phase 6) |
| Testing | pytest, TypeScript tests |

## Security

- Environment variables for configuration (`.env.example` provided)
- Server-side validation on all inputs
- No API keys in source code
- Assessment data not sent to LLMs without explicit user action

## Directory Structure

```
ai-governance-assessment/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/        # Pydantic request/response (Phase 2)
│   │   ├── services/       # Business logic (Phase 2+)
│   │   │   ├── scoring/
│   │   │   ├── recommendations/
│   │   │   ├── risk/
│   │   │   └── reports/
│   │   └── api/            # Route handlers (Phase 2)
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── app/
│       ├── components/
│       ├── lib/
│       └── types/
├── docs/
└── tests/
```
