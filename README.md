# AI Governance Readiness Assessment

A professional web application that helps organizations assess how prepared they are to govern and responsibly deploy AI systems.

> **Disclaimer:** This tool provides an **indicative AI governance readiness assessment** and is **not legal advice**, regulatory certification, or a guarantee of compliance or safety. Results should be reviewed by qualified human professionals.

## Why AI Governance Matters

Organizations deploying AI face growing expectations around accountability, transparency, fairness, and human oversight. Without structured governance, AI systems can create privacy risks, biased outcomes, opaque decisions, and compliance gaps — even when the underlying technology works correctly.

This application evaluates governance maturity across nine dimensions, calculates a transparent readiness score, identifies gaps, and generates prioritized recommendations with an actionable improvement roadmap.

## Features

- **Nine-dimension governance assessment** across accountability, oversight, privacy, fairness, transparency, security, risk management, lifecycle, and affected people
- **Deterministic scoring engine** — transparent, reproducible, never LLM-controlled
- **Separate governance readiness and AI system risk** metrics
- **Rule-based recommendations** with priority levels and improvement roadmap
- **5×5 governance risk matrix**
- **Professional PDF report** generation
- **Demo assessment** (Northstar College scenario)
- **Full score explainability** — every result traces to underlying answers

## Assessment Framework

| Category | Weight |
|----------|--------|
| Accountability & Governance | 15% |
| Human Oversight | 15% |
| Privacy & Data Governance | 15% |
| Fairness & Non-Discrimination | 15% |
| Transparency & Explainability | 10% |
| Security & Robustness | 10% |
| AI Impact & Risk Management | 10% |
| Monitoring & Lifecycle Management | 5% |
| Accountability to Affected People | 5% |

See [docs/assessment-framework.md](docs/assessment-framework.md) for details.

## Scoring Methodology

```
Question Score = response / 4
Category Score = (sum of question scores / applicable questions) × 100
Overall Score = weighted sum of category scores (rounded to 1 decimal)
```

Response scale: Fully implemented (4), Mostly (3), Partially (2), Planned (1), Not implemented (0), Not applicable (excluded).

See [docs/scoring-methodology.md](docs/scoring-methodology.md) for formulas and readiness levels.

## Architecture

```
Frontend (Next.js/React/TypeScript/Tailwind)
    ↕ REST API
Backend (Python/FastAPI/Pydantic)
    ↕ SQLAlchemy ORM
Database (SQLite dev / PostgreSQL prod)
```

See [docs/architecture.md](docs/architecture.md) for the full architecture diagram and entity relationships.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS, Recharts |
| Backend | Python 3.11+, FastAPI, Pydantic, SQLAlchemy |
| Database | SQLite (development), PostgreSQL (production) |
| PDF | WeasyPrint (Phase 6) |
| Testing | pytest, TypeScript tests |

## Project Structure

```
ai-governance-assessment/
├── backend/           # FastAPI API and scoring engine
├── frontend/          # Next.js web application
├── docs/              # Architecture, methodology, development phases
├── tests/             # Cross-cutting tests
├── .cursor/rules/     # Cursor development instructions
├── .env.example       # Environment variable template
├── CONTRIBUTING.md
└── SECURITY.md
```

## Installation

### Prerequisites

- Python 3.11+
- Node.js 20+
- npm or yarn

### Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp ../.env.example .env
```

### Frontend

```bash
cd frontend
npm install
cp ../.env.example .env.local
```

## Running Locally

Start the backend:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Start the frontend (separate terminal):

```bash
cd frontend
npm run dev
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

## Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## Development Phases

This project is built incrementally. See [docs/development-phases.md](docs/development-phases.md).

**Current status: Phase 5 complete.** Full assessment workflow with scoring, recommendations, risk matrix, and professional reporting.

## Deployment

Deployment configuration will be added in Phase 10. The application is designed for:

- Backend: any Python-compatible host (Railway, Render, AWS, Azure)
- Frontend: Vercel, Netlify, or static export
- Database: PostgreSQL recommended for production

## Privacy Notice

> Do not enter confidential, personal, proprietary, or sensitive information into this demonstration application.

The application collects minimal assessment data, provides delete functionality (Phase 8), and does not send data to external LLMs without explicit user action.

## Limitations

- Results are **indicative**, not certifying compliance or safety
- Not a substitute for legal, regulatory, or professional advice
- Scoring reflects self-reported maturity, not verified controls
- Demo mode uses fictional sample data only

## License

MIT License — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md).
