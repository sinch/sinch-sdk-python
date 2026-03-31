from typing import Optional
from pydantic import Field, StrictInt, conlist
from sinch.domains.sms.models.v1.response.recipient_delivery_report import (
    RecipientDeliveryReport,
)
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class ListDeliveryReportsResponse(BaseModelConfigurationResponse):
    count: Optional[StrictInt] = Field(
        default=None,
        description="The total number of entries matching the given filters.",
    )
    page: Optional[StrictInt] = Field(
        default=None, description="The requested page."
    )
    page_size: Optional[StrictInt] = Field(
        default=None,
        description="The number of entries returned in this request.",
    )
    delivery_reports: Optional[conlist(RecipientDeliveryReport)] = Field(
        default=None,
        description="The page of delivery reports matching the given filters.",
    )

    @property
    def content(self):
        """Returns the content of the delivery report list."""
        return self.delivery_reports or []
