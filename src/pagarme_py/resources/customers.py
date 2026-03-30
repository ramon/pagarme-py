"""
Implementation of the Customers resource and Cards sub-resource.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pagarme_py.models.cards import (
    CardCreateRequest,
    CardResponse,
)
from pagarme_py.models.customers import (
    CustomerCreateRequest,
    CustomerResponse,
    CustomerUpdateRequest,
)

if TYPE_CHECKING:
    from pagarme_py.client import PagarMeClient, PagarMeSyncClient


class CustomerResource:
    """Asynchronous resource to manage customers and their cards."""

    def __init__(self, client: PagarMeClient) -> None:
        self._client = client

    async def create(self, data: CustomerCreateRequest) -> CustomerResponse:
        """Creates a new customer."""
        response = await self._client._request(
            "POST", "customers", json=data.model_dump(exclude_none=True)
        )
        return CustomerResponse.model_validate(response)

    async def get(self, customer_id: str) -> CustomerResponse:
        """Gets a customer by ID."""
        response = await self._client._request("GET", f"customers/{customer_id}")
        return CustomerResponse.model_validate(response)

    async def list(
        self, page: int = 1, size: int = 10, **params: Any
    ) -> list[CustomerResponse]:
        """Lists registered customers."""
        query_params = {"page": page, "size": size, **params}
        response = await self._client._request("GET", "customers", params=query_params)
        # The PagarMe API usually returns a list in 'data' or directly
        if isinstance(response, dict):
            data = response.get("data", response)
        else:
            data = response
        return [CustomerResponse.model_validate(item) for item in data]

    async def update(
        self, customer_id: str, data: CustomerUpdateRequest
    ) -> CustomerResponse:
        """Updates a customer's data."""
        response = await self._client._request(
            "PUT",
            f"customers/{customer_id}",
            json=data.model_dump(exclude_none=True),
        )
        return CustomerResponse.model_validate(response)

    # Cards sub-resource
    async def create_card(
        self, customer_id: str, data: CardCreateRequest
    ) -> CardResponse:
        """Creates a new card for a customer."""
        response = await self._client._request(
            "POST",
            f"customers/{customer_id}/cards",
            json=data.model_dump(exclude_none=True),
        )
        return CardResponse.model_validate(response)

    async def get_card(self, customer_id: str, card_id: str) -> CardResponse:
        """Gets a card from a customer."""
        response = await self._client._request(
            "GET", f"customers/{customer_id}/cards/{card_id}"
        )
        return CardResponse.model_validate(response)

    async def list_cards(
        self, customer_id: str, page: int = 1, size: int = 10
    ) -> list[CardResponse]:
        """Lists a customer's cards."""
        params = {"page": page, "size": size}
        response = await self._client._request(
            "GET", f"customers/{customer_id}/cards", params=params
        )
        if isinstance(response, dict):
            data = response.get("data", response)
        else:
            data = response
        return [CardResponse.model_validate(item) for item in data]

    async def delete_card(self, customer_id: str, card_id: str) -> CardResponse:
        """Removes a card from a customer."""
        response = await self._client._request(
            "DELETE", f"customers/{customer_id}/cards/{card_id}"
        )
        return CardResponse.model_validate(response)


class SyncCustomerResource:
    """Synchronous resource to manage customers and their cards."""

    def __init__(self, client: PagarMeSyncClient) -> None:
        self._client = client

    def create(self, data: CustomerCreateRequest) -> CustomerResponse:
        """Creates a new customer."""
        response = self._client._request(
            "POST", "customers", json=data.model_dump(exclude_none=True)
        )
        return CustomerResponse.model_validate(response)

    def get(self, customer_id: str) -> CustomerResponse:
        """Gets a customer by ID."""
        response = self._client._request("GET", f"customers/{customer_id}")
        return CustomerResponse.model_validate(response)

    def list(
        self, page: int = 1, size: int = 10, **params: Any
    ) -> list[CustomerResponse]:
        """Lists registered customers."""
        query_params = {"page": page, "size": size, **params}
        response = self._client._request("GET", "customers", params=query_params)
        if isinstance(response, dict):
            data = response.get("data", response)
        else:
            data = response
        return [CustomerResponse.model_validate(item) for item in data]

    def update(
        self, customer_id: str, data: CustomerUpdateRequest
    ) -> CustomerResponse:
        """Updates a customer's data."""
        response = self._client._request(
            "PUT",
            f"customers/{customer_id}",
            json=data.model_dump(exclude_none=True),
        )
        return CustomerResponse.model_validate(response)

    # Cards sub-resource
    def create_card(
        self, customer_id: str, data: CardCreateRequest
    ) -> CardResponse:
        """Creates a new card for a customer."""
        response = self._client._request(
            "POST",
            f"customers/{customer_id}/cards",
            json=data.model_dump(exclude_none=True),
        )
        return CardResponse.model_validate(response)

    def get_card(self, customer_id: str, card_id: str) -> CardResponse:
        """Gets a card from a customer."""
        response = self._client._request(
            "GET", f"customers/{customer_id}/cards/{card_id}"
        )
        return CardResponse.model_validate(response)

    def list_cards(
        self, customer_id: str, page: int = 1, size: int = 10
    ) -> list[CardResponse]:
        """Lists a customer's cards."""
        params = {"page": page, "size": size}
        response = self._client._request(
            "GET", f"customers/{customer_id}/cards", params=params
        )
        if isinstance(response, dict):
            data = response.get("data", response)
        else:
            data = response
        return [CardResponse.model_validate(item) for item in data]

    def delete_card(self, customer_id: str, card_id: str) -> CardResponse:
        """Removes a card from a customer."""
        response = self._client._request(
            "DELETE", f"customers/{customer_id}/cards/{card_id}"
        )
        return CardResponse.model_validate(response)
