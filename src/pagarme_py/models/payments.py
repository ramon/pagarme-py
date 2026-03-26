"""
Pydantic models for payments in the PagarMe SDK.
"""

from pydantic import BaseModel, ConfigDict, Field

from pagarme_py.models.cards import CardCreateRequest, CardResponse


class PaymentCreditCard(BaseModel):
    """Credit card payment data."""

    card_id: str | None = None
    card: CardCreateRequest | None = None
    installments: int = 1
    statement_descriptor: str | None = None
    operation_type: str | None = Field(None, pattern="^(auth_only|auth_and_capture)$")


class PaymentBoleto(BaseModel):
    """Boleto payment data."""

    bank: str | None = None
    instructions: str | None = None
    due_at: str | None = None
    nosso_numero: str | None = None


class PaymentPix(BaseModel):
    """Pix payment data."""

    expires_in: int | None = None
    additional_information: list[dict[str, str]] | None = None


class PaymentRequest(BaseModel):
    """Data for creating a payment."""

    payment_method: str = Field(
        ..., pattern="^(credit_card|boleto|pix|voucher|debit_card)$"
    )
    credit_card: PaymentCreditCard | None = None
    boleto: PaymentBoleto | None = None
    pix: PaymentPix | None = None


class PaymentCreditCardResponse(BaseModel):
    """Credit card payment response data."""

    card: CardResponse | None = None
    installments: int | None = None
    statement_descriptor: str | None = None


class PaymentBoletoResponse(BaseModel):
    """Boleto payment response data."""

    bank: str | None = None
    instructions: str | None = None
    due_at: str | None = None
    qr_code: str | None = None
    line: str | None = None
    pdf: str | None = None


class PaymentPixResponse(BaseModel):
    """Pix payment response data."""

    expires_in: int | None = None
    additional_information: list[dict[str, str]] | None = None
    qr_code: str | None = None
    qr_code_url: str | None = None


class PaymentResponse(BaseModel):
    """Payment response from the PagarMe API."""

    payment_method: str
    status: str
    amount: int
    success: bool | None = None
    credit_card: PaymentCreditCardResponse | None = None
    boleto: PaymentBoletoResponse | None = None
    pix: PaymentPixResponse | None = None

    model_config = ConfigDict(from_attributes=True, extra="allow")
