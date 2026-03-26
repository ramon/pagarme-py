"""
Pydantic models for order items in the PagarMe SDK.
"""

from pydantic import BaseModel, ConfigDict


class OrderItemRequest(BaseModel):
    """Data for creating an order item."""

    amount: int
    description: str
    quantity: int
    category: str | None = None
    code: str | None = None


class OrderItemResponse(BaseModel):
    """Order item response from the PagarMe API."""

    id: str
    amount: int
    description: str
    quantity: int
    category: str | None = None
    code: str | None = None
    status: str
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True, extra="allow")
