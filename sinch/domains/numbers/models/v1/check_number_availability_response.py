from typing import Optional
from pydantic import Field, StrictInt, StrictStr, StrictBool
from sinch.domains.numbers.models.v1.capability_type import CapabilityType
from sinch.domains.numbers.models.v1.internal import BaseModelConfigResponse
from sinch.domains.numbers.models.v1.money import Money
from sinch.domains.numbers.models.v1.number_type import NumberType


class CheckNumberAvailabilityResponse(BaseModelConfigResponse):
    phone_number: Optional[StrictStr] = Field(default=None, alias="phoneNumber")
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    type: Optional[NumberType] = None
    capabilities: Optional[CapabilityType] = None
    setup_price: Optional[Money] = Field(default=None, alias="setupPrice")
    monthly_price: Optional[Money] = Field(default=None, alias="monthlyPrice")
    payment_interval_months: Optional[StrictInt] = Field(default=None, alias="paymentIntervalMonths")
    supporting_documentation_required: Optional[StrictBool] = (
        Field(default=None, alias="supportingDocumentationRequired"))
