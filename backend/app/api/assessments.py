"""Assessment API routes."""

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.assessment import (
    AssessmentCreateOut,
    AssessmentOut,
    AssessmentResultOut,
    CategoryScoreOut,
    ProfileIn,
    ResponseOut,
    ResponsesIn,
)
from app.schemas.recommendation import RecommendationOut, RecommendationsOut, RoadmapOut, RoadmapPhaseOut
from app.services.assessment_service import (
    calculate_and_store_results,
    create_assessment,
    get_assessment_by_public_id,
    upsert_profile,
    upsert_responses,
)
from app.services.recommendation_service import get_stored_recommendations, recommendation_to_generated
from app.services.recommendations.roadmap import build_roadmap

router = APIRouter(prefix="/assessments", tags=["assessments"])


def _recommendation_out(rec) -> RecommendationOut:
    category = rec.category
    return RecommendationOut(
        id=rec.id,
        category_code=category.code if category else "",
        category_name=category.name if category else "",
        question_id=rec.question_id,
        priority=rec.priority.value,
        identified_gap=rec.identified_gap,
        recommendation=rec.recommendation,
        why_it_matters=rec.why_it_matters,
        suggested_action=rec.suggested_action,
        responsible_role=rec.responsible_role,
        suggested_timeframe=rec.suggested_timeframe,
        source_rule_key=rec.source_rule_key,
    )


def _build_assessment_out(assessment) -> AssessmentOut:
    result_out = None
    if assessment.result:
        category_scores = json.loads(assessment.result.category_scores_json)
        trace = (
            json.loads(assessment.result.calculation_trace_json)
            if assessment.result.calculation_trace_json
            else None
        )
        result_out = AssessmentResultOut(
            overall_score=assessment.result.overall_score,
            readiness_level=assessment.result.readiness_level.value,
            ai_system_risk=assessment.result.ai_system_risk.value,
            governance_gap=assessment.result.governance_gap.value,
            category_scores=[CategoryScoreOut(**item) for item in category_scores],
            calculation_trace=trace,
            calculated_at=assessment.result.calculated_at,
        )

    return AssessmentOut(
        public_id=assessment.public_id,
        status=assessment.status.value,
        is_demo=assessment.is_demo,
        organization=assessment.organization,
        ai_system=assessment.ai_system,
        responses=[
            ResponseOut(
                question_id=r.question_id,
                response_value=r.response_value.value,
                notes=r.notes,
            )
            for r in assessment.responses
        ],
        result=result_out,
        created_at=assessment.created_at,
        completed_at=assessment.completed_at,
    )


@router.post("", response_model=AssessmentCreateOut, status_code=201)
def create_new_assessment(db: Session = Depends(get_db)) -> AssessmentCreateOut:
    assessment = create_assessment(db)
    return AssessmentCreateOut(public_id=assessment.public_id, status=assessment.status.value)


@router.get("/{public_id}", response_model=AssessmentOut)
def get_assessment(public_id: str, db: Session = Depends(get_db)) -> AssessmentOut:
    assessment = get_assessment_by_public_id(db, public_id)
    return _build_assessment_out(assessment)


@router.put("/{public_id}/profile", response_model=AssessmentOut)
def update_profile(
    public_id: str,
    payload: ProfileIn,
    db: Session = Depends(get_db),
) -> AssessmentOut:
    assessment = get_assessment_by_public_id(db, public_id)
    assessment = upsert_profile(
        db,
        assessment,
        payload.organization.model_dump(),
        payload.ai_system.model_dump(),
    )
    return _build_assessment_out(assessment)


@router.put("/{public_id}/responses", response_model=AssessmentOut)
def update_responses(
    public_id: str,
    payload: ResponsesIn,
    db: Session = Depends(get_db),
) -> AssessmentOut:
    assessment = get_assessment_by_public_id(db, public_id)
    assessment = upsert_responses(
        db,
        assessment,
        [item.model_dump() for item in payload.responses],
    )
    return _build_assessment_out(assessment)


@router.post("/{public_id}/calculate", response_model=AssessmentResultOut)
def calculate_assessment(public_id: str, db: Session = Depends(get_db)) -> AssessmentResultOut:
    assessment = get_assessment_by_public_id(db, public_id)
    if assessment.organization is None or assessment.ai_system is None:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization and AI system profile required before scoring",
        )
    result = calculate_and_store_results(db, assessment)
    category_scores = json.loads(result.category_scores_json)
    trace = json.loads(result.calculation_trace_json) if result.calculation_trace_json else None
    return AssessmentResultOut(
        overall_score=result.overall_score,
        readiness_level=result.readiness_level.value,
        ai_system_risk=result.ai_system_risk.value,
        governance_gap=result.governance_gap.value,
        category_scores=[CategoryScoreOut(**item) for item in category_scores],
        calculation_trace=trace,
        calculated_at=result.calculated_at,
    )


@router.get("/{public_id}/results", response_model=AssessmentResultOut)
def get_results(public_id: str, db: Session = Depends(get_db)) -> AssessmentResultOut:
    assessment = get_assessment_by_public_id(db, public_id)
    if assessment.result is None:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Results not yet calculated for this assessment",
        )
    result = assessment.result
    category_scores = json.loads(result.category_scores_json)
    trace = json.loads(result.calculation_trace_json) if result.calculation_trace_json else None
    return AssessmentResultOut(
        overall_score=result.overall_score,
        readiness_level=result.readiness_level.value,
        ai_system_risk=result.ai_system_risk.value,
        governance_gap=result.governance_gap.value,
        category_scores=[CategoryScoreOut(**item) for item in category_scores],
        calculation_trace=trace,
        calculated_at=result.calculated_at,
    )


@router.get("/{public_id}/recommendations", response_model=RecommendationsOut)
def get_recommendations(public_id: str, db: Session = Depends(get_db)) -> RecommendationsOut:
    assessment = get_assessment_by_public_id(db, public_id)
    if assessment.result is None:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Results not yet calculated for this assessment",
        )
    recs = get_stored_recommendations(db, assessment.id)
    items = [_recommendation_out(r) for r in recs]
    return RecommendationsOut(total=len(items), recommendations=items)


@router.get("/{public_id}/roadmap", response_model=RoadmapOut)
def get_roadmap(public_id: str, db: Session = Depends(get_db)) -> RoadmapOut:
    assessment = get_assessment_by_public_id(db, public_id)
    if assessment.result is None:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Results not yet calculated for this assessment",
        )
    recs = get_stored_recommendations(db, assessment.id)
    generated = [recommendation_to_generated(r) for r in recs]
    phases = build_roadmap(generated)
    return RoadmapOut(
        phases=[
            RoadmapPhaseOut(
                key=phase.key,
                label=phase.label,
                description=phase.description,
                recommendations=[
                    RecommendationOut(
                        category_code=item.category_code,
                        category_name=item.category_name,
                        question_id=item.question_id,
                        priority=item.priority.value,
                        identified_gap=item.identified_gap,
                        recommendation=item.recommendation,
                        why_it_matters=item.why_it_matters,
                        suggested_action=item.suggested_action,
                        responsible_role=item.responsible_role,
                        suggested_timeframe=item.suggested_timeframe,
                        source_rule_key=item.source_rule_key,
                    )
                    for item in phase.items
                ],
            )
            for phase in phases
        ]
    )
