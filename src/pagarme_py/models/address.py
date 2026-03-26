"""
Pydantic model for addresses in the PagarMe SDK.
"""

from pydantic import BaseModel, ConfigDict


class Address(BaseModel):
    """General address model used for customers and billing."""

    street: str
    number: str
    complement: str | None = None
    zip_code: str
    neighborhood: str
    city: str
    state: str
    country: str = "BR"

    model_config = ConfigDict(populate_by_name=True)
