"""Assessment API schemas."""

from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

from app.models.organization import (
    AITechnologyType,
    DeploymentStatus,
    DevelopmentStatus,
    OrganizationType,
    VendorType,
)
from app.models.response import ResponseValue


class OrganizationIn(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    organization_type: OrganizationType
    industry: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, max_length=128)
    assessment_owner: str | None = Field(default=None, max_length=255)
    assessment_date: date | None = None


class AISystemIn(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    primary_purpose: str | None = None
    technology_type: AITechnologyType | None = None
    vendor_type: VendorType | None = None
    development_status: DevelopmentStatus | None = None
    deployment_status: DeploymentStatus | None = None
    processes_personal_info: bool = False
    processes_sensitive_info: bool = False
    processes_public_data: bool = False
    processes_employee_data: bool = False
    processes_customer_data: bool = False
    processes_student_data: bool = False
    processes_health_info: bool = False
    processes_financial_info: bool = False
    makes_decisions_about_people: bool = False
    recommends_decisions: bool = False
    can_materially_affect_individual: bool = False
    affects_employment: bool = False
    affects_education: bool = False
    affects_healthcare: bool = False
    affects_financial_access: bool = False
    affects_public_services: bool = False
    affects_housing: bool = False
    affects_insurance: bool = False
    affects_legal_rights: bool = False


class ProfileIn(BaseModel):
    organization: OrganizationIn
    ai_system: AISystemIn


class ResponseIn(BaseModel):
    question_id: int
    response_value: int
    notes: str | None = None

    @field_validator("response_value")
    @classmethod
    def validate_response_value(cls, value: int) -> int:
        allowed = {item.value for item in ResponseValue}
        if value not in allowed:
            raise ValueError(f"response_value must be one of {sorted(allowed)}")
        return value


class ResponsesIn(BaseModel):
    responses: list[ResponseIn]


class OrganizationOut(OrganizationIn):
    id: int

    model_config = {"from_attributes": True}


class AISystemOut(AISystemIn):
    id: int

    model_config = {"from_attributes": True}


class ResponseOut(BaseModel):
    question_id: int
    response_value: int
    notes: str | None

    model_config = {"from_attributes": True}


class CategoryScoreOut(BaseModel):
    code: str
    name: str
    weight_percent: float
    score: float
    applicable_questions: int


class AssessmentResultOut(BaseModel):
    overall_score: float
    readiness_level: str
    ai_system_risk: str
    governance_gap: str
    category_scores: list[CategoryScoreOut]
    calculation_trace: dict | None
    calculated_at: datetime

    model_config = {"from_attributes": True}


class AssessmentOut(BaseModel):
    public_id: str
    status: str
    is_demo: bool
    organization: OrganizationOut | None = None
    ai_system: AISystemOut | None = None
    responses: list[ResponseOut] = Field(default_factory=list)
    result: AssessmentResultOut | None = None
    created_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


class AssessmentCreateOut(BaseModel):
    public_id: str
    status: str

    model_config = {"from_attributes": True}
