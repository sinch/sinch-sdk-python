from typing import Optional
from pydantic import Field, StrictBool, StrictInt, StrictStr
from sinch.domains.numbers.models.v1.internal import BaseModelConfigResponse
from sinch.domains.numbers.models.v1.shared_params import (
    CapabilityType, Money, NumberType
)


class AvailableNumber(BaseModelConfigResponse):
    phone_number: Optional[StrictStr] = Field(default=None, alias="phoneNumber")
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    type: Optional[NumberType] = Field(default=None)
    capability: Optional[CapabilityType] = Field(default=None)
    setup_price: Optional[Money] = Field(default=None, alias="setupPrice")
    monthly_price: Optional[Money] = Field(default=None, alias="monthlyPrice")
    payment_interval_months: Optional[StrictInt] = Field(default=None, alias="paymentIntervalMonths")
    supporting_documentation_required: Optional[StrictBool] = (
        Field(default=None, alias="supportingDocumentationRequired"))
