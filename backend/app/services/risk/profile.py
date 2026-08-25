"""AI system risk profile analysis."""

from dataclasses import dataclass

from app.models.assessment import AISystemRiskLevel
from app.services.scoring.engine import AISystemProfileInput, calculate_ai_system_risk


@dataclass
class RiskFactor:
    code: str
    label: str
    present: bool
    weight: int


@dataclass
class AISystemRiskProfile:
    level: AISystemRiskLevel
    score: int
    factors: list[RiskFactor]
    summary: str


def build_ai_system_risk_profile(profile: AISystemProfileInput) -> AISystemRiskProfile:
    factors = [
        RiskFactor("makes_decisions_about_people", "Makes decisions about people", profile.makes_decisions_about_people, 3),
        RiskFactor("can_materially_affect_individual", "Can materially affect individuals", profile.can_materially_affect_individual, 3),
        RiskFactor("recommends_decisions", "Recommends decisions", profile.recommends_decisions, 2),
        RiskFactor("processes_sensitive_info", "Processes sensitive information", profile.processes_sensitive_info, 2),
        RiskFactor("processes_health_info", "Processes health information", profile.processes_health_info, 2),
        RiskFactor("processes_personal_info", "Processes personal information", profile.processes_personal_info, 1),
        RiskFactor("affects_healthcare", "Affects healthcare", profile.affects_healthcare, 2),
        RiskFactor("affects_employment", "Affects employment", profile.affects_employment, 2),
        RiskFactor("affects_legal_rights", "Affects legal rights or opportunities", profile.affects_legal_rights, 2),
        RiskFactor("affects_financial_access", "Affects financial access", profile.affects_financial_access, 2),
        RiskFactor("affects_education", "Affects education", profile.affects_education, 2),
        RiskFactor("affects_housing", "Affects housing", profile.affects_housing, 2),
        RiskFactor("affects_insurance", "Affects insurance", profile.affects_insurance, 2),
        RiskFactor("affects_public_services", "Affects public services", profile.affects_public_services, 2),
    ]

    score = sum(f.weight for f in factors if f.present)
    level = calculate_ai_system_risk(profile)

    summaries = {
        AISystemRiskLevel.LOW: "The AI system profile indicates limited personal data use and low consequential impact on individuals.",
        AISystemRiskLevel.MODERATE: "The AI system profile indicates moderate data sensitivity or advisory influence over individual outcomes.",
        AISystemRiskLevel.HIGH: "The AI system profile indicates consequential decisions or impacts affecting individuals in sensitive domains.",
        AISystemRiskLevel.CRITICAL: "The AI system profile indicates high-impact automated or semi-automated decisions affecting individuals in regulated or sensitive areas.",
    }

    return AISystemRiskProfile(
        level=level,
        score=score,
        factors=factors,
        summary=summaries[level],
    )
