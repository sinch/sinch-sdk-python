from typing import Optional
from pydantic import StrictStr, Field, conlist
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.numbers.models.v1.types import NumberType


class AvailableRegion(BaseModelConfigurationResponse):
    region_code: Optional[StrictStr] = Field(default=None, alias="regionCode")
    region_name: Optional[StrictStr] = Field(default=None, alias="regionName")
    types: Optional[conlist(NumberType)] = Field(default=None)
