"""Tests for governance risk matrix."""

import pytest

from app.models.risk import RiskClassification
from app.services.risk.matrix import calculate_risk_score, classify_risk_score, matrix_cell_level
from app.services.risk.profile import build_ai_system_risk_profile
from app.services.risk.suggestions import suggest_risks
from app.services.scoring.engine import AISystemProfileInput


class TestMatrixCalculations:
    @pytest.mark.parametrize(
        "score,expected",
        [(4, RiskClassification.LOW), (9, RiskClassification.MODERATE), (16, RiskClassification.HIGH), (25, RiskClassification.CRITICAL)],
    )
    def test_classify(self, score, expected):
        assert classify_risk_score(score) == expected

    def test_risk_score_product(self):
        assert calculate_risk_score(4, 5) == 20

    def test_cell_level(self):
        assert matrix_cell_level(5, 5) == RiskClassification.CRITICAL


class TestAISystemRiskProfile:
    def test_high_impact_profile(self):
        profile = AISystemProfileInput(
            makes_decisions_about_people=True,
            affects_healthcare=True,
            processes_personal_info=True,
        )
        result = build_ai_system_risk_profile(profile)
        assert result.level.value in {"high", "critical"}
        assert any(f.present for f in result.factors)


class TestSuggestedRisks:
    def test_generates_risks_from_profile(self):
        profile = AISystemProfileInput(processes_personal_info=True, makes_decisions_about_people=True)
        risks = suggest_risks(profile)
        assert len(risks) >= 2
        assert all(1 <= r["likelihood"] <= 5 for r in risks)
        assert all(r["risk_score"] == r["likelihood"] * r["impact"] for r in risks)
