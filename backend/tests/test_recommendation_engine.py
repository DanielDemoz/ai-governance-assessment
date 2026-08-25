"""Unit tests for the recommendation engine."""

import pytest

from app.models.assessment import AISystemRiskLevel
from app.models.question import RiskLevel
from app.models.recommendation import RecommendationPriority
from app.models.response import ResponseValue
from app.services.recommendations.engine import (
    QuestionContext,
    determine_priority,
    determine_timeframe,
    generate_recommendations,
)
from app.services.recommendations.roadmap import build_roadmap
from app.services.recommendations.rules_data import all_recommendation_keys, get_rule_content


def _ctx(response: int, risk: RiskLevel = RiskLevel.HIGH, key: str = "ho_human_involved") -> QuestionContext:
    return QuestionContext(
        question_id=1,
        question_code="test_q",
        question_text="Is a human involved in consequential decisions?",
        category_id=1,
        category_code="human_oversight",
        category_name="Human Oversight",
        recommendation_key=key,
        governance_objective="Ensure meaningful human involvement.",
        risk_level=risk,
        response_value=response,
    )


class TestDeterminePriority:
    def test_fully_implemented_no_recommendation(self):
        assert determine_priority(4, RiskLevel.CRITICAL, AISystemRiskLevel.HIGH) is None

    def test_not_applicable_no_recommendation(self):
        assert determine_priority(-1, RiskLevel.CRITICAL, AISystemRiskLevel.HIGH) is None

    def test_not_implemented_critical_risk_is_critical(self):
        priority = determine_priority(0, RiskLevel.CRITICAL, AISystemRiskLevel.LOW)
        assert priority == RecommendationPriority.CRITICAL

    def test_high_system_risk_elevates_priority(self):
        priority = determine_priority(2, RiskLevel.MEDIUM, AISystemRiskLevel.HIGH)
        assert priority == RecommendationPriority.HIGH


class TestSpecExamples:
    def test_human_oversight_zero_is_critical(self):
        recs = generate_recommendations([_ctx(0)], AISystemRiskLevel.MODERATE)
        assert len(recs) == 1
        assert recs[0].priority == RecommendationPriority.CRITICAL
        assert "human-review" in recs[0].recommendation.lower()

    def test_fairness_testing_zero_is_high_or_critical(self):
        recs = generate_recommendations(
            [_ctx(0, RiskLevel.CRITICAL, "fair_bias_testing")],
            AISystemRiskLevel.MODERATE,
        )
        assert len(recs) == 1
        assert recs[0].priority == RecommendationPriority.CRITICAL
        assert "fairness" in recs[0].recommendation.lower()

    def test_all_fully_implemented_produces_no_recommendations(self):
        recs = generate_recommendations([_ctx(4)], AISystemRiskLevel.HIGH)
        assert recs == []


class TestTimeframes:
    def test_critical_is_immediate(self):
        assert determine_timeframe(RecommendationPriority.CRITICAL, AISystemRiskLevel.LOW) == "0-30 days"

    def test_high_with_high_risk_is_immediate(self):
        assert determine_timeframe(RecommendationPriority.HIGH, AISystemRiskLevel.HIGH) == "0-30 days"

    def test_low_is_long_term(self):
        assert determine_timeframe(RecommendationPriority.LOW, AISystemRiskLevel.LOW) == "6-12 months"


class TestRoadmap:
    def test_groups_by_timeframe(self):
        recs = generate_recommendations(
            [
                _ctx(0, RiskLevel.CRITICAL, "ho_human_involved"),
                _ctx(3, RiskLevel.LOW, "lc_retirement"),
            ],
            AISystemRiskLevel.LOW,
        )
        phases = build_roadmap(recs)
        keys = {p.key for p in phases}
        assert "immediate" in keys
        assert "long_term" in keys


class TestRulesCoverage:
    def test_all_question_keys_have_rule_content(self):
        keys = all_recommendation_keys()
        assert len(keys) == 67
        for key in keys:
            content = get_rule_content(key, "Sample question?", "Sample objective", "accountability")
            assert content.recommendation
            assert content.why_it_matters
            assert content.suggested_action
            assert content.responsible_role
