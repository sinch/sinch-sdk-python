from typing import Optional

from pydantic import Field, StrictInt

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class BatchOptions(BaseModelConfiguration):
    max_cps: Optional[StrictInt] = Field(
        default=None,
        alias="maxCps",
        description="Requested maximum call initiation rate, in calls per second (CPS), for this batch.\nActual CPS may be lower depending on routing, carrier, and platform capacity, as well as account limitations.",
    )
    ttl_seconds: Optional[StrictInt] = Field(
        default=None,
        alias="ttlSeconds",
        description="Batch time-to-live (TTL). The maximum amount of time the platform will keep attempting to start queued call sessions in this batch.\nWhen the TTL expires, any call sessions that have not yet been initiated will stop being processed (calls already in progress are not affected).",
    )
