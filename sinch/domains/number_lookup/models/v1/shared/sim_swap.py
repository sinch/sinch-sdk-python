from typing import Optional
from pydantic import Field, StrictBool
from sinch.domains.number_lookup.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.number_lookup.models.v1.shared.lookup_error import (
    LookupError,
)
from sinch.domains.number_lookup.models.v1.types import SwapPeriodType


class SimSwap(BaseModelConfigurationResponse):
    swapped: Optional[StrictBool] = None
    swap_period: Optional[SwapPeriodType] = Field(
        default=None, alias="swapPeriod"
    )
    error: Optional[LookupError] = None
