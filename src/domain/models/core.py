import uuid
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


def generate_uuid() -> str:
    return str(uuid.uuid4())


class CustomerType(StrEnum):
    INDIVIDUAL = "individual"
    TEAM = "team"
    GROUP = "group"
    FUNCTION = "function"
    EXTERNAL = "external"


class ServiceVersion(StrEnum):
    CURRENT = "current"
    ONE_MONTH = "1-month"
    THREE_MONTH = "3-month"


class Talent(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    role: str
    team: str
    hris_reference: str | None = None


class Customer(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    type: CustomerType
    name: str


class Service(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    name: str
    description: str
    importance: int = Field(ge=1, le=10, description="1-10 importance rating")
    quality: int = Field(ge=1, le=10, description="1-10 quality rating")
    svm: float = Field(default=0.0, description="Service Value Metric")


class ServiceAllocation(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    person_id: str
    service_id: str
    customer_id: str
    fte_percentage: float = Field(gt=0, le=100)
    version: ServiceVersion


class TalentServicePortfolio(BaseModel):
    """
    A collection of all service allocations for a single Talent profile.
    Enforces the critical business rule that %FTE must equal exactly 100%
    per version (Current, 1-Month, 3-Month).
    """

    talent_id: str
    allocations: list[ServiceAllocation]

    @model_validator(mode="after")
    def validate_100_percent_fte(self) -> "TalentServicePortfolio":
        # Group allocations by version
        versions_map: dict[ServiceVersion, float] = {}

        for alloc in self.allocations:
            # We must only validate allocations belonging to this specific talent
            if alloc.person_id != self.talent_id:
                raise ValueError(
                    f"Allocation {alloc.id} does not belong to Talent {self.talent_id}"
                )

            versions_map[alloc.version] = (
                versions_map.get(alloc.version, 0.0) + alloc.fte_percentage
            )

        # Check each populated version sums to 100.0 (with float tolerance)
        for version, total_fte in versions_map.items():
            if not (99.9 <= total_fte <= 100.1):
                raise ValueError(
                    f"Total %FTE for {version.value} profile must equal exactly 100%. "
                    f"Current sum: {total_fte}%"
                )

        return self
