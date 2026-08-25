"""Generate suggested governance risks from the AI system profile."""

from app.models.risk import RiskClassification, RiskType
from app.services.risk.matrix import calculate_risk_score, classify_risk_score
from app.services.scoring.engine import AISystemProfileInput


def _defaults(profile: AISystemProfileInput) -> tuple[int, int]:
    """Base likelihood and impact from profile severity."""
    if profile.makes_decisions_about_people and profile.can_materially_affect_individual:
        return 4, 4
    if profile.makes_decisions_about_people or profile.can_materially_affect_individual:
        return 3, 4
    if profile.recommends_decisions:
        return 3, 3
    return 2, 2


def suggest_risks(profile: AISystemProfileInput) -> list[dict]:
    """Return suggested risk entries derived from the AI system profile."""
    base_l, base_i = _defaults(profile)
    suggestions: list[dict] = []

    mapping: list[tuple[str, RiskType, bool, str]] = [
        ("processes_personal_info", RiskType.PRIVACY_BREACH, profile.processes_personal_info, "Personal data processing increases privacy exposure."),
        ("processes_sensitive_info", RiskType.DATA_LEAKAGE, profile.processes_sensitive_info, "Sensitive data requires strengthened access and handling controls."),
        ("makes_decisions_about_people", RiskType.INCORRECT_DECISIONS, profile.makes_decisions_about_people, "Automated decisions may produce incorrect or unfair outcomes."),
        ("recommends_decisions", RiskType.AUTOMATION_BIAS, profile.recommends_decisions, "Staff may over-rely on AI recommendations without sufficient review."),
        ("affects_employment", RiskType.ALGORITHMIC_BIAS, profile.affects_employment, "Employment-related AI use requires fairness and oversight controls."),
        ("affects_education", RiskType.ALGORITHMIC_BIAS, profile.affects_education, "Education-related AI use may affect access to opportunities."),
        ("affects_healthcare", RiskType.INCORRECT_DECISIONS, profile.affects_healthcare, "Healthcare-related AI errors may cause patient harm."),
        ("affects_legal_rights", RiskType.LACK_OF_TRANSPARENCY, profile.affects_legal_rights, "Opaque AI use in legal contexts may affect due process."),
        ("makes_decisions_about_people", RiskType.LACK_OF_HUMAN_OVERSIGHT, profile.makes_decisions_about_people, "Consequential AI use requires documented human oversight."),
    ]

    seen: set[RiskType] = set()
    for _key, risk_type, condition, description in mapping:
        if not condition or risk_type in seen:
            continue
        seen.add(risk_type)
        likelihood = base_l
        impact = base_i
        if risk_type in {RiskType.PRIVACY_BREACH, RiskType.INCORRECT_DECISIONS, RiskType.LACK_OF_HUMAN_OVERSIGHT}:
            impact = min(5, base_i + 1)
        score = calculate_risk_score(likelihood, impact)
        suggestions.append(
            {
                "risk_type": risk_type,
                "description": description,
                "likelihood": likelihood,
                "impact": impact,
                "risk_score": score,
                "classification": classify_risk_score(score),
            }
        )

    if not suggestions:
        score = calculate_risk_score(2, 2)
        suggestions.append(
            {
                "risk_type": RiskType.MODEL_FAILURE,
                "description": "All AI systems carry baseline operational and reliability risk.",
                "likelihood": 2,
                "impact": 2,
                "risk_score": score,
                "classification": classify_risk_score(score),
            }
        )

    return suggestions
