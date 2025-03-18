from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, StrictStr, StrictInt, StrictBool
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigResponse
from sinch.domains.numbers.models.v1.shared import Money
from sinch.domains.numbers.models.v1.types import NumberType, CapabilityType


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


class ListAvailableNumbersResponse(BaseModel):
    available_numbers: Optional[List[AvailableNumber]] = Field(default=None, alias="availableNumbers")

    model_config = ConfigDict(
        populate_by_name=True
    )
