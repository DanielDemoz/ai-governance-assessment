"""Deterministic scoring engine — no LLM involvement."""

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP

from app.models.assessment import (
    AISystemRiskLevel,
    GovernanceGapLevel,
    ReadinessLevel,
)

NOT_APPLICABLE = -1
MAX_RESPONSE_VALUE = 4

CATEGORY_WEIGHTS: dict[str, Decimal] = {
    "accountability": Decimal("0.15"),
    "human_oversight": Decimal("0.15"),
    "privacy": Decimal("0.15"),
    "fairness": Decimal("0.15"),
    "transparency": Decimal("0.10"),
    "security": Decimal("0.10"),
    "risk_management": Decimal("0.10"),
    "lifecycle": Decimal("0.05"),
    "affected_people": Decimal("0.05"),
}


@dataclass
class QuestionInput:
    question_id: int
    question_code: str
    question_text: str
    category_code: str
    response_value: int  # 0–4 or -1 for N/A


@dataclass
class QuestionScoreDetail:
    question_id: int
    question_code: str
    question_text: str
    response_value: int
    normalized_score: float | None
    excluded: bool


@dataclass
class CategoryScoreDetail:
    category_code: str
    category_name: str
    weight_percent: float
    applicable_questions: int
    answered_questions: int
    category_score: float
    questions: list[QuestionScoreDetail] = field(default_factory=list)


@dataclass
class AISystemProfileInput:
    makes_decisions_about_people: bool = False
    recommends_decisions: bool = False
    can_materially_affect_individual: bool = False
    affects_employment: bool = False
    affects_education: bool = False
    affects_healthcare: bool = False
    affects_financial_access: bool = False
    affects_public_services: bool = False
    affects_housing: bool = False
    affects_insurance: bool = False
    affects_legal_rights: bool = False
    processes_personal_info: bool = False
    processes_sensitive_info: bool = False
    processes_health_info: bool = False


@dataclass
class ScoringResult:
    overall_score: float
    readiness_level: ReadinessLevel
    ai_system_risk: AISystemRiskLevel
    governance_gap: GovernanceGapLevel
    category_scores: list[CategoryScoreDetail]
    calculation_trace: dict


def normalize_response(response_value: int) -> float | None:
    if response_value == NOT_APPLICABLE:
        return None
    if response_value < 0 or response_value > MAX_RESPONSE_VALUE:
        raise ValueError(f"Invalid response value: {response_value}")
    return response_value / MAX_RESPONSE_VALUE


def calculate_category_score(questions: list[QuestionScoreDetail]) -> float:
    applicable = [q for q in questions if not q.excluded]
    if not applicable:
        return 0.0
    total = sum(q.normalized_score or 0.0 for q in applicable)
    return round((total / len(applicable)) * 100, 1)


