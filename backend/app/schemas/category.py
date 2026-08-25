"""Category and question API schemas."""

from pydantic import BaseModel, Field


class QuestionOut(BaseModel):
    id: int
    code: str
    text: str
    governance_objective: str | None
    risk_level: str
    sort_order: int

    model_config = {"from_attributes": True}


class CategoryOut(BaseModel):
    id: int
    code: str
    name: str
    description: str | None
    weight: float
    sort_order: int
    questions: list[QuestionOut] = Field(default_factory=list)

    model_config = {"from_attributes": True}
