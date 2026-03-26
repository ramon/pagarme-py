import pytest
from pytest_httpx import HTTPXMock

from pagarme_py.client import PagarMeClient
from pagarme_py.models.items import OrderItemRequest
from pagarme_py.models.orders import OrderCreateRequest
from pagarme_py.models.payments import PaymentCreditCard, PaymentRequest


@pytest.mark.asyncio
async def test_create_order(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.pagar.me/core/v5/orders",
        status_code=200,
        json={
            "id": "or_123",
            "code": "ORD-001",
            "amount": 1000,
            "currency": "BRL",
            "status": "paid",
            "items": [
                {
                    "id": "oi_123",
                    "amount": 1000,
                    "description": "Item 1",
                    "quantity": 1,
                    "status": "active",
                    "created_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2023-01-01T00:00:00Z"
                }
            ],
            "closed": True,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeClient(api_key="sk_test")
    order_data = OrderCreateRequest(
        items=[
            OrderItemRequest(
                amount=1000,
                description="Item 1",
                quantity=1
            )
        ],
        payments=[
            PaymentRequest(
                payment_method="credit_card",
                credit_card=PaymentCreditCard(
                    card_id="card_123"
                )
            )
        ],
        code="ORD-001"
    )

    order = await client.orders.create(order_data)
    assert order.id == "or_123"
    assert order.status == "paid"
    assert len(order.items) == 1
    assert order.items[0].description == "Item 1"


@pytest.mark.asyncio
async def test_get_order(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.pagar.me/core/v5/orders/or_123",
        status_code=200,
        json={
            "id": "or_123",
            "amount": 1000,
            "currency": "BRL",
            "status": "pending",
            "items": [],
            "closed": False,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeClient(api_key="sk_test")
    order = await client.orders.get("or_123")
    assert order.id == "or_123"
    assert order.status == "pending"
