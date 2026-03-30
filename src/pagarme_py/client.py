"""
Main client for the PagarMe SDK, supporting both asynchronous and synchronous calls.
"""

from abc import ABC, abstractmethod
from typing import Any, Self

import httpx
from pydantic import ValidationError

from pagarme_py.exceptions import (
    PagarMeAPIError,
    PagarMeAuthenticationError,
    PagarMeValidationError,
)
from pagarme_py.models.config import PagarMeConfig
from pagarme_py.resources.charges import ChargeResource, SyncChargeResource
from pagarme_py.resources.customers import CustomerResource, SyncCustomerResource
from pagarme_py.resources.orders import OrderResource, SyncOrderResource


class BasePagarMeClient(ABC):
    """
    Base client for PagarMe SDK.
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

    @property
    @abstractmethod
    def client(self) -> httpx.AsyncClient | httpx.Client:
        """Returns the configured HTTPX client."""
        pass

    def _handle_response_error(self, e: httpx.HTTPStatusError) -> None:
        """Handles HTTP status errors from the API."""
        if e.response.status_code == 401:
            raise PagarMeAuthenticationError(
                "Invalid API Key", e.response.json()
            ) from e
        raise PagarMeAPIError(
            f"PagarMe API Error: {e.response.text}",
            e.response.status_code,
            e.response.json(),
        ) from e

    def _handle_unexpected_error(self, e: Exception) -> None:
        """Handles unexpected errors in requests."""
        raise PagarMeAPIError(f"Unexpected error in request: {str(e)}", 500) from e


class PagarMeSyncClient(BasePagarMeClient):
    """
    Synchronous client to interact with the PagarMe API.

    This client uses `httpx.Client` and Basic Auth.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        super().__init__(api_key, base_url, timeout)
        self._client: httpx.Client | None = None
        self._customers: SyncCustomerResource | None = None
        self._orders: SyncOrderResource | None = None
        self._charges: SyncChargeResource | None = None

    @property
    def customers(self) -> SyncCustomerResource:
        """Access to the customers resource."""
        if self._customers is None:
            self._customers = SyncCustomerResource(self)
        return self._customers

    @property
    def orders(self) -> SyncOrderResource:
        """Access to the orders resource."""
        if self._orders is None:
            self._orders = SyncOrderResource(self)
        return self._orders

    @property
    def charges(self) -> SyncChargeResource:
        """Access to the charges resource."""
        if self._charges is None:
            self._charges = SyncChargeResource(self)
        return self._charges

    @property
    def client(self) -> httpx.Client:
        """
        Returns the configured synchronous HTTPX client.

        Returns:
            httpx.Client: The client configured with authentication and headers.
        """
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(
                base_url=str(self.config.base_url),
                auth=(self.config.api_key, ""),
                timeout=self.config.timeout,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "PagarMe-Python-SDK/0.1.2",
                },
            )
        return self._client

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def close(self) -> None:
        """Closes the HTTPX client if it is open."""
        if self._client and not self._client.is_closed:
            self._client.close()

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Performs a synchronous HTTP request to the PagarMe API.
        """
        try:
            response = self.client.request(method, path, json=json, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_response_error(e)
            raise  # Should not be reached
        except Exception as e:
            self._handle_unexpected_error(e)
            raise  # Should not be reached


class PagarMeClient(BasePagarMeClient):
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
        super().__init__(api_key, base_url, timeout)
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
                    "User-Agent": "PagarMe-Python-SDK/0.1.2",
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
        Performs an asynchronous HTTP request to the PagarMe API.
        """
        try:
            response = await self.client.request(method, path, json=json, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_response_error(e)
            raise  # Should not be reached
        except Exception as e:
            self._handle_unexpected_error(e)
            raise  # Should not be reached
