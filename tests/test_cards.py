import pytest
from pytest_httpx import HTTPXMock

from pagarme_py.client import PagarMeClient
from pagarme_py.models.address import Address
from pagarme_py.models.cards import CardCreateRequest


@pytest.mark.asyncio
async def test_create_card(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.pagar.me/core/v5/customers/cust_123/cards",
        status_code=200,
        json={
            "id": "card_123",
            "last_four_digits": "1234",
            "brand": "Visa",
            "holder_name": "Tony Stark",
            "exp_month": 12,
            "exp_year": 2030,
            "status": "active",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeClient(api_key="sk_test")
    card_data = CardCreateRequest(
        number="1234567812341234",
        holder_name="Tony Stark",
        exp_month=12,
        exp_year=2030,
        cvv="123",
        billing_address=Address(
            street="Heroes Street",
            number="100",
            zip_code="01234567",
            neighborhood="Downtown",
            city="New York",
            state="NY"
        )
    )

    card = await client.customers.create_card("cust_123", card_data)
    assert card.id == "card_123"
    assert card.last_four_digits == "1234"
    assert card.brand == "Visa"

@pytest.mark.asyncio
async def test_create_card_with_token(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.pagar.me/core/v5/customers/cust_123/cards",
        status_code=200,
        json={
            "id": "card_token_123",
            "last_four_digits": "1111",
            "brand": "Mastercard",
            "holder_name": "Tony Stark",
            "exp_month": 11,
            "exp_year": 2031,
            "status": "active",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeClient(api_key="sk_test")
    card_data = CardCreateRequest(token="token_xyz")

    card = await client.customers.create_card("cust_123", card_data)
    assert card.id == "card_token_123"
    assert card.brand == "Mastercard"

    request = httpx_mock.get_request()
    import json
    payload = json.loads(request.read())
    assert payload["token"] == "token_xyz"
    assert "number" not in payload

@pytest.mark.asyncio
async def test_create_card_with_metadata(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.pagar.me/core/v5/customers/cust_123/cards",
        status_code=200,
        json={
            "id": "card_meta_123",
            "brand": "Visa",
            "exp_month": 12,
            "exp_year": 2030,
            "status": "active",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "metadata": {"origin": "mobile_app"}
        }
    )

    client = PagarMeClient(api_key="sk_test")
    card_data = CardCreateRequest(
        number="1234567812341234",
        holder_name="Tony Stark",
        exp_month=12,
        exp_year=2030,
        cvv="123",
        metadata={"origin": "mobile_app"}
    )

    card = await client.customers.create_card("cust_123", card_data)
    assert card.metadata == {"origin": "mobile_app"}

def test_card_create_validation() -> None:
    from pydantic import ValidationError
    
    # Missing everything
    with pytest.raises(ValidationError):
        CardCreateRequest()
    
    # Missing partial data without token
    with pytest.raises(ValidationError):
        CardCreateRequest(number="123")
    
    # Valid with token
    card = CardCreateRequest(token="abc")
    assert card.token == "abc"

@pytest.mark.asyncio
async def test_delete_card(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="DELETE",
        url="https://api.pagar.me/core/v5/customers/cust_123/cards/card_123",
        status_code=200,
        json={
            "id": "card_123",
            "last_four_digits": "1234",
            "brand": "Visa",
            "holder_name": "Tony Stark",
            "exp_month": 12,
            "exp_year": 2030,
            "status": "deleted",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeClient(api_key="sk_test")
    card = await client.customers.delete_card("cust_123", "card_123")
    assert card.status == "deleted"
