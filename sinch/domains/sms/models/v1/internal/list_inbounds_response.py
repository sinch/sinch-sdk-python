from typing import Optional

from pydantic import Field, StrictInt, conlist

from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.sms.models.v1.types.inbound_message import InboundMessage


class ListInboundsResponse(BaseModelConfigurationResponse):
    count: Optional[StrictInt] = Field(default=None, description="The total number of inbounds matching the given filters")
    page: Optional[StrictInt] = Field(default=None, description="The requested page.")
    inbounds: Optional[conlist(InboundMessage)] = Field(default=None, description="The page of inbounds matching the given filters.")
    page_size: Optional[StrictInt] = Field(default=None, description="The number of inbounds returned in this request.")
