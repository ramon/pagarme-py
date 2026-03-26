"""
Custom exceptions module for the PagarMe SDK.
"""

from typing import Any


class PagarMeError(Exception):
    """Base exception for all PagarMe SDK failures."""

    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class PagarMeAuthenticationError(PagarMeError):
    """Error raised when authentication fails (invalid API Key)."""


class PagarMeValidationError(PagarMeError):
    """Data validation error via Pydantic or user input data."""


class PagarMeAPIError(PagarMeError):
    """Error for API response failures (status code != 2xx)."""

    def __init__(
        self, message: str, status_code: int, details: Any | None = None
    ) -> None:
        super().__init__(message, details)
        self.status_code = status_code
