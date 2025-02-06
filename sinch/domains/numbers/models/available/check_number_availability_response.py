from typing import Optional
from pydantic import Field, StrictInt, StrictStr, StrictBool
from sinch.domains.numbers.models.base_model_numbers import BaseModelConfigResponse
from sinch.domains.numbers.models.numbers import CapabilityType, Money, NumberType


class CheckNumberAvailabilityResponse(BaseModelConfigResponse):
    phone_number: Optional[StrictStr] = Field(default=None, alias="phoneNumber")
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    type: Optional[NumberType] = None
    capability: Optional[CapabilityType] = None
    setup_price: Optional[Money] = Field(default=None, alias="setupPrice")
    monthly_price: Optional[Money] = Field(default=None, alias="monthlyPrice")
    payment_interval_months: Optional[StrictInt] = Field(default=None, alias="paymentIntervalMonths")
    supporting_documentation_required: Optional[StrictBool] = (
        Field(default=None, alias="supportingDocumentationRequired"))
