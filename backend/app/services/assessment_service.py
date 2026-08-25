"""Assessment business logic."""

import json
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.assessment import Assessment, AssessmentResult, AssessmentStatus
from app.models.category import Category
from app.models.organization import AISystem, Organization
from app.models.question import Question
from app.models.recommendation import Recommendation
from app.models.response import Response, ResponseValue
from app.models.risk import Risk
from app.services.recommendation_service import generate_and_store_recommendations
from app.services.risk_service import generate_and_store_risks
from app.services.scoring.engine import AISystemProfileInput, QuestionInput, score_assessment


def get_assessment_by_public_id(db: Session, public_id: str) -> Assessment:
    assessment = (
        db.query(Assessment)
        .options(
            joinedload(Assessment.organization),
            joinedload(Assessment.ai_system),
            joinedload(Assessment.responses),
            joinedload(Assessment.result),
            joinedload(Assessment.recommendations).joinedload(Recommendation.category),
            joinedload(Assessment.risks),
        )
        .filter(Assessment.public_id == public_id)
        .first()
    )
    if assessment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")
    return assessment


def create_assessment(db: Session) -> Assessment:
    assessment = Assessment(status=AssessmentStatus.DRAFT)
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment


def upsert_profile(
    db: Session,
    assessment: Assessment,
    organization_data: dict,
    ai_system_data: dict,
) -> Assessment:
    if assessment.organization is None:
        assessment.organization = Organization(assessment_id=assessment.id, **organization_data)
    else:
        for key, value in organization_data.items():
            setattr(assessment.organization, key, value)

    if assessment.ai_system is None:
        assessment.ai_system = AISystem(assessment_id=assessment.id, **ai_system_data)
    else:
        for key, value in ai_system_data.items():
            setattr(assessment.ai_system, key, value)

    if assessment.status == AssessmentStatus.DRAFT:
        assessment.status = AssessmentStatus.IN_PROGRESS

    db.commit()
    db.refresh(assessment)
    return assessment


def upsert_responses(
    db: Session,
    assessment: Assessment,
    responses_data: list[dict],
) -> Assessment:
    existing = {r.question_id: r for r in assessment.responses}
    for item in responses_data:
        question_id = item["question_id"]
        response_value = ResponseValue(item["response_value"])
        notes = item.get("notes")

        if question_id in existing:
            existing[question_id].response_value = response_value
            existing[question_id].notes = notes
        else:
            db.add(
                Response(
                    assessment_id=assessment.id,
                    question_id=question_id,
                    response_value=response_value,
                    notes=notes,
                )
            )

    if assessment.status == AssessmentStatus.DRAFT:
        assessment.status = AssessmentStatus.IN_PROGRESS

    db.commit()
    db.refresh(assessment)
    return assessment


def calculate_and_store_results(db: Session, assessment: Assessment) -> AssessmentResult:
    questions = db.query(Question).options(joinedload(Question.category)).order_by(Question.sort_order).all()
    categories = db.query(Category).all()
    category_names = {c.code: c.name for c in categories}
    response_map = {r.question_id: r for r in assessment.responses}

    unanswered = [q for q in questions if q.id not in response_map]
    if unanswered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Assessment incomplete: {len(unanswered)} questions unanswered",
        )

    question_inputs = [
        QuestionInput(
            question_id=q.id,
            question_code=q.code,
            question_text=q.text,
            category_code=q.category.code,
            response_value=response_map[q.id].response_value.value,
        )
        for q in questions
    ]

    profile = AISystemProfileInput()
    if assessment.ai_system:
        ai = assessment.ai_system
        profile = AISystemProfileInput(
            makes_decisions_about_people=ai.makes_decisions_about_people,
            recommends_decisions=ai.recommends_decisions,
            can_materially_affect_individual=ai.can_materially_affect_individual,
            affects_employment=ai.affects_employment,
            affects_education=ai.affects_education,
            affects_healthcare=ai.affects_healthcare,
            affects_financial_access=ai.affects_financial_access,
            affects_public_services=ai.affects_public_services,
            affects_housing=ai.affects_housing,
            affects_insurance=ai.affects_insurance,
            affects_legal_rights=ai.affects_legal_rights,
            processes_personal_info=ai.processes_personal_info,
            processes_sensitive_info=ai.processes_sensitive_info,
            processes_health_info=ai.processes_health_info,
        )

    result_data = score_assessment(question_inputs, category_names, profile)

    category_scores_json = json.dumps(
        [
            {
                "code": c.category_code,
                "name": c.category_name,
                "weight_percent": c.weight_percent,
                "score": c.category_score,
                "applicable_questions": c.applicable_questions,
            }
            for c in result_data.category_scores
        ]
    )
    trace_json = json.dumps(result_data.calculation_trace)

    if assessment.result:
        assessment.result.overall_score = result_data.overall_score
        assessment.result.readiness_level = result_data.readiness_level
        assessment.result.ai_system_risk = result_data.ai_system_risk
        assessment.result.governance_gap = result_data.governance_gap
        assessment.result.category_scores_json = category_scores_json
        assessment.result.calculation_trace_json = trace_json
        assessment.result.calculated_at = datetime.now(timezone.utc)
        result = assessment.result
    else:
        result = AssessmentResult(
            assessment_id=assessment.id,
            overall_score=result_data.overall_score,
            readiness_level=result_data.readiness_level,
            ai_system_risk=result_data.ai_system_risk,
            governance_gap=result_data.governance_gap,
            category_scores_json=category_scores_json,
            calculation_trace_json=trace_json,
            calculated_at=datetime.now(timezone.utc),
        )
        db.add(result)

    generate_and_store_recommendations(db, assessment, result_data.ai_system_risk)
    generate_and_store_risks(db, assessment)

    assessment.status = AssessmentStatus.COMPLETED
    assessment.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(result)
    return result
