"""FastAPI application entry point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.api import api_router
from app.config import get_settings
from app.db.seed import seed_reference_data
from app.db.session import SessionLocal, init_db

settings = get_settings()

app = FastAPI(
    title="AI Governance Readiness Assessment API",
    description=(
        "Deterministic AI governance assessment, scoring, and reporting. "
        "This tool provides indicative readiness assessments — not legal advice or certification."
    ),
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
def on_startup() -> None:
    if settings.database_url.startswith("sqlite"):
        db_path = settings.database_url.replace("sqlite:///", "")
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    init_db()
    db = SessionLocal()
    try:
        seed_reference_data(db)
    finally:
        db.close()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


static_root = Path(settings.static_dir) if settings.static_dir else None
if static_root and static_root.is_dir():
    app.mount("/", StaticFiles(directory=static_root, html=True), name="frontend")
