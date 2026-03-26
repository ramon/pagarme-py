"""
Main client for the PagarMe SDK for asynchronous calls.
"""

from typing import Any, Self

import httpx
from pydantic import ValidationError

from pagarme_py.exceptions import (
    PagarMeAPIError,
    PagarMeAuthenticationError,
    PagarMeValidationError,
)
from pagarme_py.models.config import PagarMeConfig
from pagarme_py.resources.charges import ChargeResource
from pagarme_py.resources.customers import CustomerResource
from pagarme_py.resources.orders import OrderResource


class PagarMeClient:
    """
    Asynchronous client to interact with the PagarMe API.

    This client uses `httpx.AsyncClient` and Basic Auth.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        """
        Initializes the PagarMe client.

        Args:
            api_key: Secret API Key for authentication.
            base_url: Custom base URL for the API (optional).
            timeout: Request timeout in seconds (optional).

        Raises:
            PagarMeValidationError: If the configuration is invalid.
        """
        try:
            config_params: dict[str, Any] = {"api_key": api_key}
            if base_url:
                config_params["base_url"] = base_url
            if timeout is not None:
                config_params["timeout"] = timeout

            self.config = PagarMeConfig(**config_params)
        except ValidationError as e:
            raise PagarMeValidationError(
                "Invalid client configuration", e.errors()
            ) from e

        self._client: httpx.AsyncClient | None = None
        self._customers: CustomerResource | None = None
        self._orders: OrderResource | None = None
        self._charges: ChargeResource | None = None

    @property
    def customers(self) -> CustomerResource:
        """Access to the customers resource."""
        if self._customers is None:
            self._customers = CustomerResource(self)
        return self._customers

    @property
    def orders(self) -> OrderResource:
        """Access to the orders resource."""
        if self._orders is None:
            self._orders = OrderResource(self)
        return self._orders

    @property
    def charges(self) -> ChargeResource:
        """Access to the charges resource."""
        if self._charges is None:
            self._charges = ChargeResource(self)
        return self._charges

    @property
    def client(self) -> httpx.AsyncClient:
        """
        Returns the configured asynchronous HTTPX client.

        Returns:
            httpx.AsyncClient: The client configured with authentication and headers.
        """
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=str(self.config.base_url),
                auth=(self.config.api_key, ""),
                timeout=self.config.timeout,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "PagarMe-Python-SDK/0.1.0",
                },
            )
        return self._client

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    async def close(self) -> None:
        """Closes the HTTPX client if it is open."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Performs an HTTP request to the PagarMe API.

        Args:
            method: HTTP method (GET, POST, etc.).
            path: Endpoint path.
            json: Data for the request body (optional).
            params: Query string parameters (optional).

        Returns:
            dict[str, Any]: JSON response from the API.

        Raises:
            PagarMeAuthenticationError: If authentication fails (401).
            PagarMeAPIError: If the API returns an unexpected error.
        """
        try:
            response = await self.client.request(method, path, json=json, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise PagarMeAuthenticationError(
                    "Invalid API Key", e.response.json()
                ) from e
            raise PagarMeAPIError(
                f"PagarMe API Error: {e.response.text}",
                e.response.status_code,
                e.response.json(),
            ) from e
        except Exception as e:
            raise PagarMeAPIError(
                f"Unexpected error in request: {str(e)}", 500
            ) from e
