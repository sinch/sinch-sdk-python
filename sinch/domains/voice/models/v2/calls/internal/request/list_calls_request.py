from datetime import datetime
from typing import Optional

from pydantic import Field, StrictInt, StrictStr

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.types.call_reason import CallReason
from sinch.domains.voice.models.v2.types.call_result import CallResult
from sinch.domains.voice.models.v2.types.call_type import CallType


class ListCallsRequest(BaseModelConfiguration):
    service_id: Optional[StrictStr] = Field(
        default=None,
        alias="serviceId",
        description="The ID of the service.",
    )
    from_: Optional[StrictStr] = Field(
        default=None,
        alias="from",
        description="Only include calls where `from` matches this origin.  For inbound calls, this is the caller; for outbound calls, this is the calling party.",
    )
    to: Optional[StrictStr] = Field(
        default=None,
        description="Only include calls where `to` matches this destination. For inbound calls, this is the called party; for outbound calls, this is the callee/recipient.",
    )
    call_type: Optional[CallType] = Field(
        default=None,
        alias="callType",
        description="Only include calls of the specified type.\n\nIf omitted, calls of all types are included.",
    )
    start_time: Optional[datetime] = Field(
        default=None,
        alias="startTime",
        description="Only include calls that started **at or after** `startTime`.\n\nUse a more precise timestamp to narrow the results. For example:\n- `2025-02-01` matches calls starting from 2025-02-01T00:00:00Z\n- `2025-02-01T14:00:00Z` matches calls starting from 14:00:00Z on 2025-02-01",
    )
    end_time: Optional[datetime] = Field(
        default=None,
        alias="endTime",
        description="Only include calls that ended **before** `endTime` (exclusive).\n\nUse a more precise timestamp to narrow the results. For example:\n- `2025-03-01` matches calls ending up to 2025-03-01T00:00:00Z\n- `2025-03-01T14:00:00Z` matches calls ending up to 14:00:00Z on 2025-03-01",
    )
    call_result: Optional[CallResult] = Field(
        default=None,
        alias="callResult",
        description="Filter results to only include calls whose `callResult` matches the specified value.\n\nIf omitted, calls with any result are included.",
    )
    call_reason: Optional[CallReason] = Field(
        default=None,
        alias="callReason",
        description="Filter results to only include calls whose `callReason` matches the specified value.\n\nIf omitted, calls with any reason are included.",
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        alias="pageSize",
        description="Number of items to be returned on each page.",
    )
    page: Optional[StrictInt] = Field(
        default=None,
        description="Page number (1-based)",
    )
