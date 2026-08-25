"""Governance risk matrix calculations."""

from app.models.risk import RiskClassification


def calculate_risk_score(likelihood: int, impact: int) -> int:
    if not (1 <= likelihood <= 5 and 1 <= impact <= 5):
        raise ValueError("Likelihood and impact must be between 1 and 5")
    return likelihood * impact


def classify_risk_score(score: int) -> RiskClassification:
    if score <= 4:
        return RiskClassification.LOW
    if score <= 9:
        return RiskClassification.MODERATE
    if score <= 16:
        return RiskClassification.HIGH
    return RiskClassification.CRITICAL


def matrix_cell_level(likelihood: int, impact: int) -> RiskClassification:
    return classify_risk_score(calculate_risk_score(likelihood, impact))
