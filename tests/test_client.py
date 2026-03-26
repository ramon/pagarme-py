import pytest
from pytest_httpx import HTTPXMock

from pagarme_py.client import PagarMeClient
from pagarme_py.exceptions import (
    PagarMeAPIError,
    PagarMeAuthenticationError,
    PagarMeValidationError,
)


def test_client_init_success() -> None:
    client = PagarMeClient(api_key="ak_test_123")
    assert client.config.api_key == "ak_test_123"
    assert str(client.config.base_url) == "https://api.pagar.me/core/v5/"
    assert client.config.timeout == 30.0


def test_client_init_custom_params() -> None:
    client = PagarMeClient(
        api_key="ak_test_123",
        base_url="https://custom-api.pagar.me/",
        timeout=10.0
    )
    assert client.config.api_key == "ak_test_123"
    assert str(client.config.base_url) == "https://custom-api.pagar.me/"
    assert client.config.timeout == 10.0


def test_client_init_invalid_api_key() -> None:
    with pytest.raises(PagarMeValidationError):
        PagarMeClient(api_key="")


@pytest.mark.asyncio
async def test_client_authentication_header(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.pagar.me/core/v5/customers",
        status_code=200,
        json={"data": []}
    )

    client = PagarMeClient(api_key="sk_test_abc")
    async with client:
        await client._request("GET", "customers")

    request = httpx_mock.get_request()
    assert request is not None
    assert request.headers["Authorization"].startswith("Basic ")
    # sk_test_abc: -> c2tfdGVzdF9hYmM6 in base64
    import base64
    auth_header = request.headers["Authorization"].split(" ")[1]
    auth_decoded = base64.b64decode(auth_header).decode()
    assert auth_decoded == "sk_test_abc:"


@pytest.mark.asyncio
async def test_client_auth_error(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.pagar.me/core/v5/customers",
        status_code=401,
        json={"message": "Invalid API Key"}
    )

    client = PagarMeClient(api_key="wrong_key")
    async with client:
        with pytest.raises(PagarMeAuthenticationError) as excinfo:
            await client._request("GET", "customers")
        assert excinfo.value.message == "Invalid API Key"


@pytest.mark.asyncio
async def test_client_api_error(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url="https://api.pagar.me/core/v5/orders",
        status_code=400,
        json={"message": "Invalid params"}
    )

    client = PagarMeClient(api_key="ak_test_123")
    async with client:
        with pytest.raises(PagarMeAPIError) as excinfo:
            await client._request("POST", "orders", json={})
        assert excinfo.value.status_code == 400
