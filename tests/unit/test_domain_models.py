import pytest
from pydantic import ValidationError

from src.domain.models.core import (
    Customer,
    CustomerType,
    Service,
    ServiceAllocation,
    ServiceVersion,
    Talent,
    TalentServicePortfolio,
)


def test_valid_talent_portfolio():
    talent = Talent(role="Engineer", team="Backend")
    service1 = Service(
        name="API Dev", description="Building APIs", importance=8, quality=7
    )
    service2 = Service(name="Ops", description="Deployment", importance=9, quality=8)
    customer = Customer(name="Frontend Team", type=CustomerType.TEAM)

    alloc1 = ServiceAllocation(
        person_id=talent.id,
        service_id=service1.id,
        customer_id=customer.id,
        fte_percentage=60.0,
        version=ServiceVersion.CURRENT,
    )
    alloc2 = ServiceAllocation(
        person_id=talent.id,
        service_id=service2.id,
        customer_id=customer.id,
        fte_percentage=40.0,
        version=ServiceVersion.CURRENT,
    )

    portfolio = TalentServicePortfolio(
        talent_id=talent.id, allocations=[alloc1, alloc2]
    )
    assert len(portfolio.allocations) == 2
    assert portfolio.allocations[0].fte_percentage == 60.0


def test_invalid_fte_portfolio_raises_error():
    talent = Talent(role="Engineer", team="Backend")
    customer = Customer(name="Frontend Team", type=CustomerType.TEAM)
    service = Service(
        name="API Dev", description="Building APIs", importance=8, quality=7
    )

    alloc1 = ServiceAllocation(
        person_id=talent.id,
        service_id=service.id,
        customer_id=customer.id,
        fte_percentage=90.0,  # Not 100%
        version=ServiceVersion.CURRENT,
    )

    with pytest.raises(ValidationError) as exc:
        TalentServicePortfolio(talent_id=talent.id, allocations=[alloc1])
    assert "Total %FTE for current profile must equal exactly 100%" in str(exc.value)


def test_allocation_wrong_talent_id_raises_error():
    talent = Talent(role="Engineer", team="Backend")
    customer = Customer(name="Frontend Team", type=CustomerType.TEAM)
    service = Service(
        name="API Dev", description="Building APIs", importance=8, quality=7
    )

    alloc1 = ServiceAllocation(
        person_id="wrong_id",  # Belongs to someone else
        service_id=service.id,
        customer_id=customer.id,
        fte_percentage=100.0,
        version=ServiceVersion.CURRENT,
    )

    with pytest.raises(ValidationError) as exc:
        TalentServicePortfolio(talent_id=talent.id, allocations=[alloc1])
    assert "does not belong to Talent" in str(exc.value)
