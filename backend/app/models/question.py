"""Assessment questionnaire items."""

import enum

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Question(Base, TimestampMixin):
    """
    A single governance question within a category.
    Response scale: 0=Not implemented, 1=Planned, 2=Partial, 3=Mostly, 4=Fully, N/A excluded.
    """

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    governance_objective: Mapped[str | None] = mapped_column(Text)
    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel, name="risk_level"),
        default=RiskLevel.MEDIUM,
        nullable=False,
    )
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)
    recommendation_key: Mapped[str | None] = mapped_column(String(128))

    category: Mapped["Category"] = relationship(back_populates="questions")
    responses: Mapped[list["Response"]] = relationship(back_populates="question")
