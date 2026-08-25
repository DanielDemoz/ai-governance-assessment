"""Governance assessment category (dimension)."""

from decimal import Decimal

from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Category(Base, TimestampMixin):
    """
    One of nine governance dimensions (e.g. Accountability & Governance).
    Weights are stored as percentages (15.0 = 15%).
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    weight: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)

    questions: Mapped[list["Question"]] = relationship(back_populates="category")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="category")
