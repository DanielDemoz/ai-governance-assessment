"""User-identified AI risks for the governance risk matrix."""

import enum

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class RiskClassification(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class RiskType(str, enum.Enum):
    PRIVACY_BREACH = "privacy_breach"
    ALGORITHMIC_BIAS = "algorithmic_bias"
    INCORRECT_DECISIONS = "incorrect_decisions"
    LACK_OF_TRANSPARENCY = "lack_of_transparency"
    AUTOMATION_BIAS = "automation_bias"
    SECURITY_ATTACK = "security_attack"
    DATA_LEAKAGE = "data_leakage"
    MODEL_FAILURE = "model_failure"
    VENDOR_DEPENDENCY = "vendor_dependency"
    LACK_OF_HUMAN_OVERSIGHT = "lack_of_human_oversight"
    OTHER = "other"


class Risk(Base, TimestampMixin):
    """
    A risk entry on the 5×5 governance risk matrix.
    Risk Score = Likelihood (1–5) × Impact (1–5)
    """

    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=False, index=True)
    risk_type: Mapped[RiskType] = mapped_column(Enum(RiskType, name="risk_type"), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    likelihood: Mapped[int] = mapped_column(Integer, nullable=False)  # 1–5
    impact: Mapped[int] = mapped_column(Integer, nullable=False)  # 1–5
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    classification: Mapped[RiskClassification] = mapped_column(
        Enum(RiskClassification, name="risk_classification"), nullable=False
    )

    assessment: Mapped["Assessment"] = relationship(back_populates="risks")
