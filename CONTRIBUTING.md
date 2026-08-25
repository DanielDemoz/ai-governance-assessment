# Contributing

Thank you for contributing to the AI Governance Readiness Assessment project.

## Development Approach

This project is built in **phases**. See [docs/development-phases.md](docs/development-phases.md) for the current phase and scope.

Before starting work:

1. Read the README and architecture documentation.
2. Confirm which phase is active — do not implement future-phase features prematurely.
3. Inspect existing code before making changes.

## Setup

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Code Standards

- **Python**: Type hints, Pydantic models, pytest for tests.
- **TypeScript**: Strict mode, consistent types shared via API contracts.
- **Scoring**: Deterministic only — never use an LLM for numerical scores.
- **Separation**: Keep scoring logic independent from UI and API handlers.

## Testing

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

## Pull Requests

- Keep changes focused on the current development phase.
- Include tests for scoring, recommendations, and validation logic.
- Do not commit secrets, `.env` files, or generated build artifacts.
- Use meaningful commit messages.

## Reporting Issues

Use GitHub issues for bugs, enhancements, and phase-related tasks. See [docs/github-issues.md](docs/github-issues.md) for planned improvements.
