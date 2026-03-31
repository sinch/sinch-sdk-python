from datetime import datetime
from typing import Optional
from pydantic import Field, StrictBool, StrictStr
from sinch.domains.number_lookup.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.number_lookup.models.v1.shared.lookup_error import (
    LookupError,
)


class Line(BaseModelConfigurationResponse):
    carrier: Optional[StrictStr] = None
    type: Optional[StrictStr] = None
    mobile_country_code: Optional[StrictStr] = Field(
        default=None, alias="mobileCountryCode"
    )
    mobile_network_code: Optional[StrictStr] = Field(
        default=None, alias="mobileNetworkCode"
    )
    ported: Optional[StrictBool] = None
    porting_date: Optional[datetime] = Field(default=None, alias="portingDate")
    error: Optional[LookupError] = None
