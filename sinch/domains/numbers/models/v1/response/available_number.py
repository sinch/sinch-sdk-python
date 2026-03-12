from typing import Optional
from pydantic import Field, StrictBool, StrictInt, StrictStr, conlist
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.numbers.models.v1.shared import Money
from sinch.domains.numbers.models.v1.types import CapabilityType, NumberType


class AvailableNumber(BaseModelConfigurationResponse):
    phone_number: Optional[StrictStr] = Field(
        default=None,
        alias="phoneNumber",
        description="Phone number in E.164 format with leading '+'. Example: '+12025550134'.",
    )
    region_code: Optional[StrictStr] = Field(
        default=None,
        alias="regionCode",
        description="ISO 3166-1 alpha-2 country code. Example: US, GB or SE.",
    )
    type: Optional[NumberType] = Field(default=None)
    capability: Optional[conlist(CapabilityType)] = Field(default=None)
    setup_price: Optional[Money] = Field(default=None, alias="setupPrice")
    monthly_price: Optional[Money] = Field(default=None, alias="monthlyPrice")
    payment_interval_months: Optional[StrictInt] = Field(
        default=None, alias="paymentIntervalMonths"
    )
    supporting_documentation_required: Optional[StrictBool] = Field(
        default=None, alias="supportingDocumentationRequired"
    )
