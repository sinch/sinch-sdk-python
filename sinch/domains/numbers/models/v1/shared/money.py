from typing import Optional
from pydantic import StrictStr, Field, condecimal
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class Money(BaseModelConfigurationResponse):
    currency_code: Optional[StrictStr] = Field(alias="currencyCode")
    amount: Optional[condecimal()] = None
