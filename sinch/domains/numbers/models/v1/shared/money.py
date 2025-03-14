from decimal import Decimal
from pydantic import StrictStr, Field
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigResponse


class Money(BaseModelConfigResponse):
    currency_code: StrictStr = Field(alias="currencyCode")
    amount: Decimal
