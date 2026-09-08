from pydantic import Field, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class Money(BaseModelConfiguration):
    currency_code: StrictStr = Field(
        default=...,
        alias="currencyCode",
        description="The 3-letter currency code defined in [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html).",
    )
    amount: StrictStr = Field(
        default=...,
        description='The monetary amount as a string to preserve precision. Supports up to 4 decimal places (e.g., "10.5000", "0.9999").',
    )
