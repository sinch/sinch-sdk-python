from typing import List, Optional, Literal
from pydantic import Field, StrictInt, StrictStr, StrictBool
from sinch.core.models.base_model import BaseModelConfigResponse
from sinch.domains.numbers.models.numbers import Money


class CheckNumberAvailabilityResponse(BaseModelConfigResponse):
    phone_number: Optional[StrictStr] = Field(default=None, alias="phoneNumber")
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    type: Optional[Literal["MOBILE", "LOCAL", "TOLL_FREE"]] = None
    capability: Optional[List[Literal["SMS", "VOICE"]]] = None
    setup_price: Optional[Money] = Field(default=None, alias="setupPrice")
    monthly_price: Optional[Money] = Field(default=None, alias="monthlyPrice")
    payment_interval_months: Optional[StrictInt] = Field(default=None, alias="paymentIntervalMonths")
    supporting_documentation_required: Optional[StrictBool] = \
        (Field(default=None, alias="supportingDocumentationRequired"))
