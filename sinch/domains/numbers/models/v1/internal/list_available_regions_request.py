from typing import Optional
from pydantic import Field, conlist
from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)
from sinch.domains.numbers.models.v1.types import NumberType


class ListAvailableRegionsRequest(BaseModelConfigurationRequest):
    types: Optional[conlist(NumberType)] = Field(default=None)
