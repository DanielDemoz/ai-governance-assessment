"""Risk API schemas."""

from pydantic import BaseModel, Field, field_validator


class RiskIn(BaseModel):
    risk_type: str
    description: str | None = None
    likelihood: int = Field(ge=1, le=5)
    impact: int = Field(ge=1, le=5)


class RiskOut(BaseModel):
    id: int
    risk_type: str
    description: str | None
    likelihood: int
    impact: int
    risk_score: int
    classification: str

    model_config = {"from_attributes": True}


class RisksOut(BaseModel):
    total: int
    risks: list[RiskOut]


class RiskFactorOut(BaseModel):
    code: str
    label: str
    present: bool
    weight: int


class AISystemRiskProfileOut(BaseModel):
    level: str
    score: int
    summary: str
    factors: list[RiskFactorOut]


class MatrixCellOut(BaseModel):
    likelihood: int
    impact: int
    classification: str
    count: int


class RiskMatrixOut(BaseModel):
    cells: list[MatrixCellOut]
    risks: list[RiskOut]
    ai_system_risk_profile: AISystemRiskProfileOut
