"""
Pydantic models for charges in the PagarMe SDK.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict

from pagarme_py.models.customers import CustomerResponse


class ChargeCaptureRequest(BaseModel):
    """Data for capturing a charge."""

    amount: int | None = None
    code: str | None = None
    metadata: dict[str, Any] | None = None


class ChargeRefundRequest(BaseModel):
    """Data for refunding a charge."""

    amount: int | None = None
    metadata: dict[str, Any] | None = None


class ChargeUpdateRequest(BaseModel):
    """Data for updating a charge."""

    due_at: str | None = None
    metadata: dict[str, Any] | None = None


class TransactionResponse(BaseModel):
    """Generic transaction response."""

    id: str
    transaction_type: str
    status: str
    amount: int
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True, extra="allow")


class ChargeResponse(BaseModel):
    """Charge response from the PagarMe API."""

    id: str
    code: str | None = None
    amount: int
    paid_amount: int | None = None
    status: str
    currency: str
    payment_method: str
    paid_at: str | None = None
    created_at: str
    updated_at: str
    customer: CustomerResponse | None = None
    last_transaction: TransactionResponse | None = None
    metadata: dict[str, Any] | None = None

    model_config = ConfigDict(from_attributes=True, extra="allow")
