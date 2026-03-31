from typing import Optional
from pydantic import StrictStr, Field, conlist
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.numbers.models.v1.types import NumberType


class AvailableRegion(BaseModelConfigurationResponse):
    region_code: Optional[StrictStr] = Field(
        default=None,
        alias="regionCode",
        description="ISO 3166-1 alpha-2 country code. Example: US, GB or SE.",
    )
    region_name: Optional[StrictStr] = Field(default=None, alias="regionName")
    types: Optional[conlist(NumberType)] = Field(default=None)
