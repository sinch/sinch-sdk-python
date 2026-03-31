from typing import Optional
from pydantic import StrictBool
from sinch.domains.number_lookup.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.number_lookup.models.v1.shared.lookup_error import (
    LookupError,
)


class Rnd(BaseModelConfigurationResponse):
    disconnected: Optional[StrictBool] = None
    error: Optional[LookupError] = None
