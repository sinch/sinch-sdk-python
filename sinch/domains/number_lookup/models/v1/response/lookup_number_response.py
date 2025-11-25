from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.number_lookup.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.number_lookup.models.v1.shared import (
    Line,
    SimSwap,
    VoIPDetection,
    Rnd,
)


class LookupNumberResponse(BaseModelConfigurationResponse):
    line: Optional[Line] = None
    sim_swap: Optional[SimSwap] = Field(default=None, alias="simSwap")
    voip_detection: Optional[VoIPDetection] = Field(
        default=None, alias="voIPDetection"
    )
    rnd: Optional[Rnd] = None
    country_code: Optional[StrictStr] = Field(
        default=None, alias="countryCode"
    )
    trace_id: Optional[StrictStr] = Field(default=None, alias="traceId")
    number: Optional[StrictStr] = None
