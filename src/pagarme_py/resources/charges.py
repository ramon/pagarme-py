"""
Implementation of the Charges resource.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pagarme_py.models.charges import (
    ChargeCaptureRequest,
    ChargeRefundRequest,
    ChargeResponse,
    ChargeUpdateRequest,
)

if TYPE_CHECKING:
    from pagarme_py.client import PagarMeClient, PagarMeSyncClient


class ChargeResource:
    """Asynchronous resource to manage charges."""

    def __init__(self, client: PagarMeClient) -> None:
        self._client = client

    async def get(self, charge_id: str) -> ChargeResponse:
        """Gets a charge by ID."""
        response = await self._client._request("GET", f"charges/{charge_id}")
        return ChargeResponse.model_validate(response)

    async def list(
        self, page: int = 1, size: int = 10, **params: Any
    ) -> list[ChargeResponse]:
        """Lists registered charges."""
        query_params = {"page": page, "size": size, **params}
        response = await self._client._request("GET", "charges", params=query_params)
        if isinstance(response, dict):
            data = response.get("data", response)
        else:
            data = response
        return [ChargeResponse.model_validate(item) for item in data]

    async def update(self, charge_id: str, data: ChargeUpdateRequest) -> ChargeResponse:
        """Updates a charge's data."""
        response = await self._client._request(
            "PUT",
            f"charges/{charge_id}",
            json=data.model_dump(exclude_none=True),
        )
        return ChargeResponse.model_validate(response)

    async def capture(
        self, charge_id: str, data: ChargeCaptureRequest | None = None
    ) -> ChargeResponse:
        """Captures a pre-authorized charge."""
        json_data = data.model_dump(exclude_none=True) if data else {}
        response = await self._client._request(
            "POST", f"charges/{charge_id}/capture", json=json_data
        )
        return ChargeResponse.model_validate(response)

    async def refund(
        self, charge_id: str, data: ChargeRefundRequest | None = None
    ) -> ChargeResponse:
        """Refunds a charge."""
        json_data = data.model_dump(exclude_none=True) if data else {}
        response = await self._client._request(
            "POST", f"charges/{charge_id}/refund", json=json_data
        )
        return ChargeResponse.model_validate(response)

    async def retry(self, charge_id: str) -> ChargeResponse:
        """Retries a failed charge."""
        response = await self._client._request("POST", f"charges/{charge_id}/retry")
        return ChargeResponse.model_validate(response)


class SyncChargeResource:
    """Synchronous resource to manage charges."""

    def __init__(self, client: PagarMeSyncClient) -> None:
        self._client = client

    def get(self, charge_id: str) -> ChargeResponse:
        """Gets a charge by ID."""
        response = self._client._request("GET", f"charges/{charge_id}")
        return ChargeResponse.model_validate(response)

    def list(
        self, page: int = 1, size: int = 10, **params: Any
    ) -> list[ChargeResponse]:
        """Lists registered charges."""
        query_params = {"page": page, "size": size, **params}
        response = self._client._request("GET", "charges", params=query_params)
        if isinstance(response, dict):
            data = response.get("data", response)
        else:
            data = response
        return [ChargeResponse.model_validate(item) for item in data]

    def update(self, charge_id: str, data: ChargeUpdateRequest) -> ChargeResponse:
        """Updates a charge's data."""
        response = self._client._request(
            "PUT",
            f"charges/{charge_id}",
            json=data.model_dump(exclude_none=True),
        )
        return ChargeResponse.model_validate(response)

    def capture(
        self, charge_id: str, data: ChargeCaptureRequest | None = None
    ) -> ChargeResponse:
        """Captures a pre-authorized charge."""
        json_data = data.model_dump(exclude_none=True) if data else {}
        response = self._client._request(
            "POST", f"charges/{charge_id}/capture", json=json_data
        )
        return ChargeResponse.model_validate(response)

    def refund(
        self, charge_id: str, data: ChargeRefundRequest | None = None
    ) -> ChargeResponse:
        """Refunds a charge."""
        json_data = data.model_dump(exclude_none=True) if data else {}
        response = self._client._request(
            "POST", f"charges/{charge_id}/refund", json=json_data
        )
        return ChargeResponse.model_validate(response)

    def retry(self, charge_id: str) -> ChargeResponse:
        """Retries a failed charge."""
        response = self._client._request("POST", f"charges/{charge_id}/retry")
        return ChargeResponse.model_validate(response)
