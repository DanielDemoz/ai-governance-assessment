"""Generate and persist assessment recommendations."""

from sqlalchemy.orm import Session, joinedload

from app.models.assessment import AISystemRiskLevel, Assessment
from app.models.question import Question
from app.models.recommendation import Recommendation
from app.models.response import ResponseValue
from app.services.recommendations.engine import GeneratedRecommendation, QuestionContext, generate_recommendations


def _build_question_contexts(assessment: Assessment, questions: list[Question]) -> list[QuestionContext]:
    response_map = {r.question_id: r for r in assessment.responses}
    contexts: list[QuestionContext] = []

    for question in questions:
        response = response_map.get(question.id)
        if response is None:
            continue
        contexts.append(
            QuestionContext(
                question_id=question.id,
                question_code=question.code,
                question_text=question.text,
                category_id=question.category_id,
                category_code=question.category.code,
                category_name=question.category.name,
                recommendation_key=question.recommendation_key or question.code,
                governance_objective=question.governance_objective,
                risk_level=question.risk_level,
                response_value=response.response_value.value,
            )
        )
    return contexts


def generate_and_store_recommendations(
    db: Session,
    assessment: Assessment,
    ai_system_risk: AISystemRiskLevel,
) -> list[Recommendation]:
    questions = (
        db.query(Question)
        .options(joinedload(Question.category))
        .order_by(Question.sort_order)
        .all()
    )
    contexts = _build_question_contexts(assessment, questions)
    generated = generate_recommendations(contexts, ai_system_risk)

    db.query(Recommendation).filter(Recommendation.assessment_id == assessment.id).delete()

    stored: list[Recommendation] = []
    for item in generated:
        rec = Recommendation(
            assessment_id=assessment.id,
            category_id=item.category_id,
            question_id=item.question_id,
            priority=item.priority,
            identified_gap=item.identified_gap,
            recommendation=item.recommendation,
            why_it_matters=item.why_it_matters,
            suggested_action=item.suggested_action,
            responsible_role=item.responsible_role,
            suggested_timeframe=item.suggested_timeframe,
            source_rule_key=item.source_rule_key,
        )
        db.add(rec)
        stored.append(rec)

    db.flush()
    return stored


def recommendation_to_generated(rec: Recommendation) -> GeneratedRecommendation:
    category = rec.category
    return GeneratedRecommendation(
        question_id=rec.question_id or 0,
        category_id=rec.category_id or 0,
        category_code=category.code if category else "",
        category_name=category.name if category else "",
        priority=rec.priority,
        identified_gap=rec.identified_gap,
        recommendation=rec.recommendation,
        why_it_matters=rec.why_it_matters,
        suggested_action=rec.suggested_action,
        responsible_role=rec.responsible_role,
        suggested_timeframe=rec.suggested_timeframe,
        source_rule_key=rec.source_rule_key or "",
    )


def get_stored_recommendations(db: Session, assessment_id: int) -> list[Recommendation]:
    return (
        db.query(Recommendation)
        .options(joinedload(Recommendation.category))
        .filter(Recommendation.assessment_id == assessment_id)
        .order_by(Recommendation.priority, Recommendation.id)
        .all()
    )
