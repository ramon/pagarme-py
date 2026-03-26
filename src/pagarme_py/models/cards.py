"""
Pydantic models for card management in the PagarMe SDK.
"""


from pydantic import BaseModel, ConfigDict

from pagarme_py.models.address import Address


class CardCreateRequest(BaseModel):
    """Data for creating a card linked to a customer."""

    number: str
    holder_name: str
    exp_month: int
    exp_year: int
    cvv: str
    billing_address: Address | None = None
    brand: str | None = None


class CardUpdateRequest(BaseModel):
    """Data for updating a card."""

    exp_month: int | None = None
    exp_year: int | None = None
    billing_address: Address | None = None


class CardResponse(BaseModel):
    """Card response from the PagarMe API."""

    id: str
    last_four_digits: str
    brand: str
    holder_name: str
    exp_month: int
    exp_year: int
    status: str
    created_at: str
    updated_at: str
    billing_address: Address | None = None

    model_config = ConfigDict(from_attributes=True, extra="allow")
