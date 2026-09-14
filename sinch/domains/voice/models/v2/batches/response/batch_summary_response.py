from datetime import datetime
from typing import Optional

from pydantic import Field, StrictInt, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class BatchSummaryResponse(BaseModelConfiguration):
    batch_id: StrictStr = Field(
        default=...,
        alias="batchId",
        description="Unique identifier of the batch call operation (ULID).\n\nUse this value to retrieve the batch details ([GET] `/v2/projects/{projectId}/batches/{batchId}/details`) or stop processing ([DELETE] `/v2/projects/{projectId}/batches/{batchId}`).",
    )
    session_count: StrictInt = Field(
        default=...,
        alias="sessionCount",
        description="Total number of call sessions requested in this batch.",
    )
    end_time: Optional[datetime] = Field(
        default=None,
        alias="endTime",
        description="Timestamp (RFC 3339) when the batch finished processing (all call sessions reached a final state). Omitted if the batch is still in progress or has not completed yet.",
    )
    queued: StrictInt = Field(
        default=...,
        description="Number of call sessions that are queued and waiting to be initiated (not yet in progress).",
    )
    in_progress: StrictInt = Field(
        default=...,
        alias="inProgress",
        description="Number of call sessions that are in progress.",
    )
    completed: StrictInt = Field(
        default=...,
        description="Number of call sessions that have completed successfully.",
    )
    expired: StrictInt = Field(
        default=...,
        description="Number of queued call sessions that were not initiated before the batch TTL (`ttlSeconds`) elapsed and therefore expired.",
    )
    ttl_seconds: Optional[StrictInt] = Field(
        default=None,
        alias="ttlSeconds",
        description="Batch time-to-live (TTL) in seconds. The maximum amount of time the platform will keep attempting to start queued call sessions in this batch.\n\nWhen the TTL expires, any call sessions that have not yet been initiated will stop being processed (calls already in progress are not affected).",
    )
    requested_cps: StrictInt = Field(
        default=...,
        alias="requestedCps",
        description="Requested maximum call initiation rate, in calls per second (CPS), for this batch.\n\nActual CPS may be lower depending on routing, carrier, and platform capacity, as well as account limitations.",
    )
