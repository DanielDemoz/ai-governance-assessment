"""Verify database schema and model integrity."""

import pytest
from decimal import Decimal

from app.db.base import Base
from app.models import (
    Assessment,
    AssessmentResult,
    Category,
    Organization,
    AISystem,
    Question,
    Response,
    Risk,
    Recommendation,
    Report,
)


EXPECTED_CATEGORIES = [
    ("accountability", Decimal("15.00")),
    ("human_oversight", Decimal("15.00")),
    ("privacy", Decimal("15.00")),
    ("fairness", Decimal("15.00")),
    ("transparency", Decimal("10.00")),
    ("security", Decimal("10.00")),
    ("risk_management", Decimal("10.00")),
    ("lifecycle", Decimal("5.00")),
    ("affected_people", Decimal("5.00")),
]


def test_all_entities_registered_on_base():
    """All required entities must map to database tables."""
    table_names = set(Base.metadata.tables.keys())
    required = {
        "assessments",
        "organizations",
        "ai_systems",
        "categories",
        "questions",
        "responses",
        "risks",
        "recommendations",
        "assessment_results",
        "reports",
    }
    assert required.issubset(table_names)


def test_category_weights_total_100():
    """Category weights must sum to 100%."""
    total = sum(weight for _, weight in EXPECTED_CATEGORIES)
    assert total == Decimal("100.00")


def test_nine_categories_defined():
    assert len(EXPECTED_CATEGORIES) == 9


def test_assessment_has_required_relationships():
    mapper = Assessment.__mapper__
    rel_names = set(mapper.relationships.keys())
    assert rel_names >= {
        "organization",
        "ai_system",
        "responses",
        "risks",
        "recommendations",
        "result",
        "reports",
    }


def test_response_unique_constraint():
    constraints = {c.name for c in Response.__table__.constraints if hasattr(c, "name") and c.name}
    assert "uq_assessment_question" in constraints
