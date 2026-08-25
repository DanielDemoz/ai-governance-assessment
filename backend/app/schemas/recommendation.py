"""Recommendation API schemas."""

from pydantic import BaseModel


class RecommendationOut(BaseModel):
    id: int | None = None
    category_code: str
    category_name: str
    question_id: int | None
    priority: str
    identified_gap: str
    recommendation: str
    why_it_matters: str
    suggested_action: str
    responsible_role: str
    suggested_timeframe: str
    source_rule_key: str | None

    model_config = {"from_attributes": True}


class RoadmapPhaseOut(BaseModel):
    key: str
    label: str
    description: str
    recommendations: list[RecommendationOut]


class RecommendationsOut(BaseModel):
    total: int
    recommendations: list[RecommendationOut]


class RoadmapOut(BaseModel):
    phases: list[RoadmapPhaseOut]
