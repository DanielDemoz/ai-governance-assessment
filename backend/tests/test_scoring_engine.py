"""Unit tests for the deterministic scoring engine."""

import pytest

from app.models.assessment import AISystemRiskLevel, GovernanceGapLevel, ReadinessLevel
from app.services.scoring.engine import (
    AISystemProfileInput,
    QuestionInput,
    calculate_category_score,
    calculate_overall_score,
    normalize_response,
    readiness_level_from_score,
    score_assessment,
)


def _question(
    category: str,
    response: int,
    qid: int = 1,
    code: str = "q1",
    text: str = "Sample question?",
) -> QuestionInput:
    return QuestionInput(
        question_id=qid,
        question_code=code,
        question_text=text,
        category_code=category,
        response_value=response,
    )


class TestNormalizeResponse:
    def test_fully_implemented(self):
        assert normalize_response(4) == 1.0

    def test_not_implemented(self):
        assert normalize_response(0) == 0.0

    def test_not_applicable_excluded(self):
        assert normalize_response(-1) is None

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            normalize_response(5)


class TestCategoryScore:
    def test_all_fully_implemented(self):
        questions = [
            type("Q", (), {"excluded": False, "normalized_score": 1.0})(),
            type("Q", (), {"excluded": False, "normalized_score": 1.0})(),
        ]
        assert calculate_category_score(questions) == 100.0

    def test_not_applicable_excluded_from_denominator(self):
        result = score_assessment(
            [
                _question("accountability", 4, qid=1, code="a1"),
                _question("accountability", -1, qid=2, code="a2"),
            ],
            {"accountability": "Accountability & Governance"},
        )
        acc = next(c for c in result.category_scores if c.category_code == "accountability")
        assert acc.applicable_questions == 1
        assert acc.category_score == 100.0


class TestOverallScore:
    def test_weighted_calculation(self):
        scores = {
            "accountability": 80.0,
            "human_oversight": 80.0,
            "privacy": 80.0,
            "fairness": 80.0,
            "transparency": 80.0,
            "security": 80.0,
            "risk_management": 80.0,
            "lifecycle": 80.0,
            "affected_people": 80.0,
        }
        assert calculate_overall_score(scores) == 80.0

    def test_rounds_to_one_decimal(self):
        scores = {
            "accountability": 72.0,
            "human_oversight": 68.0,
            "privacy": 75.0,
            "fairness": 70.0,
            "transparency": 65.0,
            "security": 60.0,
            "risk_management": 55.0,
            "lifecycle": 50.0,
            "affected_people": 45.0,
        }
        overall = calculate_overall_score(scores)
        assert overall == round(overall, 1)


class TestReadinessLevels:
    @pytest.mark.parametrize(
        "score,expected",
        [
            (95, ReadinessLevel.LEADING),
            (82, ReadinessLevel.ADVANCED),
            (68, ReadinessLevel.ESTABLISHED),
            (50, ReadinessLevel.DEVELOPING),
            (25, ReadinessLevel.INITIAL),
        ],
    )
    def test_levels(self, score, expected):
        assert readiness_level_from_score(score) == expected


class TestKnownExample:
    """Verify scoring against a hand-calculated example."""

    def test_mixed_responses(self):
        # accountability: [4, 3, 2, 0] => (1.0+0.75+0.5+0)/4 * 100 = 56.25
        questions = [
            _question("accountability", 4, 1, "a1"),
            _question("accountability", 3, 2, "a2"),
            _question("accountability", 2, 3, "a3"),
            _question("accountability", 0, 4, "a4"),
        ]
        for code, value in [
            ("human_oversight", 4),
            ("privacy", 4),
            ("fairness", 4),
            ("transparency", 4),
            ("security", 4),
            ("risk_management", 4),
            ("lifecycle", 4),
            ("affected_people", 4),
        ]:
            questions.append(_question(code, value, len(questions) + 1, f"{code}_1"))

        result = score_assessment(questions, {"accountability": "Accountability & Governance"})
        acc = next(c for c in result.category_scores if c.category_code == "accountability")
        assert acc.category_score == 56.2  # rounded to 1 decimal

        # Overall: 56.2*0.15 + 100*0.85 = 8.43 + 85 = 93.43
        assert result.overall_score == 93.4
        assert result.readiness_level == ReadinessLevel.LEADING


class TestAISystemRisk:
    def test_high_risk_profile(self):
        profile = AISystemProfileInput(
            makes_decisions_about_people=True,
            can_materially_affect_individual=True,
            affects_healthcare=True,
            affects_education=True,
            processes_sensitive_info=True,
        )
        result = score_assessment([_question("accountability", 4)], {}, profile)
        assert result.ai_system_risk in {AISystemRiskLevel.HIGH, AISystemRiskLevel.CRITICAL}

    def test_low_risk_profile(self):
        result = score_assessment([_question("accountability", 4)], {}, AISystemProfileInput())
        assert result.ai_system_risk == AISystemRiskLevel.LOW


class TestGovernanceGap:
    def test_high_risk_low_readiness_is_critical_gap(self):
        profile = AISystemProfileInput(
            makes_decisions_about_people=True,
            can_materially_affect_individual=True,
            affects_legal_rights=True,
            affects_healthcare=True,
        )
        questions = [_question("accountability", 0, 1, "a1")]
        for code in [
            "human_oversight", "privacy", "fairness", "transparency",
            "security", "risk_management", "lifecycle", "affected_people",
        ]:
            questions.append(_question(code, 0, len(questions) + 1, f"{code}_1"))

        result = score_assessment(questions, {}, profile)
        assert result.governance_gap == GovernanceGapLevel.CRITICAL
