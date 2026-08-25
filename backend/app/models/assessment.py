"""Core assessment session entity."""

import enum
import uuid

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class AssessmentStatus(str, enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Assessment(Base, TimestampMixin):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    status: Mapped[AssessmentStatus] = mapped_column(
        Enum(AssessmentStatus, name="assessment_status"),
        default=AssessmentStatus.DRAFT,
        nullable=False,
    )
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    organization: Mapped["Organization | None"] = relationship(
        back_populates="assessment", uselist=False, cascade="all, delete-orphan"
    )
    ai_system: Mapped["AISystem | None"] = relationship(
        back_populates="assessment", uselist=False, cascade="all, delete-orphan"
    )
    responses: Mapped[list["Response"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )
    risks: Mapped[list["Risk"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )
    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )
    result: Mapped["AssessmentResult | None"] = relationship(
        back_populates="assessment", uselist=False, cascade="all, delete-orphan"
    )
    reports: Mapped[list["Report"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )


class ReadinessLevel(str, enum.Enum):
    INITIAL = "initial"
    DEVELOPING = "developing"
    ESTABLISHED = "established"
    ADVANCED = "advanced"
    LEADING = "leading"


class AISystemRiskLevel(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class GovernanceGapLevel(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class AssessmentResult(Base, TimestampMixin):
    """Computed deterministic assessment outcomes. Never LLM-generated."""

    __tablename__ = "assessment_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessments.id"), unique=True, nullable=False
    )
    overall_score: Mapped[float] = mapped_column(nullable=False)
    readiness_level: Mapped[ReadinessLevel] = mapped_column(
        Enum(ReadinessLevel, name="readiness_level"), nullable=False
    )
    ai_system_risk: Mapped[AISystemRiskLevel] = mapped_column(
        Enum(AISystemRiskLevel, name="ai_system_risk_level"), nullable=False
    )
    governance_gap: Mapped[GovernanceGapLevel] = mapped_column(
        Enum(GovernanceGapLevel, name="governance_gap_level"), nullable=False
    )
    category_scores_json: Mapped[str] = mapped_column(String, nullable=False)
    calculation_trace_json: Mapped[str | None] = mapped_column(String)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    assessment: Mapped["Assessment"] = relationship(back_populates="result")


class ReportFormat(str, enum.Enum):
    PDF = "pdf"


class Report(Base, TimestampMixin):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=False, index=True)
    format: Mapped[ReportFormat] = mapped_column(Enum(ReportFormat, name="report_format"), nullable=False)
    file_path: Mapped[str | None] = mapped_column(String(512))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    assessment: Mapped["Assessment"] = relationship(back_populates="reports")
