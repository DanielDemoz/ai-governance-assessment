"""Organization and AI system profile entities."""

import enum
from datetime import date

from sqlalchemy import Boolean, Date, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class OrganizationType(str, enum.Enum):
    SMB = "smb"
    EDUCATION = "education"
    NONPROFIT = "nonprofit"
    GOVERNMENT = "government"
    CONSULTING = "consulting"
    OTHER = "other"


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    organization_type: Mapped[OrganizationType] = mapped_column(
        Enum(OrganizationType, name="organization_type"),
        nullable=False,
    )
    industry: Mapped[str | None] = mapped_column(String(255))
    country: Mapped[str | None] = mapped_column(String(128))
    assessment_owner: Mapped[str | None] = mapped_column(String(255))
    assessment_date: Mapped[date | None] = mapped_column(Date)

    assessment: Mapped["Assessment"] = relationship(back_populates="organization")


class AITechnologyType(str, enum.Enum):
    MACHINE_LEARNING = "machine_learning"
    DEEP_LEARNING = "deep_learning"
    NLP = "nlp"
    COMPUTER_VISION = "computer_vision"
    RULE_BASED = "rule_based"
    GENERATIVE_AI = "generative_ai"
    HYBRID = "hybrid"
    OTHER = "other"


class VendorType(str, enum.Enum):
    IN_HOUSE = "in_house"
    VENDOR = "vendor"
    BOTH = "both"


class DevelopmentStatus(str, enum.Enum):
    CONCEPT = "concept"
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
    RETIRED = "retired"


class DeploymentStatus(str, enum.Enum):
    NOT_DEPLOYED = "not_deployed"
    PILOT = "pilot"
    LIMITED = "limited"
    FULL = "full"


class AISystem(Base, TimestampMixin):
    __tablename__ = "ai_systems"

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    primary_purpose: Mapped[str | None] = mapped_column(Text)
    technology_type: Mapped[AITechnologyType | None] = mapped_column(
        Enum(AITechnologyType, name="ai_technology_type")
    )
    vendor_type: Mapped[VendorType | None] = mapped_column(Enum(VendorType, name="vendor_type"))
    development_status: Mapped[DevelopmentStatus | None] = mapped_column(
        Enum(DevelopmentStatus, name="development_status")
    )
    deployment_status: Mapped[DeploymentStatus | None] = mapped_column(
        Enum(DeploymentStatus, name="deployment_status")
    )

    # Data processing flags
    processes_personal_info: Mapped[bool] = mapped_column(Boolean, default=False)
    processes_sensitive_info: Mapped[bool] = mapped_column(Boolean, default=False)
    processes_public_data: Mapped[bool] = mapped_column(Boolean, default=False)
    processes_employee_data: Mapped[bool] = mapped_column(Boolean, default=False)
    processes_customer_data: Mapped[bool] = mapped_column(Boolean, default=False)
    processes_student_data: Mapped[bool] = mapped_column(Boolean, default=False)
    processes_health_info: Mapped[bool] = mapped_column(Boolean, default=False)
    processes_financial_info: Mapped[bool] = mapped_column(Boolean, default=False)

    # Impact flags (used for AI system risk profile)
    makes_decisions_about_people: Mapped[bool] = mapped_column(Boolean, default=False)
    recommends_decisions: Mapped[bool] = mapped_column(Boolean, default=False)
    can_materially_affect_individual: Mapped[bool] = mapped_column(Boolean, default=False)
    affects_employment: Mapped[bool] = mapped_column(Boolean, default=False)
    affects_education: Mapped[bool] = mapped_column(Boolean, default=False)
    affects_healthcare: Mapped[bool] = mapped_column(Boolean, default=False)
    affects_financial_access: Mapped[bool] = mapped_column(Boolean, default=False)
    affects_public_services: Mapped[bool] = mapped_column(Boolean, default=False)
    affects_housing: Mapped[bool] = mapped_column(Boolean, default=False)
    affects_insurance: Mapped[bool] = mapped_column(Boolean, default=False)
    affects_legal_rights: Mapped[bool] = mapped_column(Boolean, default=False)

    assessment: Mapped["Assessment"] = relationship(back_populates="ai_system")
