"""Rule-based governance recommendations."""

import enum

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class RecommendationPriority(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Recommendation(Base, TimestampMixin):
    """Generated from deterministic rules — not LLM output."""

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=False, index=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), index=True)
    question_id: Mapped[int | None] = mapped_column(ForeignKey("questions.id"), index=True)
    priority: Mapped[RecommendationPriority] = mapped_column(
        Enum(RecommendationPriority, name="recommendation_priority"), nullable=False
    )
    identified_gap: Mapped[str] = mapped_column(Text, nullable=False)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    why_it_matters: Mapped[str] = mapped_column(Text, nullable=False)
    suggested_action: Mapped[str] = mapped_column(Text, nullable=False)
    responsible_role: Mapped[str] = mapped_column(String(255), nullable=False)
    suggested_timeframe: Mapped[str] = mapped_column(String(128), nullable=False)
    source_rule_key: Mapped[str | None] = mapped_column(String(128))

    assessment: Mapped["Assessment"] = relationship(back_populates="recommendations")
    category: Mapped["Category | None"] = relationship(back_populates="recommendations")
