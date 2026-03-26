"""
Pydantic models for orders in the PagarMe SDK.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict

from pagarme_py.models.charges import ChargeResponse
from pagarme_py.models.customers import (
    CustomerCreateRequest,
    CustomerResponse,
)
from pagarme_py.models.items import OrderItemRequest, OrderItemResponse
from pagarme_py.models.payments import PaymentRequest


class OrderCreateRequest(BaseModel):
    """Data for creating an order."""

    items: list[OrderItemRequest]
    customer: CustomerCreateRequest | None = None
    customer_id: str | None = None
    payments: list[PaymentRequest] | None = None
    code: str | None = None
    metadata: dict[str, Any] | None = None
    closed: bool = True


class OrderResponse(BaseModel):
    """Order response from the PagarMe API."""

    id: str
    code: str | None = None
    amount: int
    currency: str
    status: str
    items: list[OrderItemResponse]
    customer: CustomerResponse | None = None
    charges: list[ChargeResponse] | None = None
    created_at: str
    updated_at: str
    closed: bool

    model_config = ConfigDict(from_attributes=True, extra="allow")
