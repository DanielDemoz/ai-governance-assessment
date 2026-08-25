"""Risk assessment services."""

from sqlalchemy.orm import Session

from app.models.risk import Risk
from app.services.risk.suggestions import suggest_risks
from app.services.scoring.engine import AISystemProfileInput


def profile_from_ai_system(ai_system) -> AISystemProfileInput:
    return AISystemProfileInput(
        makes_decisions_about_people=ai_system.makes_decisions_about_people,
        recommends_decisions=ai_system.recommends_decisions,
        can_materially_affect_individual=ai_system.can_materially_affect_individual,
        affects_employment=ai_system.affects_employment,
        affects_education=ai_system.affects_education,
        affects_healthcare=ai_system.affects_healthcare,
        affects_financial_access=ai_system.affects_financial_access,
        affects_public_services=ai_system.affects_public_services,
        affects_housing=ai_system.affects_housing,
        affects_insurance=ai_system.affects_insurance,
        affects_legal_rights=ai_system.affects_legal_rights,
        processes_personal_info=ai_system.processes_personal_info,
        processes_sensitive_info=ai_system.processes_sensitive_info,
        processes_health_info=ai_system.processes_health_info,
    )


def generate_and_store_risks(db: Session, assessment) -> list[Risk]:
    if assessment.ai_system is None:
        return []

    db.query(Risk).filter(Risk.assessment_id == assessment.id).delete()

    profile = profile_from_ai_system(assessment.ai_system)
    suggested = suggest_risks(profile)

    stored: list[Risk] = []
    for item in suggested:
        risk = Risk(
            assessment_id=assessment.id,
            risk_type=item["risk_type"],
            description=item["description"],
            likelihood=item["likelihood"],
            impact=item["impact"],
            risk_score=item["risk_score"],
            classification=item["classification"],
        )
        db.add(risk)
        stored.append(risk)

    db.flush()
    return stored


def get_assessment_risks(db: Session, assessment_id: int) -> list[Risk]:
    return db.query(Risk).filter(Risk.assessment_id == assessment_id).order_by(Risk.risk_score.desc()).all()
