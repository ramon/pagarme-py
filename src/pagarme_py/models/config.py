"""
Pydantic models for PagarMe SDK configuration.
"""

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class PagarMeConfig(BaseModel):
    """
    Configuration for PagarMeClient.

    Attributes:
        api_key (str): Secret API Key for authentication.
        base_url (HttpUrl): PagarMe API base URL.
        timeout (float): Timeout for HTTP requests (in seconds).
    """

    api_key: str = Field(..., min_length=1, description="The secret API key")
    base_url: HttpUrl = Field(
        default=HttpUrl("https://api.pagar.me/core/v5/"),
        description="PagarMe API base URL"
    )
    timeout: float = Field(default=30.0, ge=0, description="Request timeout")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
    )
