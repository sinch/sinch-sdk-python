from typing import Optional
from pydantic import StrictStr, StrictInt
from sinch.domains.number_lookup.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class LookupError(BaseModelConfigurationResponse):
    status: Optional[StrictInt] = None
    title: Optional[StrictStr] = None
    detail: Optional[StrictStr] = None
    type: Optional[StrictStr] = None
