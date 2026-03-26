"""
Pydantic models for customers in the PagarMe SDK.
"""

import re
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from pagarme_py.models.address import Address


class CustomerPhone(BaseModel):
    """Customer phone."""

    country_code: str | None = None
    area_code: str | None = None
    number: str | None = None
    full_phone: str | None = Field(None, exclude=True)

    @model_validator(mode="after")
    def parse_full_phone(self) -> Self:
        """Parses a full phone string into country_code, area_code and number."""
        if self.full_phone:
            # Remove all non-numeric characters except +
            clean_phone = re.sub(r"[^\d+]", "", self.full_phone)
            if clean_phone.startswith("+"):
                # Format: +5511999999999
                # We assume country code is 2 digits for now as per
                # Pagar.me context (usually BR +55)
                # But a more robust approach would be needed for general cases.
                # Pagar.me docs usually show country_code as 2 digits.
                match = re.match(r"\+(\d{2})(\d{2})(\d+)", clean_phone)
                if match:
                    self.country_code = match.group(1)
                    self.area_code = match.group(2)
                    self.number = match.group(3)
            elif len(clean_phone) >= 10:
                # Format: 5511999999999 or 11999999999
                if len(clean_phone) == 11 or len(clean_phone) == 10:
                    # Assume BR without country code (add 55)
                    self.country_code = "55"
                    self.area_code = clean_phone[:2]
                    self.number = clean_phone[2:]
                else:
                    # Assume starts with country code
                    self.country_code = clean_phone[:2]
                    self.area_code = clean_phone[2:4]
                    self.number = clean_phone[4:]

        if not all([self.country_code, self.area_code, self.number]):
            raise ValueError(
                "Phone must have country_code, area_code and number, "
                "or a valid full_phone."
            )
        return self


class CustomerPhones(BaseModel):
    """Customer phones."""

    home_phone: CustomerPhone | str | None = None
    mobile_phone: CustomerPhone | str | None = None
    work_phone: CustomerPhone | str | None = None

    @model_validator(mode="before")
    @classmethod
    def convert_strings_to_dict(cls, data: Any) -> Any:
        """Converts raw phone strings to CustomerPhone dict format."""
        if isinstance(data, dict):
            for field in ["home_phone", "mobile_phone", "work_phone"]:
                value = data.get(field)
                if isinstance(value, str):
                    data[field] = {"full_phone": value}
        return data


class CustomerCreateRequest(BaseModel):
    """Data for creating a customer."""

    name: str
    email: EmailStr
    document: str
    type: str = Field(..., pattern="^(individual|company)$")
    address: Address | None = None
    phones: CustomerPhones | None = None
    metadata: dict[str, Any] | None = None
    code: str | None = None


class CustomerUpdateRequest(BaseModel):
    """Data for updating a customer."""

    name: str | None = None
    email: EmailStr | None = None
    document: str | None = None
    type: str | None = Field(None, pattern="^(individual|company)$")
    address: Address | None = None
    phones: CustomerPhones | None = None
    metadata: dict[str, Any] | None = None


class CustomerResponse(BaseModel):
    """Customer response from the PagarMe API."""

    id: str
    name: str
    email: str
    document: str
    type: str
    delinquent: bool
    created_at: str
    updated_at: str
    address: Address | None = None
    phones: CustomerPhones | None = None
    metadata: dict[str, Any] | None = None
    code: str | None = None

    model_config = ConfigDict(from_attributes=True, extra="allow")
