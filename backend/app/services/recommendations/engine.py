"""Deterministic recommendation engine — never uses an LLM."""

from dataclasses import dataclass

from app.models.assessment import AISystemRiskLevel
from app.models.question import RiskLevel
from app.models.recommendation import RecommendationPriority
from app.models.response import ResponseValue
from app.services.recommendations.rules_data import get_rule_content

RESPONSE_LABELS = {
    ResponseValue.NOT_IMPLEMENTED.value: "Not implemented",
    ResponseValue.PLANNED.value: "Planned",
    ResponseValue.PARTIALLY_IMPLEMENTED.value: "Partially implemented",
    ResponseValue.MOSTLY_IMPLEMENTED.value: "Mostly implemented",
}

PRIORITY_ORDER = {
    RecommendationPriority.CRITICAL: 0,
    RecommendationPriority.HIGH: 1,
    RecommendationPriority.MEDIUM: 2,
    RecommendationPriority.LOW: 3,
}


@dataclass
class QuestionContext:
    question_id: int
    question_code: str
    question_text: str
    category_id: int
    category_code: str
    category_name: str
    recommendation_key: str
    governance_objective: str | None
    risk_level: RiskLevel
    response_value: int


@dataclass
class GeneratedRecommendation:
    question_id: int
    category_id: int
    category_code: str
    category_name: str
    priority: RecommendationPriority
    identified_gap: str
    recommendation: str
    why_it_matters: str
    suggested_action: str
    responsible_role: str
    suggested_timeframe: str
    source_rule_key: str


def _elevate_priority(
    priority: RecommendationPriority,
    ai_system_risk: AISystemRiskLevel,
) -> RecommendationPriority:
    if ai_system_risk not in {AISystemRiskLevel.HIGH, AISystemRiskLevel.CRITICAL}:
        return priority
    order = [
        RecommendationPriority.LOW,
        RecommendationPriority.MEDIUM,
        RecommendationPriority.HIGH,
        RecommendationPriority.CRITICAL,
    ]
    idx = order.index(priority)
    return order[min(idx + 1, len(order) - 1)]


def determine_priority(
    response_value: int,
    risk_level: RiskLevel,
    ai_system_risk: AISystemRiskLevel,
) -> RecommendationPriority | None:
    if response_value in {ResponseValue.FULLY_IMPLEMENTED.value, ResponseValue.NOT_APPLICABLE.value}:
        return None
    if response_value == ResponseValue.NOT_IMPLEMENTED.value:
        if risk_level in {RiskLevel.CRITICAL, RiskLevel.HIGH}:
            base = RecommendationPriority.CRITICAL
        elif risk_level == RiskLevel.MEDIUM:
            base = RecommendationPriority.HIGH
        else:
            base = RecommendationPriority.MEDIUM
    elif response_value == ResponseValue.PLANNED.value:
        if risk_level in {RiskLevel.CRITICAL, RiskLevel.HIGH}:
            base = RecommendationPriority.HIGH
        else:
            base = RecommendationPriority.MEDIUM
    elif response_value == ResponseValue.PARTIALLY_IMPLEMENTED.value:
        base = RecommendationPriority.MEDIUM
    else:  # MOSTLY_IMPLEMENTED
        base = RecommendationPriority.LOW

    return _elevate_priority(base, ai_system_risk)


def determine_timeframe(
    priority: RecommendationPriority,
    ai_system_risk: AISystemRiskLevel,
) -> str:
    if priority == RecommendationPriority.CRITICAL:
        return "0-30 days"
    if priority == RecommendationPriority.HIGH:
        if ai_system_risk in {AISystemRiskLevel.HIGH, AISystemRiskLevel.CRITICAL}:
            return "0-30 days"
        return "31-90 days"
    if priority == RecommendationPriority.MEDIUM:
        return "3-6 months"
    return "6-12 months"


def generate_recommendations(
    questions: list[QuestionContext],
    ai_system_risk: AISystemRiskLevel,
) -> list[GeneratedRecommendation]:
    recommendations: list[GeneratedRecommendation] = []

    for q in questions:
        priority = determine_priority(q.response_value, q.risk_level, ai_system_risk)
        if priority is None:
            continue

        rule = get_rule_content(
            q.recommendation_key,
            q.question_text,
            q.governance_objective,
            q.category_code,
        )
        response_label = RESPONSE_LABELS.get(q.response_value, str(q.response_value))
        identified_gap = (
            f"{q.question_text} Currently rated as '{response_label}'."
        )

        recommendations.append(
            GeneratedRecommendation(
                question_id=q.question_id,
                category_id=q.category_id,
                category_code=q.category_code,
                category_name=q.category_name,
                priority=priority,
                identified_gap=identified_gap,
                recommendation=rule.recommendation,
                why_it_matters=rule.why_it_matters,
                suggested_action=rule.suggested_action,
                responsible_role=rule.responsible_role,
                suggested_timeframe=determine_timeframe(priority, ai_system_risk),
                source_rule_key=q.recommendation_key,
            )
        )

    recommendations.sort(key=lambda r: (PRIORITY_ORDER[r.priority], r.category_name, r.identified_gap))
    return recommendations
