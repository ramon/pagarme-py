import pytest
from pytest_httpx import HTTPXMock

from pagarme_py.client import PagarMeClient
from pagarme_py.models.charges import ChargeCaptureRequest, ChargeRefundRequest


@pytest.mark.asyncio
async def test_get_charge(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.pagar.me/core/v5/charges/ch_123",
        status_code=200,
        json={
            "id": "ch_123",
            "amount": 1000,
            "status": "paid",
            "currency": "BRL",
            "payment_method": "credit_card",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeClient(api_key="sk_test")
    charge = await client.charges.get("ch_123")
    assert charge.id == "ch_123"
    assert charge.status == "paid"


@pytest.mark.asyncio
async def test_capture_charge(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.pagar.me/core/v5/charges/ch_123/capture",
        status_code=200,
        json={
            "id": "ch_123",
            "amount": 1000,
            "status": "paid",
            "currency": "BRL",
            "payment_method": "credit_card",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeClient(api_key="sk_test")
    charge = await client.charges.capture("ch_123", ChargeCaptureRequest(amount=1000))
    assert charge.status == "paid"


@pytest.mark.asyncio
async def test_refund_charge(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.pagar.me/core/v5/charges/ch_123/refund",
        status_code=200,
        json={
            "id": "ch_123",
            "amount": 1000,
            "status": "refunded",
            "currency": "BRL",
            "payment_method": "credit_card",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeClient(api_key="sk_test")
    charge = await client.charges.refund("ch_123", ChargeRefundRequest(amount=1000))
    assert charge.status == "refunded"
