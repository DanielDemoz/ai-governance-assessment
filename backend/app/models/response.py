"""Questionnaire response entity."""

import enum

from sqlalchemy import Enum, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class ResponseValue(int, enum.Enum):
    NOT_IMPLEMENTED = 0
    PLANNED = 1
    PARTIALLY_IMPLEMENTED = 2
    MOSTLY_IMPLEMENTED = 3
    FULLY_IMPLEMENTED = 4
    NOT_APPLICABLE = -1


class Response(Base, TimestampMixin):
    __tablename__ = "responses"
    __table_args__ = (UniqueConstraint("assessment_id", "question_id", name="uq_assessment_question"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False, index=True)
    response_value: Mapped[ResponseValue] = mapped_column(
        Enum(ResponseValue, name="response_value"), nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text)

    assessment: Mapped["Assessment"] = relationship(back_populates="responses")
    question: Mapped["Question"] = relationship(back_populates="responses")