def calculate_overall_score(category_scores: dict[str, float]) -> float:
    total = Decimal("0")
    for code, weight in CATEGORY_WEIGHTS.items():
        score = Decimal(str(category_scores.get(code, 0.0)))
        total += score * weight
    return float(total.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def readiness_level_from_score(score: float) -> ReadinessLevel:
    if score >= 90:
        return ReadinessLevel.LEADING
    if score >= 75:
        return ReadinessLevel.ADVANCED
    if score >= 60:
        return ReadinessLevel.ESTABLISHED
    if score >= 40:
        return ReadinessLevel.DEVELOPING
    return ReadinessLevel.INITIAL


def calculate_ai_system_risk(profile: AISystemProfileInput) -> AISystemRiskLevel:
    score = 0
    if profile.makes_decisions_about_people:
        score += 3
    if profile.can_materially_affect_individual:
        score += 3
    if profile.recommends_decisions:
        score += 2
    if profile.processes_sensitive_info or profile.processes_health_info:
        score += 2
    if profile.processes_personal_info:
        score += 1

    high_impact_domains = [
        profile.affects_healthcare,
        profile.affects_employment,
        profile.affects_legal_rights,
        profile.affects_financial_access,
        profile.affects_education,
        profile.affects_housing,
        profile.affects_insurance,
        profile.affects_public_services,
    ]
    score += sum(2 for flag in high_impact_domains if flag)

    if score >= 10:
        return AISystemRiskLevel.CRITICAL
    if score >= 6:
        return AISystemRiskLevel.HIGH
    if score >= 3:
        return AISystemRiskLevel.MODERATE
    return AISystemRiskLevel.LOW


def calculate_governance_gap(
    readiness_score: float,
    ai_system_risk: AISystemRiskLevel,
) -> GovernanceGapLevel:
    risk_weight = {
        AISystemRiskLevel.LOW: 0,
        AISystemRiskLevel.MODERATE: 1,
        AISystemRiskLevel.HIGH: 2,
        AISystemRiskLevel.CRITICAL: 3,
    }[ai_system_risk]

    if readiness_score < 40:
        base = 3
    elif readiness_score < 60:
        base = 2
    elif readiness_score < 75:
        base = 1
    else:
        base = 0

    combined = base + risk_weight
    if combined >= 5:
        return GovernanceGapLevel.CRITICAL
    if combined >= 3:
        return GovernanceGapLevel.HIGH
    if combined >= 2:
        return GovernanceGapLevel.MODERATE
    return GovernanceGapLevel.LOW


def score_assessment(
    questions: list[QuestionInput],
    category_names: dict[str, str],
    profile: AISystemProfileInput | None = None,
) -> ScoringResult:
    """Calculate full assessment scores from question responses."""
    by_category: dict[str, list[QuestionInput]] = {}
    for q in questions:
        by_category.setdefault(q.category_code, []).append(q)

    category_details: list[CategoryScoreDetail] = []
    category_score_map: dict[str, float] = {}

    for code in CATEGORY_WEIGHTS:
        cat_questions = by_category.get(code, [])
        question_details: list[QuestionScoreDetail] = []
        for q in cat_questions:
            normalized = normalize_response(q.response_value)
            question_details.append(
                QuestionScoreDetail(
                    question_id=q.question_id,
                    question_code=q.question_code,
                    question_text=q.question_text,
                    response_value=q.response_value,
                    normalized_score=normalized,
                    excluded=normalized is None,
                )
            )
        cat_score = calculate_category_score(question_details)
        category_score_map[code] = cat_score
        category_details.append(
            CategoryScoreDetail(
                category_code=code,
                category_name=category_names.get(code, code),
                weight_percent=float(CATEGORY_WEIGHTS[code] * 100),
                applicable_questions=len([q for q in question_details if not q.excluded]),
                answered_questions=len(question_details),
                category_score=cat_score,
                questions=question_details,
            )
        )

    overall = calculate_overall_score(category_score_map)
    readiness = readiness_level_from_score(overall)
    ai_risk = calculate_ai_system_risk(profile or AISystemProfileInput())
    gap = calculate_governance_gap(overall, ai_risk)

    trace = {
        "formula": {
            "question_score": "response_value / 4",
            "category_score": "(sum of question scores / applicable questions) × 100",
            "overall_score": "weighted sum of category scores",
        },
        "category_weights": {k: float(v) for k, v in CATEGORY_WEIGHTS.items()},
        "category_scores": category_score_map,
        "overall_score": overall,
        "readiness_level": readiness.value,
        "ai_system_risk": ai_risk.value,
        "governance_gap": gap.value,
        "categories": [
            {
                "code": c.category_code,
                "name": c.category_name,
                "weight_percent": c.weight_percent,
                "score": c.category_score,
                "applicable_questions": c.applicable_questions,
                "questions": [
                    {
                        "question_id": q.question_id,
                        "code": q.question_code,
                        "text": q.question_text,
                        "response_value": q.response_value,
                        "normalized_score": q.normalized_score,
                        "excluded": q.excluded,
                    }
                    for q in c.questions
                ],
            }
            for c in category_details
        ],
    }

    return ScoringResult(
        overall_score=overall,
        readiness_level=readiness,
        ai_system_risk=ai_risk,
        governance_gap=gap,
        category_scores=category_details,
        calculation_trace=trace,
    )
