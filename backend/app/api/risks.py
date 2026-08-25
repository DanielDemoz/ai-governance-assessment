"""Risk matrix API routes."""

from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.risk import Risk, RiskType
from app.schemas.risk import (
    AISystemRiskProfileOut,
    MatrixCellOut,
    RiskFactorOut,
    RiskIn,
    RiskMatrixOut,
    RiskOut,
    RisksOut,
)
from app.services.assessment_service import get_assessment_by_public_id
from app.services.risk.matrix import calculate_risk_score, classify_risk_score, matrix_cell_level
from app.services.risk.profile import build_ai_system_risk_profile
from app.services.risk_service import get_assessment_risks, profile_from_ai_system

router = APIRouter(prefix="/assessments", tags=["risks"])


def _risk_out(risk: Risk) -> RiskOut:
    return RiskOut(
        id=risk.id,
        risk_type=risk.risk_type.value,
        description=risk.description,
        likelihood=risk.likelihood,
        impact=risk.impact,
        risk_score=risk.risk_score,
        classification=risk.classification.value,
    )


def _build_matrix(risks: list[Risk]) -> list[MatrixCellOut]:
    counts: dict[tuple[int, int], int] = defaultdict(int)
    for risk in risks:
        counts[(risk.likelihood, risk.impact)] += 1

    cells: list[MatrixCellOut] = []
    for likelihood in range(1, 6):
        for impact in range(1, 6):
            cells.append(
                MatrixCellOut(
                    likelihood=likelihood,
                    impact=impact,
                    classification=matrix_cell_level(likelihood, impact).value,
                    count=counts.get((likelihood, impact), 0),
                )
            )
    return cells


@router.get("/{public_id}/risks", response_model=RisksOut)
def list_risks(public_id: str, db: Session = Depends(get_db)) -> RisksOut:
    assessment = get_assessment_by_public_id(db, public_id)
    if assessment.result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment results not available")
    risks = get_assessment_risks(db, assessment.id)
    return RisksOut(total=len(risks), risks=[_risk_out(r) for r in risks])


@router.get("/{public_id}/risk-matrix", response_model=RiskMatrixOut)
def get_risk_matrix(public_id: str, db: Session = Depends(get_db)) -> RiskMatrixOut:
    assessment = get_assessment_by_public_id(db, public_id)
    if assessment.result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment results not available")
    if assessment.ai_system is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="AI system profile required")

    risks = get_assessment_risks(db, assessment.id)
    profile = build_ai_system_risk_profile(profile_from_ai_system(assessment.ai_system))

    return RiskMatrixOut(
        cells=_build_matrix(risks),
        risks=[_risk_out(r) for r in risks],
        ai_system_risk_profile=AISystemRiskProfileOut(
            level=profile.level.value,
            score=profile.score,
            summary=profile.summary,
            factors=[RiskFactorOut(code=f.code, label=f.label, present=f.present, weight=f.weight) for f in profile.factors],
        ),
    )


@router.post("/{public_id}/risks", response_model=RiskOut, status_code=201)
def add_risk(public_id: str, payload: RiskIn, db: Session = Depends(get_db)) -> RiskOut:
    assessment = get_assessment_by_public_id(db, public_id)
    if assessment.result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment results not available")

    try:
        risk_type = RiskType(payload.risk_type)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid risk type") from exc

    score = calculate_risk_score(payload.likelihood, payload.impact)
    risk = Risk(
        assessment_id=assessment.id,
        risk_type=risk_type,
        description=payload.description,
        likelihood=payload.likelihood,
        impact=payload.impact,
        risk_score=score,
        classification=classify_risk_score(score),
    )
    db.add(risk)
    db.commit()
    db.refresh(risk)
    return _risk_out(risk)


@router.delete("/{public_id}/risks/{risk_id}", status_code=204)
def delete_risk(public_id: str, risk_id: int, db: Session = Depends(get_db)) -> None:
    assessment = get_assessment_by_public_id(db, public_id)
    risk = db.query(Risk).filter(Risk.id == risk_id, Risk.assessment_id == assessment.id).first()
    if risk is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk not found")
    db.delete(risk)
    db.commit()
