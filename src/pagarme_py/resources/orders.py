"""
Implementation of the Orders resource.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pagarme_py.models.items import OrderItemRequest, OrderItemResponse
from pagarme_py.models.orders import OrderCreateRequest, OrderResponse

if TYPE_CHECKING:
    from pagarme_py.client import PagarMeClient, PagarMeSyncClient


class OrderResource:
    """Asynchronous resource to manage orders."""

    def __init__(self, client: PagarMeClient) -> None:
        self._client = client

    async def create(self, data: OrderCreateRequest) -> OrderResponse:
        """Creates a new order."""
        response = await self._client._request(
            "POST", "orders", json=data.model_dump(exclude_none=True)
        )
        return OrderResponse.model_validate(response)

    async def get(self, order_id: str) -> OrderResponse:
        """Gets an order by ID."""
        response = await self._client._request("GET", f"orders/{order_id}")
        return OrderResponse.model_validate(response)

    async def list(
        self, page: int = 1, size: int = 10, **params: Any
    ) -> list[OrderResponse]:
        """Lists registered orders."""
        query_params = {"page": page, "size": size, **params}
        response = await self._client._request("GET", "orders", params=query_params)
        if isinstance(response, dict):
            data = response.get("data", response)
        else:
            data = response
        return [OrderResponse.model_validate(item) for item in data]

    async def add_item(
        self, order_id: str, data: OrderItemRequest
    ) -> OrderItemResponse:
        """Adds a new item to an order."""
        response = await self._client._request(
            "POST",
            f"orders/{order_id}/items",
            json=data.model_dump(exclude_none=True),
        )
        return OrderItemResponse.model_validate(response)

    async def get_item(self, order_id: str, item_id: str) -> OrderItemResponse:
        """Gets an item from an order."""
        response = await self._client._request(
            "GET", f"orders/{order_id}/items/{item_id}"
        )
        return OrderItemResponse.model_validate(response)

    async def delete_item(self, order_id: str, item_id: str) -> OrderItemResponse:
        """Removes an item from an order."""
        # Note: Delete item endpoint might return the deleted item
        response = await self._client._request(
            "DELETE", f"orders/{order_id}/items/{item_id}"
        )
        return OrderItemResponse.model_validate(response)


class SyncOrderResource:
    """Synchronous resource to manage orders."""

    def __init__(self, client: PagarMeSyncClient) -> None:
        self._client = client

    def create(self, data: OrderCreateRequest) -> OrderResponse:
        """Creates a new order."""
        response = self._client._request(
            "POST", "orders", json=data.model_dump(exclude_none=True)
        )
        return OrderResponse.model_validate(response)

    def get(self, order_id: str) -> OrderResponse:
        """Gets an order by ID."""
        response = self._client._request("GET", f"orders/{order_id}")
        return OrderResponse.model_validate(response)

    def list(
        self, page: int = 1, size: int = 10, **params: Any
    ) -> list[OrderResponse]:
        """Lists registered orders."""
        query_params = {"page": page, "size": size, **params}
        response = self._client._request("GET", "orders", params=query_params)
        if isinstance(response, dict):
            data = response.get("data", response)
        else:
            data = response
        return [OrderResponse.model_validate(item) for item in data]

    def add_item(
        self, order_id: str, data: OrderItemRequest
    ) -> OrderItemResponse:
        """Adds a new item to an order."""
        response = self._client._request(
            "POST",
            f"orders/{order_id}/items",
            json=data.model_dump(exclude_none=True),
        )
        return OrderItemResponse.model_validate(response)

    def get_item(self, order_id: str, item_id: str) -> OrderItemResponse:
        """Gets an item from an order."""
        response = self._client._request(
            "GET", f"orders/{order_id}/items/{item_id}"
        )
        return OrderItemResponse.model_validate(response)

    def delete_item(self, order_id: str, item_id: str) -> OrderItemResponse:
        """Removes an item from an order."""
        response = self._client._request(
            "DELETE", f"orders/{order_id}/items/{item_id}"
        )
        return OrderItemResponse.model_validate(response)
