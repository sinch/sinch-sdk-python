from typing import Optional
from pydantic import StrictStr
from sinch.domains.number_lookup.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.number_lookup.models.v1.shared.lookup_error import (
    LookupError,
)


class VoIPDetection(BaseModelConfigurationResponse):
    probability: Optional[StrictStr] = None
    error: Optional[LookupError] = None
