from typing import Optional
from sinch.domains.number_lookup.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.number_lookup.models.v1.shared.lookup_error import (
    LookupError,
)
from sinch.domains.number_lookup.models.v1.types import VoIPProbabilityType


class VoIPDetection(BaseModelConfigurationResponse):
    probability: Optional[VoIPProbabilityType] = None
    error: Optional[LookupError] = None
