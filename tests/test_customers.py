import pytest
from pytest_httpx import HTTPXMock

from pagarme_py.client import PagarMeClient
from pagarme_py.models.address import Address
from pagarme_py.models.customers import CustomerCreateRequest


@pytest.mark.asyncio
async def test_create_customer(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.pagar.me/core/v5/customers",
        status_code=200,
        json={
            "id": "cust_123",
            "name": "Tony Stark",
            "email": "tony@stark.com",
            "document": "12345678909",
            "type": "individual",
            "delinquent": False,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeClient(api_key="sk_test")
    customer_data = CustomerCreateRequest(
        name="Tony Stark",
        email="tony@stark.com",
        document="12345678909",
        type="individual",
        address=Address(
            street="Heroes Street",
            number="100",
            zip_code="01234567",
            neighborhood="Downtown",
            city="New York",
            state="NY"
        )
    )

    customer = await client.customers.create(customer_data)
    assert customer.id == "cust_123"
    assert customer.name == "Tony Stark"

@pytest.mark.asyncio
async def test_get_customer(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.pagar.me/core/v5/customers/cust_123",
        status_code=200,
        json={
            "id": "cust_123",
            "name": "Tony Stark",
            "email": "tony@stark.com",
            "document": "12345678909",
            "type": "individual",
            "delinquent": False,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeClient(api_key="sk_test")
    customer = await client.customers.get("cust_123")
    assert customer.id == "cust_123"

@pytest.mark.asyncio
async def test_list_customers(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.pagar.me/core/v5/customers?page=1&size=10",
        status_code=200,
        json={
            "data": [
                {
                    "id": "cust_123",
                    "name": "Tony Stark",
                    "email": "tony@stark.com",
                    "document": "12345678909",
                    "type": "individual",
                    "delinquent": False,
                    "created_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2023-01-01T00:00:00Z"
                }
            ]
        }
    )

    client = PagarMeClient(api_key="sk_test")
    customers = await client.customers.list()
    assert len(customers) == 1
    assert customers[0].id == "cust_123"

@pytest.mark.asyncio
async def test_create_customer_with_full_phone(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.pagar.me/core/v5/customers",
        status_code=200,
        json={
            "id": "cust_123",
            "name": "Tony Stark",
            "email": "tony@stark.com",
            "document": "12345678909",
            "type": "individual",
            "delinquent": False,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "phones": {
                "mobile_phone": {
                    "country_code": "55",
                    "area_code": "11",
                    "number": "999999999"
                }
            }
        }
    )

    from pagarme_py.models.customers import CustomerPhones

    client = PagarMeClient(api_key="sk_test")
    customer_data = CustomerCreateRequest(
        name="Tony Stark",
        email="tony@stark.com",
        document="12345678909",
        type="individual",
        phones=CustomerPhones(
            mobile_phone="+5511999999999"
        )
    )

    customer = await client.customers.create(customer_data)
    assert customer.id == "cust_123"
    
    # Verify the request payload
    request = httpx_mock.get_request()
    import json
    payload = json.loads(request.read())
    assert payload["phones"]["mobile_phone"]["country_code"] == "55"
    assert payload["phones"]["mobile_phone"]["area_code"] == "11"
    assert payload["phones"]["mobile_phone"]["number"] == "999999999"
    assert "full_phone" not in payload["phones"]["mobile_phone"]
