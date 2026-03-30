import base64

import pytest
from pytest_httpx import HTTPXMock

from pagarme_py.client import PagarMeSyncClient
from pagarme_py.exceptions import (
    PagarMeAPIError,
    PagarMeAuthenticationError,
    PagarMeValidationError,
)


def test_sync_client_init_success() -> None:
    client = PagarMeSyncClient(api_key="ak_test_123")
    assert client.config.api_key == "ak_test_123"
    assert str(client.config.base_url) == "https://api.pagar.me/core/v5/"
    assert client.config.timeout == 30.0


def test_sync_client_init_custom_params() -> None:
    client = PagarMeSyncClient(
        api_key="ak_test_123",
        base_url="https://custom-api.pagar.me/",
        timeout=10.0
    )
    assert client.config.api_key == "ak_test_123"
    assert str(client.config.base_url) == "https://custom-api.pagar.me/"
    assert client.config.timeout == 10.0


def test_sync_client_init_invalid_api_key() -> None:
    with pytest.raises(PagarMeValidationError):
        PagarMeSyncClient(api_key="")


def test_sync_client_authentication_header(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.pagar.me/core/v5/customers",
        status_code=200,
        json={"data": []}
    )

    client = PagarMeSyncClient(api_key="sk_test_abc")
    with client:
        client._request("GET", "customers")

    request = httpx_mock.get_request()
    assert request is not None
    assert request.headers["Authorization"].startswith("Basic ")
    
    auth_header = request.headers["Authorization"].split(" ")[1]
    auth_decoded = base64.b64decode(auth_header).decode()
    assert auth_decoded == "sk_test_abc:"


def test_sync_client_auth_error(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.pagar.me/core/v5/customers",
        status_code=401,
        json={"message": "Invalid API Key"}
    )

    client = PagarMeSyncClient(api_key="wrong_key")
    with client:
        with pytest.raises(PagarMeAuthenticationError) as excinfo:
            client._request("GET", "customers")
        assert excinfo.value.message == "Invalid API Key"


def test_sync_client_api_error(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.pagar.me/core/v5/orders",
        status_code=400,
        json={"message": "Invalid params"}
    )

    client = PagarMeSyncClient(api_key="ak_test_123")
    with client:
        with pytest.raises(PagarMeAPIError) as excinfo:
            client._request("POST", "orders", json={})
        assert excinfo.value.status_code == 400


def test_sync_customer_resource_get(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.pagar.me/core/v5/customers/cus_123",
        status_code=200,
        json={
            "id": "cus_123",
            "name": "Tony Stark",
            "email": "tony@stark.com",
            "document": "12345678909",
            "type": "individual",
            "delinquent": False,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeSyncClient(api_key="ak_test_123")
    customer = client.customers.get("cus_123")
    assert customer.id == "cus_123"
    assert customer.name == "Tony Stark"


def test_sync_order_resource_list(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.pagar.me/core/v5/orders?page=1&size=10",
        status_code=200,
        json={
            "data": [
                {
                    "id": "ord_123",
                    "code": "XYZ",
                    "amount": 1000,
                    "status": "pending",
                    "currency": "BRL",
                    "closed": False,
                    "items": [],
                    "created_at": "2023-01-01T00:00:00Z",
                    "updated_at": "2023-01-01T00:00:00Z",
                    "customer": {
                        "id": "cust_123",
                        "name": "Tony Stark",
                        "email": "tony@stark.com",
                        "document": "12345678909",
                        "type": "individual",
                        "delinquent": False,
                        "created_at": "2023-01-01T00:00:00Z",
                        "updated_at": "2023-01-01T00:00:00Z"
                    }
                }
            ]
        }
    )

    client = PagarMeSyncClient(api_key="ak_test_123")
    orders = client.orders.list()
    assert len(orders) == 1
    assert orders[0].id == "ord_123"


def test_sync_charge_resource_get(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.pagar.me/core/v5/charges/ch_123",
        status_code=200,
        json={
            "id": "ch_123",
            "code": "XYZ",
            "amount": 1000,
            "paid_amount": 0,
            "status": "pending",
            "currency": "BRL",
            "payment_method": "credit_card",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    )

    client = PagarMeSyncClient(api_key="ak_test_123")
    charge = client.charges.get("ch_123")
    assert charge.id == "ch_123"
    assert charge.status == "pending"
