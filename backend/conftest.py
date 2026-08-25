"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.seed import seed_reference_data
from app.db.session import SessionLocal, init_db
from app.main import app

sys.path.insert(0, str(Path(__file__).resolve().parent))


@pytest.fixture
def client():
    init_db()
    db = SessionLocal()
    try:
        seed_reference_data(db)
    finally:
        db.close()
    return TestClient(app)


@pytest.fixture
def db_session() -> Session:
    init_db()
    db = SessionLocal()
    try:
        seed_reference_data(db)
        yield db
    finally:
        db.close()
