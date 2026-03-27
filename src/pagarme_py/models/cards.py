"""
Pydantic models for card management in the PagarMe SDK.
"""


from typing import Any, Self

from pydantic import BaseModel, ConfigDict, model_validator

from pagarme_py.models.address import Address


class CardCreateRequest(BaseModel):
    """Data for creating a card linked to a customer."""

    number: str | None = None
    holder_name: str | None = None
    exp_month: int | None = None
    exp_year: int | None = None
    cvv: str | None = None
    billing_address: Address | None = None
    brand: str | None = None
    token: str | None = None
    metadata: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_card_data(self) -> Self:
        """Ensures either token or raw card data is provided."""
        if self.token:
            return self

        required_fields = ["number", "holder_name", "exp_month", "exp_year", "cvv"]
        missing = [f for f in required_fields if getattr(self, f) is None]

        if missing:
            msg = (
                "Missing required card data when token is not provided: "
                f"{', '.join(missing)}"
            )
            raise ValueError(msg)
        return self


class CardUpdateRequest(BaseModel):
    """Data for updating a card."""

    exp_month: int | None = None
    exp_year: int | None = None
    billing_address: Address | None = None
    metadata: dict[str, Any] | None = None


class CardResponse(BaseModel):
    """Card response from the PagarMe API."""

    id: str
    first_six_digits: str | None = None
    last_four_digits: str | None = None
    brand: str
    holder_name: str | None = None
    exp_month: int
    exp_year: int
    status: str
    type: str | None = None
    label: str | None = None
    created_at: str
    updated_at: str
    billing_address: Address | None = None
    metadata: dict[str, Any] | None = None

    model_config = ConfigDict(from_attributes=True, extra="allow")
